# jazz-bot: problems.py

import util
from search import subproblem, search_solver

class problem:
	"""
	defines the problem of soloing over a given chord progression;
	it delineates the problem into subproblems, consisting of a measure
	and the corresponding chord in the progression (and some more 
	heuristics to come later!) and stitches them together smoothly
	"""

	def __init__  (self, progression, alg="search"):
		self.chords = progression
		self.alg = "search"
		self.define_subproblems()

	def define_subproblems(self):
		self.subproblems = [subproblem(chord) for chord in self.chords]

	def get_solo(self):
		solo = []
		if self.alg == "search":
			for subp in self.subproblems:
				solo += search_solver(subp).get_solution()
		return solo

if __name__ == "__main__":
	numerals = [('I','7')]*4 + [('IV','7')]*2 + [('I','7')]*2 + [('V','7'), ('IV','7'), ('I','7'), ('V','7')]
	progression = util.build_progression('C', numerals)
	util.write_midi(solo=problem(progression).get_solo(), chords=progression)
