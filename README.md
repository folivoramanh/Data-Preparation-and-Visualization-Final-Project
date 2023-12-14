# Data Preparation and Visualization Final Project

This repository contains code for a machine learning project focused on predicting loan credit risk. The project is part of the Data Preparation and Visualization course at the National Economics University, Semester 5

## Project Structure

- **EDA**: Exploratory Data Analysis
  - Explore the dataset to gain insights into the data distribution, identify patterns, and understand the features.

- **FeatureEngineering**: Feature Engineering
  - Implement feature engineering techniques to prepare the data for training the machine learning model.

- **Main**: Model Fitting and Evaluation
  - Train machine learning models using the preprocessed data and evaluate their performance.

## Assigned work

  * Trinh Mai Anh
    - EDA<br /> 
      * Review and fix comments for all EDA files
      * Refactor Code 
    - Feature Engineer <br />
    - Tunning model <br />
  * Nguyen Phuong Linh
    - EDA<br />
      * Bureau
      * Bureau_balance
    - Slide <br />
  * Nguyen Thuy Linh
    - EDA<br />
      * Application_train 
      * Instalment_payment
      * Credit_card_balance 
      * POS_CASH_balance
      * Previous_application

## System Architecture

```bash
├── main.py
├── README.md
├── Document.txt
├── requirements.txt
├── blending.ipynb
├── model.py
├── save_feature_importance.py
├── final_data
│   ├── FeatEng.zip
│ 
├── EDA
│   ├── utils
│   │   ├── __init__.py
│   │   ├── categorical.py
│   │   ├── correlation.py
│   │   ├── continuous.py
│   │   ├── distribution.py
│   │   ├── imbalance.py
│   │   ├── missing_values.py
│   │   ├── outlier.py
│   │   ├── percentile.py
│   │   └── phik.py
│   ├── input.py
│   ├── application_train.ipynb
│   ├── bureau.ipynb
│   ├── bureau_balance.ipynb
│   ├── credit_card_balance.ipynb
│   ├── installments_payments.ipynb
│   ├── POS_CASH_balance.ipynb
│   └── previous_application.ipynb
│
├── FeatureEngineering
│   ├── main.py
│   ├── __init__.py
│   ├── application_train.py
│   ├── bureau.py
│   ├── bureau_balance.py
│   ├── credit_card_balance.py
│   ├── installments_payments.py
│   ├── pos_cash.py
│   ├── previous_application.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── _3sigma.py
│   │   ├── add_features.py
│   │   ├── constants.py
│   │   ├── do_aggregate.py
│   │   ├── encoder.py
│   │   ├── group.py
│   │   ├── handling_data.py
│   │   ├── parallel.py
│   │   ├── reduce_memory.py
│   │   └── timer.py

```

## Getting Started

### Prerequisites

- Python 3.10
- Git

### Clone the Repository

```bash
git clone https://github.com/folivoramanh/Data-Preparation-and-Visualization-Final-Project
```

### Create a Virtual Environment

```bash
python3.10 -m venv venv
```
or 

```bash
conda create -n venv python=3.10
```
### Activate the Virtual Environment
- For Windows
```bash
venv\Scripts\activate.bat
```
- For Linux or MacOS
```bash
source venv/bin/activate
```
- For Conda
```bash
conda activate venv
```

### Install Dependencies

```bash
pip install -r requirements.txt
```
### Source credit
Check in document.txt

### Run the Project
1. Navigate to the project directory
```bash
cd Data-Preparation-and-Visualization-Final-Project
```
2. Activate the virtual environment by instructions above

3. Run the project
- For EDA
    - Open the EDA folder
    - Open file input.py and add the path to the data folder
    - Open notebook file at EDA run it\
    **Notes:** You should read the EDA file first to understand the idea first, then if you need to run for verify, you can run it however it may have some different with the original because sometimes it depends on how package on your devices works.

- For Feature Engineering
    - Open the FeatureEngineering folder
    - Open file main.py and add the path to the data folder
    - Run main.py
    ```bash
    python FeatureEngineering\main.py
    ```
    **Notes:** Maybe it catch some error because of the lack of __pycache__ folder, so the first run maybe error. For the second run, if you catch the error like *"ImportError: attempted relative import with no known parent package"*, you need to follow the error and go to file that exist that error then add "."
    or skip "." before utils depends on your device
    - Link to the final FeatEng DataFrame: [FeatEng](https://www.kaggle.com/datasets/tma182/finalset)

- For Tunning model
    - Open main.py and add the path to the data folder of FeatEng DataFrame\
    **Notes:** You should read the main.py file first to understand the idea first,
    
    - Run main.py
    ```bash
    python main.py
    ```

- For blending
    - Open blending.ipynb
    - Replace your results path to file
    - Modify the coefficient of each features
    - Run it