#here we will do 
#scale data ,encoding and dataclening


from src.exception import CustomException
from src.logger import logging
from src.utils import save_obj

import sys 
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd 

#columntransformer ----used for generating pipeline
from sklearn.compose import ColumnTransformer
#for scaling and encoding
from sklearn.preprocessing import StandardScaler,OneHotEncoder
#for checking if null value presence #responsible for hnadling missing values
from sklearn.impute import SimpleImputer
#for creatinf an pipeline
from sklearn.pipeline import Pipeline

#as we did in data ingestion samw we will do for datatransformation
#for inputs we will create datatransformatoin config
@dataclass
class DataTransformationConfig:
    #this config will give me any path any inputs that we might required for our model 
    #we want pickle file
    preprocessor_obj_file_path=os.path.join('artifact','preprocessor.pkl')
class DataTransformation:
    #Creting all this function so that it can pickle file which will be responsible for converting cat to num 
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    
    def get_datatransformer_obj(self):
        "this function is reponsible for data transformation"




        try:
            #numerical feautures and categorigal feautures
            num_column=['reading score', 'writing score']
            cat_column=['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'test preparation course']
            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),#median ---becoz outliers are present as we seen in eda
                    ("scaler",StandardScaler())
                ]
            )
            logging.info("numerical Standard scaling completed")
            cat_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("OneHotEncoding",OneHotEncoder())
                ]
            )
            logging.info("Categorigal encoding completed")
            preprocessor=ColumnTransformer(
                [
                    ["num_pipeline",num_pipeline,num_column],
                    ['cat_pipeline',cat_pipeline,cat_column]

                ]
            )
            return preprocessor
        

        except Exception as e:
            raise CustomException(e,sys)
        

    def initiate_data_transformation(self,train_path,test_path):
        #starting all the datatransformation steps  
        try:
            #getting this values from data ingestion
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Reading data from train and test data completed")
            logging.info("Obtaing preprocessing obj")
            #above preprocessor object we created where encoding and standardscaling is getting initialized now we will use them in our train data and test data
            #make sure this needs to be converted in a pickle file
            preprocesser_obj=self.get_datatransformer_obj()
            target_column_name="math score"
            num_columns=['reading score', 'writing score']
            input_column_train_df=train_df.drop(columns=[target_column_name],axis=1)#x_train
            input_column_test_df=test_df.drop(columns=[target_column_name],axis=1)#x_test
            target_column_train_df=train_df[target_column_name]#y_train
            target_column_test_df=test_df[target_column_name]#y_test
            logging.info("appling preprocessing obj into train and test df")

            input_column_train_df_arr=preprocesser_obj.fit_transform(input_column_train_df)
            input_column_test_df_arr=preprocesser_obj.transform(input_column_test_df)
            train_arr=np.c_[
                input_column_train_df_arr,np.array(target_column_train_df)
            ]
            test_arr=np.c_[
                input_column_test_df_arr,np.array(target_column_test_df)
            ]
            logging.info("saving preprocessing object")

            logging.info("Has to save our preprocessing_obj file")
            logging.info("Savinng our pickle file")

            save_obj(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocesser_obj
            )
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        except Exception as e:
            raise CustomException(e,sys)


