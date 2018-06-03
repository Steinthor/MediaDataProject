# -*- coding: utf-8 -*-
"""
    Title:          Multimedia Data Formats
    Date:           03.06.2018
    Description:    Convert-class containing all the methodes to convert 
                    a list of images into JPEG/JPEG2000/JPEG XR/BPG 
                    compressed files with different compression ratios
                    (using iterative, linear approach).
                    
    To Do:
        1) Binary search approach
        2) Check for subprocess return-code?
        3) Better code reuse?
"""
from os import remove, path, listdir
from shutil import copy
from time import time
from subprocess import run
from glymur import Jp2k
from cv2 import imwrite, imread, IMWRITE_JPEG_QUALITY, IMREAD_UNCHANGED

class Convert:
       
    # Path for converting tools 
    path_jpegxr = './tools/nconvert/nconvert.exe'
    path_bpg = './tools/libbpg/bpgenc.exe'
    
    def __init__(self, path_infiles='./data/load/', path_outfiles='./data/save/', compression_rates=([10, 20, 30, 40, 50, 60, 70, 80, 90])):
        self.path_in = path_infiles
        self.path_out = path_outfiles
        self.compression_rates = compression_rates
    
    
    def doit(self):
        """doit():
        Converts a list of PNG files to different output formats:
            - JPEG
            - JPEG2000
            - JPEG XR
            - BPG
        """
        in_list = listdir(self.path_in)
        current_time = time()
        for file in in_list:
            if file.split('.')[1] == 'png':
                self.convert_all(file)
            else:
                print("ERROR: No supported file format!")
        elapsed_time = time() - current_time
        print('--> CONVERT-DOIT: Elapsed time in seconds ' + str(elapsed_time))
    
    
    def convert_all(self, in_file):
        """convert_all(in_file):
        Converts a PNG file to different output formats:
            - JPEG
            - JPEG2000
            - JPEG XR
            - BPG
        Also copys the original PNG file to the output folder.
        """
        self.copy_png(in_file)
        self.convert_jpeg(in_file, self.compression_rates)
        self.convert_jpeg2000(in_file, self.compression_rates)
        self.convert_jpegxr(in_file, self.compression_rates)
        self.convert_bpg(in_file, self.compression_rates)
    
    
    def copy_png(self, in_file):
        """copy_png(in_file):
        Copys the original input file (PNG format) to the output path.
        
        Parameters:
            in_file:            Filename to copy.
        """
        copy(self.path_in + in_file, self.path_out + in_file)
    
         
    def convert_jpeg(self, in_file, compression_rates):
        """convert_jpeg(in_file, compression_rates):
        Converts a file to JPEG format for given compression_rates.
        (Imput fomrat: PNG)
        
        Parameters:
            in_file:            Filename to convert.
            compression_rates:  List of all targeted compression rates.
            
        Return:     Returns a list containing the filenames of the newly
                    converted files.
        """
        qualities = list(reversed(range(1, 101, 1)))    # quality range: [1 100]
        img = imread(self.path_in + in_file, IMREAD_UNCHANGED)
        in_size = self.get_imgsize(img)
        out_list = []
        
        # Conversion
        for r in compression_rates:
            out_file = self.path_out + in_file.split('.')[0] + '_jpeg_' + str(r) + '.jpeg'
            success = False
            for q in qualities:
                # Write file
                imwrite(out_file, img, [IMWRITE_JPEG_QUALITY, q])
                out_size = self.get_filesize(out_file)
                # Compare file size
                rate =  in_size / out_size
                print('(JPEG) q=' + str(q) + ' | rate=' + str(rate))
                if r <= rate:
                    qualities = list(filter(lambda x: x < q, qualities))     # Drop used quality levels
                    out_list.append(out_file)
                    print('--> (JPEG) Success: r=' + str(r) + ' | rate=' + str(rate))
                    print('--> ' + out_file)
                    success = True
                    break
            if success == False and qualities != []:    # Stop if comression rate not reachable
                remove(out_file)
                print('WARNING: Compressions not reachable ' + str(list(filter(lambda x: x >= r, compression_rates))))
                break
        return out_list
    
    
    def convert_jpeg2000(self, in_file, compression_rates):
        """convert_jpeg2000(in_list, compression_rates):
        Converts a file to JPEG2000 format for given compression_rates.
        (Uses JPEG2000 internal algorithm)
        (Input format: PNG)
        
        Parameters:
            in_file:            Filename to convert.
            compression_rates:  List of all targeted compression rates.
            
        Return:     Returns a list containing the filenames of the newly
                    converted files.
        """
        img = imread(self.path_in + in_file, IMREAD_UNCHANGED)
        out_list = []
        
        # Conversion
        for r in compression_rates:
            args_jpeg2000 = {'cratios': [r]}
            out_file = self.path_out + in_file.split('.')[0] + '_jpeg2000_' + str(r) + '.jp2'
            Jp2k(out_file, img, **args_jpeg2000)
            out_list.append(out_file)
            print('--> (JPEG2000) Success: rate=' + str(r))
            print('--> ' + out_file)
        return out_list
    
    
    def convert_jpegxr(self, in_file, compression_rates):
        """convert_jpegxr(in_list, compression_rates):
        Converts a file to JPEG XR format for given compression_rates.
        (Imput fomrat: PNG)
        
        Parameters:
            in_file:            Filename to convert.
            compression_rates:  List of all targeted compression rates.
            
        Return:     Returns a list containing the filenames of the newly
                    converted files.
        """
        qualities = list(reversed(range(1, 101, 1)))    # quality range: [-10 100]
        img = imread(self.path_in + in_file, IMREAD_UNCHANGED)
        in_size = self.get_imgsize(img)
        out_list = []
        
        for r in compression_rates:
            out_file = self.path_out + in_file.split('.')[0] + '_jpegxr_' + str(r) + '.jxr'
            success = False
            for q in qualities:
                run([self.path_jpegxr, '-overwrite', '-out', 'jxr', '-q', str(q), '-o', out_file, self.path_in + in_file])
                out_size = self.get_filesize(out_file)
                rate =  in_size / out_size
                print('(JPEG XR) q=' + str(q) + ' | rate=' + str(rate))
                if r <= rate:  
                    qualities = list(filter(lambda x: x < q, qualities))     # Drop used quality levels
                    out_list.append(out_file)
                    print('--> (JPEG XR) Success: r=' + str(r) + ' | rate=' + str(rate))
                    print('--> ' + out_file)
                    success = True
                    break
            if success == False and qualities != []:    # Stop if compression rate not reachable
                remove(out_file)
                print('WARNING: Compressions not reachable ' + str(list(filter(lambda x: x >= r, compression_rates))))
                break
        return out_list
    
    
    def convert_bpg(self, in_file, compression_rates):
        """convert_bpg(in_list, compression_rates):
        Converts a file to BPG format for given compression_rates.
        (Imput fomrat: PNG)
        
        Parameters:
            in_file:            Filename to convert.
            compression_rates:  List of all targeted compression rates.
            
        Return:     Returns a list containing the filenames of the newly
                    converted files.
        """
        qualities = list(range(0, 52, 1))               # quality range: [0 51]
        img = imread(self.path_in + in_file, IMREAD_UNCHANGED)
        in_size = self.get_imgsize(img)
        out_list = []
        
        for r in compression_rates:
            out_file = self.path_out + in_file.split('.')[0] + '_bpg_' + str(r) + '.bpg'
            success = False
            for q in qualities:
                msg = run([self.path_bpg, '-o', out_file, '-q', str(q), '-m', '9', self.path_in + in_file])
                out_size = self.get_filesize(out_file)
                rate =  in_size / out_size
                print('(BPG) q=' + str(q) + ' | ratio=' + str(rate))
                if r <= rate:
                    qualities = list(filter(lambda x: x > q, qualities))     # Drop used quality levels
                    out_list.append(out_file)
                    print('--> (BPG) Success: r=' + str(r) + ' | rate=' + str(rate))
                    print('--> ' + out_file)
                    success = True
                    break
            if success == False and qualities != []:    # Stop if compression rate not reachable
                remove(out_file)
                print('WARNING: Compressions not reachable ' + str(list(filter(lambda x: x >= r, compression_rates))))
                break
        return out_list
    
    
    def check_file(self, filename):
        """check_file(filename):
        Checks if a file is present.
        
        Parameters:
            filename:           Filename including path.
        
        Return:     Returns True if file is present, False otherwise.
        """
        return path.exists(filename)
    
    
    def get_imgsize(self, img_data):
        """get_imgsize(img_data):
        Returns the size of an image in memory
        
        Parameters:
            img_data:           Array of image.
        
        Return:     Returns filesize in bytes.
        """
        return img_data.size
    
    
    def get_filesize(self, filename):
        """get_filesize(filename):
        Returns the size of a file.
        
        Parameters:
            filename:           Filename including path.
        
        Return:     Returns filesize in bytes.
        """
        return path.getsize(filename)


# Do convertion
#path_small_in = 'C:/Admin/CoMoFoD_small/'
#path_small_out = 'C:/Admin/CoMoFoD_small_converted/'
path_small_in = './data/CoMoFoD_small/'
path_small_out = './data/CoMoFoD_small_converted/'
path_large_in = './data/Co/MoFod_large/'
path_large_out = './data/Co/MoFod_large_converted/' 
cr_small = [10, 20, 30, 40, 50]
cr_large = [10, 20, 30, 40, 50, 60, 70, 80, 90]

# CoMoFoD_small
comofod_small = Convert(path_infiles=path_small_in, path_outfiles=path_small_out, compression_rates=cr_small)
comofod_small.doit()
# CoMoFoD_large
#comofod_large = Convert(path_infiles=path_large_in, path_outfiles=path_large_out, compression_rates=cr_large)
#comofod_large.doit()
# TIFS
#tifs = Convert(path_infiles='./data/TIFS', path_outfiles='./data/converted/', compression_rates=cr_large)
#tifs.doit()