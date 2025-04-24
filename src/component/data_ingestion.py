# as we have seen that we were using jupter and in that we were mostly using predefined modules of python or methods were used now from here with the help of python coding we will create our model steps will be same as in ipynb model trainer file only difference is we will use python code for actualling describing hte methods etc


# main work :
# loading the data------------can be from anywhere haddoop ,api,mongodbetc database
# aim:to readdataset from specific soures
# and spliting of data( train_test_split)




# Generaaly we will be using hte functions ,class ,variables ,assignments, inheritence and package importing in all our python file    




import os
import sys

from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass

import pandas as pd


from sklearn.model_selection import train_test_split

#whenever we are performing the data ingestion there should be some inputs that may be probably required by the data ingestion such as location of train dataset ,locatoin of test dataset, location of raw dataset this type of inputs will be stored in different class od data ingestion

# and this class will be callled as dataingestionconfig class----whatever inputs we are required in my data ingestion comoponent  we will give over here
#so when doing datatransformation there also we are required to pass this dataingestionconfig


# output can be anything ---numpy array,file_folder can be anything 

@dataclass
class DataIngestionConfig:
    train_data_path:str=os.path.join('artifact','train.csv')
    test_data_path:str=os.path.join('artifact','test.csv')
    raw_data_path:str=os.path.join('artifact','raw.csv')

class DataIngestion:

    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    def Initiate_data_ingestion(self):
        logging.info("entered the initiate data ingestion function")
        try:
            #so first read datset
            logging.info("loading the dataset has a dataframe")
            df=pd.read_csv(r'C:\Users\cnc\Desktop\0.0.1\notebook\DataSet\StudentData.csv')
            logging.info("Read the dataset has a dataframe")
            #lets create data path or folders for our train ,test, raw dataset---------folder is artifact---file inside this folder are train.csv,test.csv,raw.csv
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)# folder (directory) can be created with (  test or raw_data_path also)
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            logging.info("train_test_split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            logging.info("ingestion of data is completed")
            #this below step is important in data transformation 
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)

if __name__=='__main__':
    obj=DataIngestion()
    obj.Initiate_data_ingestion()

