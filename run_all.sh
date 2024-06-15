#!/bin/bash

# Update package list and install required packages
echo "Installing necessary packages..."
sudo apt update
sudo apt install -y wget python3 python3-pip git

# Define the Discogs data dump URLs
ARTISTS_URL="https://discogs-data-dumps.s3-us-west-2.amazonaws.com/data/2024/discogs_20240601_artists.xml.gz"
RELEASES_URL="https://discogs-data-dumps.s3-us-west-2.amazonaws.com/data/2024/discogs_20240601_releases.xml.gz"
MASTERS_URL="https://discogs-data-dumps.s3-us-west-2.amazonaws.com/data/2024/discogs_20240601_masters.xml.gz"
LABELS_URL="https://discogs-data-dumps.s3-us-west-2.amazonaws.com/data/2024/discogs_20240601_labels.xml.gz"

# Download the Discogs data dump files
echo "Downloading Discogs data dump files..."
wget -O discogs_artists.xml.gz $ARTISTS_URL
wget -O discogs_releases.xml.gz $RELEASES_URL
wget -O discogs_masters.xml.gz $MASTERS_URL
wget -O discogs_labels.xml.gz $LABELS_URL

# Unzip the downloaded files
echo "Unzipping downloaded files..."
gunzip discogs_artists.xml.gz
gunzip discogs_releases.xml.gz
gunzip discogs_masters.xml.gz
gunzip discogs_labels.xml.gz

# Clone the discogs-xml2db repository
echo "Cloning discogs-xml2db repository..."
git clone https://github.com/philipmat/discogs-xml2db.git
cd discogs-xml2db

# Create a virtual environment and activate it
echo "Creating and activating virtual environment..."
python3 -m venv .discogsenv
source .discogsenv/bin/activate

# Install requirements
echo "Installing requirements..."
pip3 install -r requirements.txt

# Create the csv-dir folder
echo "Creating csv-dir folder..."
mkdir -p csv-dir

# Run the data conversion script
echo "Running data conversion script..."
python run.py --apicounts --output ../csv-dir ../discogs_20240601_artists.xml ../discogs_20240601_labels.xml ../discogs_20240601_masters.xml ../discogs_20240601_releases.xml

# Deactivate the virtual environment
deactivate
cd ..

# Print the start time
echo "Script started at: $(date)"

# Run each Python script sequentially
echo "Running 1_IranFilter.py..."
python3 1_IranFilter.py

echo "Running 2-artistCombine.py..."
python3 2-artistCombine.py

echo "Running 3-metadataCleaning.py..."
python3 3-metadataCleaning.py

echo "Running 4-dataGeneration.py..."
python3 4-dataGeneration.py

echo "Running 5-dataAnalysis.py..."
python3 5-dataAnalysis.py

# Print the end time
echo "Script completed at: $(date)"
