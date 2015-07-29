from SongBuilder import *
from PianoUtilities import *
from GUI import *
from tkinter import *

new_chooser = MusicChooser()
new_chooser.start()

my_song = Song(2, tempo=new_chooser.tempo, input_instrument='piano')
my_song.add_channel(track=0, input_instrument='piano')
my_song.add_random_triads(track_and_channels=[(0,0), (0,1), (1,0)],
                          num_triads=100,
                          key=new_chooser.key)
#my_song.add_random_triads(1, 0, 100, Major_Pentatonic, cs1)
my_song.write_to_disk()