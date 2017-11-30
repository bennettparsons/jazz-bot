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

	pitches = ['C', 'Db', 'D', 'Eb', 'E', 'F', 
			   'Gb', 'G', 'Ab', 'A', 'Bb', 'B']


class Note:
	"""
	A Note consists of midi pitch value and a duration
	"""

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

	def __str__ (self):
		return MusicTheory.pitches[self.pitch%12] + ": " + str(self.duration)



class Chord:
	"""
	A Chord consists of a bunch of notes, and a quality
	"""

	def __init__ (self, notes, numeral=None, quality=None, duration=std_chord_dur, volume=std_volume):
		self.notes = notes
		self.duration = duration
		self.volume = std_volume

	def __str__ (self):
		s = ""
		for note in self.notes:
			# get letter name of constituent pitches
			s += MusicTheory.pitches[note.pitch%12] + " "
		s += ": " + str(self.duration)
		return s

	# other stuff...


if __name__ == "__main__":
	# unit tests
	pass

