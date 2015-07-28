from MidiFile3 import MIDIFile
from Piano_Utilities import *
from random import *

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

    def __init__(self, num_tracks,  num_channels=2, tempo=120):
        self.MyMIDI = MIDIFile(num_tracks)
        self.MyMIDI.addTempo(track=0, tempo=tempo, time=0)

        self.channel_locations = []

        for x in range(num_tracks):
            self.add_track(x)

    def add_track(self, track):
        self.MyMIDI.addTrackName(track, 0, str(track))
        self.channel_locations.append([])
        self.add_channel(track)

    def add_channel(self, track):
        channel = len(self.channel_locations[track])
        self.channel_locations[track].append(0)
        self.MyMIDI.addProgramChange(track=track, channel=channel, time=0, program=instrument['piano'])

    def add_notes(self, notes, track, channel, volume=100):
        for note in notes:
            if note[0] >= 0:
                self.MyMIDI.addNote(track, channel, pitch=note[0], time=self.channel_locations[track][channel], duration=note[1], volume=volume)
            self.channel_locations[track][channel] += note[1]

    def add_single_chord(self, chord, length, track, channel, volume=100):
        for note in chord:
            if note >= 0:
                self.MyMIDI.addNote(track, channel, note, self.channel_locations[track][channel], length, volume)
        self.channel_locations[track][channel] += length

    def add_chords(self, chords, track, channel, volume=100):
        for chord in chords:
            self.add_single_chord(chord[0], chord[1], track, channel)

    def set_instrument(self, track, channel, instrument_text):
        self.MyMIDI.addProgramChange(track, channel, 0, instrument[instrument_text])

    def write_to_disk(self):
        binfile = open("output.mid", 'wb')
        self.MyMIDI.writeFile(binfile)
        binfile.close()
        print("Written to file!")

    def add_random_triads(self, track, channel, num_triads, key, start_note):
        displacement = 0
        for x in range(num_triads):
            displacement += randint(-2,2)
            if displacement < -10:
                displacement = -10
            elif displacement > 10:
                displacement = 10
            length = [full,half,quarter,eighth].pop(randint(0,3))
            self.add_single_chord(chord=triad(key, n_notes_away(key, start_note, displacement)), length=length, track=track, channel=channel)

    def set_instrument(self, track, channel, instrument_text):
        self.MyMIDI.addProgramChange(track, channel, 0, instrument[instrument_text])

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

my_song = Song(2, tempo=120)
my_song.add_random_triads(0, 0, 100, Major_Pentatonic, cs3)
my_song.add_random_triads(1, 0, 100, Major_Pentatonic, cs1)
my_song.set_instrument(0,0,'trumpet')
my_song.write_to_disk()
