from MidiFile3 import MIDIFile
from PianoUtilities import *
from random import *

class Song:

    def __init__(self, tempo, key, num_measures, instruments, singers, volumes):
        self.num_tracks = len(instruments)
        self.MyMIDI = MIDIFile(self.num_tracks)
        self.MyMIDI.addTempo(track=0, tempo=tempo, time=0)
        self.triads = self.create_triad_sequence(num_measures, key)
        self.instruments = instruments
        self.singers = singers
        self.volumes = volumes
        self.notes_for_track = []

        for x in range(self.num_tracks):
            self.add_track(x, self.instruments[x])
            self.singers[x].track = x
            self.singers[x].channel = x
            self.notes_for_track.append([])

        self.time = 0

        self.build_song()

    def add_track(self, track, input_instrument):
        self.MyMIDI.addTrackName(track, 0, str(self.singers[track]) + ', Volume: ' + str(self.volumes[track]))
        self.MyMIDI.addProgramChange(track=track, channel=track, time=0, program=input_instrument)

    def add_single_note(self, pitch, duration, track):
        if pitch >= 0:
            self.MyMIDI.addNote(track=track, channel=track, pitch=pitch, time=self.time, duration=duration, volume=self.volumes[track])

    def set_instrument(self, track, instrument_text):
        self.MyMIDI.addProgramChange(track, track, 0, instrument_dic[instrument_text])

    def create_triad_sequence(self, num_triads, key):
        triads = []
        for x in range(num_triads-1):
            start_note = key.notes_in_key[randint(0,7)]
            triads.append(triad(key, start_note))
        triads.append(triad(key, key.notes_in_key[0]))
        return triads

    def return_next_pitch(self, input_singer, input_triad):
        possible_notes = []
        for note in input_triad:
            note_choices = input_singer.octave_notes_in_range(note)
            for note in note_choices:
                possible_notes.append(note)
        if len(self.notes_for_track[input_singer.track]) > 0:
            previous = self.notes_for_track[input_singer.track][len(self.notes_for_track[input_singer.track])-1]
            jumps = []
            steps = []
            for note in possible_notes:
                difference = abs(note-previous)
                if difference < 5:
                    steps.append(note)
                elif difference <= 12:
                    jumps.append(note)
            jump_or_step = randint(0,9)
            if len(jumps) == 0:
                return get_biased_random_note(steps)
            if len(steps) == 0:
                return get_biased_random_note(jumps)
            if jump_or_step <= 1:
                return get_biased_random_note(jumps)
            else:
                return get_biased_random_note(steps)
        else:
            pick_any = randint(0,len(possible_notes)-1)
            return possible_notes[pick_any]

    def build_song(self):
        for triad in self.triads:
            for singer in self.singers:
                self.build_measure(singer, triad, self.time)
            self.time += 4

    def build_measure(self, singer, input_triad, time):
            orig_time = deepcopy(time)

            if singer.name == 'Bass':
                duration_options = [1,2]

            elif singer.name == 'Tenor':
                duration_options = [1,2]

            elif singer.name == 'Alto':
                random = randint(0,100)
                if 0 <= random <= 25:
                    duration_options = [.25,.5,1]
                elif 25 < random <= 75:
                    duration_options = [.5,1]
                elif 75 < random:
                    duration_options = [.25,1]

            elif singer.name == 'Soprano':
                random = randint(0,100)
                if 0 <= random <= 25:
                    duration_options = [.25,.5,1]
                elif 25 < random <= 75:
                    duration_options = [.5,1]
                elif 75 < random:
                    duration_options = [.25,1]


            while time < orig_time + 4:
                temp_options = [duration for duration in duration_options if duration <= (orig_time+4)-time]
                duration = temp_options[randint(0,len(temp_options)-1)]
                if duration == .25:
                    self.build_beat(input_triad, time, singer, duration)
                    time += .25
                    self.build_beat(input_triad, time, singer, duration)
                    time += .25
                else:
                    self.build_beat(input_triad, time, singer, duration)
                    time += duration


    def build_beat(self, input_triad, time, singer, duration=1):
        pitch = self.return_next_pitch(singer, input_triad)
        self.notes_for_track[singer.track].append(pitch)
        self.MyMIDI.addNote(singer.track, singer.track, pitch, time, duration, 100)

    def build_x_sixteenths(self, num_sixteenths, input_triad, time, singer):
        for x in range(num_sixteenths):
            pitch = self.return_next_pitch(singer, input_triad)
            self.MyMIDI.addNote(singer.track, singer.track, pitch, time, .25, 100)
            self.notes_for_track[singer.track].append(pitch)
            time += .25

    def set_instrument(self, track, channel, instrument_text):
        self.MyMIDI.addProgramChange(track, channel, 0, instrument_dic[instrument_text])

    def write_to_disk(self, output_name):
        binfile = open(output_name + '.mid', 'wb')
        self.MyMIDI.writeFile(binfile)
        binfile.close()
        print("Written to file with name: '{}'!".format(output_name + '.mid'))
