# jazz-bot: problems.py

import util

class subproblem:
	"""
	defines the subproblem of soloing over one measure with one chord;
	eventually, we can expand the features to we condition on, but for
	now we keep it to just the current chord
	"""

	def __init__ (self, chord):
		self.chord = chord

	# more stuff
