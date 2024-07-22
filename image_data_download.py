"""
Script for downloading image data from the internet, renaming them accordingly, and cropping.
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
    """
    Reads a YAML configuration file and returns its content as a ConfigBox object.

    Args:
        path_to_yaml (Path): The path to the YAML configuration file.

    Returns:
        ConfigBox: The content of the YAML file as a ConfigBox object.

    Raises:
        CustomException: If there is an error in reading the YAML file.
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            print(f"YAML file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except Exception as e:
        raise CustomException(e, sys)


def create_directory(image_data_dir: str) -> None:
    """
    Creates a directory for storing images if it doesn't exist.

    Args:
        image_data_dir (str): The path to the directory to be created.
    """
    print(f"Creating {image_data_dir} directory...")
    directory_path = Path(image_data_dir)
    directory_path.mkdir(parents=True, exist_ok=True)
    print(f"{image_data_dir} directory created")


def download_images(query: str, output_dir: str, number_of_images: int) -> None:
    """
    Downloads images from the internet using the Bing Image Downloader.

    Args:
        query (str): The search query for downloading images.
        output_dir (str): The directory to save the downloaded images.
        number_of_images (int): The number of images to download.
    """
    print(f"Downloading {number_of_images} images of {query}...")
    downloader.download(query, limit=number_of_images, output_dir=output_dir, verbose=False)
    print(f"Downloaded {number_of_images} images of {query}\n")


def rename_image_files(folder: str, query: str) -> None:
    """
    Renames image files in a specified folder based on the query.

    Args:
        folder (str): The folder containing the images to be renamed.
        query (str): The query to be used as the prefix for renaming images.
    
    Raises:
        CustomException: If there is an error in renaming the files.
    """
    try:
        count = 1
        image_extensions = ['jpg', 'jpeg', 'png']

        for filename in os.listdir(folder):
            if os.path.isfile(os.path.join(folder, filename)):
                file_extension = filename.split('.')[-1].lower()

                if file_extension in image_extensions:
                    new_filename = f"{query}_{count}.jpg"
                    os.rename(os.path.join(folder, filename),
                              os.path.join(folder, new_filename))
                    count += 1
    except Exception as e:
        raise CustomException(e, sys)


'''
def crop_image(folder: str, pixel_value: int, scale_percent: int) -> None:
    """
    Crops images in a specified folder to a specified pixel value and scales them.

    Args:
        folder (str): The folder containing the images to be cropped.
        pixel_value (int): The desired pixel size for cropping.
        scale_percent (int): The percentage to scale down the images.
    """
    for filename in os.listdir(folder):google
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

                cv.imwrite(new_filename, img)
'''


def main():
    """
    The main function to load configuration, download images, rename and crop them.
    """
    # Load config file
    config = read_yaml("config.yaml")
    image_data_dir = config.parent_directiory

    # Image search key
    query_input = input("Enter search query or queries separated by comma (','): ")

    delimiter = config.delimiter
    queries = query_input.split(delimiter)

    # Number of Images to be downloaded
    number_of_images = int(input("Enter number of images to download: "))

    create_directory(image_data_dir)
    
    # Download image data
    for query in queries:
        download_images(query, image_data_dir, number_of_images)
        # Rename files according to queries
        rename_image_files(f"{image_data_dir}/{query}/", query)
        # Crop image to pixel values
        # crop_image(f"{image_data_dir}/{query}/", config.pixel_value, config.scale_percent)


if __name__ == "__main__":
    main()
