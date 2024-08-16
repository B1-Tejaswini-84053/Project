


import flask
import pickle
import pandas as pd
import numpy as np



# load models at top of app to load into memory only one time
with open('models/model.pkl', 'rb') as f:
    model = pickle.load(f)







app = flask.Flask(__name__, template_folder='templates')
@app.route('/')
def main():
    return (flask.render_template('index.html'))

@app.route('/report')
def report():
    return (flask.render_template('report.html'))



@app.route("/Individual", methods=['GET', 'POST'])
def Individual():
    
    if flask.request.method == 'GET':
        return (flask.render_template('Individual.html'))
    
    if flask.request.method =='POST':
        
        #get input
        
        # 1. age as integer
        age = int(flask.request.form['age'])

        # 2. monthly income as float
        monthly_inc = float(flask.request.form['monthly_inc'])

        # 3. credit score as integer
        credit_score = int(flask.request.form['credit_score'])

        # 4. number of months employed
        monthsEmployed = int(flask.request.form['monthsEmployed'])

        # 5. debt to income as float
        dti = float(flask.request.form['dti'])/100

        # 6. Rate of Interest
        roi = float(flask.request.form['interest_rate'])

        # 7. loan amount as integer
        loan_amnt = float(flask.request.form['loan_amnt'])

        # 8. education
        education_h = flask.request.form['education']

        if education_h == "Bachelor's":
            education = 0
        elif education_h == "High School":
            education = 1
        elif education_h == "Master's" :
            education = 2
        else:
            education = 3


        # 9. Has Mortgage
        hasMortgage_h = flask.request.form['hasMortgage']

        if hasMortgage_h == "Yes":
            hasMortgage = 1
        else:
            hasMortgage = 0

        # 10. Has Dependents
        hasDependents_h = flask.request.form['hasDependents']
        if hasDependents_h == "Yes":
            hasDependents = 1
        else:
            hasDependents = 0

        # 11. Has CoSigner
        hasCoSigner_h = flask.request.form['hasCoSigner']
        if hasCoSigner_h == "Yes":
            hasCoSigner = 1
        else:
            hasCoSigner = 0



        temp = pd.DataFrame(index=[1])

        temp['Age']=age
        temp['Income']=monthly_inc
        temp['LoanAmount'] = loan_amnt
        temp['CreditScore']=credit_score
        temp['MonthsEmployed']=monthsEmployed
        temp['InterestRate'] = roi
        temp['DTIRatio'] = dti
        temp['Education']=education
        temp['HasMortgage']=hasMortgage
        temp['HasDependents']=hasDependents
        temp['HasCoSigner']=hasCoSigner
        

        

        
            
        #make prediction
        pred = model.predict(temp)
        
        if dti > 43:
            res = 'Debt to income too high!'
        elif age > 50:
            res = 'Loan Denied'
        elif pred == 1:
            res = 'Loan Denied'

        else:
            res = 'Congratulations! Approved!'

        original_input = {
            'Age': age,
            'Income': monthly_inc,
            'LoanAmount': loan_amnt,
            'CreditScore': credit_score,
            'MonthsEmployed': monthsEmployed,
            'InterestRate': roi,
            'DTIRatio': dti,
            'Education': education_h,
            'HasMortgage': hasMortgage_h,
            'HasDependents': hasDependents_h,
            'HasCoSigner': hasCoSigner_h
        }
        
        # render form again and add prediction
        return flask.render_template('Individual.html',
                                     result=res,
                                     original_input=original_input
                                     )


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)