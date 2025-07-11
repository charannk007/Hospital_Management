from flask import Blueprint, render_template, request, redirect, session, flash, send_file
from config.settings import get_db_connection
import hashlib
import datetime, math, io
import xlsxwriter
from fpdf import FPDF
import pymysql
import random

reception_bp = Blueprint('reception', __name__, url_prefix='/reception')

# ---------------------- LOGIN ---------------------- #
@reception_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        entered_name = request.form['username']
        entered_password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, password_hash FROM receptionists WHERE name=%s", (entered_name,))
        result = cursor.fetchone()
        conn.close()

        if result:
            hashed_input = hashlib.sha256(entered_password.encode()).hexdigest()
            if hashed_input == result['password_hash']:
                session['receptionist_id'] = result['id']
                return redirect('/reception/dashboard')

        flash('Invalid credentials')

    return render_template('reception/login.html')


# ---------------------- DASHBOARD ---------------------- #
@reception_bp.route('/dashboard')
def dashboard():
    if 'receptionist_id' not in session:
        return redirect('/reception/')

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT value FROM settings WHERE name = 'hospital_name' LIMIT 1")
    result = cursor.fetchone()
    conn.close()

    hospital_name = result['value'] if result else 'Hospital'
    return render_template('reception/dashboard.html', hospital_name=hospital_name)


# ---------------------- LOGOUT ---------------------- #
@reception_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out securely.")
    resp = redirect('/reception/')
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp


