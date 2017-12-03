# jazz-bot: theory.py

import theory

std_volume = 100
std_note_dur = .5
std_chord_dur = 4


class Note:
	"""
	A Note consists of midi pitch value and a duration
	"""

	pitches = ['C', 'Db', 'D', 'Eb', 'E', 'F', 
			   'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

	def __init__ (self, pitch, duration=std_note_dur, volume=std_volume):
		assert(pitch >= 0 and pitch <= 127)
		self.pitch = pitch
		self.duration = duration
		self.volume = std_volume

	def set_duration(self, duration):
		self.duration = duration

	def transpose(self, steps, up=True):
		if up:
			self.pitch += steps
		else:
			self.pitch -= steps

	def as_pitch(self):
		return self.pitch

	def as_letter(self):
		return self.pitches[self.pitch%12]

	def __str__ (self):
		return self.as_letter() + ": " + str(self.duration)

	def get_pitch(self):
		return self.pitch

class Chord:
	"""
	A Chord consists of a bunch of notes, and a quality
	"""

	def __init__ (self, notes=None, key=None, numeral=None, quality=None, duration=std_chord_dur, volume=std_volume):
		self.notes = notes
		self.key = key
		self.numeral = numeral
		self.quality = quality
		self.duration = duration
		self.volume = std_volume

	def get_root(self):
		return self.notes[0]

	def get_chord_tones(self):
		return [n.as_letter() for n in self.notes]

	def get_third_and_seventh(self):
		if len(self.notes) >= 4:
			return [self.notes[1].as_letter()] + [self.notes[3].as_letter()]
		else:
			return [self.notes[1].as_letter()]

	def get_scale(self):
		key_offset = theory.keys[self.key]
		scale = [p + key_offset for p in theory.scales[self.quality]]
		return [Note(p).as_letter() for p in scale]

	def get_tensions(self):
		key_offset = theory.keys[self.key]
		tensions = [(p1 + key_offset, p2 + key_offset) for p1, p2 in theory.tensions[self.quality]]
		return [(Note(p1).as_letter(), Note(p2).as_letter()) for p1, p2 in tensions]

	def is_chord_tone(self, letter):
		return letter in self.get_chord_tones()

	def is_third_or_seventh(self, letter):
		return letter in self.get_third_and_seventh()

	def is_in_scale(self, letter):
		return letter in self.get_scale()

	def is_tension(self, letter):
		return letter in [p[0] for p in self.get_tensions()]

	def is_tension_resolution(self, letter_pair):
		return letter_pair in self.get_tensions()

	def is_five_chord(self):
		return self.numeral == 'V'

	def as_pitches(self):
		return [note.as_pitch() for note in self.notes]

	def as_letters(self):
		return [note.as_letter() for note in self.notes]

	def __str__ (self):
		return " ".join(self.as_letters()) + ": " + str(self.duration)

	# other stuff...


if __name__ == "__main__":
	C = Note(48)
	E = Note(52)
	G = Note(55)
	Bb = Note(58)
	CM = Chord([C,E,G, Bb], key='C', numeral='I', quality='7')
	assert(C == CM.get_root())
	assert('C' and 'E' and 'G' in CM.get_chord_tones())
	assert('D' not in CM.get_chord_tones())
	assert('C' not in CM.get_third_and_seventh())
	assert('E' and 'Bb' in CM.get_third_and_seventh())
	assert('C' and 'D' and 'E' and 'F' and 'G' and 'A' and 'Bb' and 'B' in CM.get_scale())
	assert('Db' and 'Eb' and 'Gb' and 'Ab' not in CM.get_scale())
	assert(('Db','C') and ('Eb','E') and ('Gb', 'F') and ('Ab', 'A') in CM.get_tensions())
	assert(CM.is_chord_tone('C'))
	assert(CM.is_third_or_seventh('E'))
	assert(not CM.is_third_or_seventh('C'))
	assert(CM.is_in_scale('B'))
	assert(not CM.is_in_scale('Ab'))
	assert(CM.is_tension('Db') and CM.is_tension('Ab'))
	assert(CM.is_tension_resolution(('Db', 'C')))
	assert(not CM.is_tension_resolution(('Db', 'D')))
	assert(not CM.is_five_chord())

