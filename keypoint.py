# -*- coding: utf-8 -*-
"""
    Title:          Multimedia Data Formats
    Date:           27.04.2018
    Description:    Computes different keypoint descriptors (ORB, BRISK, SIFT, SURF)
                    for image files (PNG, JPEG, JPEG2000, JPEG XR, BPG)
                    
    ToDo:
"""
import cv2
from imageio import imread
from os import remove
from subprocess import run

class Keypoint:
    
    # Path for converting tools 
    path_bpg = './tools/libbpg/bpgdec.exe'

    def __init__(self):
        return None
    
    def compute_all(self, file):
        """compute_all(file):
        For a given image file (PNG, JPEG, JPEG2000, JPEG XR, BPG), 
        computes different descriptors (ORB, BRISK, SIFT, SURF).
        
        Parameters:
            file:       Image filename including path.
        
        Return:     Returns keypoints and corresponding descriptors.
        """
        img = self.read_file(file)
        orb_kp, orb_des = self.compute_ORB(img)
        brisk_kp, brisk_des = self.compute_BRISK(img)
        sift_kp, sift_des = self.compute_SIFT(img)
        surf_kp, surf_des = self.compute_SURF(img)
        return [orb_des, brisk_des, sift_des, surf_des]
    
    
    def compute_ORB(self, img):
        """compute_ORB(img):
        Detects the ORB keypoints for a given image and computes the 
        destrictors using openCV ORB algroithm.
        
        Parameters:
            img:        Image array.
        
        Return:     Returns keypoints and corresponding descriptors.
        """
        orb = cv2.ORB_create()
        return orb.detectAndCompute(img, None)
    
    
    def compute_BRISK(self, img):
        """compute_BRISK(img):
        Detects the BRISK keypoints for a given image and computes the 
        destrictors using openCV BRISK algroithm.
        
        Parameters:
            img:        Image array.
        
        Return:     Returns keypoints and corresponding descriptors.
        """
        brisk = cv2.BRISK_create()
        return brisk.detectAndCompute(img, None)
    
    
    def compute_SIFT(self, img):
        """compute_SIFT(img):
        Detects the SIFT keypoints for a given image and computes the 
        destrictors using openCV SIFT algroithm.
        
        Parameters:
            img:        Image array.
        
        Return:     Returns keypoints and corresponding descriptors.
        """
        sift = cv2.xfeatures2d.SIFT_create()
        return sift.detectAndCompute(img, None)
    
    
    def compute_SURF(self, img):
        """compute_SURF(img):
        Detects the SURF keypoints for a given image and computes the 
        destrictors using openCV SURF algroithm.
        
        Parameters:
            img:        Image array.
        
        Return:     Returns keypoints and corresponding descriptors.
        """
        surf = cv2.xfeatures2d.SURF_create()
        return surf.detectAndCompute(img, None)
    
    
    def read_file(self, filename):
        """read_file(filename):
        Reads PNG, JPEG, JPEG2000, JPEG XR and BPG files.
        Returns error if 
        
        Parameters:
            filename:   Filename including path.
        
        Return:     Returns image array.
        """
        check_format = filename.split('.')[2]
        if check_format == 'png':
            return imread(filename, format='PNG-FI')
        elif check_format == 'jpeg':
            return imread(filename, format='JPEG-FI')
        elif check_format == 'jp2':
            return imread(filename, format='JP2-FI')
        elif check_format == 'jxr':
            return imread(filename, format='JPEG-XR-FI')
        elif check_format == 'bpg':
            run([self.path_bpg, '-o', 'temp.png', filename])
            img = imread('temp.png')
            remove('temp.png')
            return img
        else:
            print('ERROR --> Not supported file format.')
            return None
    
    