# ---------------------- NEW PATIENT ---------------------- #
@reception_bp.route('/new_patient', methods=['GET', 'POST'])
def new_patient():
    if 'receptionist_id' not in session:
        return redirect('/reception/')

    patient = None
    hospital_name = 'Hospital'

    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        age = request.form['age']
        phone = request.form['phone']
        address = request.form['address']

        # Barcode and patient ID generation
        raw_data = f"{name}{phone}{datetime.datetime.now()}"
        barcode_data = hashlib.sha256(raw_data.encode()).hexdigest()[:12].upper()
        patient_id = f"happy{random.randint(100000, 999999)}"

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO patients (name, gender, age, phone, address, barcode, registered_on, patient_id)
            VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)
        """, (name, gender, age, phone, address, barcode_data, patient_id))
        conn.commit()

        # Fetch hospital name
        cursor.execute("SELECT value FROM settings WHERE name = 'hospital_name' LIMIT 1")
        result = cursor.fetchone()
        conn.close()

        if result:
            hospital_name = result['value']

        patient = {
            'name': name,
            'gender': gender,
            'age': age,
            'phone': phone,
            'address': address,
            'barcode': barcode_data,
            'patient_id': patient_id,
            'date': datetime.datetime.now().strftime("%d-%m-%Y")
        }

    return render_template('reception/new_patient.html', patient=patient, hospital_name=hospital_name)

# ---------------------- Existing PATIENTS ---------------------- #
@reception_bp.route('/existing_patient', methods=['GET', 'POST'])
def existing_patient():
    if 'receptionist_id' not in session:
        return redirect('/reception/')

    hospital_name = ''
    patient = None

    # Get hospital name
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT value FROM settings WHERE name = 'hospital_name'")
    row = cursor.fetchone()
    if row:
        hospital_name = row['value']

    if request.method == 'POST':
        search_input = request.form.get('barcode', '').strip()
        if search_input:
            cursor.execute("""
                SELECT * FROM patients
                WHERE barcode = %s OR patient_id = %s
            """, (search_input, search_input))
            patient = cursor.fetchone()

    conn.close()
    return render_template('reception/existing_patient.html', hospital_name=hospital_name, patient=patient)

# ---------------------- MANAGE PATIENTS ---------------------- #
@reception_bp.route('/manage_patients', methods=['GET', 'POST'])
def manage_patients():
    if 'receptionist_id' not in session:
        return redirect('/reception/')

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    search_term = request.form.get('search', '').strip()
    date_filter = request.form.get('date_filter', '').strip()
    page = int(request.args.get('page', 1))
    limit = 10
    offset = (page - 1) * limit

    # Added patient_id to SELECT
    query = "SELECT id, patient_id, name, gender, age, phone, address, created_at FROM patients WHERE 1=1"
    params = []

    if search_term:
        query += " AND (name LIKE %s OR phone LIKE %s)"
        like_term = f"%{search_term}%"
        params.extend([like_term, like_term])

    if date_filter:
        try:
            formatted_date = datetime.datetime.strptime(date_filter, "%Y-%m-%d").date()
            query += " AND DATE(created_at) = %s"
            params.append(formatted_date)
        except ValueError:
            flash("Invalid date format", "danger")

    query += " ORDER BY id DESC LIMIT %s OFFSET %s"
    params.extend([limit, offset])
    cursor.execute(query, tuple(params))
    patients = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) as total FROM patients WHERE 1=1")
    total_rows = cursor.fetchone()['total']
    total_pages = math.ceil(total_rows / limit)

    cursor.execute("SELECT value FROM settings WHERE name='hospital_name'")
    result = cursor.fetchone()
    hospital_name = result['value'] if result else 'Hospital'
    conn.close()

    return render_template('reception/manage_patients.html',
                           patients=patients,
                           hospital_name=hospital_name,
                           page=page,
                           total_pages=total_pages,
                           search_term=search_term,
                           date_filter=date_filter)


# ---------------------- UPDATE PATIENT ---------------------- #
@reception_bp.route('/update_patient/<int:patient_id>', methods=['GET', 'POST'])
def update_patient(patient_id):
    if 'receptionist_id' not in session:
        return redirect('/reception/')

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        age = request.form['age']
        phone = request.form['phone']
        address = request.form['address']

        cursor.execute("""
            UPDATE patients
            SET name=%s, gender=%s, age=%s, phone=%s, address=%s
            WHERE id=%s
        """, (name, gender, age, phone, address, patient_id))
        conn.commit()
        conn.close()
        flash("Patient record updated successfully.")
        return redirect('/reception/manage_patients')

    cursor.execute("SELECT name, gender, age, phone, address FROM patients WHERE id=%s", (patient_id,))
    patient = cursor.fetchone()
    conn.close()

    if not patient:
        flash("Patient not found.")
        return redirect('/reception/manage_patients')

    return render_template('reception/update_patient.html', patient=patient)


# ---------------------- EXPORT TO EXCEL ---------------------- #
@reception_bp.route('/export_patients_excel')
def export_patients_excel():
    search = request.args.get('search', '').strip()
    date_filter = request.args.get('date', '').strip()

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = """
        SELECT patient_id, name, gender, age, phone, address, created_at
        FROM patients WHERE 1=1
    """
    params = []

    if search:
        query += " AND (name LIKE %s OR phone LIKE %s)"
        like_term = f"%{search}%"
        params.extend([like_term, like_term])

    if date_filter:
        try:
            formatted_date = datetime.datetime.strptime(date_filter, "%Y-%m-%d").date()
            query += " AND DATE(created_at) = %s"
            params.append(formatted_date)
        except ValueError:
            pass

    query += " ORDER BY id DESC"
    cursor.execute(query, tuple(params))
    patients = cursor.fetchall()
    conn.close()

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet("Patients")

    headers = ['Patient ID', 'Name', 'Gender', 'Age', 'Phone', 'Address', 'Date of Registration']
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    for row_num, row in enumerate(patients, start=1):
        date_str = row['created_at'].strftime('%d-%m-%Y') if row['created_at'] else ''
        data = [row['patient_id'], row['name'], row['gender'], row['age'], row['phone'], row['address'], date_str]
        for col_num, value in enumerate(data):
            worksheet.write(row_num, col_num, value)

    workbook.close()
    output.seek(0)
    return send_file(output, download_name="patients.xlsx", as_attachment=True)


# ---------------------- EXPORT TO PDF ---------------------- #
@reception_bp.route('/export_patients_pdf', methods=['GET', 'POST'])
def export_patients_pdf():
    if 'receptionist_id' not in session:
        return redirect('/reception/')

    # Get filter date (YYYY-MM-DD)
    date_filter = request.args.get('date', '').strip()

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Get receptionist name
    cursor.execute("SELECT name FROM receptionists WHERE id = %s", (session['receptionist_id'],))
    receptionist_row = cursor.fetchone()
    receptionist_name = receptionist_row['name'] if receptionist_row else ''

    # Get hospital name
    cursor.execute("SELECT value FROM settings WHERE name = 'hospital_name'")
    hospital_row = cursor.fetchone()
    hospital_name = hospital_row['value'] if hospital_row else 'Hospital'

    # Build query
    query = """
        SELECT patient_id, name, gender, age, phone, address, created_at
        FROM patients WHERE 1=1
    """
    params = []

    if date_filter:
        try:
            formatted_date = datetime.datetime.strptime(date_filter, "%Y-%m-%d").date()
            query += " AND DATE(created_at) = %s"
            params.append(formatted_date)
        except ValueError:
            flash("Invalid date format", "danger")

    query += " ORDER BY id DESC"
    cursor.execute(query, tuple(params))
    patients = cursor.fetchall()
    conn.close()

    # Create PDF
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"{hospital_name} - Patient List", ln=True, align="C")

    # Printed Info
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, f"Printed on: {datetime.datetime.now().strftime('%d-%m-%Y')}", ln=False, align="L")
    pdf.cell(-1, 6, f"Printed by: {receptionist_name}", ln=True, align="R")

    # Table Headers
    pdf.set_font("Arial", "B", 10)
    col_widths = [10, 30, 20, 10, 30, 40, 25]
    headers = ['S.No', 'Patient ID', 'Name', 'Gender', 'Age', 'Phone', 'Address', 'Date']
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i] if i < len(col_widths) else 25, 8, header, border=1)
    pdf.ln()

    # Table Rows
    pdf.set_font("Arial", "", 10)
    for idx, row in enumerate(patients, start=1):
        data = [
            str(idx),
            row['patient_id'] if row['patient_id'] is not None else '',
            row['name'] if row['name'] is not None else '',
            row['gender'] if row['gender'] is not None else '',
            str(row['age']) if row['age'] is not None else '',
            row['phone'] if row['phone'] is not None else '',
            row['address'] if row['address'] is not None else '',
            row['created_at'].strftime('%d-%m-%Y') if row['created_at'] else ''
        ]
        for i, item in enumerate(data):
            pdf.cell(col_widths[i] if i < len(col_widths) else 25, 8, str(item), border=1)
        pdf.ln()

    # Footer (place after table, not at bottom of page)
    pdf.ln(5)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 10, f"Report generated by: {receptionist_name}", align='R')

    # Return PDF
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    output = io.BytesIO(pdf_bytes)
    return send_file(output, download_name="patients.pdf", as_attachment=True)




