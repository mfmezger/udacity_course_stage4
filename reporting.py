import pandas as pd
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from diagnostics import model_predictions


###############Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path'], "finaldata.csv")
cm_path = os.path.join(config['output_model_path'], "confusionmatrix.png")



##############Function for reporting
def score_model():
    #calculate a confusion matrix using the test data and the deployed model
    #write the confusion matrix to the workspace

    predictions = model_predictions(pd.read_csv(dataset_csv_path))

    # create the confusion matrix
    cm = metrics.confusion_matrix(pd.read_csv(dataset_csv_path)['exited'], predictions)

    # plot the confusion matrix
    plt.figure(figsize=(9,9))

    sns.heatmap(cm, annot=True, fmt=".3f", linewidths=.5, square = True, cmap = 'Blues_r');

    plt.ylabel('Actual label')
    plt.xlabel('Predicted label')

    # save the confusion matrix plot to the workspace
    plt.savefig(cm_path)


if __name__ == '__main__':
    score_model()
