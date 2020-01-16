# -*- coding: utf-8 -*-

from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from pymediainfo import MediaInfo
# from win32com.client import Dispatch
import re
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

class App:
    def __init__(self):
        
        # def callback(count):
        #     os.system('start ' +fileNames[count])

        # def makeLink(files):
        #     localCount = count
        #     link = Button(frame1, text=(count , files), bg="light blue", cursor="hand2", command=lambda: callback(localCount))
        #     link.pack()    


        
        # oldDir = os.getcwd()
        # newDir = os.chdir(r"K:\_Media Buying\Отчеты\mbag_scripts\Creatives_naming\test\Combo\Видео\Pack 1")
        # fileNames = os.listdir(os.getcwd())

        
        # count = 0

        # for files in fileNames:
        #     makeLink(files)
        #     count += 1

        self.rn = Rename()
        self.root = Tk()
        self.root.title('Creative renamer')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.resizable(FALSE,FALSE)

        self.mainframe = ttk.Frame(self.root, padding="6 6 6 6")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.dir_name = StringVar()
        self.creative_name = StringVar()
        self.task_number = StringVar()
        self.localization = StringVar()
        self.a_dir = StringVar()
        self.min_var = IntVar()
        self.min_var.set(1)
        self.max_var = IntVar()
        self.max_var.set(148)
        self.a_dir.set('Directory')
        self.folder = None
        self.tree = ttk.Treeview(self.mainframe, columns=('newname'))
        self.tree.grid(column=1, row=3, columnspan=5)
        self.tree.heading('#0', text='Current name')
        self.tree.heading('0', text='New name')
        self.tree.column('#0',width=400)
        self.tree.column('0', width=500)

        self.scroll = ttk.Scrollbar(self.mainframe, orient=VERTICAL, command=self.tree.yview)
        self.scroll.grid(column=7, row=3, sticky=(N,S))

        self.tree.configure(yscrollcommand=self.scroll.set)

        from os import popen    
        def openfile():
            curItem = self.tree.focus()
            os.chdir(self.folder)
            os.system(f"open {self.tree.item(curItem)['values'][0]}")
            # popen(self.tree.item(curItem)['values'][0])
     
        

        self.button = ttk.Button(self.mainframe, text="Open", command=openfile)  # <------
        self.button.grid(column=8, row=3, sticky=E)


        self.path = ttk.Label(self.mainframe, width=100, text="Project name")
        self.path.grid(column=1, row=6, columnspan=10, sticky=W)

        self.dir_entry = ttk.Entry(self.mainframe, width=3, textvariable=self.dir_name)
        self.dir_entry.grid(column=1, row=7, columnspan=2, sticky=(W, E))

        self.path = ttk.Label(self.mainframe, width=100, text="Creative name")
        self.path.grid(column=1, row=8, columnspan=10, sticky=W)
        self.creative_entry = ttk.Entry(self.mainframe, width=3, textvariable=self.creative_name)
        self.creative_entry.grid(column=1, row=9, columnspan=2, sticky=(W, E))



        self.path = ttk.Label(self.mainframe, width=100, text="Localization")
        self.path.grid(column=1, row=10, columnspan=10, sticky=W)

        self.locals = ttk.Entry(self.mainframe, width=3, textvariable=self.localization)
        self.locals.grid(column=1, row=11, columnspan=2, sticky=(W, E))







        self.path = ttk.Label(self.mainframe, width=100, text="TASK")
        self.path.grid(column=1, row=12, columnspan=10, sticky=W)

        self.task_entry = ttk.Entry(self.mainframe, width=3, textvariable=self.task_number)
        self.task_entry.grid(column=1, row=13, columnspan=2, sticky=(W, E))



        # self.path = ttk.Label(self.mainframe, width=100, text="Localization")
        # self.path.grid(column=1, row=6, columnspan=10, sticky=W)

        # self.dir_entry = ttk.Entry(self.mainframe, width=3, textvariable=self.localization)
        # self.dir_entry.grid(column=1, row=7, columnspan=2, sticky=(W, E))

        # self.path = ttk.Label(self.mainframe, width=100, text="Creative name")
        # self.path.grid(column=1, row=8, columnspan=10, sticky=W)

        # self.creative_entry = ttk.Entry(self.mainframe, width=3, textvariable=self.creative_name)
        # self.creative_entry.grid(column=1, row=9, columnspan=2, sticky=(W, E))





        # self.min = ttk.Entry(self.mainframe, width=4, textvariable=self.min_var)
        # self.min.grid(column=3, row=5)

        # self.max = ttk.Entry(self.mainframe, width=4, textvariable=self.max_var)
        # self.max.grid(column=4, row=5)

        self.ab = ttk.Button(self.mainframe, text='Select dir', command=self.open_dir)
        self.ab.grid(column=1, row=5, sticky=W)

        # self.excelfile = ttk.Button(self.mainframe, text='Выбрать excel-файл', command=self.open_excel_file)
        # self.excelfile.grid(column=5, row=4, sticky=E)

        self.refresh = ttk.Button(self.mainframe, text='preview', command=self.refresh)
        self.refresh.grid(column=2, row=5, sticky=W)

        self.apply = ttk.Button(self.mainframe, text='Rename', command=self.apply)
        self.apply.grid(column=5, row=5, sticky=E)
        self.apply.state(['disabled'])

        self.addcode = ttk.Button(self.mainframe, text='add code and write to excel', command=self.addcode)
        self.addcode.grid(column=5, row=6, sticky=E)
        self.addcode.state(['disabled'])


        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=8, pady=5)

    def open_dir(self):
        self.folder = filedialog.askdirectory()
        os.chdir(self.folder)
        os.system("find . -name '.DS_Store' -type f -delete")
        if len(self.folder) > 0:
            self.a_dir.set(self.folder)

            self.folder = self.rn.inputs(self.folder)
            self.tree.delete(*self.tree.get_children())
            preview = self.rn.preview(self.folder,self.tree)
            print(self.tree)
            self.dir_name.set(preview)
            self.creative_name.set(preview)
            self.localization.set("EN")
            self.apply.state(['!disabled'])
            self.addcode.state(['!disabled'])

        else:
            self.apply.state(['disabled'])
            self.addcode.state(['disabled'])
            return 
  


    def open_excel_file(self):
        self.excelname = filedialog.askopenfilename(initialdir = r"K:\_Media Buying\CREATIVES\Creatives sorted",title = "Select file", filetypes = (("excel files","*.xlsx"),("all files","*.*")))
        return self.excelname

    def refresh(self):
        print('refreshed')
        self.tree.delete(*self.tree.get_children())
        self.dir_name.set(self.rn.preview(self.folder, self.tree,self.dir_name.get(),self.creative_name.get(), self.task_number.get(),self.localization.get()))

    def apply(self):
        name = self.dir_name.get()
        creative = self.creative_name.get()
        task = self.task_number.get()
        localization = self.localization.get()
        self.rn.renames(self.folder, name, creative, self.min_var.get(), self.max_var.get, task, localization)

    def addcode(self):
        name = self.dir_name.get()
        creative = self.creative_name.get()
        task = self.task_number.get()
        localization = self.localization.get()
        excelname = self.open_excel_file()
        self.rn.addcodes(self.folder, name, creative, self.min_var.get(), self.max_var.get, task, localization, excelname)





