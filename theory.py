# jazz-bot: theory.py

std_volume = 100
std_note_dur = 1
std_chord_dur = 4

class MusicTheory:
	"""
	A static class containting structures defining Roman Numeral
	chords, chord qualities, and key areas associated with their
	respective MIDI pitch values
	"""

	keys = {'A':45, 'Bb':46, 'B':47, 'C':48, 'Db':49, 'D':50,
	 		'Eb':51, 'E':52, 'F':53, 'Gb':54, 'G':55, 'Ab':56}

	numerals = {'I':0, 'bII':1, 'II':2, 'III':4, 'IV':5, 'bV':6,
				'V':7, 'bVI':8, 'VI': 9, 'bVII':10, 'VII': 11}

	qualities = {'M': [0,4,7], 'm': [0,3,7], 'M7': [0,4,7,11], 
			'm7': [0,3,7,10], '7': [0,4,7,10]}

	tensions = {
				'M': [], 
				'm': [], 
				'M7': [], 
				'm7': [], 
				'7': [(1,0), (3,4), (6,5), (8,9)]  # b9, #9, #11, b13
			   }

	scales = {
			  'M': [], 
			  'm': [], 
			  'M7': [], 
			  'm7': [], 
			  '7': [0,2,4,5,7,9,10,11]   # bebop scale
			 }


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

	def set_duration(duration):
		self.duration = duration

	def transpose(steps, up=True):
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



class Chord:
	"""
	A Chord consists of a bunch of notes, and a quality
	"""

	def __init__ (self, notes, key=None, numeral=None, quality=None, duration=std_chord_dur, volume=std_volume):
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
		if len(self.notes >= 4):
			return [self.notes[1].as_letter()] + [self.notes[3].as_letter()]
		else:
			return self.notes[1].as_letter()

	def get_scale(self):
		key_offset = MusicTheory.keys[self.key]
		scale = [p + key_offset for p in MusicTheory.scales[self.quality]]
		return [Note(p).as_letter() for p in scale]

	def get_tensions(self):
		key_offset = MusicTheory.keys[self.key]
		tensions = [(p1 + key_offset, p2 + key_offset) for p1, p2 in MusicTheory.tensions[self.quality]]
		return [(Note(p1).as_letter(), Note(p2).as_letter()) for p1, p2 in tensions]

	def is_chord_tone(self, letter):
		return letter in self.get_chord_tones()

	def is_third_or_seventh(self, letter):
		return letter in self.get_third_and_seventh()

	def is_in_scale(self, letter):
		return letter in self.get_scale()

	def is_tension_resolution(self, letter_pair):
		return letter_pair in self.get_tensions

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
	# unit tests
	pass

