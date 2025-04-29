# Why importtant -----create web app which will be interacting with our pickle files
# here we will create a form where we will be giving an input data data which will be required for predicating a students performance
#then on clicking submit the data will be submitted and from backend the process wil interact with preprocessor.pkl and model.pkl

import sys
import os
import pandas as pd
from src.exception import CustomException
from src.utils import load_obj

class PredictPipeline:
    def __init__(self):
        pass
    def predict(self,feauture):
        try:
            model_path=os.path.join('artifact','model.pkl')
            preprocessing_path=os.path.join('artifact','preprocessor.pkl')
            print("Before loading")
            model=load_obj(file_path=model_path)
            preprocessing=load_obj(file_path=preprocessing_path)
            print("after loading")
            data_scaled=preprocessing.transform(feauture)
            main_predication=model.predict(data_scaled)
            return main_predication
        
        except Exception as e:
            raise CustomException(e,sys)

        

class CustomData:
    def __init__(self,
                 gender:str,
                 race_ethnicity:str,
                 parental_level_of_education,lunch:str,
                 test_preparation_course:str,
                 reading_score:int,
                 writing_score:int):
        
        self.gender=gender
        self.race_ethnicity=race_ethnicity
        self.parental_level_of_education=parental_level_of_education
        self.lunch=lunch
        self.test_preparation_course=test_preparation_course
        self.reading_score=reading_score
        self.writing_score=writing_score
        
    def get_data_as_data_frame(self):
        #will return input in the form of dataframe
        try:
            custom_data_input_dict={
                "gender":[self.gender],
                "race_ethnicity":[self.race_ethnicity],
                "parental_level_of_education":[self.parental_level_of_education],
                "lunch":[self.lunch],
                "test_preparation_course":[self.test_preparation_course],
                "reading_score":[self.reading_score],
                "writing_score":[self.writing_score]
            }
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise CustomException(e,sys)
