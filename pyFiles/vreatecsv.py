import csv

# Define the path for the new CSV file
csv_file_path = "../datasets/materials.csv"

# Sample data to populate the CSV file
materials_data = [
    ["material_name", "youngs_modulus", "poissons_ratio", "density"],
    ["Aluminum", 69e9, 0.33, 2700],
    ["Steel", 210e9, 0.3, 7850],
    ["Titanium", 116e9, 0.34, 4500],
]

# Write the data to the CSV file
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(materials_data)

print("CSV file created successfully!")
