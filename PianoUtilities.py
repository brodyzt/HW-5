from Errors import *
from copy import *

class Singer:
    def __init__(self, low_note, high_note, track, channel, name):
        self.low_note = low_note
        self.high_note = high_note
        self.vocal_range = high_note - low_note
        self.track = track
        self.channel = channel
        self.name = name

    def __str__(self):
        return self.name

    def octave_notes_in_range(self, input_pitch):
        possible_notes = []
        for x in range(self.vocal_range+1):
            pitch = x + self.low_note
            difference = pitch - input_pitch
            if difference % 12 == 0:
                possible_notes.append(pitch)
        return possible_notes


class Soprano(Singer):
    def __init__(self, low_note=60, high_note=81, track=0, channel=0, name='Soprano'):
        super(Soprano, self).__init__(low_note,high_note,track,channel,name)
class Alto(Singer):
    def __init__(self, low_note=55, high_note=77, track=0, channel=1, name='Alto'):
        super(Alto, self).__init__(low_note,high_note,track,channel,name)
class Tenor(Singer):
    def __init__(self, low_note=48, high_note=69, track=1, channel=0, name='Tenor'):
        super(Tenor, self).__init__(low_note,high_note,track,channel,name)
class Bass(Singer):
    def __init__(self, low_note=40, high_note=64, track=1, channel=1, name='Bass'):
        super(Bass, self).__init__(low_note,high_note,track,channel,name)

instrument_list = [('piano',0), ('harpsichord',6), ('glock',9), ('vibes',11),
                            ('marimba',12), ('organ',19), ('guitar',24), ('bass',32),
                            ('violin',40), ('cello',42), ('harp',46), ('timps',47),
                            ('voice',54), ('trumpet',56), ('tuba',58), ('horn',60),
                            ('alto sax', 65), ('oboe',68), ('bassoon',70), ('clarinet',71),
                            ('flute',73), ('recorder',74), ('bottle',75), ('whistle',78),
                            ('synth 1',81), ('synth 2',82), ('synth 3',83), ('synth 4',84),
                            ('fifths',96), ('halo',94), ('goblins',101), ('koto',107),
                            ('bagpipe',109), ('taiko',116), ('toms',117), ('breath',121),
                            ('seashore',122), ('bird',123), ('phone',124), ('applause',126)]

instrument_dic = dict(instrument_list)

singer_list = [('Soprano',Soprano()),('Alto',Alto()),('Tenor',Tenor()),('Bass',Bass())]

singer_dic = dict(singer_list)


# Variables for Key Pitches
c1 = 36
cs1 = 37
df1 = 37
d1 = 38
ds1 = 39
ef1 = 39
e1 = 40
f1 = 41
fs1 = 42
gf1 = 42
g1 = 43
gs1 = 44
af1 = 44
a1 = 45
as1 = 46
bf1 = 46
b1 = 47
c2 = 48
cs2 = 49
df2 = 49
d2 = 50
ds2 = 51
ef2 = 51
e2 = 52
f2 = 53
fs2 = 54
gf2 = 54
g2 = 55
gs2 = 56
af2 = 56
a2 = 57
as2 = 58
bf2 = 58
b2 = 59
c3 = 60
cs3 = 61
df3 = 61
d3 = 62
ds3 = 63
ef3 = 63
e3 = 64
f3 = 65
fs3 = 66
gf3 = 66
g3 = 67
gs3 = 68
af3 = 68
a3 = 69
as3 = 70
bf3 = 70
b3 = 71
c4 = 72
cs4 = 73
df4 = 73
d4 = 74
ds4 = 75
ef4 = 75
e4 = 76
f4 = 77
fs4 = 78
gf4 = 78
g4 = 79
gs4 = 80
af4 = 80
a4 = 81
as4 = 82
bf4 = 82
b4 = 83

# Code for rest
rest = -1

# Variables for Key Lengths
full = 4
half = 2
quarter = 1
eighth = .5
sixteenth = .25

# Keys

c = 0
c_sharp = 1
d_flat = 1
d = 2
d_sharp = 3
e_flat = 3
e = 4
f = 5
f_sharp = 6
g_flat = 6
g = 7
g_sharp = 8
a_flat = 8
a = 9
a_sharp = 10
b_flat = 10
b = 11

class Key:

    def __init__(self, name, input_key):
        self.name = name
        self.notes_in_key = self.notes_in_key(input_key)

    @staticmethod
    def notes_in_key(input_key):
        notes = []
        for x in range(10):
            for key in input_key:
                if key + 12*x < input_key[0]+ 12*x:
                    notes.append(key + 12*(x+1))
                else:
                    notes.append(key + 12*x)
        return notes

C_Major = Key('C Major', [c,d,e,f,g,a,b])
C_Minor = Key('C Minor', [c,d,e_flat,f,g,a_flat,b_flat])
D_Major = Key('D Major', [d,e,f_sharp,g,a,c_sharp])
D_Minor = Key('D Minor', [d,e,f,g,a,b_flat,c])
E_Major = Key('E Major', [e,f_sharp,g_sharp,a,b,c_sharp,d_sharp])
E_Minor = Key('E Minor', [e,f_sharp,g,a,b,c,d])
F_Major = Key('F Major', [f,g,a,b_flat,c,d,e])
F_Minor = Key('F Minor', [f,g,a_flat,b_flat,c,d_flat,e_flat])
G_Major = Key('G Major', [g,a,b,c,d,e,f_sharp])
G_Minor = Key('G Minor', [g,a,b_flat,c,d,e_flat,f])
A_Major = Key('A Major', [a,b,c_sharp,d,e,f_sharp,g_sharp])
A_Minor = Key('A Minor', [a,b,c,d,e,f,g])
B_Major = Key('B Major', [b,c_sharp,d_sharp,e,f_sharp,g_sharp,a_sharp])
B_Minor = Key('B Minor', [b,c_sharp,d,e,f_sharp,g,a])

Major_Pentatonic = Key('Major Pentatonic', [g_flat,a_flat,b_flat,d_flat,e_flat])

key_list = [C_Major,
            C_Minor,
            D_Major,
            D_Minor,
            E_Major,
            E_Minor,
            F_Major,
            F_Minor,
            G_Major,
            G_Minor,
            A_Major,
            A_Minor,
            B_Major,
            B_Minor,
            Major_Pentatonic]

key_dic = dict((key.name,key) for key in key_list)


def n_notes_away(input_key, start_note, num_away):
    index = input_key.notes_in_key.index(start_note)
    index += num_away
    return input_key.notes_in_key[index]


def triad(input_key, start_note):
    chord = []
    for x in range(3):
        index = input_key.notes_in_key.index(start_note)
        chord.append(input_key.notes_in_key[index] % 12)
        index += 2

    return chord
