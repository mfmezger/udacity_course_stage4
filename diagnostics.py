
import pandas as pd
import subprocess
import pickle
import numpy as np
import timeit
import os
import json
from ingestion import merge_multiple_dataframes
from training import train_model
from loguru import logger


##################Load config.json and get environment variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path'], "finaldata.csv") 
test_data_path = os.path.join(config['test_data_path'], "testdata.csv") 
model_path = os.path.join(config['output_model_path'], "trainedmodel.pkl")


##################Function to get model predictions
def model_predictions(dataset: pd.DataFrame):

    # read the deployed model
    model = pickle.load(open(model_path, 'rb'))

    # predict the test data
    x_data = dataset[['lastmonth_activity', 'lastyear_activity', 'number_of_employees']]
    y_pred = model.predict(x_data)

    return y_pred

##################Function to get summary statistics
def dataframe_summary():
    #calculate summary statistics here

    # load the dataset
    df = pd.read_csv(dataset_csv_path)

    # do pandas describe only for the numeric columns
    df_numeric = df[['lastmonth_activity', 'lastyear_activity', 'number_of_employees']]
    return df_numeric.describe()

def missing_values_percentage():
    df = pd.read_csv(dataset_csv_path)
    # calculate the nan percentage for each column
    return df.isnull().sum() / len(df) * 100


##################Function to get timings
def execution_time():

    # start the timer
    start = timeit.default_timer()
    train_model()
    stop = timeit.default_timer()
    training_time = stop - start

    # start the timer
    start = timeit.default_timer()
    merge_multiple_dataframes()
    stop = timeit.default_timer()
    ingestion_time = stop - start

    return [ingestion_time, training_time]


##################Function to check dependencies
def outdated_packages_list():
    #get a list of current and latest versions of modules used in this script
    with open('requirements.txt', 'r') as f:
        modules = f.read().splitlines()

    modules_info = []
    for module in modules:
        module_name, current_version = module.split('==')
        latest_version_output = subprocess.run(['pip', 'index', 'versions', module_name],
                                               capture_output=True, text=True)
        latest_version = latest_version_output.stdout.split('versions: ')[1].split(', ')[0]
        modules_info.append({
            'module_name': module_name,
            'current_version': current_version,
            'latest_version': latest_version
        })

    df_modules = pd.DataFrame(modules_info)

    with open('dependencies.json', 'w') as f:
        json.dump(df_modules.to_dict('records'), f)

    return df_modules.to_json(orient="records")



if __name__ == '__main__':

    dataset = pd.read_csv(test_data_path)
    logger.info(model_predictions(dataset=dataset))
    logger.info(dataframe_summary())
    logger.info(execution_time())
    logger.info(outdated_packages_list())





    
