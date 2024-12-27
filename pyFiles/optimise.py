import numpy as np
import pandas as pd
import joblib
from scipy.optimize import minimize
import analyse
import train
import csv
from analyse import run_analysis
# Load the pre-trained model
model = joblib.load('../models/ridge_model.joblib')

print("Model loaded for optimization.")

def objective(params, length, thresholdS, thresholdD):
    ym, pr, width, height = params
    prediction = model.predict([[ym, pr, length, width, height]])
    predicted_stress, predicted_displacement = prediction[0]
    # Calculate penalties
    stress_penalty = max(0, predicted_stress - thresholdS)
    displacement_penalty = max(0, predicted_displacement - thresholdD)
    # Add regularization terms to avoid zero/near-zero dimensions
    dimension_penalty = 1e6 * (1 / max(width, 1e-3) + 1 / max(height, 1e-3)) # Large penalty for very small values
    # Objective is to minimize penalties and avoid small dimensions
    return stress_penalty + displacement_penalty + dimension_penalty


def validate_and_adjust(ym, pr, l, w, h, force, thresholdS, thresholdD):

    # Run FEA with the discrete material properties
    displacement, stress = analyse.run_analysis(ym, pr, l, w, h, force)
    # Adjust w and h iteratively if thresholds are exceeded
    while stress > thresholdS or displacement > thresholdD:
    # Slightly reduce w and h to bring stress and displacement down
        w *= 1.2  # Reduce width by 5%
        h *= 1.2  # Reduce height by 5%
    # Re-run FEA with adjusted dimensions
        displacement, stress = analyse.run_analysis(ym, pr, l, w, h, force)
    return w, h, displacement, stress

def retrain(ym, pr, l, w, h, displacement, stress):
    prediction = model.predict([[ym, pr, l, w, h]])
    predicted_displacement, predicted_stress = prediction[0]
    tolerance = 1e-5
    if abs(predicted_stress - stress) > 0.05 * stress or abs(predicted_displacement - displacement) > tolerance:
        dataset_csv = '../datasets/dataset_csv.csv'
        row = [ym, pr, w, h, displacement, stress]
        with open(dataset_csv, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)
        train.train_model()
        regression = "These are the optimized parameters and corresponding FEA values"
        return ym, pr, l, w, h, displacement, stress, regression
    else:
        regression = "These are the optimized parameters and corresponding regression values"
        return ym, pr, l, w, h, predicted_displacement, predicted_stress, regression #test

def findClosestYMPR(optimal_Ym, optimal_Pr):
    data = pd.read_csv('../datasets/materials.csv')
    ymColumn  = 'Youngs_modulus'
    prColumn = 'Poissons_ratio'
    ymValues = data[ymColumn].values
    prValues = data[prColumn].values
    return ymValues[np.abs(ymValues - optimal_Ym).argmin()], prValues[np.abs(ymValues - optimal_Pr).argmin()]
def optimise(ym, pr, l, w, h, force, thresholdS, thresholdD):
    bounds = [(0, None), # Young's modulus
    (0, 0.5), # Poisson's ratio
    (0, None), # Width
    (0, None)]
    fea_displacement, fea_stress = run_analysis(ym, pr, l , w, h, force)
    if fea_displacement <= thresholdD and fea_stress <= thresholdS:
        ym, pr, l, w, h, displacement, stress, regression = retrain(ym, pr, l, w, h, fea_displacement, fea_stress)
        return ym, pr, l, w, h, displacement, stress, regression
    initial_guess = np.array([ym,pr, w, h])
    # Set initial guess and bounds based on initial data range
    result = minimize(
    objective,
    initial_guess,
    args=(l, thresholdS, thresholdD),
    bounds=bounds,
    method='L-BFGS-B' # Suitable for continuous variable optimization
    )
    ym, pr, w, h = result.x
    ym, pr = findClosestYMPR(ym, pr)
    w, h, displacement, stress = validate_and_adjust(ym, pr, l, w, h, force, thresholdS, thresholdD)
    ym, pr, l, w, h, displacement, stress, regression = retrain(ym, pr, l, w, h, displacement, stress)
    return ym, pr, l, w, h, displacement, stress, regression


#finds closest youngs modulus and poissons ratio



