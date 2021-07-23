import matplotlib.pyplot as plt
import cv2
import numpy as np


class ImageColorAnalyzerService:
    def __init__(self, image_path):
        self.image_path = image_path

    def determine_mean_rgb(self):
        image_bgr = cv2.imread(self.image_path, cv2.IMREAD_COLOR)
        channels = cv2.mean(image_bgr)
        mean_rbg = np.array([(channels[2], channels[1], channels[0])])
        return mean_rbg.tolist()

    def determine_mean_grayscale(self):
        image_bgr = cv2.imread(self.image_path, cv2.IMREAD_COLOR)
        grayscale_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        return cv2.mean(grayscale_image)