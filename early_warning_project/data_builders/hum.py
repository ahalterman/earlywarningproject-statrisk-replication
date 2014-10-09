#!/usr/bin/env python

import urllib2
import shutil as shutil
from early_warning_project.dataset import Dataset
import subprocess


class Hum(Dataset):

    def __init__(self):
        super(Hum, self).__init__()
        self.name = self.config.get('hum', 'name')
        self.url = self.config.get('hum', 'url')

    def download_data(self):
        # Download latest file
        print('downloading - ' + self.url + ' ...')
        response = urllib2.urlopen(self.url)
        print('download completed successfully')

        filename = self.config.get('hum', 'filename')

        src_file = self.download_directory + "/" + filename

        input_file = open(src_file, 'wb+')
        input_file.write(response.read())
        input_file.close()

        shutil.copyfile(src_file, self.data_in_directory + "/" + filename)

    def build_data(self):

        print('running R hum transformation ...')

        rscript = self.config.get('files_and_directories', 'r_script_install')
        working_directory = self.config.get('files_and_directories', 'working_directory')
        hum_r_file = working_directory + self.config.get('hum', 'hum_r_file')
        input_r_file = self.config.get('hum', 'input_file_for_R')
        output_r_file = self.config.get('hum', 'output_file_for_R')

        command = rscript, hum_r_file, working_directory, input_r_file, output_r_file

        print(command)
        print(subprocess.check_output(command))

        print('successfully completed R hum transformation')



# All you are doing here is making it possible for this dataset to run on it's own
# You can simply change the name of the 'Template' class to the name of your dataset class
def main():
    dataset = Hum()
    Hum.download_data(dataset)
    Hum.build_data(dataset)

if __name__ == '__main__':
    main()