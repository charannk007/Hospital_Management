import os
import sys
import hashlib
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import pymysql

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import get_db_connection

manager_bp = Blueprint('manager', __name__, url_prefix='/manager')

@manager_bp.route('/', methods=['GET', 'POST'])
def manager_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM manager_admins WHERE username=%s AND password_hash=%s", (username, password_hash))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()

        if admin:
            session['manager_logged_in'] = True
            session['manager_admin'] = username
            return redirect(url_for('manager.manager_dashboard'))
        else:
            flash("Invalid login credentials", "error")

    return render_template('manager/login.html')

@manager_bp.route('/dashboard')
def manager_dashboard():
    if not session.get('manager_logged_in'):
        return redirect(url_for('manager.manager_login'))

    return render_template('manager/dashboard.html')

@manager_bp.route('/receptionist', methods=['GET', 'POST'])
def manage_receptionist():
    if not session.get('manager_logged_in'):
        return redirect(url_for('manager.manager_login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("INSERT INTO receptionists (name, password_hash) VALUES (%s, %s)", (name, password_hash))
        conn.commit()
        flash("Receptionist account created", "success")
        return redirect(url_for('manager.manage_receptionist'))

    cursor.execute("SELECT id, name FROM receptionists")
    receptionists = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("manager/receptionist.html", receptionists=receptionists)

@manager_bp.route('/receptionist/delete/<int:id>')
def delete_receptionist(id):
    if not session.get('manager_logged_in'):
        return redirect(url_for('manager.manager_login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM receptionists WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Receptionist deleted", "success")
    return redirect(url_for('manager.manage_receptionist'))


@manager_bp.route('/receptionist/reset/<int:id>')
def reset_receptionist_password(id):
    if not session.get('manager_logged_in'):
        return redirect(url_for('manager.manager_login'))

    default_password = '123456'
    password_hash = hashlib.sha256(default_password.encode()).hexdigest()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE receptionists SET password_hash = %s WHERE id = %s", (password_hash, id))
    conn.commit()
    cursor.close()
    conn.close()

    flash(f"Password reset to '{default_password}'", "success")
    return redirect(url_for('manager.manage_receptionist'))


@manager_bp.route('/laboratory', methods=['GET', 'POST'])
def manage_laboratory():
    if not session.get('manager_logged_in'):
        return redirect(url_for('manager.manager_login'))

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        name = request.form['name'].strip()
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("INSERT INTO laboratory_accounts (name, password_hash) VALUES (%s, %s)", (name, password_hash))
        conn.commit()
        flash(f"Laboratory account '{name}' created.", "success")
        return redirect(url_for('manager.manage_laboratory'))

    # Search functionality
    search = request.args.get('search', '')
    if search:
        cursor.execute("SELECT id, name FROM laboratory_accounts WHERE name LIKE %s", ('%' + search + '%',))
    else:
        cursor.execute("SELECT id, name FROM laboratory_accounts")

    laboratory_accounts = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("manager/laboratory.html", laboratory_accounts=laboratory_accounts)


@manager_bp.route('/reset-lab-password/<int:lab_id>')
def reset_lab_password(lab_id):
    if not session.get('manager_logged_in'):
        return redirect(url_for('manager.manager_login'))

    default_password = '123456'
    password_hash = hashlib.sha256(default_password.encode()).hexdigest()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE laboratory_accounts SET password_hash=%s WHERE id=%s", (password_hash, lab_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Password reset to default (123456).", "success")
    return redirect(url_for('manager.manage_laboratory'))


@manager_bp.route('/delete-lab/<int:lab_id>')
def delete_lab_account(lab_id):
    if not session.get('manager_logged_in'):
        return redirect(url_for('manager.manager_login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM laboratory_accounts WHERE id=%s", (lab_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Laboratory account deleted.", "success")
    return redirect(url_for('manager.manage_laboratory'))


@manager_bp.route('/cashier', methods=['GET', 'POST'])
def manage_cashier():
    if not session.get('manager_logged_in'):
        return redirect(url_for('manager.manager_login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute("INSERT INTO cashier_accounts (name, password_hash) VALUES (%s, %s)", (name, password_hash))
        conn.commit()
        flash("Cashier account created successfully", "success")
        return redirect(url_for('manager.manage_cashier'))

    search_query = request.args.get('search', '')
    if search_query:
        cursor.execute("SELECT id, name FROM cashier_accounts WHERE name LIKE %s", ('%' + search_query + '%',))
    else:
        cursor.execute("SELECT id, name FROM cashier_accounts")
    cashiers = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('manager/cashier.html', cashiers=cashiers, search_query=search_query)


@manager_bp.route('/cashier/reset/<int:id>')
def reset_cashier_password(id):
    if not session.get('manager_logged_in'):
        return redirect(url_for('manager.manager_login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    default_pass = hashlib.sha256("123456".encode()).hexdigest()
    cursor.execute("UPDATE cashier_accounts SET password_hash = %s WHERE id = %s", (default_pass, id))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Cashier password reset to '123456'", "info")
    return redirect(url_for('manager.manage_cashier'))


@manager_bp.route('/cashier/delete/<int:id>')
def delete_cashier(id):
    if not session.get('manager_logged_in'):
        return redirect(url_for('manager.manager_login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cashier_accounts WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Cashier deleted successfully", "info")
    return redirect(url_for('manager.manage_cashier'))


@manager_bp.route('/fix-price', methods=['GET', 'POST'])
def fix_price():
    if not session.get('manager_logged_in'):
        return redirect(url_for('manager.manager_login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        service_name = request.form['service'].strip()
        price = float(request.form['price'])

        # Check if service already exists
        cursor.execute("SELECT * FROM service_prices WHERE service = %s", (service_name,))
        existing = cursor.fetchone()

        if existing:
            flash("Service already exists. Use update option.", "warning")
        else:
            cursor.execute("INSERT INTO service_prices (service, price) VALUES (%s, %s)", (service_name, price))
            conn.commit()
            flash("Service added successfully", "success")

        return redirect(url_for('manager.fix_price'))

    search_query = request.args.get('search', '')
    if search_query:
        cursor.execute("SELECT * FROM service_prices WHERE service LIKE %s", ('%' + search_query + '%',))
    else:
        cursor.execute("SELECT * FROM service_prices")
    services = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('manager/fix_price.html', services=services, search_query=search_query)



@manager_bp.route('/fix-price/update/<int:id>', methods=['POST'])
def update_price(id):
    if not session.get('manager_logged_in'):
        return redirect(url_for('manager.manager_login'))

    new_price = float(request.form['new_price'])
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE service_prices SET price = %s WHERE id = %s", (new_price, id))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Price updated successfully", "success")
    return redirect(url_for('manager.fix_price'))


@manager_bp.route('/fix-price/delete/<int:id>')
def delete_service(id):
    if not session.get('manager_logged_in'):
        return redirect(url_for('manager.manager_login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM service_prices WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Service deleted successfully", "info")
    return redirect(url_for('manager.fix_price'))

@manager_bp.route('/logout')
def manager_logout():
    session.pop('manager_logged_in', None)
    session.pop('manager_admin', None)
    flash("You have been logged out.", "success")
    return redirect(url_for('manager.manager_login'))