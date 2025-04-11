from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


# Function to calculate real size
def calculate_real_size(microscope_size, magnification_factor):
    return microscope_size / magnification_factor

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        microscope_size = float(request.form['microscope_size'])
        magnification_factor = float(request.form['magnification_factor'])
        
        real_size = calculate_real_size(microscope_size, magnification_factor)


        
        # Insert data into database
        conn = sqlite3.connect('specimens.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS specimen_data (
                    username TEXT,
                    microscope_size REAL,
                    magnification_factor REAL,
                    real_size REAL)''')
        cursor.execute('''INSERT INTO specimen_data (username, microscope_size, magnification_factor, real_size) 
                          VALUES (?, ?, ?, ?)''', (username, microscope_size, magnification_factor, real_size))
        conn.commit()
        conn.close()
        
        return render_template('index.html', real_size=real_size)
    return render_template('index.html', real_size=None)

if __name__ == '__main__':
    app.run(debug=True)
