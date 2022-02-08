import os
import shutil
import argparse

#BASE_PATH = '/Users/juanaboites/mix-splits-organizer/tests/test'

SPLIT_LIST = ['__', '_', ' ', '.']

SURROUND_LIST = ['Surround', '5.1', 'SURR']
STEREO_LIST = ['Stereo', 'ST']
TV_LIST = ['FUL', 'FullMix', 'MIX']
STEMS_LIST = ['FUL', 'MIX', 'FullMix', 'AVO', 'VO', 'SFX', 'FX', 'SOT', 'DIA', 'MSC', 'MUS', 'SD1', 'SD2', 'SD3'] #
CHANNEL_LIST = ['.L', '.Ls', '.C', '.R', '.Rs', '.LFE']
EXTENSION_LIST = ['.wav', '.WAV']

REDUCE_LIST = SURROUND_LIST + STEREO_LIST + TV_LIST + STEMS_LIST + EXTENSION_LIST
REDUCE_LIST.append('OLV')

def ReduceFilename(file_name):
        
        for pattern in REDUCE_LIST:
            file_name = file_name.replace(pattern, '')
            for ext in CHANNEL_LIST: # Remove left over extensions seperately
                if file_name.endswith(ext):
                    file_name = os.path.splitext(file_name)[0]

        # these fix some side effects of removing things
        file_name = file_name.replace('__', '_')
        file_name = file_name[:len(file_name) - 1]
        return file_name



def Sort(base_path):
            
    wav_files = [f for f in os.listdir(base_path) if f.endswith('.wav')]
    reduced_files = [ReduceFilename(f) for f in wav_files] #remove extra stuff to get to the project/spot name
    folder_names = list(set(reduced_files)) #remove duplicates
    folder_objects = {folder_name: {'files': [f for f in wav_files if ReduceFilename(f) in folder_name]} for folder_name in folder_names} #collect files for each folder 
    
    for folder_object in folder_objects:

        files = folder_objects[folder_object]['files']
        
        # set the olv only switch
        olv_only = True
        for file in files:
            if any(tv_pattern in file for tv_pattern in TV_LIST):
                olv_only = False 

    
        project_path = base_path + '/' + folder_object + '_MixSplits'

        for file in files:
            
            # Recursively break up the file name according to each split criteria
            split_file = [file]
            for split_basis in SPLIT_LIST:
                for i, splitElement in enumerate(split_file): #
                    temp_split = splitElement.split(split_basis)
                    del split_file[i] # replace the previous with the results of new split basis
                    for ts in temp_split:
                        split_file.insert(i, ts)
        
            slash = '/'
            if base_path.endswith('/'):
                slash = ''

            #if there are surrounds we have to create subfolders for each stem type
            if any(surr_pattern in file for surr_pattern in SURROUND_LIST):                 
            
                overlap = set(STEMS_LIST) & set(split_file)
                if len(overlap) > 0:
                    sub_path = project_path + '/TV/Surround/' + list(overlap)[0] #there should only be one
                    if not os.path.isdir(sub_path):
                        os.makedirs(sub_path)
                    
                    src = base_path + slash + file
                    dest = sub_path + '/' + file
                    shutil.move(src, dest)

            #olv always goes in olv folder
            elif "OLV" in split_file:
                
                sub_path = project_path + '/OLV'
                if not os.path.isdir(sub_path):
                    os.makedirs(sub_path)
                
                src = base_path + slash + file
                dest = sub_path + '/' + file
                shutil.move(src, dest)


            #stero files go in tv if it exists, otherwise olv
            elif any(sub_f in file for sub_f in STEMS_LIST):
                
                if olv_only:
                    sub_path = project_path + '/OLV'
                else:
                    sub_path = project_path + '/TV/Stereo'

                if not os.path.isdir(sub_path):
                    os.makedirs(sub_path)
                
                src = base_path + slash + file
                dest = sub_path + '/' + file
                shutil.move(src, dest)



parser = argparse.ArgumentParser(description='Organizes audio deliverables in a path assuming file naming follows a few conventions')
parser.add_argument('path', help='Organize the .wav files in this path, does not consider sub folders')
args = parser.parse_args()
Sort(os.path.abspath(args.path))

