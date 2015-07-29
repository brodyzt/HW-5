from tkinter import *

from PianoUtilities import *

class MusicChooser:

    def __init__(self):
        root = Tk()
        self.master = root
        self.frame = Frame(self.master)
        self.frame.pack()
        self.row = 0
        self.add_chooser_elements()

    def start(self):
        self.master.mainloop()

    def add_chooser_elements(self):
        self.tempo_text = Label(self.frame, text='Tempo:')
        self.tempo_text.grid(row=self.row, column=0, sticky=W)

        self.tempo_input = Entry(self.frame)
        self.tempo_input.grid(row=self.row,column=1, stick=E)

        self.row +=1

        self.tracks_text = Label(self.frame, text='# of Tracks:')
        self.tracks_text.grid(row=self.row, column=0, sticky=W)

        self.tracks_input = Entry(self.frame)
        self.tracks_input.grid(row=self.row,column=1, stick=E)

        self.row +=1

        self.tracks_text = Label(self.frame, text='# of Channels:')
        self.tracks_text.grid(row=self.row, column=0, sticky=W)

        self.channels_input = Entry(self.frame)
        self.channels_input.grid(row=self.row,column=1, stick=E)

        self.row += 1

        self.key_text = Label(self.frame, text='Key:')
        self.key_text.grid(row=self.row, column=0, sticky=W)

        self.key_var = StringVar(self.master)
        self.key_var.set(key_list[0].name)
        self.key_input = OptionMenu(self.frame, self.key_var, *[key.name for key in key_list])
        self.key_input.grid(row=self.row,column=1, stick=E)

        self.row +=1

        self.complete_button = Button(self.frame, text='Done', command=self.close)
        self.complete_button.grid(row=self.row, columnspan=2)

    def close(self):
        print('Number of tracks: ' + str(self.tracks_input.get()))
        self.tempo = self.tempo_input.get()
        self.num_tracks = self.tracks_input.get()
        self.channels_per_track = self.channels_input.get()
        self.key = key_dic[self.key_var.get()]
        self.master.destroy()