#__________________________________________________________________________________________________________________________________________________________________________________________________________________________
#                                                                                                Класс ренейминга

###########################################################################################################################################################################################################################





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
        print((glob.glob(f"{directory}/*")))
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

            try:
                duration = pattern.findall(file_info['tracks'][0]['other_duration'][0])
                duration_wo_quotes = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])), duration)) 
            except:
                duration_wo_quotes = "XXX"
            print(count)

            try:
                duration = pattern.findall(file_info['tracks'][0]['other_duration'][0])
                duration_wo_quotes = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])), duration)) 
                size = str(file_info['tracks'][1]['sampled_width'])+"x"+str(file_info['tracks'][1]['sampled_height'])
                epno = str(count).zfill(2)
                nameString = f"{parts}_{creative}_{size}_{locals}_{str(duration_wo_quotes).replace('[', '').replace(']', '')}s_CODE_MKT{task}{path.suffix}"
            except:
                try:
                    size = str(file_info['tracks'][1]['width'])+"x"+str(file_info['tracks'][1]['height'])
                except:
                    size = "size"
                    
                epno = str(count).zfill(2)
                duration_wo_quotes = "XXX"
                nameString = f"{parts}_{creative}_{size}_{locals}_{str(duration_wo_quotes).replace('[', '').replace(']', '')}_CODE_MKT{task}{path.suffix}"
            gui.insert('', 'end', path.name, text=path.name, values=(nameString,''))
            if count == maxcount:
                exit()
            count += 1
        return parts


    def renames(self, directory, name, creative, count, maxcount, task, locals):
        сount = self.start
        codes = []
        duration = []
        print(directory)
        os.chdir(directory)
        paths = []
        for path in sorted(directory.glob('*')):
            
            parts = directory.parts
            parts = parts[len(directory.parts)-1]
            epno = str(count).zfill(2)
            file_info = MediaInfo.parse(path).to_data()
            pattern = re.compile('\d+ [s]')

            try:
                duration = pattern.findall(file_info['tracks'][0]['other_duration'][0])
                duration_wo_quotes = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])), duration)) 
            except:
                duration_wo_quotes = "XXX"

            code = randomStringDigits(6)
            codes.append(code)
            

            try:
                duration = pattern.findall(file_info['tracks'][0]['other_duration'][0])
                duration_wo_quotes = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])), duration)) 
                size = str(file_info['tracks'][1]['sampled_width'])+"x"+str(file_info['tracks'][1]['sampled_height'])
                epno = str(count).zfill(2)
                nameString = f"{name}_{creative}_{size}_{locals}_{str(duration_wo_quotes).replace('[', '').replace(']', '')}s_CODE_MKT{task}{path.suffix}"
                nameString2 = f"{name}_{creative}{str(count)}_{size}_{locals}_{str(duration_wo_quotes).replace('[', '').replace(']', '')}s_CODE_MKT{task}{path.suffix}"
            except:
                duration_wo_quotes = "XXX"
                try:
                    size = str(file_info['tracks'][1]['width'])+"x"+str(file_info['tracks'][1]['height'])
                except:
                    size = "size"
                    
                epno = str(count).zfill(2)
                nameString = f"{name}_{creative}_{size}_{locals}_{str(duration_wo_quotes).replace('[', '').replace(']', '')}_CODE_MKT{task}{path.suffix}"
                nameString2 = f"{name}_{creative}{str(count)}_{size}_{locals}_{str(duration_wo_quotes).replace('[', '').replace(']', '')}_CODE_MKT{task}{path.suffix}"
            

            # nameString = f"{directory}\{name}_{creative}_{size}_{locals}_{str(duration_wo_quotes).replace('[', '').replace(']', '')}s_CODE_MKT{task}{path.suffix} "
            paths.append(str(nameString))
            print(paths[:-1])
            print(nameString)
            if nameString in paths[:-1]:
                print('yes')
                count += 1
                path.rename(nameString2)
            else:
                print('no')
                path.rename(nameString)
            paths.append(str(nameString))
            # for i in range(0, len(paths)-1):
            #     if (paths[i] in paths):
            #         print(paths[i])
            #         print(paths)
            #         print('yes')
            #         count += 1
            #         path.rename(nameString2)
            #     else:
            #         count += 1
            #         print(paths[i])
            #         print(paths)
            #         print('no')
            #         path.rename(nameString)
            
    # закомментил до финальной версии
    def addcodes(self, directory, name, creative, count, maxcount, task, locals, excelname):
        codes,names,packs = [],[],[]
        path = directory
        files = os.listdir(path)
        # переписать с пандаса на простое чтение и запись
        database = pd.read_excel(excelname)
        print(files)
        print("_______________________________________")
        database['Code'] = ""
        database['Name'] = ""
        database['Pack_name'] = ""
        print(database['Code'])

        for file in files:
            try:
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
                
                filename, file_extension = os.path.splitext(file)
                names.append(str(projectname + "_" + creativename + "_" + resolution + "_" + localizations + "_" + durations + "_" + str(code) + "_" + taskname))
                packs.append('temp')
                new_data = DataFrame()
                # print(codes)
                # print(packs)
                # print(names)
                new_data['Pack_name'] = packs
                new_data['Name'] = names
                new_data['Code'] = codes
                
                os.rename(os.path.join(path, file), os.path.join(path, projectname + "_" + creativename + "_" + resolution + "_"+ localizations + "_"  + durations + "_" + str(code) + "_" + taskname ))
            except:
                pass
        result = pd.concat([database,new_data], sort= False)
        result.to_excel(excelname, index = None)  
        return 0

a_app = App()
a_app.root.mainloop()
