import os
import json
import requests
from loguru import logger

#Specify a URL that resolves to your workspace
URL = "http://127.0.0.1:5000/"
with open('config.json','r') as f:
    config = json.load(f) 


apireturns = os.path.join(config["output_model_path"], "apireturns.txt")

#Call each API endpoint and store the responses
response1 = requests.post(URL + 'prediction', data={'path': json.dumps(os.path.join(config["test_data_path"],"testdata.csv"))})
logger.info(f"API response for prediction: {response1.json()}")
response2 = requests.get(URL + 'scoring')
logger.info(f"API response for scoring: {response2.json()}")
response3 = requests.get(URL + 'summarystats')
logger.info(f"API response for summarystats: {response3.json()}")
response4 = requests.get(URL + 'diagnostics')
logger.info(f"API response for diagnostics: {response4.json()}")

#combine all API responses
responses = {
    'prediction': response1.json(),
    'scoring': response2.json(),
    'summarystats': response3.json(),
    'diagnostics': response4.json()
}

#write the responses to your workspace
with open(apireturns, 'w') as f:
    json.dump(responses, f)

logger.info("API responses written to {}".format(apireturns))