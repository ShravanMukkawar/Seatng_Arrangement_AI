import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import csv

rows = {
    "R1": 20, "R2": 20, "R3": 20, "R4": 25, "R5": 27, "R6": 28, "R7": 29,
    "R8": 29, "R9": 29, "R10": 29, "R11": 29, "R12": 29, "R13": 29, "R14": 29,
    "R15": 29, "R16": 29, "R17": 29, "R18": 29, "R19": 29, "R20": 29, "R21": 29,
    "R22": 29
}

guest_rows = ["R1", "R2"]
student_rows = list(rows.keys())[2:]

seating_chart = []

# Guest seating
for row in guest_rows:
    seating_chart.append([1] * rows[row])

# Student seating
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

# Add text labels
for i in range(len(seating_chart)):
    for j in range(len(seating_chart[i])):
        if grid[i, j] == 1:
            ax.text(j, i, 'G', va='center', ha='center', color='white')
        elif grid[i, j] == 2:
            ax.text(j, i, 'S', va='center', ha='center', color='white')

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

plt.show()

students = []
student_index = 0
for row_idx, row in enumerate(seating_chart):
    row_label = list(rows.keys())[row_idx]
    for seat_idx, seat in enumerate(row):
        if seat == 2:  
            student_name = f"Student{student_index + 1}"
            seat_number = seat_idx + 1 
            students.append([student_name, row_label, seat_number])
            student_index += 1

with open('students_seating.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Student Name', 'Row', 'Seat Number'])
    writer.writerows(students)

print("Student seating information has been written to 'students_seating.csv'")
