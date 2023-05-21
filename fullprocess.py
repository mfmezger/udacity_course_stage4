import os
import json
import subprocess
import training
import scoring
import deployment
import diagnostics
import reporting


def main():
    with open('config.json', 'r') as f:
        config = json.load(f)

    input_folder_path = config['input_folder_path']
    output_folder_path = config['output_folder_path']
    prod_deployment_path = config['prod_deployment_path']

    deployed_model_path = os.path.join(prod_deployment_path, "trainedmodel.pkl")
    ingested_files_path = os.path.join(prod_deployment_path, "ingestedfiles.txt")
    latest_score_path = os.path.join(prod_deployment_path, "latestscore.txt")

    ##################Check and read new data
    with open(ingested_files_path) as f:
        ingested_files_list = f.read().splitlines()

    all_files_ingested = all(
        os.path.join(input_folder_path, file_name) in ingested_files_list
        for file_name in os.listdir(input_folder_path)
    )

    ##################Deciding whether to proceed, part 1
    if not all_files_ingested:
        print(f"New data found. Ingest new datasets from {input_folder_path}")
        subprocess.call(['python', 'ingestion.py'])
    else:
        print("No new data found. Exit the process")
        return

    ##################Checking for model drift
    with open(latest_score_path, 'r') as f:
        latest_score = float(f.read())
    new_score = scoring.score_model()
    print(f'latest score: {latest_score}, score on newly ingested data: {new_score}')

    ##################Deciding whether to proceed, part 2
    if new_score < latest_score:
        print('Detect model drift. Retrain and redeploy model')
    else:
        print('No model drift happened')
        return

    ##################Re-deployment
    subprocess.call(['python', 'training.py'])
    subprocess.call(['python', 'scoring.py'])
    subprocess.call(['python', 'deployment.py'])

    ##################Diagnostics and reporting
    subprocess.call(['python', 'diagnostics.py'])
    subprocess.call(['python', 'reporting.py'])
    subprocess.call(['python', 'apicalls.py'])


if __name__ == '__main__':
    main()