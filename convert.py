# -*- coding: utf-8 -*-
"""
    Title:          Multimedia Data Formats
    Date:           10.04.2018
    Description:    
                    
    To Do:
        1) 
"""

from os import path
from numpy import linspace
from imageio import imread, imwrite

class Convert:
    
    # Paths to directorys
    path_in = './data/CoMoFoD/'
    path_out = './data/converted/'
    
    # Path for converting tools 
    path_jpeg2000 = './tools/openjpself.get_filesize(current)eg/opj_compress.exe'
    path_jpegxr = './tools/nconvert/nconvert.exe'
    path_bpg = './tools/bpg/bpgenc.exe'
    
    def __init__(self):
        return None
        
    def convert_jpeg(self, in_list, compression_rates):
        """convert_jpeg(filelist, compression_rates)
        Converts files JPEG format with given compression_rates.
        (Input format: PNG)
        
        Parameters:
            in_list:            List of all files to convert to jpeg format.
            compression_rates:  List of all targeted compression rates.
        """
        qualities = list(reversed(range(5, 100, 5)))    # quality range: [5 95]
        out_list = [];
        
        for in_file in in_list:
            # Check if file is not present
            if self.check_file(self.path_in + in_file) != True:
                break
            img = imread(self.path_in + in_file, format='PNG-FI')
            
            # Conversion
            for r in compression_rates:
                for q in qualities:
                    # Output options
                    args_jpeg = {"quality": q, "progressive": True, "optimize": True}
                    out_file = self.path_out + in_file.split('.')[0] + '_jpeg_' + str(r) + '.jpeg'
                    
                    # Write file
                    imwrite(out_file, img, format='JPEG-PIL', **args_jpeg)
                    
                    # Compare file size
                    rate = self.get_filesize(self.path_in + in_file) / self.get_filesize(out_file)
                    if (r-1) <= rate <= (r+1):  
                        qualities = list(filter(lambda x: x <= q, qualities))     # Drop low quality levels
                        out_list.append(out_file)
                        break;
        return out_list
                    

    
    def convert_jpeg2000(self, in_list, compression_rates):
        return 0
    
    def convert_jpegxr(self, in_list, compression_rates):
        return 0
    
    def convert_bpg(self, in_list, compression_rates):
        return 0
    
    
    
    def check_file(self, filename):
        return path.exists(filename)
        
    def get_filesize(self, filename):
        return path.getsize(filename)
    
    
    
# Test Functions
c = Convert()
files = ['test_png.png']
rates = [10, 20, 30]
c.convert_jpeg(files, rates)