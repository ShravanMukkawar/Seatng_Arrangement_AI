import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import csv
import pandas as pd

# Define rows with seat counts
rows = {
    "R1": 20, "R2": 20,  # Guest rows
    "R3": 20, "R4": 25,  # Faculty rows
    "R5": 27, "R6": 28,  # Gold medalist rows
    "R7": 29, "R8": 29, "R9": 29, "R10": 29, "R11": 29,
    "R12": 29, "R13": 29, "R14": 29, "R15": 29, "R16": 29,
    "R17": 29, "R18": 29, "R19": 29, "R20": 29, "R21": 29,
    "R22": 29,
    "R23": 20, "R24": 20 
}

guest_rows = ["R1", "R2"]
faculty_rows = ["R3", "R4"]
gold_medalist_rows = ["R5", "R6"]

student_rows = [row for row in rows.keys() if row not in guest_rows + faculty_rows + gold_medalist_rows]

# Initialize seating chart
seating_chart = []

# Load data from the CSV file
data_df = pd.read_csv('students_guests.csv')

# Guests data
guests_df = data_df[data_df['Type'] == 'Guest']
print("Number of guests loaded:", len(guests_df))
for row in guest_rows:
    seating_chart.append([1] * rows[row])  # Use 1 for guests

# Faculty data
faculty_df = data_df[data_df['Type'] == 'Faculty']
print("Number of faculty loaded:", len(faculty_df))
for row in faculty_rows:
    seating_chart.append([3] * rows[row])  # Use 3 for faculty

# Gold medalists data
gold_df = data_df[data_df['Type'] == 'Gold']
print("Number of gold medalists loaded:", len(gold_df))
for row in gold_medalist_rows:
    seating_chart.append([4] * rows[row])  # Use 4 for gold medalists

# Students data
students_df = data_df[data_df['Type'] == 'Student']
print("Number of students loaded:", len(students_df))
for row in student_rows:
    seating_chart.append([2] * rows[row])  # Use 2 for students

# Create grid for seating chart
max_seats = max(rows.values())
grid = np.zeros((len(seating_chart), max_seats))

for i, seats in enumerate(seating_chart):
    grid[i, :len(seats)] = seats

# Plot seating arrangement
fig, ax = plt.subplots(figsize=(10, 10))

cmap = plt.get_cmap("viridis")
colors = [cmap(i / 4) for i in range(5)]
cmap = mcolors.ListedColormap(colors)
bounds = [0, 1, 2, 3, 4, 5]
norm = mcolors.BoundaryNorm(bounds, cmap.N)

ax.imshow(grid, cmap=cmap, norm=norm, interpolation='none')

# Create output CSV
output_data = []

guest_index = 0
faculty_index = 0
gold_index = 0
student_index = 0

for row_idx, row in enumerate(seating_chart):
    row_label = list(rows.keys())[row_idx]
    for seat_idx, seat in enumerate(row):
        if seat == 1 and guest_index < len(guests_df):  # Guests
            guest_name = guests_df.iloc[guest_index]['Name']
            output_data.append([guest_name, 'Guest', f"{row_label}-{seat_idx + 1}"])
            guest_index += 1
        elif seat == 2 and student_index < len(students_df):  # Students
            student_name = students_df.iloc[student_index]['Name']
            output_data.append([student_name, 'Student', f"{row_label}-{seat_idx + 1}"])
            student_index += 1
        elif seat == 3 and faculty_index < len(faculty_df):  # Faculty
            faculty_name = faculty_df.iloc[faculty_index]['Name']
            output_data.append([faculty_name, 'Faculty', f"{row_label}-{seat_idx + 1}"])
            faculty_index += 1
        elif seat == 4 and gold_index < len(gold_df):  # Gold Medalists
            gold_name = gold_df.iloc[gold_index]['Name']
            output_data.append([gold_name, 'Gold Medalist', f"{row_label}-{seat_idx + 1}"])
            gold_index += 1

with open('students_guests_seating.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Type', 'Seat Number'])
    writer.writerows(output_data)

print("Seating information has been written to 'students_guests_seating.csv'")


print("Seating information has been written to 'students_guests_seating.csv'")
