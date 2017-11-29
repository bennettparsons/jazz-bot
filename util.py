from theory import MusicTheory, Note, Chord

def build_chord(key, numeral, quality, duration=4):
	key_offset = MusicTheory.keys[key]
	numeral_offset = MusicTheory.numerals[numeral]
	pitches = [p+key_offset+numeral_offset for p in MusicTheory.qualities[quality]]
	return Chord([Note(p, duration) for p in pitches], duration)

def build_progression(key, numerals, duration=4):
	return [build_chord(key, n, q, duration=duration) for n,q in numerals]

if __name__ == "__main__":
	print "C major chord: ", build_chord('C', 'I', 'M')
	numerals = [('I','7')]*4 + [('IV','7')]*2 + [('I','7')]*2 + [('V','7'), ('IV','7'), ('I','7'), ('V','7')]
	progression = build_progression('C', numerals)
	print "C Blues: "
	for chord in progression:
		print chord
