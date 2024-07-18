"""
For downloading image data from the internet, renaming according and cropping
"""
import os
import sys
import yaml
import cv2 as cv
from pathlib import Path
from bing_image_downloader import downloader
from box import ConfigBox
from exceptions import CustomException


def read_yaml(path_to_yaml: Path) -> ConfigBox:
  try:
    with open(path_to_yaml) as yaml_file:
      content = yaml.safe_load(yaml_file)
      print(f"yaml file: {path_to_yaml} loaded successfully")
      return ConfigBox(content)
  except Exception as e:
    raise CustomException(e, sys)


def create_directory(image_data_dir: str) -> None:
  print(f"Creating {image_data_dir} directory...")
  # Create the parent image directory
  directory_path = Path(image_data_dir)
  directory_path.mkdir(parents=True, exist_ok=True)
  print(f"{image_data_dir} directory created")


def download_images(query: str, output_dir: str, number_of_images: int) -> None:
  print(f"Downloading {number_of_images} images of {query}...")
  downloader.download(query, limit=number_of_images, output_dir=output_dir, verbose=False)
  print(f"Downloaded {number_of_images} images of {query}\n")


def rename_image_files(folder: str, query: str) -> None:
  try:
    count = 1
    image_extensions = ['jpg', 'jpeg', 'png']

    for filename in os.listdir(folder):
      if os.path.isfile(os.path.join(folder, filename)):
        file_extension = filename.split('.')[-1].lower()

        if file_extension in image_extensions:
          #new_filename = f"{query}_{count}.{file_extension}"
          new_filename = f"{query}_{count}.jpg"
          os.rename(os.path.join(folder, filename),
                    os.path.join(folder, new_filename))
          count += 1
  except Exception as e:
    raise CustomException(e, sys)


def crop_image(folder: str, pixel_value: int, scale_percent: int) -> None:
  for filename in os.listdir(folder):
    image_path = os.path.join(folder, filename)

    if os.path.isfile(image_path):
      img = cv.imread(image_path)

      if img is not None:
        # Scale down the image
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        img = cv.resize(img, dim, interpolation=cv.INTER_AREA)

        # Crop image
        height, width, _ = img.shape
        left = (width - pixel_value) // 2
        top = (height - pixel_value) // 2
        right = left + pixel_value
        bottom = top + pixel_value

        img = img[top:bottom, left:right]

        base, file_extension = os.path.splitext(image_path)
        new_filename = f"{base}_crop{file_extension}"
        '''
        os.rename(os.path.join(folder, filename),
                  os.path.join(folder, new_filename))
        '''

        cv.imwrite(new_filename, img)


def main():
  # load config file
  config = read_yaml("config.yaml")
  image_data_dir = config.parent_directiory

  # Image search key
  query_input = input("Enter search query or queries separated by comma (','): ")

  delimiter = config.delimiter
  queries = query_input.split(delimiter)

  # Number of Images to be downloaded
  number_of_images = int(input("Enter number of images to download: "))

  create_directory(image_data_dir)
    
  # Download Image data
  for query in queries:
    download_images(query, image_data_dir, number_of_images)
    # Rename files according to queries
    rename_image_files(f"{image_data_dir}/{query}/", query)
    # Crop image to pixel values
    crop_image(f"{image_data_dir}/{query}/", config.pixel_value, config.scale_percent)


if __name__ == "__main__":
  main()
