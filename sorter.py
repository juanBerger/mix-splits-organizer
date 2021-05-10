import os
import shutil
import fnmatch
import glob
import re
import argparse
import shutil


'''

TO DO:

    Create a progress bar for the zipping process that appears in the app GUI
    Add error handling (Add these for the most common cases so far)

'''

'''
Assumptions:
Stereo files always have some stereo file indicator in the presence of 5.1
In the case where there is no stereo signature, FUL indicates TV/Stereo. Put another way, OLVs have to be named 'OLV'
This means that if a group of files has no surround and no FUL it will fail

'''





class Sorter():
    
    def __init__(self, base_path):

        self.base_path = base_path

        self.strip_list = ['.wav', '.WAV', '5.1', 'Surround', 'SURR', 'Stereo', 'ST', 
                                'FUL', 'FullMix', 'MIX', 'AVO', 'VO', 'SFX', 'FX', 
                                'SOT', 'DIA', 'MSC', 'MUS', 'OLV', 'SD1', 'SD2', 'SD3']     
        
        self.file_type_list = ['FUL', 'MIX', 'AVO', 'VO', 'SFX', 'FX', 'SOT', 'DIA', 'MSC', 'MUS', 'SD1', 'SD2', 'SD3', 'OLV']
        self.channel_type_list = ['Surround', '5.1', 'SURR', 'Stereo', 'ST']
        self.surround_type_list = ['Surround', '5.1', 'SURR']
        self.stereo_type_list = ['Stereo', 'ST']
        self.fullmix_type_list = ['FUL', 'MIX']

        self.completed_folder_objects = []

    def StripFromFilename(self, file_name):
        
        #file_pattern = os.path.splitext(os.path.splitext(file_name)[0])[0]
        for pattern in self.strip_list:
            file_name = file_name.replace(pattern, '')
            for surr_ext in ['.L', '.Ls', '.C', '.R', '.Rs', '.LFE']: # Remove left over extensions seperately for various reasons
                if file_name.endswith(surr_ext):
                    file_name = os.path.splitext(file_name)[0]

        file_name = file_name.replace('__', '_') 
        return file_name


    def CreateFolderObjects(self, base_path):
            
        folder_objects = []
        wav_files = [f for f in os.listdir(base_path) if f.endswith('.wav')]
        files = []
        for f in wav_files:
            f = self.StripFromFilename(f) # Removes many name elements 
            files.append(f)
            
        # Remove duplicate entries
        unique_names = list(set(files))   

        # Add names to folder objects list (each folder object is itself a list)
        for name in unique_names:
            folder_objects.append([name, []]) # Create Folder object. The empty list will hold files that should go into the folder

        return folder_objects, wav_files

    def AddFiles(self, folder_objects, all_files):
        
        # For each file 
        for f in all_files:
            stripped_f = self.StripFromFilename(f) # Remove extraneous stuff for matching to folder name
            
            for fo in folder_objects: # check the name entry in each folder object
                if stripped_f == fo[0]:
                    fo[1].append(f) # add file to file list in file object if there is a match

        return folder_objects

    def GetPatterns(self, folder_object):

        file_type_patterns = []
        channel_type_patterns = []
        for fo_file in folder_object[1]:
            fo_file = os.path.splitext(fo_file)[0] # drops file extension

            for channel_type in self.channel_type_list:
                if channel_type in fo_file:
                    channel_type_patterns.append(channel_type)
            
            for file_pattern in fo_file.split('_'):
                file_type_patterns.append(file_pattern)

        file_type_patterns = set(file_type_patterns)
        guide_patterns = set(self.file_type_list)
        
        if len(file_type_patterns.intersection(guide_patterns)) > 0:
            return list(file_type_patterns.intersection(guide_patterns)), list(set(channel_type_patterns))
        else:
            return 'No Common Elements'

    # folder_objects = [[name, [files]],]
    def Distribute(self, folder_object, fo_file_path, fo_file):
        
        # Check if surround, then check which file_type it is and place in corresponding folder
        for surround_type in self.surround_type_list:
            if surround_type in fo_file:
                for file_type in folder_object[2]:
                    if file_type in fo_file:
                        shutil.move(fo_file_path, self.base_path + '/' + folder_object[0] + 'MixSplits/TV/Surround/' + file_type + '/' + fo_file)
                        return

        # Check if stereo signature exists 
        for stereo_type in self.stereo_type_list:
            if stereo_type in fo_file:
                if 'OLV' in fo_file:
                    shutil.move(fo_file_path, self.base_path + '/' + folder_object[0] + 'MixSplits/OLV/' + fo_file)
                    return
                    
                else:
                    shutil.move(fo_file_path, self.base_path + '/' + folder_object[0] + 'MixSplits/TV/Stereo/' + fo_file)
                    return

        # When stereo only, stereo files often don't have stereo signatures. 
        # In that case if there is no 'FUL' all files go in OLV. If there is a 'FUL' all files go in TV/Stereo except OLV which goes in 'OLV' (if it exists)
        for file_type in folder_object[2]:
            if file_type == 'FUL': # This essentially checks if there are any 'FUL's anywhere for this folder_object
                if 'OLV' not in fo_file:
                    shutil.move(fo_file_path, self.base_path + '/' + folder_object[0] + 'MixSplits/TV/Stereo/' + fo_file)
                    return


        # Everything else
        shutil.move(fo_file_path, self.base_path + '/' + folder_object[0] + 'MixSplits/OLV/' + fo_file)
        return

    def UndoSort(self, base_path):
        for root, subs, files in os.walk(base_path):
            for f in files:
                if f.endswith('.wav'):
                    shutil.move(os.path.join(root, f), base_path + '/' + f)

        for fo in self.completed_folder_objects:
            name = self.base_path + '/' + fo[0] + 'MixSplits'
            #if [f for f in os.listdir(name) if not f.startswith('.')] == []:
            os.rename(name, name + '_____TO_BE_DELETED')

    def make_archive(self, source, destination):
        base = os.path.basename(destination)
        name = base.split('.')[0]
        format = base.split('.')[1]
        archive_from = os.path.dirname(source)
        archive_to = os.path.basename(source.strip(os.sep))
        shutil.make_archive(name, format, archive_from, archive_to)
        shutil.move('%s.%s'%(name,format), destination)

    def ZipFolders(self):
        # Dont allow zipping unitl organizing is done
        if len(self.completed_folder_objects) > 0:
            for fo in self.completed_folder_objects:
                name = self.base_path + '/' + fo[0] + 'MixSplits'
                self.make_archive(name, name + '.zip')

    def CreateFolders(self, fo, base_path):
        
        #Create Mix/Splits Folder
        folder_name = fo[0] + 'MixSplits'
        folder_path = base_path + '/' + folder_name
        os.mkdir(folder_path)
       

        # Check if there are surrounds
        if len(set(fo[3]).intersection(set(self.surround_type_list))) > 0: 
            os.mkdir(folder_path + '/TV')
            os.mkdir(folder_path + '/TV/Surround')
            for file_type in fo[2]:
                if file_type != 'OLV':
                    os.mkdir(folder_path + '/TV/Surround/' + file_type)

            # Check if there are any stereo files, we assume in the presence of 5.1, stereo will be marked as stereo in some way (not blank)
            if len(set(fo[3]).intersection(set(self.stereo_type_list))) > 0: 
                os.mkdir(folder_path + '/TV/Stereo')
        
            # Check if there are any OLV files
            if len(set(fo[2]).intersection({'OLV'})) > 0:
                os.mkdir(folder_path + '/OLV')
            
            return

        if len(set(fo[2]).intersection({'OLV'})) > 0:
            os.mkdir(folder_path + '/OLV')

        for fo_file in fo[1]:
            for fullmix_type in self.fullmix_type_list:
                if fullmix_type in fo_file:
                    os.mkdir(folder_path + '/TV')
                    os.mkdir(folder_path + '/TV/Stereo')

        return
    
    # this is where we start
    def Sort(self):

        folder_objects, all_files = self.CreateFolderObjects(self.base_path)
        folder_objects = self.AddFiles(folder_objects, all_files)

        for fo in folder_objects:
            fo.append(self.GetPatterns(fo)[0])
            fo.append(self.GetPatterns(fo)[1])
            self.CreateFolders(fo, self.base_path)
            
            for fo_file in fo[1]:
                fo_file_path = self.base_path + '/' + fo_file
                self.Distribute(fo, fo_file_path, fo_file)

            self.completed_folder_objects.append(fo)

        return 'Done!'