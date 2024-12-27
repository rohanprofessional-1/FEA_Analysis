import requests
url = 'http://127.0.0.1:5000/analyze'
data = {'Youngs_modulus': 0.3, 'Poissons_ratio': 0.5, 'thresholdD' : 0.23,'thresholdS': 0.24, 'Length' : 1, 'Width' : 0.05, 'Height': 0.05, }

response = requests.post(url, json=data)
