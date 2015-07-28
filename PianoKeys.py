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

C_Major = [c,d,e,f,g,a,b]
C_Minor = [c,d,e_flat,f,g,a_flat,b_flat]
D_Major = [d,e,f_sharp,g,a,c_sharp]
D_Minor = [d,e,f,g,a,b_flat,c]
E_Major = [e,f_sharp,g_sharp,a,b,c_sharp,d_sharp]
E_Minor = [e,f_sharp,g,a,b,c,d]
F_Major = [f,g,a,b_flat,c,d,e]
F_Minor = [f,g,a_flat,b_flat,c,d_flat,e_flat]
G_Major = [g,a,b,c,d,e,f_sharp]
G_Minor = [g,a,b_flat,c,d,e_flat,f]
A_Major = [a,b,c_sharp,d,e,f_sharp,g_sharp]
A_Minor = [a,b,c,d,e,f,g]
B_Major = [b,c_sharp,d_sharp,e,f_sharp,g_sharp,a_sharp]
B_Minor = [b,c_sharp,d,e,f_sharp,g,a]

def notes_in_key(key, octave):
    for x in range(len(key)):
        if key[x] + 12 * (octave + 2) < key[0]:
            key[x] += 12 * (octave + 3)
        else:
            key[x] += 12 * (octave + 2)
    return key

