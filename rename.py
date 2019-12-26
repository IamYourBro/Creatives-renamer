import pathlib
import glob
from pymediainfo import MediaInfo
resolution, file_name, file_extension,file_size, other_duration,sampled_width,sampled_height  = [],[],[],[],[],[],[]
codes = []
duration = []
import random
import string
import re

def randomStringDigits(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_lowercase + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

class Rename:
    max = 200
    start = 1

    def inputs(self, path):
        # apath = input('File path')
        apath = pathlib.Path(path)
        return apath

    def getstartandmax(self):
        duo = input('start number and max eps').split(',')
        self.start = int(duo[0])
        self.max = int(duo[1])

    def preview(self, directory, gui, name=False, creative=False):
        print(f'+ {directory}')
        count = self.start
        maxcount = self.max
        parts = directory.parts
        parts = parts[len(directory.parts) - 1]
        duration = []
        if name:
            parts = name
        for path in sorted(directory.glob('*')):
            # depth = len(path.relative_to(directory).parts)
            # spacer = '    ' * depth
            # print(f'{spacer}+ {path.name}')

            file_info = MediaInfo.parse(path).to_data()

            # other_duration = (file_info['tracks'][0]['other_duration'][0])
            pattern = re.compile('\d+ [s]')
            duration.append(pattern.findall(file_info['tracks'][0]['other_duration'][0]))

            print(codes)
            print(count)
            size = str(file_info['tracks'][1]['sampled_width'])+"x"+str(file_info['tracks'][1]['sampled_height'])
            print(size)
            epno = str(count).zfill(2)

            nameString = f"{parts}_{creative}_{size}_{duration[int(count-1)]}_CODE_{path.suffix}"
            # nameString = f"{parts} - {other_duration} - {epno}{path.suffix}"
            gui.insert('', 'end', path.name, text=path.name, values=(nameString,''))
            if count == maxcount:
                exit()
            count += 1
        
        return parts



    def renames(self, directory, name, creative, count, maxcount):
        # count = self.start
        # maxcount = self.max
        codes = []
        duration = []
        for path in sorted(directory.glob('*')):
            parts = directory.parts
            parts = parts[len(directory.parts)-1]
            epno = str(count).zfill(2)
            file_info = MediaInfo.parse(path).to_data()

            # other_duration = (file_info['tracks'][0]['other_duration'][0])
            pattern = re.compile('\d+ [s]')
            duration = pattern.findall(file_info['tracks'][0]['other_duration'][0])
            code = randomStringDigits(6)
            codes.append(code)


            size = str(file_info['tracks'][1]['sampled_width'])+"x"+str(file_info['tracks'][1]['sampled_height'])
            print(size)
            nameString = f"{directory}\{name}_{creative}_{size}_{duration}_{codes[int(count-1)]}_{path.suffix} "
            # nameString = f"{directory}\{name} - {other_duration} - {epno}{path.suffix} "
            path.rename(nameString)
            
            
            if count == maxcount:
                exit()
            count += 1
