from MidiFile3 import MIDIFile
from PianoUtilities import *
from random import *
from copy import *

class Song:

    def __init__(self, tempo, key, num_measures, instruments, singers, num_tracks):
        self.num_tracks = num_tracks
        self.num_measures = num_measures
        self.MyMIDI = MIDIFile(self.num_tracks + 1)
        self.instruments = instruments
        self.singers = singers
        self.key = key
        self.time = 0

        self.sections = [] # stores the order of song sections. E.g. Chorus, Verse, Bridge

        self.MyMIDI.addTempo(track=0, tempo=tempo, time=0)
        self.triads = self.create_triad_sequence(num_measures, key)
        self.notes_for_track = [[]] # creates the list of notes for each track

        # sets the unique track and channel number for each singer
        for x in range(self.num_tracks//3):
            for singer_index in range(len(self.singers[x])):
                if self.num_tracks//3*singer_index + x >= 9: # skips over track 10, which is reserved for percussion instruments only
                    self.singers[x][singer_index].track = self.num_tracks//3*singer_index + x + 1
                    self.singers[x][singer_index].channel = self.num_tracks//3*singer_index + x + 1
                else:
                    self.singers[x][singer_index].track = self.num_tracks//3*singer_index + x
                    self.singers[x][singer_index].channel = self.num_tracks//3*singer_index + x

        # creates the tracks for each singer
        for singer in [row[0] for row in self.singers]:
            self.add_track(singer)
        for singer in [row[1] for row in self.singers]:
            self.add_track(singer)
        for singer in [row[2] for row in self.singers]:
            self.add_track(singer)

        self.build_song()

    def add_track(self, singer):
        self.MyMIDI.addTrackName(singer.track, 0, singer.name + ', Volume:' + str(singer.volume))
        self.MyMIDI.addProgramChange(track=singer.track, channel=singer.channel, time=0, program=singer.instrument)
        self.notes_for_track.append([]) # adds a sublist for the note sequence of the new track

    def add_single_note(self, singer, pitch, duration):
        if pitch >= 0:
            self.MyMIDI.addNote(track=singer.track, channel=singer.track, pitch=pitch, time=self.time, duration=duration, volume=singer.volume)

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
            note_choices = input_singer.octave_notes_in_range(note) # returns all the octaves of the input_not within the given singer's vocal range
            for note in note_choices:
                possible_notes.append(note) # adds notes in the vocal range to the possible_notes list
        if len(self.notes_for_track[input_singer.track]) > 0: # if it's not the singer's first note
            previous = self.notes_for_track[input_singer.track][len(self.notes_for_track[input_singer.track])-1] # gets the last note the singer sang
            jumps = []
            steps = []
            for note in possible_notes:
                difference = abs(note-previous)
                if difference < 5: # if the new note isn't too far from the previous, add to steps list
                    steps.append(note)
                elif difference <= 12: # if the new note is very far, add it to jumps list
                    jumps.append(note)
            jump_or_step = randint(0,9)
            if len(jumps) == 0: # if the jumps list is empty, pick a random step
                pick_step = randint(0,len(steps)-1)
                return steps[pick_step]
            if len(steps) == 0: # if the steps list is empty, pick a random jump
                pick_jump = randint(0,len(jumps)-1)
                return jumps[pick_jump]
            if jump_or_step <= 1:  # 1/5 notes will be a jump
                pick_jump = randint(0,len(jumps)-1)
                return jumps[pick_jump]
            else: # 4/5 notes will be steps
                pick_step = randint(0,len(steps)-1)
                return steps[pick_step]
        else: # pick a random note from the possible_notes if it's the singer's first note
            pick_any = randint(0,len(possible_notes)-1)
            return possible_notes[pick_any]

    def build_song(self):
        section_length = 8 # constant that determines the number of measure in each song section
        # chorus:0,verse:1,bridge:2
        self.build_verse(section_length) # always starts the song with a verse
        self.sections.append(1) # adds a 1 to self.sections to state that a verse was just played
        for x in range(self.num_measures//section_length-2):
            if x != self.num_measures//section_length-2: # if it's not the second to last section
                choices = [0,1,2] # set possible options to Verse, Chorus, and Bridge
                choices.pop(self.sections[len(self.sections)-1]) # remove whatever the last section was from the possible options to avoid repetition
                section_type = choices[randint(0,1)] # pick from the remaining option
                self.sections.append(section_type) # add the corresponding section number to the list of sections

            else: # ensures that the second to last measure isn't a chorus
                choices = [0,1,2]
                if self.sections[len(self.sections)-1] != 0: # if the last sections wasn't a chorus, remove it as an option as well
                    choices.pop(self.sections[len(self.sections)-1])
                choices.pop(0) # removes chorus as an option
                section_type = choices[0] #selection the only remaining option

            if section_type == 0:
                self.build_chorus(section_length)
            elif section_type == 1:
                self.build_verse(section_length)
            elif section_type == 2:
                self.build_bridge(section_length)

        self.build_chorus(self.num_measures-(self.time//4)-1) # creates a chorus for the rest of the measure

        for singer in [row[0] for row in self.singers]:
            self.build_measure(singer, triad(self.key, self.key.notes_in_key[0]), self.time, [[4],[4],[4],[4]]) # makes a whole note for each singer in the last measure

    def build_chorus(self, length):
        # duration_options format [Bass Note lengths:[...], Tenor:[...], Alto:[...], Soprano:[....]]
        duration_options = [[1,2],[1],[.5,1],[.25,.5]]
        for x in range(length-1):
            for singer in [row[0] for row in self.singers]: # for each singer in the chorus section
                self.build_measure(singer, self.triads[0], self.time, duration_options)
            self.triads.pop(0) # remove the used triad from the beginning of the sequence
            self.time += 4 # move the song time to the next measure
        for singer in [row[0] for row in self.singers]:
            self.build_measure(singer, triad(self.key, self.key.notes_in_key[0]), self.time, duration_options) # end the section on the I chord
        self.triads.pop(0)
        self.time+=4

    def build_verse(self, length):
        duration_options = [[1,2,4],[1,2],[.5,1],[.25,.5,1]]
        for x in range(length-1):
            for singer in [row[1] for row in self.singers]:
                self.build_measure(singer, self.triads[0], self.time, duration_options)
            self.triads.pop(0)
            self.time += 4
        for singer in [row[1] for row in self.singers]:
            self.build_measure(singer, triad(self.key, self.key.notes_in_key[0]), self.time, duration_options)
        self.triads.pop(0)
        self.time+=4

    def build_bridge(self, length):
        duration_options = [[2],[1],[.25,.5,1],[.25,.5,1]]
        for x in range(length-1):
            for singer in [row[2] for row in self.singers]:
                self.build_measure(singer, self.triads[0], self.time, duration_options)
            self.triads.pop(0)
            self.time += 4
        for singer in [row[2] for row in self.singers]:
            self.build_measure(singer, triad(self.key, self.key.notes_in_key[0]), self.time, duration_options)
        self.triads.pop(0)
        self.time+=4

    def build_measure(self, singer, input_triad, time, note_options):
        orig_time = deepcopy(time) # ensures the original input isn't edited, only a copy

        if singer.name == 'Bass':
            duration_options = note_options[0]

        elif singer.name == 'Tenor':
            duration_options = note_options[1]

        elif singer.name == 'Alto':
            duration_options = note_options[2]

        elif singer.name == 'Soprano':
            duration_options = note_options[3]


        while time < orig_time + 4:
            if time > orig_time + 3: # if there is less than one beat left in the measure
                temp_options = [duration for duration in duration_options if time+duration <= (orig_time+4)-time and duration!=.25] # only add a note that will fit in the measure but also don't add a 1/16 note because they come in sets of 4
            else:
                temp_options = [duration for duration in duration_options if time+duration <= (orig_time+4)-time] # only add a note that will fit in the measure
            duration = temp_options[randint(0,len(temp_options)-1)] # pick a random duration
            if duration == .25:
                for x in range(4): # if a 1/16 notes, add 4 of them
                    self.build_beat(input_triad, time, singer, duration)
                    time += .25
            else: # otherwise just build a new note
                self.build_beat(input_triad, time, singer, duration)
                time += duration

    def build_beat(self, input_triad, time, singer, duration=1):
        pitch = self.return_next_pitch(singer, input_triad)
        self.notes_for_track[singer.track].append(pitch)
        self.MyMIDI.addNote(singer.track, singer.track, pitch, time, duration, singer.volume)

    def write_to_disk(self, output_name):
        binfile = open(r'Songs/{}.mid'.format(output_name), 'wb')
        self.MyMIDI.writeFile(binfile)
        binfile.close()
        print("Written to file with name: '{}'!".format(output_name + '.mid'))
