# Application_tracking_system
software application designed to streamline and facilitate the process of recruiting and hiring new employees for organizations. It serves as a centralized platform to manage and automate various stages of the recruitment process, from receiving and reviewing applications to finalizing job offers.
## Dependencies:
- java +8 version to run apache tika
- Python +3.10
## Setup : 
To setup the environment, run these commands:
- pip insall requirements.txt
- python -m spacy download en_core_web_sm
- python -m spacy download en_core_web_lg
- python -m nltk.downloader words
- python -m nltk.downloader punkt
<br>

## Project architecture 
### Data 
#### raw_data : resumes before preprocessing 
#### jobs_data  : Dataset of job descriptions 
#### clean_data : resumes and job_descriptions after pre-processing 
####  data_fact : Files that contain all the names of public and private colleges In tunisia In french, english, and their abbreveation 
### src 
#### data_ingestion : Contains script for importing and exporting data 
#### data_preprocessing : Script for data preprocessing 
#### test  To run the resumes extraction script run this file : main.py
## Referneces : 
- https://aclanthology.org/2021.icnlsp-1.15.pdf
- https://ijcrt.org/papers/IJCRT_197410.pdf
