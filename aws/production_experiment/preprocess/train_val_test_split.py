"""
runs train_val_test spilt on all files in the ec2 instances standard input;
saves them to standard output, random_seed=0
"""
import os
from sklearn import train_test_split
import pandas as pd
## constants, file locations
PERCENT = 0.15
SEED = 0
INPUT_PATH = '/opt/ml/processing/input'
OUTPUT_PATH_TRAIN = '/opt/ml/processing/output/train'
OUTPUT_PATH_VAL = '/opt/ml/processing/output/validation'
OUTPUT_PATH_TEST = '/opt/ml/processing/output/test'
## load, combine
def main():
    """intakes, concats, splits, saves"""
    ## loads and concats
    files = os.listdir(INPUT_PATH)
    df_multi = [pd.read_csv(f'{file}') for file in files]
    df_full = pd.concat(df_multi)
    ## split
    df_inter, df_test = train_test_split(df_full, test_size=PERCENT, random_state=SEED)
    df_train, df_val = train_test_split(df_inter, test_size=PERCENT, random_state=SEED)
    ## save
    df_train.to_csv(OUTPUT_PATH_TRAIN)
    df_val.to_csv(OUTPUT_PATH_VAL)
    df_test.to_csv(OUTPUT_PATH_TEST)
if __name__ == '__main__':
    main()
