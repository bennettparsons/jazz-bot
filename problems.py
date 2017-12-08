# jazz-bot: problems.py

import util, theory
from search import subproblem, search_solver
import random, copy

class problem:
	"""
		defines the problem of soloing over a given chord progression;
		it delineates the problem into subproblems, consisting of a measure
		and the corresponding chord in the progression (and some more 
		heuristics to come later!) and stitches them together smoothly
	"""

	def __init__  (self, progression, alg, res_chord=[], choruses=1):
		self.chords = progression*choruses + [res_chord]
		self.alg = alg
		self.choruses = choruses
		self.chorus = 1
		self.define_subproblems()

	def define_subproblems(self):
		"""
			setup suproblems that are solved sequentially by get_solo
		"""
		subps = []
		bar = 1
		curr_chord = self.chords[0]
		for res_chord in self.chords[1:]:
			if bar == 13:
				self.chorus += 1
				bar = 0
			sz = self.get_problem_size()
			subps.append(subproblem(curr_chord, res_chord=res_chord, size=sz))
			curr_chord = res_chord
			bar += 1
		self.subproblems = subps

	def get_problem_size(self):
		"""
		number of notes per measure is a gaussian whose mean and standard 
		deviationsis are linearly increasing and decreasing functions,
		respectively, of the current chorus
		"""
		mean = 8.0 / self.choruses * self.chorus
		sd = 3.0 / self.choruses * (self.choruses - self.chorus + 1)
		sz = int(random.gauss(mean, sd))
		# print (mean, sd), sz
		while sz < 1 or sz > 8:
			sz = int(random.gauss(mean, sd))
		return sz

	def get_solo(self):
		"""
			create a solo over the progression; dynamically add constraints to
			subproblems based on solutions just created
		"""
		sz = 4    # used in get_rhythms
		solo = []
		sub_sol = None
		fixed_notes = None
		
		for subp in self.subproblems:
			# setup problem constraints
			if sub_sol:
				subp.set_init_sol(copy.deepcopy(sub_sol))
			if fixed_notes:
				subp.set_fixed_notes(fixed_notes)

			# solve
			solver = search_solver(subp)
			sub_sol = solver.get_solution(self.alg)
			fixed_notes = {0: solver.get_resolution()}
			solo += sub_sol
		final_note = fixed_notes[0]
		final_note.set_duration(4)
		util.assert_register(solo)
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
	# solo = get_rhythms(solo, 4)
	# util.write_midi(solo=solo + [res], chords=progression, outfile="rhythms.mid")


	numerals = [('I','7')]*4 + [('IV','7')]*2 + [('I','7')]*2 + [('V','7'), ('IV','7'), ('I','7'), ('V','7')]
	progression = util.build_progression('C', numerals)
	num_choruses = 2

	util.write_midi(solo=problem(progression, choruses=num_choruses, res_chord=util.build_chord('C', 'I', '7')).get_solo(),
					chords=progression*num_choruses + [util.build_chord('D', 'I', '7')])




