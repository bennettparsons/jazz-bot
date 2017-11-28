"""
Definitions of note, chord and ... objects
"""

import util


class Note:
	"""
	A Note consists of midi pitch value and a duration
	"""

	def __init__ (self, pitch, duration):
		self.pitch = pitch
		self.duration = duration

	def set_duration(duration):
		self.duration = duration

	def transpose(steps, up=True):
		if up:
			self.pitch += steps
		else:
			self.pitch -= steps



class Chord:
	"""
	A Chord consists of a bunch of notes, and a quality
	"""

	def __init__ (self, notes, duration):
		self.notes = notes
		self.duration = duration

	def __str__ (self):
		s = ""
		for note in self.notes:
			s += get_pitch_letter(note.pitch)
		s += ": " + self.duration

	# other stuff...

class MusicTheory:
	"""
	A static class containting structures defining Roman Numeral
	chords, chord qualities, and key areas associated with their
	respective MIDI pitch values
	"""
	keys = {'A':45, 'Bb':46, 'B':47, 'C':48, 'Db':49, 'D':50,
	 		'Eb':51, 'E':52, 'F':53, 'Gb':54, 'G':55, 'Ab':56}

	numerals = {'I': 0, 'II': 1, 'III': 2, 'IV': 3, 
				'V': 4, 'VI': 5, 'VII': 6}

	qualities = {'M': [0,4,7], 'm': [0,3,7], 'M7': [0,4,7,11], 
			'm7': [0,3,7,10], '7': [0,4,7,10]}

	pitches = ['C', 'Db', 'D', 'Eb', 'E', 'F',
			   'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
