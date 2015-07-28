from MidiFile3 import MIDIFile
from PianoKeys import *

instrument = dict([('piano',0), ('harpsichord',6), ('glock',9), ('vibes',11),
                            ('marimba',12), ('organ',19), ('guitar',24), ('bass',32),
                            ('violin',40), ('cello',42), ('harp',46), ('timps',47),
                            ('voice',54), ('trumpet',56), ('tuba',58), ('horn',60),
                            ('alto sax', 65), ('oboe',68), ('bassoon',70), ('clarinet',71),
                            ('flute',73), ('recorder',74), ('bottle',75), ('whistle',78),
                            ('fifths',96), ('halo',94), ('goblins',101), ('koto',107),
                            ('bagpipe',109), ('taiko',116), ('toms',117), ('breath',121),
                            ('seashore',122), ('bird',123), ('phone',124), ('applause',126)])

class Song:

    def __init__(self, num_channels=2, tempo=120):
        self.MyMIDI = MIDIFile(1)

        self.channel_locations = []

        for channel in range(num_channels):
            self.MyMIDI.addTrackName(0, channel, str(channel))
            self.MyMIDI.addTempo(0, channel, tempo)
            self.channel_locations.append(0)
            self.MyMIDI.addProgramChange(0, channel, 0, instrument['piano'])

    def add_notes(self, notes, track, volume=100):
        for note in notes:
            if note[0] >= 0:
                self.MyMIDI.addNote(0, track, note[0], self.channel_locations[track], note[1], volume)

            self.channel_locations[track] += note[1]

    def set_instrument(self, channel, instrument_text):
        self.MyMIDI.addProgramChange(0, channel, 0, instrument[instrument_text])

    def write_to_disk(self):
        binfile = open("output.mid", 'wb')
        self.MyMIDI.writeFile(binfile)
        binfile.close()
        print("Written to file!")

'''
my_song = Song(tempo=128)

my_song.add_notes([(rest, eighth),
                   (c3, eighth),
                   (g3, quarter),
                   (ef3, quarter),
                   (c3, quarter),
                   (rest, eighth),

                   (c3, eighth),
                   (g3, quarter),
                   (ef3, quarter),
                   (c3, quarter),
                   (rest, eighth),

                   (c3, eighth),
                   (g3, 2/3),
                   (f3, 2/3),
                   (ef3, 2/3),
                   (bf2, quarter),
                   (rest, eighth),

                   (bf2, eighth),
                   (g3, quarter),
                   (ef3, quarter),
                   (f3, quarter)], 0)
my_song.write_to_disk()
'''

print(notes_in_key(B_Minor, 1))