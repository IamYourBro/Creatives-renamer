import pathlib
import glob
from pymediainfo import MediaInfo
resolution, file_name, file_extension,file_size, other_duration,sampled_width,sampled_height  = [],[],[],[],[],[],[]
codes = []
duration = []
import random
import string
import re
import os
import pandas as pd
from pandas import DataFrame

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

    def preview(self, directory, gui, name=False, creative=False, task = "00000", locals = False):
        print(f'+ {directory}')
        count = self.start
        maxcount = self.max
        parts = directory.parts
        parts = parts[len(directory.parts) - 1]
        duration = []
        if name:
            parts = name
        for path in sorted(directory.glob('*')):
            file_info = MediaInfo.parse(path).to_data()
            pattern = re.compile('\d+ [s]')
            duration.append(pattern.findall(file_info['tracks'][0]['other_duration'][0]))
            print(count)
            size = str(file_info['tracks'][1]['sampled_width'])+"x"+str(file_info['tracks'][1]['sampled_height'])
            epno = str(count).zfill(2)
            nameString = f"{parts}_{creative}_{size}_{locals}_{duration[int(count-1)]}_CODE_MKT{task}{path.suffix}"
            gui.insert('', 'end', path.name, text=path.name, values=(nameString,''))
            if count == maxcount:
                exit()
            count += 1
        return parts



    def renames(self, directory, name, creative, count, maxcount, task, locals):
        codes = []
        duration = []
        for path in sorted(directory.glob('*')):
            parts = directory.parts
            parts = parts[len(directory.parts)-1]
            epno = str(count).zfill(2)
            file_info = MediaInfo.parse(path).to_data()
            pattern = re.compile('\d+ [s]')
            duration = pattern.findall(file_info['tracks'][0]['other_duration'][0])
            code = randomStringDigits(6)
            codes.append(code)
            size = str(file_info['tracks'][1]['sampled_width'])+"x"+str(file_info['tracks'][1]['sampled_height'])
            nameString = f"{directory}\{name}_{creative}_{size}_{locals}_{duration}_CODE_MKT{task}{path.suffix} "
            path.rename(nameString)
            
    
    def addcodes(self, directory, name, creative, count, maxcount, task, locals):
        codes,names,packs = [],[],[]
        path = directory
        files = os.listdir(path)
        # переписать с пандаса на простое чтение и запись
        database = pd.read_excel(r"C:\Users\i.shabanin\Combo_НЕЙМИНГ.xlsx")
        print(files)
        print("_______________________________________")
        print(database['Code'])

        for file in files:
            split = file.split('_')
            projectname = split[0]
            creativename = split[1]
            resolution = split[2]
            localizations = split[3]
            durations = split[4]
            code_old = split[5]
            taskname = split[6]
           

            
            code = randomStringDigits(6)
            if code in database['Code']:
                while True:
                    code = randomStringDigits(6)
                    if code not in database['Code']:
                        codes.append(code)
                        break

            else:
                codes.append(code)
            print(codes)
            filename, file_extension = os.path.splitext(file)
            names.append(str(projectname + "_" + creativename + "_" + resolution + "_" + localizations + "_" + durations + "_" + str(code) + "_" + taskname))
            packs.append('temp')
            new_data = DataFrame()
            print(codes)
            print(packs)
            print(names)
            new_data['Pack_name'] = packs
            new_data['Name'] = names
            new_data['Code'] = codes
            
            os.rename(os.path.join(path, file), os.path.join(path, projectname + "_" + creativename + "_" + resolution + "_"+ localizations + "_"  + durations + "_" + str(code) + "_" + taskname ))
        result = pd.concat([database,new_data], sort= False)
        result.to_excel(r"C:\Users\i.shabanin\Combo_НЕЙМИНГ.xlsx", index = None)  

