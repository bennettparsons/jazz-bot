# jazz-bot: search.py

import util

class search_solver(subproblem):
	"""
	defines evaluation functions for a local search solution to the subproblem,
	and solves the problem using local search
	"""

	def tonality(self):
		"""
		how well does the solo use chord tones, tensions, and scales?
		we don't want all notes to be chord tones, but we do want
		*important* notes to be chord notes; we may hardcode important
		tones as a feature of subproblem, retrievable with a call to
		get_important_notes()
		"""

