from flask import Flask,request,render_template

import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData,PredictPipeline


app=Flask(__name__)

#route forHomepage
@app.route("/")
def index():
    return render_template('index.html')


@app.route('/predictData',methods=['GET','POST'])
#here in below function we will be doing everything i. e from getting data  to doing predications 
def predication_datapoint():
    if request.method=='GET':
        return render_template('home.html')#here simple input data fields that we need to provide in our models predications
    else:
        #else means ---when method is post-----here from getting capture data standardd scaling has to be done or feauture scaling
        data=CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('race_ethnicity'),
            lunch=request.form.get('lunch'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=request.form.get('reading_score'),
            writing_score=request.form.get('writing_score')      
            )
        
        pred_df=data.get_data_as_data_frame()
        print(pred_df)
        print("Before Predications")

        predict_pipeline=PredictPipeline()
        print(predict_pipeline)
        print("mid predicayions")

        final=predict_pipeline.predict(pred_df)
        print(final)
        print("after predications")
        
        return render_template("home.html",final=int(final[0]))
    

if __name__=='__main__':
    app.run(host='127.0.0.1',port=5000,debug=True)  # use this when host='127.0.0.2' #http://127.0.0.1:5000  -----use this when host='0.0.0.0'#http://localhost:5000

