from rename import Rename
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from pymediainfo import MediaInfo

class App:
    def __init__(self):
        self.rn = Rename()
        self.root = Tk()
        self.root.title('BoarRename')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.resizable(FALSE,FALSE)

        self.mainframe = ttk.Frame(self.root, padding="6 6 6 6")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.dir_name = StringVar()
        self.creative_name = StringVar()
        self.a_dir = StringVar()
        self.min_var = IntVar()
        self.min_var.set(1)
        self.max_var = IntVar()
        self.max_var.set(148)
        self.a_dir.set('Directory')
        self.folder = None
        self.tree = ttk.Treeview(self.mainframe, columns=('newname'))
        self.tree.grid(column=1, row=3, columnspan=5)
        self.tree.heading('#0', text='Current Filename')
        self.tree.heading('0', text='New Filename')
        self.tree.column('#0',width=300)
        self.tree.column('0', width=300)

        self.scroll = ttk.Scrollbar(self.mainframe, orient=VERTICAL, command=self.tree.yview)
        self.scroll.grid(column=7, row=3, sticky=(N,S))

        self.tree.configure(yscrollcommand=self.scroll.set)


        self.path = ttk.Label(self.mainframe, width=100, text="Project name")
        self.path.grid(column=1, row=6, columnspan=10, sticky=W)

        self.dir_entry = ttk.Entry(self.mainframe, width=3, textvariable=self.dir_name)
        self.dir_entry.grid(column=1, row=7, columnspan=2, sticky=(W, E))

        self.path = ttk.Label(self.mainframe, width=100, text="Creative name")
        self.path.grid(column=1, row=8, columnspan=10, sticky=W)

        self.creative_entry = ttk.Entry(self.mainframe, width=3, textvariable=self.creative_name)
        self.creative_entry.grid(column=1, row=9, columnspan=2, sticky=(W, E))



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

        self.ab = ttk.Button(self.mainframe, text='Select Directory', command=self.open_dir)
        self.ab.grid(column=1, row=5, sticky=W)

        self.refresh = ttk.Button(self.mainframe, text='refresh/preview', command=self.refresh)
        self.refresh.grid(column=2, row=5, sticky=W)

        self.apply = ttk.Button(self.mainframe, text='Apply', command=self.apply)
        self.apply.grid(column=5, row=5, sticky=E)
        self.apply.state(['disabled'])

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=8, pady=5)

    def open_dir(self):
        self.folder = filedialog.askdirectory()
        if len(self.folder) > 0:
            self.a_dir.set(self.folder)
            self.folder = self.rn.inputs(self.folder)
            self.tree.delete(*self.tree.get_children())
            preview = self.rn.preview(self.folder,self.tree)
            print(self.tree)
            self.dir_name.set(preview)
            self.apply.state(['!disabled'])
        else:
            self.apply.state(['disabled'])
            return

    def refresh(self):
        print('refreshed')
        self.tree.delete(*self.tree.get_children())
        self.dir_name.set(self.rn.preview(self.folder, self.tree,self.dir_name.get(),self.creative_name.get()))

    def apply(self):
        name = self.dir_name.get()
        creative = self.creative_name.get()
        self.rn.renames(self.folder, name, creative, self.min_var.get(), self.max_var.get)


a_app = App()
a_app.root.mainloop()
