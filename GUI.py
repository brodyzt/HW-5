from tkinter import *

class MusicChooser:

    def __init__(self, master):
        self.master = master
        self.frame = Frame(master)
        self.frame.pack()
        self.add_chooser_elements()

    def add_chooser_elements(self):
        self.tracks_text = Label(self.frame, text='# of Tracks:')
        self.tracks_text.grid(row=0, column=0, sticky=W)

        self.tracks_input = Entry(self.frame)
        self.tracks_input.grid(row=0,column=1, stick=E)

        self.complete_button = Button(self.frame, text='Done', command=self.close)
        self.complete_button.grid(row=1, columnspan=2)

    def close(self):
        print('Number of tracks: ' + str(self.tracks_input.get()))
        self.master.destroy()

root = Tk()

chooser = MusicChooser(root)

root.mainloop()