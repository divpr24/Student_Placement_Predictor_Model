from flask import Flask,render_template, request,url_for, jsonify
import pickle
import numpy as np

model = pickle.load(open('model.pkl','rb'))
app = Flask(__name__, template_folder = "template")

@app.route('/')
def index():
    return render_template('Placement_Model.html')

@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method == 'GET':
        return render_template('Placement_Model.html')
    else:
        cgpa = float(request.form['cgpa'])
        iq = int(request.form['iq'])
        profile_score = int(request.form['profile_score'])

        # prediction
        y_pred = model.predict(np.array([cgpa,iq,profile_score]).reshape(1,3))
        status = " "
        if y_pred == 1:
            status = "Placed"
        else:
            status = "Not Placed"

    return render_template('Placement_Model.html',result = status)
    #return str(y_pred)

@app.route('/api', methods = ['POST'])
def pred_Status():
    data = request.json()
    cgpa = float(dict(data)['cgpa'])
    iq = float(dict(data)['iq'])
    profile_score = float(dict(data)['profile_score'])

    y_pred = model.predict(np.array([cgpa,iq,profile_score]).reshape(1,3))
    status = " "
    if y_pred == 1:
        status = "Placed"
    else:
        status = "Not Placed"

    return jsonify(status)

if __name__ == "__main__":
    app.run(debug = True)