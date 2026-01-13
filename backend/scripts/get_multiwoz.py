import os
import json
import urllib.request
import zipfile

def download_multiwoz_direct():
    """Download MultiWOZ 2.1 directly from the official repository"""
    os.makedirs("data/multiwoz", exist_ok=True)
    
    # Download from official MultiWOZ repository
    url = "https://github.com/budzianowski/multiwoz/raw/master/data/MultiWOZ_2.1.zip"
    zip_path = "data/multiwoz/MultiWOZ_2.1.zip"
    
    print("Downloading MultiWOZ 2.1...")
    urllib.request.urlretrieve(url, zip_path)
    
    # Extract the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("data/multiwoz/")
    
    print("Download and extraction completed!")
    
    # Remove zip file
    os.remove(zip_path)

download_multiwoz_direct()