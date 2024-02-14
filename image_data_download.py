"""
For downloading image data from the internet
"""
import os
from pathlib import Path
from bing_image_downloader import downloader

image_data_dir = input("Enter directory name: ")

# Image search key
query_input = input("Enter search query or queries separated by a delimiter: ")
delimiter = input("Enter delimiter: ")
queries = query_input.split(delimiter)

# Number of Images to be downloaded
number_of_images = int(input("Enter number of images to download: "))

def image_data_directory_setup(image_data_dir: str) -> None:
  # Create the project directory
  directory_path = Path(image_data_dir)
  directory_path.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    image_data_directory_setup(image_data_dir)
    
    # Download Image data
    for query in queries:
      downloader.download(query, limit=number_of_images, output_dir=image_data_dir)
