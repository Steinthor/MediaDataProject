# -*- coding: utf-8 -*-
"""
    Title:          Multimedia Data Formats
    Date:           14.04.2018
    Description:    Convert-class containing all the methodes to convert 
                    a list of images into JPEG/JPEG2000/JPEG XR/BPG 
                    compressed files with different compression ratios.
                    
    To Do:
        1) Check for subprocess return-code?
        2) Better code reuse?
"""

from os import remove, path, listdir
from subprocess import run
from imageio import imread, imwrite
from glymur import Jp2k

class Convert:
       
    # Path for converting tools 
    path_jpegxr = './tools/nconvert/nconvert.exe'
    path_bpg = './tools/libbpg/bpgenc.exe'
    
    def __init__(self, path_infiles='./data/CoMoFoD/', path_outfiles='./data/converted/', compression_rates=[1]):
        self.path_in = path_infiles
        self.path_out = path_outfiles
        self.compression_rates = compression_rates
    
    
    def doit(self):
        """doit(compression_rates):
        Converts a list of PNG files to different output formats:
            - JPEG
            - JPEG2000
            - JPEG XR
            - BPG
        """
        in_list = listdir(self.path_in)
        for file in in_list:
            self.convert_jpeg(file, self.compression_rates)
            self.convert_jpeg2000(file, self.compression_rates)
            self.convert_jpegxr(file, self.compression_rates)
            self.convert_bpg(file, self.compression_rates)
        return None
    
    
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
        img = imread(self.path_in + in_file, format='PNG-FI')
        in_size = self.get_imgsize(img)
        out_list = []
        
        # Conversion
        for r in compression_rates:
            out_file = self.path_out + in_file.split('.')[0] + '_jpeg_' + str(r) + '.jpeg'
            success = False
            for q in qualities:
                # Output options
                args_jpeg = {"quality": q, "progressive": True, "optimize": True}
                # Write file
                imwrite(out_file, img, format='JPEG-PIL', **args_jpeg)
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
            if success == False:    # Stop if comression rate not reachable
                remove(out_file)
                break
        return out_list
    
    
    def convert_jpeg2000(self, in_file, compression_rates):
        """convert_jpeg2000(in_list, compression_rates):
        Converts a file to JPEG2000 format for given compression_rates.
        (Uses JPEG2000 internal algorithm)
        (Imput fomrat: PNG)
        
        Parameters:
            in_file:            Filename to convert.
            compression_rates:  List of all targeted compression rates.
            
        Return:     Returns a list containing the filenames of the newly
                    converted files.
        """
        img = imread(self.path_in + in_file, format='PNG-FI')
        out_list = []
        
        # Conversion
        for r in compression_rates:
            args_jpeg2000 = {'cratios': [r]}
            out_file = self.path_out + in_file.split('.')[0] + '_jpeg2000_' + str(r) + '.jp2'
            msg = Jp2k(out_file, img, **args_jpeg2000)
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
        qualities = list(reversed(range(-10, 101, 1)))    # quality range: [-10 100]
        img = imread(self.path_in + in_file, format='PNG-FI')
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
            if success == False:    # Stop if comression rate not reachable
                remove(out_file)
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
        img = imread(self.path_in + in_file, format='PNG-FI')
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
            if success == False:    # Stop if comression rate not reachable
                remove(out_file)
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
    
    