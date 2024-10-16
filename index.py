import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import csv
import pandas as pd

rows = {
    "R1": 20, "R2": 20, "R3": 20, "R4": 25, "R5": 27, "R6": 28, "R7": 29,
    "R8": 29, "R9": 29, "R10": 29, "R11": 29, "R12": 29, "R13": 29, "R14": 29,
    "R15": 29, "R16": 29, "R17": 29, "R18": 29, "R19": 29, "R20": 29, "R21": 29,
    "R22": 29
}

guest_rows = ["R1", "R2"]
student_rows = list(rows.keys())[2:] 

seating_chart = []

data_df = pd.read_csv('students_guests.csv')

guests_df = data_df[data_df['Type'] == 'Guest']
print("Number of guests loaded:", len(guests_df))

for row in guest_rows:
    seating_chart.append([1] * rows[row])  

students_df = data_df[data_df['Type'] == 'Student']
print("Number of students loaded:", len(students_df))

for row in student_rows:
    seating_chart.append([2] * rows[row])  

max_seats = max(rows.values())
grid = np.zeros((len(seating_chart), max_seats))

for i, seats in enumerate(seating_chart):
    grid[i, :len(seats)] = seats

fig, ax = plt.subplots(figsize=(10, 10))

cmap = plt.get_cmap("viridis")
colors = [cmap(i / 2) for i in range(3)]
cmap = mcolors.ListedColormap(colors)
bounds = [0, 1, 2, 3]
norm = mcolors.BoundaryNorm(bounds, cmap.N)

ax.imshow(grid, cmap=cmap, norm=norm, interpolation='none')

guest_index = 0
student_index = 0 

for i in range(len(seating_chart)):
    for j in range(len(seating_chart[i])):
        if grid[i, j] == 1:
            if guest_index < len(guests_df):  
                ax.text(j, i, 'G', va='center', ha='center', color='white', fontsize=16, fontweight='bold')  # Guests
                guest_index += 1  # Increment index for next guest
        elif grid[i, j] == 2:
            if student_index < len(students_df):  # Ensure students available
                student_name = students_df.iloc[student_index]['Name']
                mis_no = students_df.iloc[student_index]['MIS No']
                # Display 'S' with MIS number
                ax.text(j, i, f'S {mis_no}', va='center', ha='center', color='black', fontsize=16, fontweight='bold')
                student_index += 1  # Increment index for next student
            else:
                ax.text(j, i, 'S', va='center', ha='center', color='red', fontsize=16, fontweight='bold')  # Unassigned seat

# Set ticks and labels
ax.set_xticks(np.arange(max_seats))
ax.set_yticks(np.arange(len(seating_chart)))
ax.set_xticklabels(np.arange(1, max_seats + 1))
ax.set_yticklabels(list(rows.keys()))

plt.xticks(rotation=90)
plt.yticks(rotation=0)

ax.grid(which='both', color='black', linestyle='-', linewidth=1)
ax.set_xlabel('Seat Number')
ax.set_ylabel('Row')

plt.title('Seating Arrangement')

plt.savefig('seating_arrangement.pdf', bbox_inches='tight')
print("Seating arrangement has been saved as 'seating_arrangement.pdf'")

plt.show()

students = []
guests = []  # List to store guest seating information
students_not_assigned = []
guest_index = 0
student_index = 0

for row_idx, row in enumerate(seating_chart):
    row_label = list(rows.keys())[row_idx]
    for seat_idx, seat in enumerate(row):
        if seat == 1 and guest_index < len(guests_df):  
            guest_name = guests_df.iloc[guest_index]['Name']
            guests.append([guest_name, 'Guest', '', '', row_label, seat_idx + 1])  # Append guest info
            guest_index += 1  # Increment index for next guest
        elif seat == 2 and student_index < len(students_df):  # Assign students only in student rows
            student_name = students_df.iloc[student_index]['Name']
            mis_no = students_df.iloc[student_index]['MIS No']
            branch = students_df.iloc[student_index]['Branch']
            seat_number = seat_idx + 1  # Seat numbers start from 1
            
            # Store assigned seat info
            students.append([student_name, 'Student', mis_no, branch, row_label, seat_number])
            student_index += 1

with open('students_guests_seating.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Type', 'MIS No', 'Branch', 'Row', 'Seat Number'])  # Updated header
    writer.writerows(students)  # Write student information

    # Write guest information only if available
    if guests:  # Check if there are guests to write
        writer.writerows(guests)  # Write guest information
        print(f"{len(guests)} guests have been added to the seating.")
    else:
        print("No guests to write to the CSV.")

print("Seating information has been written to 'students_guests_seating.csv'")
