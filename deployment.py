import os
import json
import shutil
from pathlib import Path


##################Load config.json and correct path variable
with open('config.json','r') as f:
    config = json.load(f) 

prod_deployment_path = os.path.join(config['prod_deployment_path']) 
ingestfiles_path = os.path.join(config['output_folder_path'], "ingestedfiles.txt")
output_model_path = os.path.join(config['output_model_path'], "trainedmodel.pkl")
latestscore_path = os.path.join(config['output_model_path'], "latestscore.txt")


####################function for deployment
def store_model_into_pickle():
    #copy the latest pickle file, the latestscore.txt value, and the ingestfiles.txt file into the deployment directory
    # copy the latest pickle file

    # generate a new folder
    Path(prod_deployment_path).mkdir(parents=True, exist_ok=True)

    shutil.copy2(ingestfiles_path, os.path.join(prod_deployment_path, "ingestedfiles.txt"))
    shutil.copy2(output_model_path, os.path.join(prod_deployment_path,"trainedmodel.pkl"))
    shutil.copy2(latestscore_path, os.path.join(prod_deployment_path,"latestscore.txt"))


if __name__ == '__main__':
    # load the trained model from the output_model_path file
    store_model_into_pickle()
    print("Done!")        
        

