from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from config.settings import get_db_connection, get_hospital_name
from datetime import datetime
import hashlib

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin_users WHERE username=%s AND password_hash=%s", (username, password_hash))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()
        if admin:
            session['admin_logged_in'] = True
            return redirect(url_for('admin.admin_dashboard'))
        else:
            return render_template('admin/admin_login.html', error="Invalid credentials")
    return render_template('admin/admin_login.html')


@admin_bp.route('/add-specialization', methods=['GET', 'POST'])
def add_specialization():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Handle deletion if ?delete=<id> is in the query string
    delete_id = request.args.get("delete")
    if delete_id:
        try:
            cursor.execute("DELETE FROM specializations WHERE id = %s", (delete_id,))
            conn.commit()
            flash("Specialization deleted successfully.", "success")
        except Exception as e:
            flash("Failed to delete specialization.", "error")
        return redirect(url_for('admin.add_specialization'))

    if request.method == 'POST':
        specialization = request.form['specialization'].strip()
        if not specialization:
            flash("Specialization cannot be empty.", "error")
        else:
            try:
                cursor.execute("INSERT INTO specializations (name) VALUES (%s)", (specialization,))
                conn.commit()
                flash(f"{specialization} added successfully!", "success")
            except Exception as e:
                flash("Specialization already exists or failed to insert.", "error")
        return redirect(url_for('admin.add_specialization'))

    # Fetch existing specializations
    cursor.execute("SELECT id, name FROM specializations")
    specializations = cursor.fetchall()
    specializations = [{"id": row['id'], "name": row['name']} for row in specializations]

    cursor.close()
    conn.close()

    return render_template(
        'admin/add_specialization.html',
        specializations=specializations,
        hospital_name=get_hospital_name(),
        year=datetime.now().year
    )


@admin_bp.route('/add-doctor', methods=['GET', 'POST'])
def add_doctor():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        password = request.form['password']
        specialization_id = request.form['specialization_id']
        password_hash = generate_password_hash(password)
        try:
            cursor.execute("""
                INSERT INTO doctors (name, phone, password_hash, specialization_id)
                VALUES (%s, %s, %s, %s)
            """, (name, phone, password_hash, specialization_id))
            conn.commit()
            flash("Doctor added successfully!", "flash")
        except Exception as e:
            print("Error:", e)
            flash("Failed to add doctor.", "error")
        return redirect(url_for('admin.add_doctor'))
    cursor.execute("SELECT id, name FROM specializations")
    specializations = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin/add_doctor.html', specializations=specializations, hospital_name=get_hospital_name(), year=datetime.now().year)


@admin_bp.route('/manage-doctors')
def manage_doctors():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT d.id, d.name, d.phone, s.name AS specialization
    FROM doctors d
    LEFT JOIN specializations s ON d.specialization_id = s.id
    """
    cursor.execute(query)
    doctors = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template(
        'admin/manage_doctors.html',
        doctors=doctors,
        hospital_name=get_hospital_name(),
        year=datetime.now().year
    )


@admin_bp.route('/reset-password/<int:doctor_id>')
def reset_password(doctor_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    new_password = 'doctor123'
    password_hash = generate_password_hash(new_password)
    cursor.execute("UPDATE doctors SET password_hash = %s WHERE id = %s", (password_hash, doctor_id))
    conn.commit()
    cursor.close()
    conn.close()
    flash(f"Password reset to '{new_password}'", 'success')
    return redirect(url_for('admin.manage_doctors'))


@admin_bp.route('/delete-doctor/<int:doctor_id>')
def delete_doctor(doctor_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM doctors WHERE id = %s", (doctor_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Doctor removed successfully.", "success")
    return redirect(url_for('admin.manage_doctors'))


@admin_bp.route('/dashboard')
def admin_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch hospital name
    cursor.execute("SELECT value FROM settings WHERE name = 'hospital_name'")
    result = cursor.fetchone()
    hospital_name = result['value'] if result else "Default Hospital"

    # Doctor count
    cursor.execute("SELECT COUNT(*) AS total FROM doctors")
    doctor_count = cursor.fetchone()['total']

    # Specialization count
    cursor.execute("SELECT COUNT(*) AS total FROM specializations")
    specialization_count = cursor.fetchone()['total']

    cursor.close()
    conn.close()

    return render_template(
        'admin/dashboard.html',
        hospital_name=hospital_name,
        doctor_count=doctor_count,
        specialization_count=specialization_count,
        year=datetime.now().year
    )


@admin_bp.route('/update-hospital-name', methods=['POST'])
def update_hospital_name():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))

    new_name = request.form.get('hospital_name', '').strip()
    if not new_name:
        flash("Hospital name cannot be empty.", "error")
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE settings SET value = %s WHERE name = 'hospital_name'", (new_name,))
            conn.commit()
            flash("Hospital name updated successfully!", "success")
        except Exception as e:
            flash("Failed to update hospital name.", "error")
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('admin.admin_dashboard'))  # Update this route name if needed

@admin_bp.route('/logout')
def admin_logout():
    session.clear()  # Clears session data
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('admin.admin_login'))

