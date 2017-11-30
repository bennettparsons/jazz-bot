# jazz-bot: search.py

import util

class search_solver(subproblem):
	"""
	defines evaluation functions for a local search solution to the
	subproblem, and solves the problem using local search
	"""


	def get_solution(self):
		"""
		generate a solution: a sequence of notes that obeys the 
		requirements of the subproblem and can be subjected to 
		the feature evaluation functions
		"""
		pass

	################################
    # Feature Evaluation Functions #
    ################################

	def tonality(self):
		"""
		how well does the solo use chord tones, tensions, and scales?
		we don't want all notes to be chord tones, but we do want
		*important* notes to be chord notes; we may hardcode important
		tones as a feature of subproblem, retrievable with a call to
		get_important_notes()
		"""
		pass


	def contour(self):
		"""
		how well does the solo use contour? This includes an evaluation
		of intervallic diversity: *in general* we want a good mix of half
		steps and whole steps, along with larger leaps of 3rds-octaves. When
		considering just a stream of eighth notes (a bebop line), we penalize
		intervalls larger than octaves, and "too many" consecutive large 
		(third or larger) intervalls
		"""
