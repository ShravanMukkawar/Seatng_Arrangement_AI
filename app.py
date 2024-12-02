from flask import Flask, render_template, send_file
import pandas as pd

app = Flask(__name__)

# Load seating data
seating_file = "students_guests_seating.csv"
seating_data = pd.read_csv(seating_file)

# Create route to display the seating chart
@app.route("/")
def seating_chart():
    rows = []
    for _, row in seating_data.iterrows():
        rows.append(row.to_dict())  # Convert rows to dictionary for template rendering
    return render_template("seating_chart.html", rows=rows)

# Route to download the CSV
@app.route("/download")
def download_csv():
    return send_file(seating_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
