# Download the dataset

From here: https://www.kaggle.com/mousehead/songlyrics#songdata.csv

# Setup venv

## Creat a new venv
python3 -m venv ./venv

## Activate the venv
source ./venv/bin/activate

## Install dependencies
pip3 install -r requirements.txt

## Exit venv
deactivate

# Scripts
You run the scripts in this order: 

- `python3 main.py`
Read the dataset and creates documents from the csv song file

- `python3 sample.py`
Samples the documents with reservoir sampling 

- `python3 similarity.py`
Calculates the similarity between the documents and creates a similarity matrix

- `python3 graph.py`
Creates a csv file with the edge weights that you can use in gephi

