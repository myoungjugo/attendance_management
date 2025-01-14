from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
import os
import mysql.connector
from datetime import datetime 

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "students_user"
app.config["MYSQL_PASSWORD"] = os.environ.get('DB_PW')
app.config["MYSQL_DB"] = "students_db"

@app.route("/", methods=["GET", "POST"])
def attendance():
    cursor = db.cursor()

    if request.method == "POST":
        student_name = request.form["student_name"]
        attendance_status = request.form["attendance_status"]
        score = float(request.form["score"])
        phone_submitted = request.form.get("phone_submitted") == "on"
        assignment_rate = float(request.form["assignment_rate"])
        class_name = request.form["class"]

        date = datetime.now().date()

            
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO attendance (student_name, attendance_status, score, phone_submitted, assignment_rate, class)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (student_name, attendance_status, score, phone_submitted, assignment_rate, class_name, date_time))

        cursor.execute("""
            SELECT AVG(score) FROM attendance WHERE class = %s
        """, (class_name,))
        average_score = cursor.fetchone()[0]

        cursor.execute("""
            UPDATE attendance SET average_score = %s WHERE class = %s
        """, (average_score, class_name))
        
        cursor.execute("""
            SET @rank := 0;
            UPDATE attendance
            SET rank = (@rank := @rank + 1)
            WHERE class = %s
            ORDER BY score DESC
        """, (class_name,))

        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('class_page', class_name=class_name))

    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT student_name, attendance_status, score, phone_submitted, assignment_rate, rank
        FROM attendance WHERE class = %s
    """, (class_name,))
    students = cursor.fetchall()
    cursor.close()

    return render_template("class_page.html", class_name=class_name, students=students)

@app.route('/class/<class_name>')
def class_page(class_name):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT student_name, score FROM attendance WHERE class = %s", (class_name,))
    students = cursor.fetchall()
    cursor.close()
    
    return render_template("class_page.html", class_name=class_name, students=students)


if __name__ == "__main__":
    app.run(debug=True)
