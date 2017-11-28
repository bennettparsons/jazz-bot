"""
Definitions of note, chord and ... objects
"""


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
	A Chord consists of a bunch of notes, and a type
	"""

