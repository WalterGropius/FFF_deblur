import cv2
import numpy as np
import glob
import shutil
import os
from tkinter import filedialog
from tkinter import Tk
from tqdm import tqdm
import statistics

def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

def move_blurry_images(percentage, image_directory, blurry_directory, image_fm):
    # Calculate the number of images to move
    num_move = int(len(image_fm) * percentage / 100)
    
    # Get the num_move blurriest images
    blurry_images = [img for fm, img in image_fm[:num_move]]
    
    for image_path in blurry_images:
        # Move the image
        shutil.move(image_path, blurry_directory + '/' + os.path.basename(image_path))

    print(f"Moved {num_move} blurry images to {blurry_directory}.")

def browse_directory():
    # Browse for the directory
    root = Tk()
    root.withdraw() # we don't want a full GUI, so keep the root window from appearing
    directory = filedialog.askdirectory() # show an "Open" dialog box and return the path to the selected directory
    return directory

# Ask user to browse for the directory
print("Please select the directory containing your images.")
image_directory = browse_directory()

# Define blurry directory
blurry_directory = image_directory + '/blurry'

# Create the blurry directory if it doesn't exist
os.makedirs(blurry_directory, exist_ok=True)

# Calculate the variance of laplacian for all images and store it with the image path
print("Calculating focus measure for all images...")
images = glob.glob(image_directory + '/*.jpg') + glob.glob(image_directory + '/*.png') + glob.glob(image_directory + '/*.bmp')
image_fm = []
for img in tqdm(images):
    fm = variance_of_laplacian(cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2GRAY))
    image_fm.append((fm, img))

# Sort the images based on the focus measure, from lowest (blurriest) to highest
image_fm.sort()

# Calculate the statistical measures
fm_values = [fm for fm, img in image_fm]
min_fm = min(fm_values)
max_fm = max(fm_values)
mean_fm = statistics.mean(fm_values)
median_fm = statistics.median(fm_values)

print(f"Statistics for focus measures:\nMinimum: {min_fm}\nMaximum: {max_fm}\nMean: {mean_fm}\nMedian: {median_fm}")

# Ask user for the percentage to move
percentage = float(input("Please enter the percentage of the blurriest images you'd like to move: "))

# Move the blurriest images
move_blurry_images(percentage, image_directory, blurry_directory, image_fm)
