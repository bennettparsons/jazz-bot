# jazz-bot: evaluation.py

import util

class RL_evaluators(subproblem):
	"""
	defines evaluation functions for an RL approach to the subproblem
	"""

	# stuff


class search_evaluators(subproblem):
	"""
	defines evaluation functions for a local search solution to the subproblem
	"""

	def tonality(self):
		"""
		how well does the solo use chord tones?
		we don't want all notes to be chord tones, but we do want
		*important* notes to be chord notes; we may hardcode important
		tones as a feature of subproblem, retrievable with a call to
		get_important_notes()
		"""

