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
		"""
		setup suproblems that are solved sequentially by get_solo
		"""
		subps = []
		curr_chord = self.chords[0]
		for res_chord in self.chords[1:]:
			subps.append(subproblem(curr_chord, res_chord=res_chord))
			curr_chord = res_chord
		self.subproblems = subps

	def get_solo(self):
		"""
		create a solo over the progression; dynamically add constraints to
		subproblems based on solutions just created
		"""
		solo = []
		sub_sol = None
		fixed_notes = None
		if self.alg == "search":
			for subp in self.subproblems:
				# setup problem constraints
				subp.set_init_sol(sub_sol)
				subp.set_fixed_notes(fixed_notes)

				# solve
				solver = search_solver(subp)
				sub_sol = solver.get_solution()
				solo += sub_sol
				fixed_notes = {0: solver.get_resolution()}
		final_note = fixed_notes[0]
		final_note.set_duration(4)
		return solo + [final_note]

if __name__ == "__main__":
	# numerals = [('V','7')]
	# progression = util.build_progression('C', numerals + [('I', '7')])
	# prob = problem(progression)
	# solver = search_solver(prob.subproblems[0])
	# solo = solver.get_solution()
	# res = solver.get_resolution()
	# res.set_duration(4)
	# print "res is definitely", res
	# util.write_midi(solo=solo + [res], chords=progression)

	numerals = [('I','7')]*4 + [('IV','7')]*2 + [('I','7')]*2 + [('V','7'), ('IV','7'), ('I','7'), ('V','7')]
	progression = util.build_progression('C', numerals + [('I', '7')])
	util.write_midi(solo=problem(progression).get_solo(), chords=progression)
