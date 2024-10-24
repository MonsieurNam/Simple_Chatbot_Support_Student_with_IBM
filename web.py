# Import necessary libraries
import os
os.add_dll_directory(r"D:\simple_chatbot_withIBM\myenv\Lib\site-packages\clidriver\bin")

import ibm_db
from flask import Flask, render_template, request, redirect, url_for, flash
# import logging
import traceback  # Import traceback module

from dotenv import load_dotenv
# Initialize Flask app
app = Flask(__name__)

load_dotenv()

# Configure logging
# logging.basicConfig(
#     filename='app.log',  # Log to app.log file
#     level=logging.DEBUG,
#     format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
# )
# app.logger.setLevel(logging.DEBUG)

# Set a secret key for session management and flash messages
app.secret_key = os.getenv("secret_key")

# IBM Db2 credentials
dsn_hostname = os.getenv("dsn_hostname")
dsn_uid = os.getenv("dsn_uid")
dsn_pwd = os.getenv("dsn_pwd")
dsn_port = os.getenv("dsn_port")
dsn_database = os.getenv("dsn_database")
dsn_driver = os.getenv("dsn_driver")
dsn_protocol = os.getenv("dsn_protocol")
dsn_security = os.getenv("dsn_security")

# Function to establish a database connection
def get_db_connection():
    dsn = (
        f"DRIVER={dsn_driver};"
        f"DATABASE={dsn_database};"
        f"HOSTNAME={dsn_hostname};"
        f"PORT={dsn_port};"
        f"PROTOCOL={dsn_protocol};"
        f"UID={dsn_uid};"
        f"PWD={dsn_pwd};"
        f"SECURITY={dsn_security};"
    )
    try:
        conn = ibm_db.connect(dsn, "", "")
        app.logger.debug("Database connection established.")
        return conn
    except Exception as e:
        app.logger.error(f"Unable to connect to the database: {e}")
        traceback.print_exc()
        return None

# Main Route - Handle all operations
@app.route('/', methods=['GET', 'POST'])
def home():
    conn = get_db_connection()

    if conn:
        if request.method == 'POST':
            try:
                # Determine which form was submitted
                if 'add_student' in request.form:
                    # Handle Add Student
                    ten_sinh_vien = request.form.get('TEN_SINH_VIEN')
                    ngay_sinh = request.form.get('NGAY_SINH')
                    ma_sv_form = request.form.get('MA_SV')
                    chuyen_nganh = request.form.get('CHUYEN_NGANH')

                    app.logger.debug(f"Adding new student: {ten_sinh_vien}, {ngay_sinh}, {ma_sv_form}, {chuyen_nganh}")

                    insert_sql = "INSERT INTO STUDENTS (TEN_SINH_VIEN, NGAY_SINH, MA_SV, CHUYEN_NGANH) VALUES (?, ?, ?, ?)"
                    stmt = ibm_db.prepare(conn, insert_sql)
                    ibm_db.bind_param(stmt, 1, ten_sinh_vien)
                    ibm_db.bind_param(stmt, 2, ngay_sinh)
                    ibm_db.bind_param(stmt, 3, ma_sv_form)
                    ibm_db.bind_param(stmt, 4, chuyen_nganh)
                    ibm_db.execute(stmt)
                    app.logger.debug("New student added successfully.")
                    flash("Thêm sinh viên thành công!", 'success')

                elif 'edit_student' in request.form:
                    # Handle Edit Student
                    ten_sinh_vien = request.form.get('TEN_SINH_VIEN')
                    ngay_sinh = request.form.get('NGAY_SINH')
                    chuyen_nganh = request.form.get('CHUYEN_NGANH')
                    ma_sv_form = request.form.get('MA_SV')

                    app.logger.debug(f"Updating student {ma_sv_form} with data: {ten_sinh_vien}, {ngay_sinh}, {chuyen_nganh}")

                    update_sql = "UPDATE STUDENTS SET TEN_SINH_VIEN=?, NGAY_SINH=?, CHUYEN_NGANH=? WHERE MA_SV=?"
                    stmt = ibm_db.prepare(conn, update_sql)
                    ibm_db.bind_param(stmt, 1, ten_sinh_vien)
                    ibm_db.bind_param(stmt, 2, ngay_sinh)
                    ibm_db.bind_param(stmt, 3, chuyen_nganh)
                    ibm_db.bind_param(stmt, 4, ma_sv_form)
                    ibm_db.execute(stmt)
                    app.logger.debug("Student updated successfully.")
                    flash("Cập nhật sinh viên thành công!", 'success')

                elif 'delete_student' in request.form:
                    # Handle Delete Student
                    ma_sv_form = request.form.get('MA_SV')
                    app.logger.debug(f"Deleting student {ma_sv_form}")

                    delete_sql = "DELETE FROM STUDENTS WHERE MA_SV = ?"
                    stmt = ibm_db.prepare(conn, delete_sql)
                    ibm_db.bind_param(stmt, 1, ma_sv_form)
                    ibm_db.execute(stmt)
                    app.logger.debug("Student deleted successfully.")
                    flash("Xóa sinh viên thành công!", 'success')

            except Exception as e:
                app.logger.error(f"Error processing request: {e}")
                traceback.print_exc()
                flash(f"Lỗi khi xử lý yêu cầu: {e}", 'danger')

            finally:
                if conn:
                    ibm_db.close(conn)
                    app.logger.debug("Database connection closed.")

            return redirect(url_for('home'))

        else:
            try:
                # Fetch all students
                command = "SELECT * FROM STUDENTS"
                stmt = ibm_db.exec_immediate(conn, command)
                result = ibm_db.fetch_assoc(stmt)
                students = []
                while result:
                    students.append(result)
                    result = ibm_db.fetch_assoc(stmt)
                app.logger.debug(f"Fetched {len(students)} students from the database.")
                return render_template('./index.html', students=students)

            except Exception as e:
                app.logger.error(f"Error fetching data: {e}")
                traceback.print_exc()
                flash(f"Lỗi khi lấy dữ liệu: {e}", 'danger')
                return render_template('./index.html', students=None)

            finally:
                if conn:
                    ibm_db.close(conn)
                    app.logger.debug("Database connection closed.")

    else:
        flash("Không thể kết nối cơ sở dữ liệu.", 'danger')
        return render_template('./index.html', students=None)

# Error Handler for 500 Errors
@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Internal server error: {error}")
    traceback.print_exc()
    flash("Đã xảy ra lỗi nội bộ trên máy chủ. Vui lòng thử lại sau.", 'danger')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)


