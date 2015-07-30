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

        self.time = 0

        self.build_song()

    def add_track(self, track, input_instrument):
        self.MyMIDI.addTrackName(track, 0, str(track))
        self.MyMIDI.addProgramChange(track=track, channel=0, time=0, program=input_instrument)

    def add_single_note(self, pitch, duration, track, volume=100):
        if pitch >= 0:
            self.MyMIDI.addNote(track=track, channel=0, pitch=pitch, time=self.time, duration=duration, volume=volume)

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
            for x in range(len(self.singers)):
                note = randint(0,len(triad)-1)
                pitch = self.singers[x].octave_notes_in_range(triad[note])[0]
                if len(triad) > 1:
                    triad.pop(note)
                self.add_single_note(pitch,1,x)
            self.time += 1

    def set_instrument(self, track, channel, instrument_text):
        self.MyMIDI.addProgramChange(track, channel, 0, instrument_dic[instrument_text])

    def write_to_disk(self):
        binfile = open("output.mid", 'wb')
        self.MyMIDI.writeFile(binfile)
        binfile.close()
        print("Written to file!")
