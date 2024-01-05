
from flask import Flask, render_template, request
import joblib
import pandas as pd
# import category_encoders as ce

app = Flask(__name__)

model = joblib.load(r'C:\Users\Admin\Desktop\car price prediction app\encoder\model.pkl')
target_encoder = joblib.load(r'C:\Users\Admin\Desktop\car price prediction app\encoder\encoder.pkl')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=["POST"])
def submit():
    carName=request.form['carName']
    print("-----------------------------")
    print(carName)
    year=int(request.form['year'])
    presentPrice=float(request.form['presentPrice'])
    kmsDriven=int(request.form['kmsDriven'])
    owner=int(request.form['owner'])
    fuelType=request.form['fuelType']
    sellerType=request.form['sellerType']
    transmissionType=request.form['transmissionType']

    if fuelType=='Diesel':
        Fuel_Type_Diesel=1
        Fuel_Type_Petrol=0
    else:
        Fuel_Type_Diesel=0
        Fuel_Type_Petrol=1

    if sellerType=='Individual':
        Seller_Type_Individual=1
    else:
        Seller_Type_Individual=0
    
    if transmissionType=='Manual':
        Transmission_Manual=1
    else:
        Transmission_Manual=0


    data=[[carName,year, presentPrice, kmsDriven, owner, Fuel_Type_Diesel,Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Manual]]

    columns = ['Car_Name', 'Year', 'Present_Price', 'Kms_Driven', 'Owner', 'Fuel_Type_Diesel', 'Fuel_Type_Petrol', 'Seller_Type_Individual', 'Transmission_Manual']

    # Create DataFrame
    input_df = pd.DataFrame(data, columns=columns)

    car_name_encoded=target_encoder.transform(input_df)
    
    prediction=model.predict(car_name_encoded)

    print(prediction)

    return render_template('submit.html', price=prediction)

if __name__ == '__main__':
    app.run(debug=True)
