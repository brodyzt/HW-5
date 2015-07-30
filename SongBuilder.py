from MidiFile3 import MIDIFile
from PianoUtilities import *
from random import *

class Song:

    def __init__(self, tempo, key, num_measures, instruments, singers):
        self.num_tracks = len(instruments)
        self.MyMIDI = MIDIFile(self.num_tracks)
        self.MyMIDI.addTempo(track=0, tempo=tempo, time=0)
        self.triads = self.create_triad_sequence(num_measures, key)
        self.instruments = instruments
        self.singers = singers

        for x in range(self.num_tracks):
            self.add_track(x, self.instruments[x])
            self.singers[x].track = x

        self.time = 0

        self.build_song()

    def add_track(self, track, input_instrument):
        self.MyMIDI.addTrackName(track, 0, str(self.singers[track]))
        self.MyMIDI.addProgramChange(track=track, channel=track, time=0, program=input_instrument)

    def add_single_note(self, pitch, duration, track, volume=100):
        if pitch >= 0:
            self.MyMIDI.addNote(track=track, channel=track, pitch=pitch, time=self.time, duration=duration, volume=volume)

    def set_instrument(self, track, channel, instrument_text):
        self.MyMIDI.addProgramChange(track, channel, 0, instrument_dic[instrument_text])

    def create_triad_sequence(self, num_triads, key):
        triads = []
        for x in range(num_triads):
            start_note = key.notes_in_key[randint(0,7)]
            triads.append(triad(key, start_note))
        return triads

    def build_song(self):
        for triad in self.triads:
            for singer in self.singers:
                self.build_measure(singer, triad, self.time)
            self.time += 4

    def build_measure(self, singer, input_triad, time):
            if singer.name in ['Soprano','Alto']:
                style = randint(1,2)
            else:
                style = randint(1,2)

            if style == 1:
                for x in range(4):
                    self.build_beat(input_triad, time, singer)
                    time += 1
            if style == 2:
                self.build_x_sixteenths(16,input_triad,time,singer)


    def build_beat(self, input_triad, time, singer):
        pitch = singer.octave_notes_in_range(input_triad[randint(0,2)])
        pitch = pitch[randint(0,len(pitch)-1)]
        self.MyMIDI.addNote(singer.track, singer.track, pitch, time, 1, 100)

    def build_x_sixteenths(self, num_sixteenths, input_triad, time, singer):
        for x in range(num_sixteenths):
            pitch = singer.octave_notes_in_range(input_triad[randint(0,2)])
            pitch = pitch[randint(0,len(pitch)-1)]
            self.MyMIDI.addNote(singer.track, singer.track, pitch, time, .25, 100)
            time += .25

    def set_instrument(self, track, channel, instrument_text):
        self.MyMIDI.addProgramChange(track, channel, 0, instrument_dic[instrument_text])

    def write_to_disk(self, output_name):
        binfile = open(output_name + '.mid', 'wb')
        self.MyMIDI.writeFile(binfile)
        binfile.close()
        print("Written to file with name: '{}'!".format(output_name + '.mid'))
