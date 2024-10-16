from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students')
def students():
    # Load student data from CSV
    df = pd.read_csv('students.csv')
    # Convert the DataFrame to a dictionary
    students_data = df.to_dict(orient='records')
    return jsonify(students_data)

if __name__ == '__main__':
    app.run(debug=True)
