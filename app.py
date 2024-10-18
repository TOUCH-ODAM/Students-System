from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'a_random_and_secure_string'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    cursor.close()
    return render_template('index.html', students=data)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO students (first_name, last_name, email) VALUES (%s, %s, %s)", 
                       (first_name, last_name, email))
        mysql.connection.commit()
        cursor.close()

        flash("Student added successfully!")
        return redirect(url_for('index'))

@app.route('/delete/<string:id>', methods=['GET'])
def delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", [id])
    mysql.connection.commit()
    cursor.close()

    flash("Student deleted successfully!")
    return redirect(url_for('index'))

@app.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit(id):
    cursor = mysql.connection.cursor()
    
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        
        cursor.execute("UPDATE students SET first_name = %s, last_name = %s, email = %s WHERE id = %s", 
                       (first_name, last_name, email, id))
        mysql.connection.commit()
        cursor.close()

        flash("Student updated successfully!")
        return redirect(url_for('index'))
    else:
        cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
        student = cursor.fetchone()
        cursor.close()
        return render_template('edit.html', student=student)

if __name__ == "__main__":
    app.run(debug=True)
