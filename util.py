from theory import Note, Chord, MusicTheory

def get_pitch_letter(num):
	MusicTheory.pitches[num%12]


def build_chord(key, numeral, quality, duration=4):
	key_offset = MusicTheory.keys[key]
	numeral_offset = MusicTheory.numerals[numeral]
	pitches = [p+key_offset+numeral_offset for p in MusicTheory.qualities[quality]]
	return Chord([Note(p, duration) for p in pitches], duration)

print build_chord('C', 'I', 'M')