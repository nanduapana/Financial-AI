import os
import subprocess
from datetime import datetime

# Define the directory paths
raw_data_dir = r'C:\Users\nandk\Documents\Project Documentation\Financial-AI\src\data\raw'

# Get today's date in the format YYYY-MM-DD
today_date = datetime.today().strftime('%Y-%m-%d')

print(today_date)

# Define the file names to check for
content_data_file = f'content_data_{today_date}.csv'
nse_indices_file = f'nse_indices_{today_date}.csv'

# Check if the content_data file exists
content_data_exists = os.path.exists(os.path.join(raw_data_dir, content_data_file))
nse_indices_exists = os.path.exists(os.path.join(raw_data_dir, nse_indices_file))

# Run files based on conditions
if not content_data_exists:
    print(f"{content_data_file} not found, running 1_web_scraper.py")
    subprocess.run(["python", "src\\1_web_scraper.py"])

if not nse_indices_exists:
    print(f"{nse_indices_file} not found, running 2_nse_data_extraction.py")
    subprocess.run(["python", "src\\2_nse_data_extraction.py"])

#Run the rest of the files in sequence
print("Running 3.1_preprocessing.py")
subprocess.run(["python", "src\\3.1_preprocessing.py"])

print("Running 3.2_preprocessing.py")
subprocess.run(["python", "src\\3.2_preprocessing.py"])

print("Running 4_data_mapping.py")
subprocess.run(["python", "src\\4_data_mapping.py"])

print("Running 5_analysis_sentiment.py")
subprocess.run(["python", "src\\5_analysis_sentiment.py"])

print("All scripts executed successfully.")
