from tkinter import *

from PianoUtilities import *


class custom_list():

    def __init__(self):
        self.list = [[None]]

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
                self.list.append([None])
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
                self.list.append([None])
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

        self.track_and_settings = []

        self.add_initial_elements()

    def start(self):
        self.master.mainloop()

    def add_initial_elements(self):
        self.tempo_title = Label(self.frame, text='Tempo:')
        self.tempo_input = Scale(self.frame, from_=0, to=300, orient=HORIZONTAL)
        self.tempo_input.set(120)
        self.grid.add_pair_of_widgets(self.tempo_title, self.tempo_input)

        self.key_text = Label(self.frame, text='Key:')
        self.key_var = StringVar(self.master)
        self.key_var.set(key_list[0].name)
        self.key_input = OptionMenu(self.frame, self.key_var, *[key.name for key in key_list])
        self.grid.add_pair_of_widgets(self.key_text,self.key_input)

        self.measures_text = Label(self.frame, text='# of Measures:')
        self.measures_input = Scale(self.frame, from_=1, to=100, orient=HORIZONTAL)
        self.measures_input.set(50)
        self.grid.add_pair_of_widgets(self.measures_text, self.measures_input)

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
        for track in self.track_and_settings:
            for widget in track[1:len(track)]:
                self.grid.remove_item(widget)
                if type(widget) != StringVar:
                    widget.destroy()
            for widget in track[0]:
                self.grid.remove_item(widget)
                widget.destroy()

        self.rebuild_grid()

        self.track_and_settings = []

        for i in range(int(self.tracks_var.get())):
            track_name_label = Label(self.frame, text = 'Track {}:'.format(str(i+1)))
            self.grid.add_with_column(0, track_name_label)

            instrument_text = Label(self.frame, text='Instrument:')
            instrument_var = StringVar()
            instrument_var.set('piano')
            instrument_picker = OptionMenu(self.frame, instrument_var, *[instrument[0] for instrument in instrument_list[0:10]])

            vocal_text = Label(self.frame, text='Vocal Range:')
            vocal_var = StringVar()
            vocal_var.set('Soprano')
            vocal_picker = OptionMenu(self.frame, vocal_var, *[vocal[0] for vocal in singer_list])

            self.grid.add_pair_of_widgets(instrument_text, instrument_picker, 1, 2)
            self.grid.add_pair_of_widgets(vocal_text, vocal_picker, 1, 2)
            self.track_and_settings.append([[], track_name_label, instrument_text, instrument_var, instrument_picker, vocal_text, vocal_var, vocal_picker])

        self.rebuild_grid()



    def close(self):
        self.tempo = int(self.tempo_input.get())
        self.key = key_dic[self.key_var.get()]
        self.num_measures = self.measures_input.get()
        self.num_tracks = self.tracks_var.get()
        self.instruments = [instrument_dic[track[3].get()] for track in self.track_and_settings]
        self.singers = [singer_dic[track[6].get()] for track in self.track_and_settings]
        self.master.destroy()

