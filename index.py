import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import csv
import pandas as pd
import random

# Constants
POPULATION_SIZE = 50
GENERATIONS = 100
MUTATION_RATE = 0.1

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

# Load data from the CSV file
data_df = pd.read_csv('students_guests.csv')
guests_df = data_df[data_df['Type'] == 'Guest']
faculty_df = data_df[data_df['Type'] == 'Faculty']
gold_df = data_df[data_df['Type'] == 'Gold']
students_df = data_df[data_df['Type'] == 'Student']

# Genetic Algorithm Functions
def encode_seating():
    """Create a random seating arrangement."""
    seating = []
    for row in rows.keys():
        seating.append([random.randint(1, 4) for _ in range(rows[row])])  # Randomly assign types
    return seating

def calculate_fitness(seating):
    """Calculate fitness of a seating arrangement."""
    score = 0
    for i, row in enumerate(seating):
        row_type = list(rows.keys())[i]
        if row_type in guest_rows:
            score += sum(1 for seat in row if seat == 1)  # Guests in guest rows
        elif row_type in faculty_rows:
            score += sum(1 for seat in row if seat == 3)  # Faculty in faculty rows
        elif row_type in gold_medalist_rows:
            score += sum(1 for seat in row if seat == 4)  # Gold medalists in correct rows
        elif row_type in student_rows:
            score += sum(1 for seat in row if seat == 2)  # Students in student rows
    return score

def mutate(seating):
    """Mutate a seating arrangement."""
    for row in seating:
        if random.random() < MUTATION_RATE:
            idx = random.randint(0, len(row) - 1)
            row[idx] = random.randint(1, 4)  # Mutate to a random type
    return seating

def crossover(parent1, parent2):
    """Perform crossover between two parents."""
    crossover_point = random.randint(0, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# Initialize population
population = [encode_seating() for _ in range(POPULATION_SIZE)]

# Run Genetic Algorithm
for generation in range(GENERATIONS):
    fitness_scores = [calculate_fitness(individual) for individual in population]
    best_fitness = max(fitness_scores)
    print(f"Generation {generation + 1}, Best Fitness: {best_fitness}")

    # Selection: Select the top individuals
    sorted_population = [x for _, x in sorted(zip(fitness_scores, population), key=lambda pair: pair[0], reverse=True)]
    population = sorted_population[:POPULATION_SIZE // 2]

    # Crossover: Generate new offspring
    new_population = population[:]
    while len(new_population) < POPULATION_SIZE:
        parent1, parent2 = random.sample(population, 2)
        child1, child2 = crossover(parent1, parent2)
        new_population.extend([child1, child2])

    # Mutation: Apply mutation to the new population
    population = [mutate(individual) for individual in new_population]

# Finalize the best solution
best_solution = max(population, key=calculate_fitness)

# Create seating chart and output CSV
output_data = []
guest_index, faculty_index, gold_index, student_index = 0, 0, 0, 0

for row_idx, row in enumerate(best_solution):
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

with open('students_guests_seating_ga.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Type', 'Seat Number'])
    writer.writerows(output_data)

print("Seating arrangement optimized and written to 'students_guests_seating_ga.csv'")
