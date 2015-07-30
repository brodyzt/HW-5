from tkinter import *

from PianoUtilities import *


class custom_list():

    def __init__(self):
        self.list = [[]]

    def __str__(self):
        return str(self.list)

    def __len__(self):
        return len(self.list)

    def insert_at_row_column(self, row, column, object):
        if row <= len(self.list) - 1:
            if column <= len(self.list[row]):
                self.list[row].insert(column, object)
            else:
                while len(self.list[row]) < column:
                    self.list[row].append(None)
                self.list[row].insert(column, object)
        else:
            while len(self.list) - 1 < row:
                self.list.append([])
            if column <= len(self.list[row]):
                self.list[row].insert(column, object)
            else:
                while len(self.list[row]) < column:
                    self.list[row].append(None)
                self.list[row].insert(column, object)

    def insert_own_row(self, row, column, object):
        if row <= len(self.list) - 1:
            self.list.insert(row, [])
            if column <= len(self.list[row]):
                self.list[row].insert(column, object)
            else:
                while len(self.list[row]) < column:
                    self.list[row].append(None)
                self.list[row].insert(column, object)
        else:
            while len(self.list) - 1 < row:
                self.list.append([])
            self.list.insert(row, [])
            if column <= len(self.list[row]):
                self.list[row].insert(column, object)
            else:
                while len(self.list[row]) < column:
                    self.list[row].append(None)
                self.list[row].insert(column, object)

    def add_with_column(self, column, object):
        self.insert_at_row_column(len(self), column, object)

    def add_pair_of_widgets(self, widget1, widget2, column1=0, column2=1):
        length = len(self)
        self.insert_at_row_column(length, column1, widget1)
        self.insert_at_row_column(length, column2, widget2)

    def remove_item(self, item):
        for row in range(len(self.list)):
            for column in range(len(self.list[row])):
                if self.list[row][column] == item:
                    self.list[row].pop(column)
                    return None

    def widget_coordinates(self, widget):
        for row in range(len(self.list)):
            for column in range(len(self.list[row])):
                if self.list[row][column] == widget:
                    return (row, column)

    def widget_row(self, widget):
        return self.widget_coordinates(widget)[0]

    def widget_column(self, widget):
        return self.widget_coordinates(widget)[1]

class MusicChooser:

    def __init__(self):
        root = Tk()
        self.master = root
        self.frame = Frame(self.master)
        self.frame.pack()
        self.grid = custom_list()

        self.track_and_channel_widgets = []

        self.add_initial_elements()

    def start(self):
        self.master.mainloop()

    def add_initial_elements(self):
        self.tempo_text = Label(self.frame, text='Tempo:')
        self.tempo_input = Entry(self.frame)
        self.grid.add_pair_of_widgets(self.tempo_text, self.tempo_input)

        self.key_text = Label(self.frame, text='Key:')
        self.key_var = StringVar(self.master)
        self.key_var.set(key_list[0].name)
        self.key_input = OptionMenu(self.frame, self.key_var, *[key.name for key in key_list])
        self.grid.add_pair_of_widgets(self.key_text,self.key_input)

        self.tracks_var = StringVar(self.master)
        self.tracks_var.set('1')
        self.tracks_var.trace('w', self.add_track_settings)
        self.tracks_text = Label(self.frame, text='# of Tracks:')
        self.tracks_input = OptionMenu(self.frame, self.tracks_var, *[str(num+1) for num in range(5)])
        self.grid.add_pair_of_widgets(self.tracks_text,self.tracks_input)

        self.complete_button = Button(self.frame, text='Done', command=self.close)

        self.rebuild_grid()
        self.add_track_settings()

    def rebuild_grid(self):
        for row in range(len(self.grid.list)):
            for column in range(len(self.grid.list[row])):
                if self.grid.list[row][column]:
                    if column == 0:
                        self.grid.list[row][column].grid(row=row, column=column, sticky=W)
                    elif column == len(self.grid.list[row])-1:
                        self.grid.list[row][column].grid(row=row, column=column, sticky=E)
                    else:
                        self.grid.list[row][column].grid(row=row, column=column)
        self.complete_button.grid(row=len(self.grid),columnspan=2)

    def add_track_settings(self, *args):
        for widget in self.track_and_channel_widgets:
            widget.destroy()
            self.grid.remove_item(widget)
        for i in range(int(self.tracks_var.get())):
            track_name = Label(self.frame, text = 'Track {}:'.format(str(i+1)))
            self.grid.add_with_column(0, track_name)
            channels_text = Label(self.frame, text='# of Channels:')
            channels_var = StringVar(self.master)
            channels_var.set('1')
            channels_var.row=len(self.grid)
            channels_var.trace_variable('w', self.add_channel_settings)
            channels_input = OptionMenu(self.frame, channels_var, *[str(num+1) for num in range(2)])
            self.grid.add_pair_of_widgets(channels_text, channels_input, 1, 2)
            self.track_and_channel_widgets.append([track_name, channels_text, channels_input,channels_var])

        self.rebuild_grid()
        self.add_channel_settings()

    def add_channel_settings(self, *args):
        for track in self.track_and_channel_widgets:
            if len(track) != 5:
                track.append([])
            else:
                for widget in track[4]:
                    widget.destroy()
                    self.grid.remove_item(widget)
                track[4] = []
            for channel in range(int(track[3].get())):
                channel_text = Label(self.frame, text='Channel {} Settings:'.format(channel+1))
                track[4].append(channel_text)
                self.grid.insert_own_row(self.grid.widget_row(track[1])+1+channel,2, channel_text)
        self.rebuild_grid()


    def close(self):
        print('Number of tracks: ' + str(self.tracks_input.get()))
        self.tempo = int(self.tempo_input.get())
        self.num_tracks = self.tracks_input.get()
        self.channels_per_track = [int(track[2].get()) for track in self.track_settings]
        self.key = key_dic[self.key_var.get()]
        self.master.destroy()
