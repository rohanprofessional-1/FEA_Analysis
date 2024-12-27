import xml.etree.ElementTree as ET
import csv

# Load XML file
xml_file = '../datasets/general mat.xml'
tree = ET.parse(xml_file)
root = tree.getroot()

# CSV file to save extracted data
csv_file = '../datasets/materials.csv'

# Open CSV file for writing
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header row
    writer.writerow(['Material Name', 'Young\'s Modulus (Pa)', 'Poisson\'s Ratio'])

    # Iterate over materials
    for material in root.findall(".//Material"):
        # Get the material name
        name = material.find(".//BulkDetails/Name").text

        # Initialize placeholders for Young's modulus and Poisson's ratio
        youngs_modulus = None
        poissons_ratio = None

        # Find property data
        for property_data in material.findall(".//PropertyData"):
            # Look for Young's Modulus
            if 'Derive from' in [qualifier.get("name") for qualifier in property_data.findall("Qualifier")]:
                youngs_modulus = property_data.find(".//ParameterValue[@parameter='pa10']/Data").text
                poissons_ratio = property_data.find(".//ParameterValue[@parameter='pa11']/Data").text

        # Write row to CSV if both properties are found
        if youngs_modulus and poissons_ratio:
            writer.writerow([name, float(youngs_modulus), float(poissons_ratio)])

print("Material properties extracted and saved to", csv_file)
