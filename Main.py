from SongBuilder import *
from PianoUtilities import *
from GUI import *
from tkinter import *

new_chooser = MusicChooser()
new_chooser.start()

tempo = new_chooser.tempo
key = new_chooser.key
num_measures = new_chooser.num_measures
instruments = new_chooser.instruments
singers = new_chooser.singers
num_tracks = new_chooser.num_tracks

my_song = Song(tempo, key, num_measures, instruments, singers, num_tracks)
my_song.write_to_disk(new_chooser.file_name)

#my_song.add_random_triads(1, 0, 100, Major_Pentatonic, cs1)
#my_song.write_to_disk()

#print(new_chooser.track_data)