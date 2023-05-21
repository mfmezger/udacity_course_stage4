import pandas as pd
import os
import json
from pathlib import Path



#############Load config.json and get input and output paths
with open('config.json','r') as f:
    config = json.load(f) 

input_folder_path = config['input_folder_path']
output_folder_path = config['output_folder_path']


#############Function for data ingestion
def merge_multiple_dataframes() -> None:
    #check for datasets, compile them together, and write to an output file
    data_frame_list = []
    file_list = []

    # iterate over the input files and load the dataframes into one list and the names
    # in another list
    for file_name in os.listdir(input_folder_path):
        file_path = os.path.join(input_folder_path, file_name)
        
        data_frame = pd.read_csv(file_path)
        data_frame_list.append(data_frame)
        
        file_list.append(file_path + '\n')

    # generate a new folder 
    Path(output_folder_path).mkdir(parents=True, exist_ok=True) 

    final_data_frame = pd.concat(data_frame_list, axis=0, ignore_index=True).drop_duplicates()
    final_data_frame.to_csv(os.path.join(output_folder_path, "finaldata.csv"), index=False)

    with open(os.path.join(output_folder_path, "ingestedfiles.txt"), 'w') as f:
        f.writelines(file_list)


if __name__ == '__main__':
    merge_multiple_dataframes()
