import os
import sys
import hashlib
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import date
today = date.today()

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

    # Handle form submission
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute(
            "INSERT INTO pharmacy_staff (name, password_hash) VALUES (%s, %s)",
            (name, password_hash)
        )
        conn.commit()
        flash(f"Staff account for {name} created", "success")
        return redirect(url_for('pharma.manage_staff'))

    # Load existing staff
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

    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        expiry = request.form['expiry']
        cursor.execute("INSERT INTO pharma_medicines (name, quantity, expiry_date) VALUES (%s, %s, %s)", (name, quantity, expiry))
        conn.commit()
        flash(f"{name} added successfully", "success")
        return redirect(url_for('pharma.add_medicine'))

    cursor.execute("SELECT id, name, quantity, expiry_date FROM pharma_medicines ORDER BY expiry_date ASC")
    medicines = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('pharma/add_medicine.html', medicines=medicines, hospital_name="Your Hospital")

@pharma_bp.route('/update-medicine', methods=['POST'])
def update_medicine():
    if not session.get('pharma_logged_in'):
        return redirect(url_for('pharma.pharma_login'))

    med_id = request.form.get('id')
    name = request.form.get('name')
    quantity = request.form.get('quantity')
    expiry = request.form.get('expiry')

    if not (med_id and name and quantity and expiry):
        flash("Missing information for update", "danger")
        return redirect(url_for('pharma.add_medicine'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE pharma_medicines
            SET name = %s, quantity = %s, expiry_date = %s
            WHERE id = %s
        """, (name, quantity, expiry, med_id))

        conn.commit()
        cursor.close()
        conn.close()

        flash(f"{name} updated successfully!", "success")
    except Exception as e:
        flash(f"Error updating medicine: {str(e)}", "danger")

    return redirect(url_for('pharma.add_medicine'))



@pharma_bp.route('/delete-medicine/<int:medicine_id>', methods=['GET'])
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


@pharma_bp.route('/sales', methods=['GET', 'POST'])
def pharma_sales():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['medicine_name']
        qty = int(request.form['quantity'])
        amount = float(request.form['amount'])
        sold_by = session.get('pharma_admin', 'Unknown')

        cursor.execute("""
            INSERT INTO pharma_sales (medicine_name, quantity_sold, amount, sold_by, sale_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, qty, amount, sold_by, today))

        cursor.execute("""
            UPDATE pharma_medicines
            SET quantity = quantity - %s
            WHERE name = %s
        """, (qty, name))

        conn.commit()
        flash("Sale entry added successfully", "success")
        return redirect(url_for('pharma.pharma_sales'))

    # Daily sales summary
    cursor.execute("""
        SELECT sale_date, SUM(amount) AS total_amount, COUNT(*) AS total_sales
        FROM pharma_sales
        GROUP BY sale_date
        ORDER BY sale_date DESC
    """)
    sales_by_day = cursor.fetchall()

    # Total collected today
    cursor.execute("""
        SELECT SUM(amount) AS today_total
        FROM pharma_sales
        WHERE sale_date = CURDATE()
    """)
    today_total = cursor.fetchone()['today_total'] or 0.0

    # Top sold overall
    cursor.execute("""
        SELECT medicine_name, SUM(quantity_sold) AS total_sold
        FROM pharma_sales
        GROUP BY medicine_name
        ORDER BY total_sold DESC
        LIMIT 5
    """)
    top_sold = cursor.fetchall()

    # Top sold medicine today
    cursor.execute("""
        SELECT medicine_name, SUM(quantity_sold) AS total
        FROM pharma_sales
        WHERE sale_date = CURDATE()
        GROUP BY medicine_name
        ORDER BY total DESC
        LIMIT 1
    """)
    top_medicine_today = cursor.fetchone()

    # Top staff today
    cursor.execute("""
        SELECT sold_by, SUM(quantity_sold) AS total
        FROM pharma_sales
        WHERE sale_date = CURDATE()
        GROUP BY sold_by
        ORDER BY total DESC
        LIMIT 1
    """)
    top_staff_today = cursor.fetchone()

    # For sales entry dropdown
    cursor.execute("SELECT name FROM pharma_medicines")
    medicines = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("pharma/sales_report.html",
                           sales_by_day=sales_by_day,
                           today_total=today_total,
                           top_sold=top_sold,
                           medicines=medicines,
                           top_medicine_today=top_medicine_today,
                           top_staff_today=top_staff_today)


