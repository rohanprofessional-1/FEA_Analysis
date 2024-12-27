import pandas as pd
from sklearn.linear_model import Ridge
import joblib

# Sample FEA analysis results (replace with actual PyMAPDL FEA output)
fea_results1 = pd.read_csv('../datasets/dataset_csv.csv')

def train_model():
    # Set up features and targets
    X = fea_results1[['Youngs_modulus', 'Poissons_ratio', 'Width', 'Height']]
    y = fea_results1[['max_displacement', 'max_stress']]

    # Train the ridge regression model
    ridge_model = Ridge(alpha=1.0)
    ridge_model.fit(X, y)

    # Save the trained model to a file
    joblib.dump(ridge_model, '../models/ridge_model.joblib')
    print("ModelYP trained and saved.")



if __name__ == '__main__':
    train_model()