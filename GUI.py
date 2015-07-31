from tkinter import *
from random import *
from PianoUtilities import *

class Preset:

    @staticmethod
    def load():
        file = open('Presets', 'r')
        contents = file.readlines()
        contents.pop(0)
        contents = [line.replace('\n','').split(',') for line in contents]
        file.close()
        return dict([(preset[0],preset) for preset in contents])

    @staticmethod
    def add_preset(preset):
        file = open('Presets', 'r')
        contents = file.readlines()
        file.close()

        file = open('Presets', 'w')
        for line in contents:
            file.write(line)

        temp_str = ''
        for item in preset:
            temp_str = temp_str + str(item) + ','
        file.write(temp_str[0:len(temp_str)-1] + '\n')

        file.close()

    @staticmethod
    def remove_preset(preset_name):
        new_file_contents = []
        file = open('Presets', 'r')
        contents = file.readlines()
        file.close()

        new_file_contents.append(contents[0])

        for line in contents[1:len(contents)]:
            if preset_name != line.split(',')[0]:
                new_file_contents.append(line)

        file = open('Presets', 'w')
        file.writelines(new_file_contents)


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

    def add_list_of_widgets(self, input_list, columns=None):
        if not columns:
            columns = [num for num in range(len(input_list))]
        length = len(self)
        for x in range(len(input_list)):
            self.insert_at_row_column(length, columns[x], input_list[x])

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
        presets_data = Preset.load()
        self.presets_label = Label(self.frame, text='Presets:')
        self.presets_var = StringVar()
        self.preset_keys = presets_data.keys()
        if len(self.preset_keys) > 0:
            self.presets_var.set(list(self.preset_keys)[0])
        else:
            self.preset_keys = ['']
        self.presets_picker = OptionMenu(self.frame, self.presets_var, *self.preset_keys)
        self.add_preset_button = Button(self.frame, text='Add Preset', command=self.ask_preset_name)
        self.delete_preset_button = Button(self.frame, text='Delete Preset', command=self.delete_preset)
        self.load_preset_button = Button(self.frame, text='Load Preset', command=self.load_preset)
        self.update_preset_button = Button(self.frame, text='Replace Preset', command=self.update_preset)
        self.grid.add_list_of_widgets([self.presets_label, self.presets_picker, self.load_preset_button, self.delete_preset_button])
        self.grid.add_list_of_widgets([self.update_preset_button, self.add_preset_button],[2,3])

        self.file_name_label = Label(self.frame, text='File Name:')
        self.file_name_input = Entry(self.frame)
        self.file_name_input.insert(0, 'output {}'.format(randint(0,1000)))
        self.grid.add_pair_of_widgets(self.file_name_label, self.file_name_input)

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
        self.tracks_input = OptionMenu(self.frame, self.tracks_var, *[str(num+1) for num in range(7)])
        self.grid.add_pair_of_widgets(self.tracks_text,self.tracks_input)

        self.complete_button = Button(self.frame, text='Build Song', command=self.close)

        self.rebuild_grid()
        self.add_track_settings()

    def load_preset(self):
        preset = Preset.load()[self.presets_var.get()]
        self.tempo_input.set(preset[1])
        self.key_var.set(preset[2])
        self.measures_input.set(preset[3])
        self.tracks_var.set(preset[4])
        self.add_track_settings()
        for x in range(len(self.track_and_settings)):
            self.track_and_settings[x][3].set(preset[5+3*x])
            self.track_and_settings[x][6].set(preset[6+3*x])
            self.track_and_settings[x][9].set(preset[7+3*x])

    def delete_preset(self):
        Preset.remove_preset(self.presets_var.get())
        self.preset_keys = Preset.load().keys()
        if len(list(self.preset_keys)) > 0:
            self.presets_var.set(list(self.preset_keys)[0])
            self.presets_picker.__init__(self.frame, self.presets_var, *self.preset_keys)
        else:
            self.presets_var.__init__(self.frame, '')
            self.presets_picker.__init__(self.frame, self.presets_var, '')
        self.grid.insert_at_row_column(0,2,self.presets_picker)

        self.rebuild_grid()

    def update_preset(self):
        temp_name = self.presets_var.get()
        self.delete_preset()

        preset = [temp_name, self.tempo_input.get(), self.key_var.get(), self.measures_input.get(), self.tracks_var.get()]
        for x in range(len(self.track_and_settings)):
            preset.extend([self.track_and_settings[x][3].get(), self.track_and_settings[x][6].get(), self.track_and_settings[x][9].get()])
        Preset.add_preset(preset)
        self.preset_keys = Preset.load().keys()
        self.presets_var.set(list(self.preset_keys)[0])
        self.presets_picker.__init__(self.frame, self.presets_var, *self.preset_keys)
        self.grid.insert_at_row_column(0,2,self.presets_picker)

        self.rebuild_grid()

    def ask_preset_name(self):
        self.preset_name_window = Toplevel()
        self.preset_name_text = Label(self.preset_name_window, text='Preset Name:')
        self.preset_name_text.grid(row=0, column=0)
        self.preset_name_input = Entry(self.preset_name_window)
        self.preset_name_input.insert(0, 'Preset Name')
        self.preset_name_input.grid(row=0, column=1)
        self.save_button = Button(self.preset_name_window, text='Save Preset', command=self.save_preset)
        self.save_button.grid(row=1,columnspan=2)

    def save_preset(self):
        preset = [self.preset_name_input.get(), self.tempo_input.get(), self.key_var.get(), self.measures_input.get(), self.tracks_var.get()]
        for x in range(len(self.track_and_settings)):
            preset.extend([self.track_and_settings[x][3].get(), self.track_and_settings[x][6].get(), self.track_and_settings[x][9].get()])
        Preset.add_preset(preset)
        self.preset_keys = Preset.load().keys()
        self.presets_var.set(list(self.preset_keys)[0])
        self.presets_picker.__init__(self.frame, self.presets_var, *self.preset_keys)
        self.grid.insert_at_row_column(0,2,self.presets_picker)

        self.rebuild_grid()

        self.preset_name_text.destroy()
        self.preset_name_input.destroy()
        self.save_button.destroy()
        self.preset_name_window.destroy()

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
        previous_length = len(self.track_and_settings)
        new_length = int(self.tracks_var.get())
        if new_length < previous_length and previous_length != 0:
            for x in range(previous_length-1,new_length-1, -1): #self.track_and_settings[new_length-1:previous_length-1]:
                for widget in self.track_and_settings[x][1:len(self.track_and_settings[x])]:
                    self.grid.remove_item(widget)
                    if type(widget) != StringVar:
                        widget.destroy()
                for widget in self.track_and_settings[x][0]:
                    self.grid.remove_item(widget)
                    widget.destroy()
                self.track_and_settings.pop(x)
        elif new_length > previous_length:
            for i in range(new_length-previous_length):
                track_name_label = Label(self.frame, text = 'Track {}:'.format(str(i+previous_length+1)))
                self.grid.add_with_column(0, track_name_label)

                instrument_text = Label(self.frame, text='Instrument:')
                instrument_var = StringVar()
                instrument_var.set(instrument_list[0][0])
                instrument_picker = OptionMenu(self.frame, instrument_var, *[instrument[0] for instrument in instrument_list])

                vocal_text = Label(self.frame, text='Vocal Range:')
                vocal_var = StringVar()
                vocal_var.set('Soprano')
                vocal_picker = OptionMenu(self.frame, vocal_var, *[vocal[0] for vocal in singer_list])

                volume_label = Label(self.frame, text='Volume:')
                volume_input = Scale(self.frame, from_=0, to=100, orient=HORIZONTAL)
                volume_input.set(100)

                self.grid.add_pair_of_widgets(instrument_text, instrument_picker, 1, 2)
                self.grid.add_pair_of_widgets(vocal_text, vocal_picker, 1, 2)
                self.grid.add_pair_of_widgets(volume_label, volume_input, 1, 2)
                self.track_and_settings.append([[], track_name_label, instrument_text, instrument_var, instrument_picker, vocal_text, vocal_var, vocal_picker, volume_label, volume_input])

        self.rebuild_grid()

    def close(self):
        self.file_name = self.file_name_input.get()
        self.tempo = int(self.tempo_input.get())
        self.key = key_dic[self.key_var.get()]
        self.num_measures = self.measures_input.get()
        self.num_tracks = self.tracks_var.get()
        self.instruments = [instrument_dic[track[3].get()] for track in self.track_and_settings]
        self.singers = [deepcopy(singer_dic[track[6].get()]) for track in self.track_and_settings]
        self.volumes = [track[9].get() for track in self.track_and_settings]
        self.master.destroy()

