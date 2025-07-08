import os
import sys
import hashlib
import pymysql
from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask import make_response
import csv
import io

# Add parent directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import get_db_connection

pharma_bp = Blueprint('pharma', __name__, url_prefix='/pharma')

@pharma_bp.route('/', methods=['GET', 'POST'])
def pharma_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pharma_admins WHERE username=%s AND password_hash=%s", (username, password_hash))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()

        if admin:
            session['pharma_logged_in'] = True
            session['pharma_admin'] = username
            return redirect(url_for('pharma.pharma_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('pharma/login.html')

@pharma_bp.route('/dashboard')
def pharma_dashboard():
    if not session.get('pharma_logged_in'):
        flash("Please login to continue", "error")
        return redirect(url_for('pharma.pharma_login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Get hospital name
    cursor.execute("SELECT value FROM settings WHERE name = 'hospital_name'")
    result = cursor.fetchone()
    hospital_name = result['value'] if result else "Happy9 Hospital"

    # Get low stock medicines
    cursor.execute("SELECT name, quantity FROM pharma_medicines WHERE quantity < 100")
    low_stock_meds = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('pharma/dashboard.html',
                           hospital_name=hospital_name,
                           low_stock_meds=low_stock_meds)

@pharma_bp.route('/logout')
def pharma_logout():
    if session.get('pharma_admin'):
        username = session['pharma_admin']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pharma_audit_logs (admin_username, action) VALUES (%s, %s)", (username, 'logout'))
        conn.commit()
        cursor.close()
        conn.close()

    session.clear()
    response = redirect(url_for('pharma.pharma_login'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    flash("You have been logged out.", "success")
    return response

@pharma_bp.route('/manage-staff', methods=['GET', 'POST'])
def manage_staff():
    if not session.get('pharma_logged_in'):
        return redirect(url_for('pharma.pharma_login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("INSERT INTO pharmacy_staff (name, password_hash) VALUES (%s, %s)", (name, password_hash))
        conn.commit()
        flash(f"Staff account for {name} created", "success")
        return redirect(url_for('pharma.manage_staff'))

    cursor.execute("SELECT id, name FROM pharmacy_staff")
    staff_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('pharma/staff.html', staff_list=staff_list, hospital_name="Happy9 Hospital")

@pharma_bp.route('/delete-staff/<int:staff_id>')
def delete_staff(staff_id):
    if not session.get('pharma_logged_in'):
        return redirect(url_for('pharma.pharma_login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pharmacy_staff WHERE id = %s", (staff_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Staff account deleted.", "success")
    return redirect(url_for('pharma.manage_staff'))

@pharma_bp.route('/reset-staff-password/<int:staff_id>')
def reset_staff_password(staff_id):
    if not session.get('pharma_logged_in'):
        return redirect(url_for('pharma.pharma_login'))

    default_password = '123456'
    password_hash = hashlib.sha256(default_password.encode()).hexdigest()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE pharmacy_staff SET password_hash=%s WHERE id=%s", (password_hash, staff_id))
    conn.commit()
    cursor.close()
    conn.close()
    flash(f"Password reset to '{default_password}'", "success")
    return redirect(url_for('pharma.manage_staff'))

@pharma_bp.route('/add-medicine', methods=['GET', 'POST'])
def add_medicine():
    if not session.get('pharma_logged_in'):
        return redirect(url_for('pharma.pharma_login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pharma_medicines ORDER BY expiry_date ASC")
    medicines = cursor.fetchall()

    cursor.execute("SELECT * FROM pharma_medicines WHERE quantity < 100")
    low_stock_meds = cursor.fetchall()

    if request.method == 'POST':
        name = request.form['name'].strip()
        quantity = int(request.form['quantity'])
        expiry = request.form['expiry']
        price = float(request.form['price'])

        cursor.execute("SELECT * FROM pharma_medicines WHERE name = %s", (name,))
        existing = cursor.fetchone()

        if existing:
            cursor.execute("""
                UPDATE pharma_medicines
                SET quantity = quantity + %s, expiry_date = %s, price = %s
                WHERE name = %s
            """, (quantity, expiry, price, name))
            flash(f"{name} updated successfully", "success")
        else:
            cursor.execute("""
                INSERT INTO pharma_medicines (name, quantity, expiry_date, price)
                VALUES (%s, %s, %s, %s)
            """, (name, quantity, expiry, price))
            flash(f"{name} added successfully", "success")

        conn.commit()
        return redirect(url_for('pharma.add_medicine'))

    cursor.close()
    conn.close()

    return render_template('pharma/add_medicine.html',
                           medicines=medicines,
                           low_stock_meds=low_stock_meds)

@pharma_bp.route('/delete-medicine/<int:medicine_id>')
def delete_medicine(medicine_id):
    if not session.get('pharma_logged_in'):
        return redirect(url_for('pharma.pharma_login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pharma_medicines WHERE id = %s", (medicine_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Medicine deleted successfully", "success")
    return redirect(url_for('pharma.add_medicine'))

@pharma_bp.route('/update-medicine', methods=['POST'])
def update_medicine():
    if not session.get('pharma_logged_in'):
        return redirect(url_for('pharma.pharma_login'))

    med_id = request.form['id']
    name = request.form['name'].strip()
    quantity = int(request.form['quantity'])
    expiry = request.form['expiry']
    price = float(request.form['price'])

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE pharma_medicines
        SET name = %s, quantity = %s, expiry_date = %s, price = %s
        WHERE id = %s
    """, (name, quantity, expiry, price, med_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash(f"{name} updated successfully", "success")
    return redirect(url_for('pharma.add_medicine'))

@pharma_bp.route("/pharma_sales", methods=["GET"])
def pharma_sales():
    conn = pymysql.connect(host="localhost", user="root", password="root123", database="hospital_db")
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    report_type = request.args.get("type", "day")
    from_date = request.args.get("from")
    to_date = request.args.get("to")

    today = datetime.now().date()
    date_filter = ""
    label = "Today"

    if report_type == "day":
        date_filter = f"DATE(sale_date) = '{today}'"
        label = today.strftime("%d-%m-%Y")
    elif report_type == "month":
        month = today.strftime('%Y-%m')
        date_filter = f"DATE_FORMAT(sale_date, '%Y-%m') = '{month}'"
        label = today.strftime("%B %Y")
    elif report_type == "range" and from_date and to_date:
        date_filter = f"DATE(sale_date) BETWEEN '{from_date}' AND '{to_date}'"
        label = f"{from_date} to {to_date}"
    else:
        date_filter = f"DATE(sale_date) = '{today}'"

    # 1. Total sales
    cursor.execute(f"SELECT IFNULL(SUM(amount), 0) AS total FROM pharma_sales WHERE {date_filter}")
    overall_total = cursor.fetchone()["total"]

    # 2. Best staff
    cursor.execute(f"""
        SELECT sold_by AS staff_name, SUM(amount) AS total_sales
        FROM pharma_sales
        WHERE {date_filter}
        GROUP BY sold_by
        ORDER BY total_sales DESC
        LIMIT 1
    """)
    best_staff = cursor.fetchone()

    # 3. Top sold item
    cursor.execute(f"""
        SELECT medicine_name AS item_name, SUM(quantity_sold) AS total_qty
        FROM pharma_sales
        WHERE {date_filter}
        GROUP BY medicine_name
        ORDER BY total_qty DESC
        LIMIT 1
    """)
    top_item = cursor.fetchone()

    # 4. Staff breakdown
    cursor.execute(f"""
        SELECT sold_by AS staff_name, SUM(amount) AS total_sales
        FROM pharma_sales
        WHERE {date_filter}
        GROUP BY sold_by
    """)
    staff_sales_raw = cursor.fetchall()

    staff_sales = []
    for staff in staff_sales_raw:
        name = staff["staff_name"]
        query = f"""
            SELECT medicine_name, SUM(quantity_sold) AS qty
            FROM pharma_sales
            WHERE sold_by = %s AND {date_filter}
            GROUP BY medicine_name
            ORDER BY qty DESC
            LIMIT 1
        """
        cursor.execute(query, (name,))
        top_item_result = cursor.fetchone()
        top_item_name = top_item_result["medicine_name"] if top_item_result else "N/A"

        staff_sales.append({
            "staff_name": name,
            "total_sales": staff["total_sales"],
            "top_item": top_item_name
        })


    conn.close()

    return render_template("pharma/sales_report.html",
        hospital_name="Happy9 Hospital",  # Or fetch dynamically
        overall_total=overall_total,
        best_staff=best_staff,
        top_item=top_item,
        staff_sales=staff_sales,
        period_label=label
    )


@pharma_bp.route('/export-sales')
def export_sales():
    if not session.get('pharma_logged_in'):
        return redirect(url_for('pharma.pharma_login'))

    report_type = request.args.get("type", "day")
    from_date = request.args.get("from")
    to_date = request.args.get("to")

    today = datetime.now().date()

    if report_type == "day":
        date_filter = f"DATE(sale_date) = '{today}'"
    elif report_type == "month":
        month = today.strftime('%Y-%m')
        date_filter = f"DATE_FORMAT(sale_date, '%Y-%m') = '{month}'"
    elif report_type == "range" and from_date and to_date:
        date_filter = f"DATE(sale_date) BETWEEN '{from_date}' AND '{to_date}'"
    else:
        date_filter = f"DATE(sale_date) = '{today}'"

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(f"""
        SELECT sale_date, medicine_name, quantity_sold, amount, sold_by
        FROM pharma_sales
        WHERE {date_filter}
        ORDER BY sale_date DESC
    """)
    sales = cursor.fetchall()
    cursor.close()
    conn.close()

    # Generate CSV
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(["Date", "Medicine", "Qty Sold", "Amount", "Sold By"])
    for row in sales:
        cw.writerow([
            row["sale_date"],
            row["medicine_name"],
            row["quantity_sold"],
            row["amount"],
            row["sold_by"]
        ])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=sales_report.csv"
    output.headers["Content-type"] = "text/csv"
    return output