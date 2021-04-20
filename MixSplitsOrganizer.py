
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, Canvas, PhotoImage
from tkinter.ttk import Frame, Label, Entry, Button
from tkinter import filedialog
import sorter as Sorter


class MixSplitsOrganizer(Frame):
    
    def __init__(self):
        super().__init__()
        self.InitUI()
        self.folder_selected = None
        self.SorterInstance = None
    
    def PrintCallBack(self, message):
        self.entry1.delete(0, 'end')
        self.entry1.insert(0, message)


    def SelectPath(self):
        self.folder_selected = filedialog.askdirectory()
        self.entry1.delete(0, 'end')
        self.entry1.insert(0, self.folder_selected)
        self.Go()

    def UndoSort(self): 
        self.SorterInstance.UndoSort(self.folder_selected)

    def Zip(self):
        self.SorterInstance.ZipFolders()

    def Go(self):
        if self.folder_selected is not None:
            self.SorterInstance = Sorter.Sorter(self.folder_selected)
            message = self.SorterInstance.Sort()
            self.entry1.delete(0, 'end')
            self.entry1.insert(0, message)
        else:
            error = 'Select Path Please'
            self.entry1.delete(0, 'end')
            self.entry1.insert(0, error)


    def InitUI(self):
        
        self.master.title('Mix + Splits Organizer')
        self.pack(fill=BOTH, expand=True)

        '''
        frame_base = Frame(self)
        frame_base.pack()
        C = Canvas(frame_base, bg='blue')
        img = PhotoImage(file='/Users/asm/Desktop/color_1.png')
        background_label = Label(frame_base, image=img)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        C.pack()
        '''
        

        # -- Choose A Path -- #
        frame1 = Frame(self)
        frame1.pack(fill=X)

        select_path = Button(frame1, text='Choose A Path', command = self.SelectPath)
        select_path.pack(side=LEFT, padx=5, pady=5)
        
        self.entry1 = Entry(frame1)
        self.entry1.pack(fill=X, padx=5, expand=True)

        # -- Undo -- #
        frame2 = Frame(self)
        frame2.pack(fill=X)
        
        undo_sort = Button(frame2, text='Undo', command = self.UndoSort)
        undo_sort.pack(side=LEFT, padx=5, pady=5)

        # -- Zip -- #
        frame3 = Frame(self)
        frame3.pack(fill=X)

        zip_folders = Button(frame3, text='Zip Folders', command = self.Zip)
        zip_folders.pack(side=LEFT, padx=5, pady=5)


def Main():
    window = Tk()
    window.geometry('500x200')
    app = MixSplitsOrganizer()
    window.mainloop()

if __name__ == '__main__':
    Main()
