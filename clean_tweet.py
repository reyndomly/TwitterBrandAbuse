import os
import pandas as pd
from datetime import datetime
import shutil

def preprocess(df):
    df_filtered = df[df['username'] != '@mandiricare']
    df_filtered = df_filtered[df_filtered['username'] != '@bankmandiri']
    df_filtered = df_filtered.dropna()
    df_target = df_filtered[df_filtered['tweet_text'].str.contains('http://|https://|lnk|wa.me|wa.link')]
    return df_target

def save_to_folder(df_target):
    # Get today's date
    today_date = datetime.now().strftime("%d-%m-%Y")
    
    # Create folder if it doesn't exist
    folder_name = ".\\data\\twitter\\" +  today_date
    folder_temp = folder_name + "\\temp" 
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        os.makedirs(folder_temp)
    
    # Save DataFrame to CSV in the folder
    df_target.to_csv(os.path.join(folder_name, f"brand_abuse_{datetime.now().strftime("%d%m%Y")}.csv"), index=False)

def move_temp() :
    current_directory = os.getcwd()  # Get current directory
    folder_name = ".\\data\\twitter\\" + datetime.now().strftime("%d-%m-%Y")
    folder_temp = folder_name + "\\temp"
    raw_replies_path = os.path.join(current_directory, "raw_replies.csv")
    raw_tweet_path = os.path.join(current_directory, "raw_tweet.csv")
    
    # Move files to temp folder
    shutil.move(raw_replies_path, folder_temp)
    shutil.move(raw_tweet_path, folder_temp)

# Load the data
df = pd.read_csv("raw_replies.csv")

# Preprocess the data
df_target = preprocess(df)

# Save to folder
save_to_folder(df_target)
move_temp()
