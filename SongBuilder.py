from MidiFile3 import MIDIFile
from PianoUtilities import *
from random import *

class Song:

    def __init__(self, num_tracks,  num_channels=2, tempo=120, input_instrument='piano'):
        self.MyMIDI = MIDIFile(num_tracks)
        self.MyMIDI.addTempo(track=0, tempo=tempo, time=0)
        self.triads = []

        self.channel_locations = []

        for x in range(num_tracks):
            self.add_track(x, input_instrument)

    def add_track(self, track, input_instrument='piano'):
        self.MyMIDI.addTrackName(track, 0, str(track))
        self.channel_locations.append([])
        self.add_channel(track, input_instrument)

    def add_channel(self, track, input_instrument='piano'):
        channel = len(self.channel_locations[track])
        self.channel_locations[track].append(0)
        self.MyMIDI.addProgramChange(track=track, channel=channel, time=0, program=instrument_dic[input_instrument])

    def add_single_note(self, pitch, duration, track, channel, volume=100):
        if pitch >= 0:
            self.MyMIDI.addNote(track=track, channel=channel, pitch=pitch, time=self.channel_locations[track][channel], duration=duration, volume=volume)
        self.channel_locations[track][channel] += duration

    def add_notes(self, notes, track, channel, volume=100):
        for note in notes:
            self.add_single_note(note)

    def add_single_chord(self, chord, length, track, channel, volume=100):
        for note in chord:
            if note >= 0:
                self.MyMIDI.addNote(track, channel, note, self.channel_locations[track][channel], length, volume)
        self.channel_locations[track][channel] += length

    def add_chords(self, chords, track, channel, volume=100):
        for chord in chords:
            self.add_single_chord(chord[0], chord[1], track, channel)

    def set_instrument(self, track, channel, instrument_text):
        self.MyMIDI.addProgramChange(track, channel, 0, instrument_dic[instrument_text])

    def write_to_disk(self):
        binfile = open("output.mid", 'wb')
        self.MyMIDI.writeFile(binfile)
        binfile.close()
        print("Written to file!")

    def add_random_triads(self, track_and_channels, num_triads, key):
        start_note = key.notes_in_key[0]
        displacement = 0
        for x in range(num_triads):
            length = [half,quarter,eighth, sixteenth].pop(randint(0,2))
            temp_triad = triad(key, start_note)
            start_index = temp_triad.index(start_note)
            displacements = [0 for item in track_and_channels]
            for x in range(len(track_and_channels)):
                displacements[x] += randint(-2,2)
                if displacements[x] > 6:
                    displacements[x] = 6
                elif displacements[x] < -6:
                    displacements[x] = -6
                note = temp_triad[start_index + displacements[x]]
                self.add_single_note(pitch=note, duration=length, track=track_and_channels[x][0], channel=track_and_channels[x][1])


    def set_instrument(self, track, channel, instrument_text):
        self.MyMIDI.addProgramChange(track, channel, 0, instrument_dic[instrument_text])

class Singer:

    def __init__(self, low_note, high_note, track, channel):
        self.low_note = low_note
        self.high_note = high_note
        self.vocal_range = high_note - low_note
        self.track = track
        self.channel = channel

    def octave_notes_in_range(self, input_pitch):
        possible_notes = []
        for x in range(self.vocal_range+1):
            pitch = x + self.low_note
            difference = pitch - input_pitch
            if difference % 12 == 0:
                possible_notes.append(pitch)
        return possible_notes

class Soprano(Singer):
    def __init__(self, low_note=60, high_note=81, track=0, channel=0):
        super(Soprano, self).__init__(low_note,high_note,track,channel)
class Alto(Singer):
    def __init__(self, low_note=55, high_note=77, track=0, channel=1):
        super(Soprano, self).__init__(low_note,high_note,track,channel)
class Tenor(Singer):
    def __init__(self, low_note=48, high_note=69, track=1, channel=0):
        super(Soprano, self).__init__(low_note,high_note,track,channel)
class Bass(Singer):
    def __init__(self, low_note=40, high_note=64, track=1, channel=1):
        super(Soprano, self).__init__(low_note,high_note,track,channel)

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

my_song = Song(2, tempo=240, input_instrument='piano')
my_song.add_channel(track=0, input_instrument='piano')
my_song.add_random_triads(track_and_channels=[(0,0), (0,1), (1,0)],
                          num_triads=100,
                          key=G_Major,
                          start_note=g3)
#my_song.add_random_triads(1, 0, 100, Major_Pentatonic, cs1)
my_song.write_to_disk()

print(A_Minor.notes_in_key)

print(triad(A_Minor, a3))'''
