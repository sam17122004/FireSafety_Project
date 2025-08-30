import cv2, numpy as np

def normalize(img):
    return cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)

def denoise(img):
    return cv2.GaussianBlur(img, (5,5), 0)
