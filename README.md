# clinical-trials

`clinical-trials` is a locally-hosted browser app that allows users to see the racial representativeness of clinical trials by drug and condition, as well as manufacturer over time. It takes canonical FDA approved drugs and links them to the NIH's clinical trials data using a combination of fuzzy string matching and SQL joins, and provides a drop-down interface for searching by drug name and manufacturer.

## Setting Up
Due to dependency issues, `clinical-trials` requires a version of Python less than 3.12 to be installed, preferably 3.11.

1. To ensure that the app is running on the correct version of python, use:
`poetry env use 3.11.8`

2. Then continue as usual:
`poetry install`

3. Ensure that in the same parent directory as the `clinicaltrials` module, there is a folder named `data`, and a folder within data named `csvs`.

The structure should look something like this:

├── README.md
├── clinicaltrials
│   └── (app contents)
├── data
│   └── csvs
├── poetry.lock
└── pyproject.toml
 
### Pulling API data
Neither the FDA api nor the NIH Clinical Trials API require an API key. Pulling should be possible out of the box. JSON data is saved to the `/data` parent directory mentioned in the setting up section.

Run: `python3 clinicaltrials/api/fetch_trials_data.py`

After running this, you should see that the /data folder in the parent directory now includes two files: `fda.json` and `trials.json`

### Extracting API data
Once API data is pulled, it should not be necessary to pull again. Whenever API data is pulled, it should be extracted and cleaned. Do this by running the following commands:

`python3 clinicaltrials/data/extract_fda_data.py` and `python3 clinicaltrials/data/extract_trials_data.py`

Note the following files in the same directory as the extraction scripts:
`clinicaltrials/dedupe_dataframe_learned_settings`
`clinicaltrials/dedupe_dataframe_training.json`

These are trained classifier files used to perform fuzzy deduplication of FDA drug records. Do not delete them. If you do, you will have to retrain the classifier.

Once you have run the cleaning screepts, you should see that the `csvs` parent data directory is now populated with nine CSVs:

`fda_full.csv`
`trial_conditions.csv`
`trial_interventions_raw.csv`
`trial_interventions.csv`
`trial_locations.csv`
`trial_race.csv`
`trial_sex.csv`
`trial_status.csv`
`trials.csv`

Note that while data about sex representation in trial is extracted, the current version of the app presently does not display data on the sex of trial participants. It is the hope of the clinical-trials team to continue maintaining this tool, and to incorporate this and further demographic analysis after the project is submitted.

### Populating the local database
Once data has been extracted and saved to csvs, run the script to populate the local database.

`python3 clinicaltrials/data/makedb.py`

### Running the app
At this point, everything you need to run the app should be there. Run the app with the following command, and input the address into your browser to view the tool:

`python3 clinicaltrials/app.py`

## Contributors
* Kristy Kwon
* Caitlin Pratt
* Alison Spencer
* David Steffen

Special thanks to CAPP 122 professor James Turk for his code contributions, and for his support throughout the project.
