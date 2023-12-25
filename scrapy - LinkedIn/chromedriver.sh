#!/bin/bash

# Step 1: Download the latest stable version of Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Step 2: Install the downloaded package
sudo dpkg -i google-chrome-stable_current_amd64.deb

# Step 3: Resolve dependencies (if any)
sudo apt --fix-broken install -y

# Step 4: Clean up temporary files
rm google-chrome-stable_current_amd64.deb

echo "Google Chrome has been installed successfully."

# Step 1: Identify current Chrome version
chrome_version=$(google-chrome-stable --version | awk -F '[ .]' '{print $3}')

# Step 2: Identify URL for the correct binary file
binary_url="https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${chrome_version}"

# Step 3: Download and install the binary file
binary_version=$(curl -s "$binary_url")
binary_download_url="https://chromedriver.storage.googleapis.com/$binary_version/chromedriver_linux64.zip"

# Download and extract the binary file
wget "$binary_download_url" -O chromedriver_linux64.zip
unzip chromedriver_linux64.zip

# Set executable permissions
chmod +x chromedriver

# Move the binary file to a directory in the PATH
sudo mv chromedriver /usr/local/bin/

# Clean up temporary files
rm chromedriver_linux64.zip

echo "ChromeDriver $binary_version has been installed successfully."
