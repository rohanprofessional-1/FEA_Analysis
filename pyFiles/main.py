#from pyFiles import analyse
import optimize
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        Ym = request.json['Youngs_modulus']
        Pr = request.json['Poissons_ratio']
        thresholdS = request.json['thresholdS']
        thresholdD = request.json['thresholdD']

        W = request.json['Width']
        H = request.json['Height']
        # F = request.form['Force']

        #analyse.run_analysis(Ym, Pr, L, W, H, F)
        print(optimize.optimise(Ym, Pr, W, H, thresholdS, thresholdD))

        return str(optimize.optimise(Ym, Pr, W, H, thresholdS, thresholdD)),



if __name__ == '__main__':
    app.run(debug = True)