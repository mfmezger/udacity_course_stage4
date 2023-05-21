import pandas as pd
import pickle
import os
from sklearn import metrics
import json
from loguru import logger



#################Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

test_data_path = os.path.join(config['test_data_path'], "testdata.csv") 
model_path = os.path.join(config['output_model_path'], "trainedmodel.pkl")


#################Function for model scoring
def score_model():
    #this function should take a trained model, load test data, and calculate an F1 score for the model relative to the test data
    #it should write the result to the latestscore.txt file

    #load the trained model from the output_model_path file
    model = pickle.load(open(model_path, 'rb'))

    # load the test data from the test_data_path file
    test_data = pd.read_csv(test_data_path)

    # split the test data into x_test and y_test
    x_data = test_data[['lastmonth_activity', 'lastyear_activity', 'number_of_employees']]
    y_data = test_data['exited']

    # calculate y_pred
    y_pred = model.predict(x_data)

    # calculate the f1 score and save it to the latestscore.txt file
    f1_score = metrics.f1_score(y_data, y_pred)
    logger.info("F1 score: {}".format(f1_score))
    with open(os.path.join(config['output_model_path'], "latestscore.txt"), 'w') as f:
        f.write(str(f1_score))

    return f1_score


if __name__ == '__main__':
    score_model()



