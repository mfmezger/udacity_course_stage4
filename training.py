import pandas as pd
import pickle
import os
from sklearn.linear_model import LogisticRegression
import json
from pathlib import Path
from loguru import logger

###################Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path'], config['dataset_csv'])
output_model_path = config['output_model_path']


#################Function for training the model
def train_model():
    
    #use this logistic regression for training
    model = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                    intercept_scaling=1, l1_ratio=None, max_iter=100,
                    multi_class='auto', n_jobs=None, penalty='l2',
                    random_state=0, solver='liblinear', tol=0.0001, verbose=0,
                    warm_start=False)
    
    #fit the logistic regression to your data
    df = pd.read_csv(dataset_csv_path)
    x_data = df[['lastmonth_activity', 'lastyear_activity', 'number_of_employees']]
    y_data = df['exited']

    logger.info("Training model...")
    model.fit(x_data, y_data)
    
    #write the trained model to your workspace in a file called trainedmodel.pkl
    Path(output_model_path).mkdir(parents=True, exist_ok=True)
    logger.info("Writing model to {}".format(output_model_path))
    pickle.dump(model, open(os.path.join(output_model_path, "trainedmodel.pkl"), 'wb'))
    logger.info("Done!")

if __name__ == '__main__':
    train_model()
