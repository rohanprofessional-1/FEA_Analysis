from itertools import product
import numpy as np
import pandas as pd
import csv
import analyse



def create_dataset():
        lower_bound = 1.0
        upper_bound = 5.0
        num_points = 25
        precision = 1
        data = np.linspace(lower_bound, upper_bound, num_points)
        dataW = np.round(data, precision)
        dataH = np.round(data, precision)
        input_data = pd.read_csv('../datasets/materials.csv')
        youngs_modulus = input_data['Youngs_modulus']
        youngs_modulus = np.array(youngs_modulus)
        poissons_ratio = input_data['Poissons_ratio']
        poissons_ratio = np.array(poissons_ratio)
        material_arr = [[youngs_modulus],[poissons_ratio]]
        headers = ['Youngs_modulus', 'Poissons_ratio', 'Width', 'Height', 'max_displacement', 'max_stress']
        combinations = list(product(dataW, dataH))

        final_combinations = [
             (a, b, (youngs_modulus[i], poissons_ratio[i]))
             for (a, b) in combinations
             for i in range(len(youngs_modulus))
        ]

        dataset_csv = '../datasets/dataset_csv.csv'


        with open(dataset_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for i in range(len(final_combinations)):
                displacement, stress = analyse.run_analysis(final_combinations[i][2][0], final_combinations[i][2][1], 1, final_combinations[i][0], final_combinations[i][1], 1000)
                row = [final_combinations[i][2][0], final_combinations[i][2][1], final_combinations[i][0], final_combinations[i][1], displacement, stress]
                writer.writerow(row)



if __name__ == '__main__':
    create_dataset()