# jazz-bot: util.py

from structures import Note, Chord
import theory
from midiutil import MIDIFile


def compress(lst):
	"""
	like uniq for python list
	"""
	s = []
	prev = None
	for elt in lst:
		if elt != prev:
			s.append(elt)
		prev = elt
	return s

def make_notes(pitches, duration=.5):
	"""
	convert a list of pitches to a list of note objects
	"""
	return [Note(p, duration=duration) for p in pitches]

def make_pitches(notes):
	return [note.as_pitch() for note in notes]

def build_chord(key, numeral, quality, duration=4):
	"""
	constructs a Chord object given a key, numeral, quality and duration
	"""
	key_offset = theory.keys[key]
	numeral_offset = theory.numerals[numeral]
	pitches = [p+key_offset+numeral_offset for p in theory.qualities[quality]]
	return Chord([Note(p, duration=duration) for p in pitches], key=key, numeral=numeral, quality=quality, duration=duration)

def build_progression(key, numerals, duration=4):
	"""
	builds a chord progression, in whole notes, given a list of chords and a key
	"""
	return [build_chord(key, n, q, duration=duration) for n,q in numerals]

# write_midi helper function: write solo to midi
def write_midi_solo(midi, track, solo, channel):
	t = 0
	for note in solo:
		midi.addNote(track, channel, note.as_pitch(), t, note.duration, note.volume)
		t += note.duration
	return midi

# write_midi helper function: write chords to midi
def write_midi_chords(midi, track, chords, channel):
	t = 0
	for chord in chords:
		for note in chord.notes:
			midi.addNote(track, channel, note.as_pitch(), t, note.duration, note.volume)
		t += note.duration
	return midi

def write_midi(solo=None, chords=None, outfile="jazzy-bot-solo.mid", channel=0, tempo=160):
	"""
	write a midi file based on solo, a list of Note objects, and chords, a
	list of chord objects
	"""
	assert(solo or chords)
	if solo and chords:
		midi = MIDIFile(2, adjust_origin=False)
		midi.addTempo(0, 0, tempo)
		write_midi_solo(midi, 0, solo, channel)
		write_midi_chords(midi, 1, chords, channel)
	else:
		midi = MIDIFile(1, adjust_origin=False)
		midi.addTempo(0, 0, tempo)
		if solo:
			write_midi_solo(midi, 0, solo, channel)
		elif chords:
			write_midi_chords(midi, 0, chords, channel)
	with open(outfile, "wb") as f:
		midi.writeFile(f)


if __name__ == "__main__":
	print Note(48)
	print "C major chord: ", build_chord('C', 'I', 'M')
	numerals = [('I','7')]*4 + [('IV','7')]*2 + [('I','7')]*2 + [('V','7'), ('IV','7'), ('I','7'), ('V','7')]
	progression = build_progression('C', numerals)
	print "C Blues: "
	for chord in progression:
		print chord
	write_midi(solo=[Note(60, duration=1.5), Note(63, duration=.5)], chords=progression)
