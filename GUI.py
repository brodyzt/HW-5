from tkinter import *
from random import *
from copy import *
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
        self.randomize_button = Button(self.frame, text='Randomize Settings (Might Sound Terrrrrible)', command=self.randomize_settings)
        self.grid.add_with_column(1, self.randomize_button)

        presets_data = Preset.load()
        self.presets_label = Label(self.frame, text='Presets:')
        self.presets_var = StringVar()
        self.preset_keys = presets_data.keys()
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
        self.measures_input = Scale(self.frame, from_=1, to=200, orient=HORIZONTAL, resolution=4)
        self.measures_input.set(100)
        self.grid.add_pair_of_widgets(self.measures_text, self.measures_input)

        self.tracks_var = StringVar(self.master)
        self.tracks_var.set('1')
        self.tracks_var.trace('w', self.add_track_settings)
        self.tracks_text = Label(self.frame, text='# of Tracks:')
        self.tracks_input = OptionMenu(self.frame, self.tracks_var, *[str(num+1) for num in range(6)])
        self.grid.add_pair_of_widgets(self.tracks_text,self.tracks_input)

        self.chorus_label = Label(self.frame, text='Chorus:')
        self.verse_label = Label(self.frame, text='Verse:')
        self.bridge_label = Label(self.frame, text='Bridge:')

        self.grid.add_list_of_widgets([self.chorus_label, self.verse_label, self.bridge_label],[2,3,4])

        self.complete_button = Button(self.frame, text='Build Song', command=self.close)

        self.rebuild_grid()
        self.add_track_settings()

    def randomize_settings(self):
        self.tempo_input.set(randint(50,200))
        self.key_var.set([key.name for key in key_list][randint(0,len(key_list)-1)])
        self.measures_input.set(randint(1,200))
        self.tracks_var.set(str(randint(1,6)))
        self.add_track_settings()
        for y in range(3):
            instrument_set = random_instrument_set()
            for track in self.track_and_settings:
                track[0][y][0].set(instrument_set[randint(0,len(instrument_set)-1)])
                track[0][y][2].set([vocal[0] for vocal in singer_list][randint(0,len(singer_list)-1)])
                track[0][y][4].set(randint(50,100))

    def load_preset(self):
        preset = Preset.load()[self.presets_var.get()]
        self.tempo_input.set(preset[1])
        self.key_var.set(preset[2])
        self.measures_input.set(preset[3])
        self.tracks_var.set(preset[4])
        self.add_track_settings()
        for x in range(len(self.track_and_settings)):
            for y in range(3):
                self.track_and_settings[x][0][y][0].set(preset[5+9*x+3*y])
                self.track_and_settings[x][0][y][2].set(preset[5+9*x+3*y+1])
                self.track_and_settings[x][0][y][4].set(preset[5+9*x+3*y+2])

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
            for y in range(3):
                preset.extend([self.track_and_settings[x][0][y][0].get(), self.track_and_settings[x][0][y][2].get(), self.track_and_settings[x][0][y][4].get()])
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
            for y in range(3):
                preset.extend([self.track_and_settings[x][0][y][0].get(), self.track_and_settings[x][0][y][2].get(), self.track_and_settings[x][0][y][4].get()])
        Preset.add_preset(preset)
        self.preset_keys = Preset.load().keys()
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
                    else:
                        self.grid.list[row][column].grid(row=row, column=column)
        self.complete_button.grid(row=len(self.grid),columnspan=2)

    def add_track_settings(self, *args):
        previous_length = len(self.track_and_settings)
        new_length = int(self.tracks_var.get())
        if new_length < previous_length and previous_length != 0:
            for x in range(previous_length-1,new_length-1, -1):
                for y in range(1,len(self.track_and_settings[x])):
                    self.grid.remove_item(self.track_and_settings[x][y])
                    self.track_and_settings[x][y].destroy()

                for widget_set in self.track_and_settings[x][0]:
                    for widget in widget_set:
                        self.grid.remove_item(widget)
                        if type(widget) != StringVar:
                            widget.destroy()

                self.track_and_settings.pop()
        elif new_length > previous_length:
            for i in range(new_length-previous_length):
                track_name_label = Label(self.frame, text = 'Track {}:'.format(str(i+previous_length+1)))
                self.grid.add_with_column(0, track_name_label)

                instrument_text = Label(self.frame, text='Instrument:')
                vocal_text = Label(self.frame, text='Vocal Range:')
                volume_label = Label(self.frame, text='Volume:')

                current_track = [[], track_name_label, instrument_text, vocal_text, volume_label]
                for x in range(3):
                    instrument_var = StringVar()
                    instrument_var.set(instrument_list[0][0])
                    instrument_picker = OptionMenu(self.frame, instrument_var, *[instrument[0] for instrument in instrument_list])

                    vocal_var = StringVar()
                    vocal_var.set('Soprano')
                    vocal_picker = OptionMenu(self.frame, vocal_var, *[vocal[0] for vocal in singer_list])

                    volume_input = Scale(self.frame, from_=0, to=100, orient=HORIZONTAL)
                    volume_input.set(100)

                    current_track[0].append([instrument_var, instrument_picker, vocal_var, vocal_picker, volume_input])

                instrument_widgets = [instrument_text]
                instrument_widgets.extend([current_track[0][x][1] for x in range(3)])
                self.grid.add_list_of_widgets(instrument_widgets,[1,2,3,4])

                vocal_widgets = [vocal_text]
                vocal_widgets.extend([current_track[0][x][3] for x in range(3)])
                self.grid.add_list_of_widgets(vocal_widgets,[1,2,3,4])

                volume_widgets = [volume_label]
                volume_widgets.extend([current_track[0][x][4] for x in range(3)])
                self.grid.add_list_of_widgets(volume_widgets,[1,2,3,4])

                self.track_and_settings.append(current_track)

        self.rebuild_grid()

    def close(self):
        self.file_name = self.file_name_input.get()
        self.tempo = int(self.tempo_input.get())
        self.key = key_dic[self.key_var.get()]
        self.num_measures = self.measures_input.get()
        self.num_tracks = int(self.tracks_var.get())*3
        vars = [track[0] for track in self.track_and_settings]
        self.instruments = [[instrument_dic[set[0][0].get()],instrument_dic[set[1][0].get()],instrument_dic[set[2][0].get()]] for set in vars]
        self.singers = [[deepcopy(singer_dic[set[0][2].get()]),deepcopy(singer_dic[set[1][2].get()]),deepcopy(singer_dic[set[2][2].get()])] for set in vars]
        volumes = [[set[0][4].get(),set[1][4].get(),set[2][4].get()] for set in vars]
        for x in range(len(self.singers)):
            for y in range(len(self.singers[x])):
                self.singers[x][y].volume = volumes[x][y]
                self.singers[x][y].instrument = self.instruments[x][y]
        self.master.destroy()

