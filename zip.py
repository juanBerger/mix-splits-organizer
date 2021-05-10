import pathlib
import os

cwd = pathlib.Path(__file__).parent
sub_dirs = [dirname for dirname in os.listdir('.') if os.path.isdir(dirname)]
print(sub_dirs)


def ZipFolders(path):
    for fo in self.completed_folder_objects:
        name = self.base_path + '/' + fo[0] + 'MixSplits'
        self.make_archive(name, name + '.zip')