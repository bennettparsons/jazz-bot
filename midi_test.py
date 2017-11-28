# adapted from example in https://pypi.python.org/pypi/MIDIUtil/

from midiutil import MIDIFile

degrees  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
track    = 0
channel  = 0
time     = 0     # In beats
duration = 1     # In beats
tempo    = 120   # In BPM
volume   = 100   # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(2, adjust_origin=False)  # One track, defaults to format 1 (tempo track is created
                      # automatically)
MyMIDI.addTempo(track, time, tempo)


keys = ['A','Bb','B','C','Db','D','Eb','E','F','Gb','G','Ab']  # set of possible keys

# from https://github.com/ckdotca/JSB2/blob/master/JSB2.py
class music_theory():
    """Defines mappings between musical notes/chords and midi notes/offsets, and defines sets of possible notes/chords to play"""

    chord_start_note_map = {
        'A':45, 'Bb':46, 'B':47, 'C':48, 'Db':49, 'D':50, 'Eb':51, 'E':52, 
        'F':53, 'Gb':54, 'G':55, 'Ab':56}  # mapping to the root note of the key's I chord
    chords = ['I', 'IM7', 'iim', 'iim7', 'iiim', 'iiim7', 'IV', 'IVM7', 'V', 'vim', 'vim7']  # set of possible chords to play
    chord_map = {
        'I':[0,4,7], 'IM7':[0,4,7,11], 'I7':[0,4,7,10], 'iim':[2,5,9], 'iim7':[2,5,9,12], 'iiim':[4,7,11], 
        'iiim7':[4,7,11,14], 'IV':[5,9,12], 'IVM7':[5,9,12,16], 'IV7':[5,9,12,15], 'IVm':[5,8,12], 'IVm7':[5,8,12,16], 
        'V':[7,11,14], 'V7':[7,11,14,17], 'vim':[9,12,16], 'vim7':[9,12,16,19]}  # mapping to offsets from the chord_start_notes

    # Bennett wrote these

    def __init__(self, key):
        self.key = key

    def build_chord(self, chord):
        return [note + self.chord_start_note_map[self.key] for note in self.chord_map[chord]]

    def build_progression(self, chords):
        return [self.build_chord(chord) for chord in chords]

M = music_theory('C')
chords = M.build_progression(['I7', 'I7', 'I7', 'I7', 'IV7', 'IV7', 'I7', 'I7', 'V7', 'IV7', 'I7', 'V7'])

# write melody/solo
# for i, pitch in enumerate(degrees):
#     MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

# write form
i = 0
for chord in chords:
    for pitch in chord:
        MyMIDI.addNote(1, channel, pitch, time + i, 4, volume)
    i += 4

# write a midi file
with open("blues-changes.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
