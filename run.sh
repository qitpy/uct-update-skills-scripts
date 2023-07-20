#!/bin/bash

# Prompt the user to set the value for SCRIPT_DATABASE_URI
read -p "Enter the value for SCRIPT_DATABASE_URI: " database_uri

# Check if the entered value is empty
while [[ -z "$database_uri" ]]; do
    echo "Error: The value cannot be empty."
    read -p "Enter the value for SCRIPT_DATABASE_URI (ex: mongodb://localhost:27017): " database_uri
done

# Set the environment variable SCRIPT_DATABASE_URI
export SCRIPT_DATABASE_URI="$database_uri"

# Prompt the user to set the value for SCRIPT_DATABASE_DBNAME
read -p "Enter the value for SCRIPT_DATABASE_DBNAME (ex: uct-crawling-dev): " database_dbname

# Check if the entered value is empty
while [[ -z "$database_dbname" ]]; do
    echo "Error: The value cannot be empty."
    read -p "Enter the value for SCRIPT_DATABASE_DBNAME: " database_dbname
done

# Set the environment variable ENV_VAR2
export SCRIPT_DATABASE_DBNAME="$database_dbname"

# Replace the following variables with your GitHub raw content URL and the filename of the Python script
github_raw_url="https://raw.githubusercontent.com/qitpy/uct-update-skills-scripts/master/filter_job_with_new_skills.py"
python_script_filename="scripts.py"

# Download the Python script using curl
curl -o "$python_script_filename" "$github_raw_url"

# Check if the download was successful
if [ $? -eq 0 ]; then
    echo "Python script downloaded successfully."
else
    echo "Failed to download the Python script. Exiting."
    exit 1
fi

# Execute the Python script using Python
python3 "$python_script_filename"

# Clean up the downloaded file
rm "$python_script_filename"

