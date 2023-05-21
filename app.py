from flask import Flask, session, jsonify, request
import pandas as pd
from diagnostics import model_predictions, dataframe_summary, missing_values_percentage, execution_time, outdated_packages_list
from scoring import score_model
import json
import os
from loguru import logger



######################Set up variables for use in our script
app = Flask(__name__)
app.secret_key = '1652d576-484a-49fd-913a-6879acfa6ba4'

with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 



#######################Prediction Endpoint
@app.route("/prediction", methods=['POST','OPTIONS'])
def predict():        
    test_data_file_path = request.form.get('path')[1:-1]
    # load the test data

    logger.info("test_data_file_path: %s", test_data_file_path)
    test_data = pd.read_csv(test_data_file_path)


    result = model_predictions(test_data)
    return json.dumps([int(item) for item in result])

#######################Scoring Endpoint
@app.route("/scoring", methods=['GET','OPTIONS'])
def stats():        
    #check the score of the deployed model
    return json.dumps(score_model())

#######################Summary Statistics Endpoint
@app.route("/summarystats", methods=['GET','OPTIONS'])
def summarystats():        
    #check means, medians, and modes for each column
    return dataframe_summary().to_json(orient='records')
#######################Diagnostics Endpoint
@app.route("/diagnostics", methods=['GET','OPTIONS'])
def diagnostics():        
    # run timing, missing data, and dependency check
    return json.dumps([execution_time(), missing_values_percentage().to_json(), outdated_packages_list()])

if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
