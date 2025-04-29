import sys
import os

from src.exception import CustomException
from src.logger import logging
from src.utils import save_obj,evaluate_models
from dataclasses import dataclass


from sklearn.linear_model import LinearRegression,Ridge,Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import AdaBoostRegressor,GradientBoostingRegressor,RandomForestRegressor
from sklearn.svm import SVR
from catboost import CatBoostRegressor

#for performance metrics
from sklearn.metrics import mean_absolute_error,root_mean_squared_error,mean_squared_error,r2_score


@dataclass
class ModelTrainerConfig:
    #this class is reponsible for creating a pickle file for our trained model
    train_model_file_path=os.path.join('artifact','model.pkl')

class ModelTrainer:
    #this class is reponsible for training our model
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()
    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Spliting training and testing input data")
            #which is cominng from data transformation (train_arr,test_arr)---and in that train_arr and test_arr last feauture which getting add is target_feature 
            x_train,x_test,y_train,y_test=(
                train_array[:,:-1],#remove last column  and add everything #x_train
                test_array[:,:-1],#Remove last column and add everything #x_test
                train_array[:,-1],#add only last column #y_train
                test_array[:,-1]#add only last column #y_test
            )
            logging.info("spliitted the train and test data")
            #lets create a dictionary of models 
            #copying from model trainer
            models={
                
                "Ridge":Ridge(),
                "lasso":Lasso(),
                "knn":KNeighborsRegressor(),
                "ADR":AdaBoostRegressor(),
                "GBR":GradientBoostingRegressor(),
                "DTree":DecisionTreeRegressor(),
                "SVR":SVR(),
                "CatBoostR":CatBoostRegressor(verbose=False),
                "RFR":RandomForestRegressor()
            } 
            logging.info("Hyperparameter tuning")

            parameters={
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                 
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                
                "Ridge":{
                    'alpha': [0.001, 0.1, 1, 10, 100],
                    'fit_intercept': [True, False],
                    'solver': ['auto', 'svd', 'cholesky', 'lsqr', 'saga']
                },
                
                "CatBoosting Regressor":{
                    'depth': [6,8,10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    # 'loss':['linear','square','exponential'],
                    'n_estimators': [8,16,32,64,128,256]
                }
             
            }
            #evaluate_model is an function we have created in utils 

            model_report:dict=evaluate_models(x_train=x_train,x_test=x_test,y_train=y_train,y_test=y_test,models=models,param=parameters)
            logging.info("Hyperparameter tuning Completed")
            #to get best model score from dict
            best_model_score=max(sorted(model_report.values()))
            #to get best model name from dict ----best model name[index will be given of the best model score]
            best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            
            best_model=models[best_model_name]

            #just putting some thresold
            if best_model_score<0.6:
                raise CustomException("no best model found")
            
            logging.info("Best found model on train and test dataset")
            #will load the pickle file next : preprocessinf.pkl
            logging.info("saving our model _trainer in model.pkl file")
            save_obj(
                file_path=self.model_trainer_config.train_model_file_path,
                obj=best_model
            )
            logging.info("saved our model _trainer in model.pkl file")
            #seeing the best predicated output
            predicates=best_model.predict(x_test)
            r2=r2_score(y_test,predicates)
            return  r2,best_model

             


        except Exception as e:
            raise CustomException(e,sys)
        






