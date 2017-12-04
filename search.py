# jazz-bot: search.py

import random, copy
import util
import theory
from structures import Note
import numpy as np


class subproblem:
	"""
	defines the subproblem of soloing over one measure with one chord;
	eventually, we can expand the features to we condition on, but for
	now we keep it to just the current chord
	"""

	def __init__ (self, chord, init_sol=None, fixed_notes=None, res_chord=None, size=8):
		self.chord = chord
		self.init_sol = init_sol
		self.fixed_notes = fixed_notes
		self.res_chord = res_chord
		self.solution = None
		self.size = size

	def set_fixed_notes(self, fixed_notes):
		self.fixed_notes = fixed_notes

	def set_init_sol(self, init_sol):
		self.init_sol = init_sol

	# more stuff?


class search_solver:
	"""
	defines evaluation functions for a local search solution to the
	subproblem, and solves the problem using local search
	"""

	def __init__ (self, subproblem):
		self.chord = subproblem.chord
		self.size = subproblem.size
		self.init_sol = subproblem.init_sol
		# init_sol must have proper length
		if self.init_sol:
			while len(self.init_sol) != self.size:
				if len(self.init_sol) < self.size:
					self.init_sol.append(self.init_sol[-1])
				else:
					del self.init_sol[random.choice(range(len(self.init_sol)))]
		self.fixed_notes = subproblem.fixed_notes
		self.res_chord = subproblem.res_chord
		self.solution = None
		self.active_chord = self.chord

	def get_solution(self):
		"""
		generate a solution: a sequence of notes that obeys the 
		requirements of the subproblem and can be subjected to 
		the feature evaluation functions
		"""
		self.search()
		self.rhythms()
		# verify invariants
		assert(sum([note.get_duration() for note in self.solution]) == 4)
		assert(len(self.solution) == self.size)
		for note in self.solution:
			assert(note.get_duration() != 0)
		return self.solution

	def get_resolution(self):
		"""
		return a single note representing the resolution of the current
		solution to the next chord in the progression (self.res_chord);
		should only be called once self.solution is generated
		"""
		assert(self.solution)
		self.active_chord = self.res_chord
		prev_note = self.solution[-1]
		proposed_soln = copy.copy(prev_note)
		proposed_soln.transpose(7, up=False)
		sols = []
		# print prev_note
		# print
		while(abs(util.interval(proposed_soln, prev_note)) <= 8):
			sols.append((self.resolution_evaluate(prev_note, proposed_soln), proposed_soln))
			# print "Score of:", sols[-1][0], "for note", sols[-1][1]
			proposed_soln = copy.copy(proposed_soln)
			proposed_soln.transpose(1)

		# print
		# print "Best sol is:", max(sols), max(sols)[0], max(sols)[1].as_letter()

		return max(sols)[1]


	def rhythms(self):
		"""
		solution must have total duration of 4 beats
		"""
		curr_dur = sum([note.get_duration() for note in self.solution])
		while curr_dur != 4:
			i = random.choice(range(len(self.solution)))
			if curr_dur < 4:
				self.solution[i].add_duration(.5)
			else:
				if self.solution[i].get_duration() == .5:
					continue
				self.solution[i].add_duration(-.5)
			curr_dur = sum([note.get_duration() for note in self.solution])
		assert(sum([note.get_duration() for note in self.solution]) == 4)


	def get_rhythms(self, sz):
		"""
		THIS FUNCTION IS DEPRECATED
		post process rhythms by sampling sz notes from self.solution
		"""
		assert(0)  # deprecated
		assert(self.solution)
		sol = copy.copy(self.solution)
		assert(sz < len(sol))

		if not self.fixed_notes:
			self.fixed_notes = {}
		new_notes = []

		# sample notes to keep
		for _ in range(sz):
			i = random.choice(range(len(sol)))
			while (i in self.fixed_notes or i in new_notes):
				i = random.choice(range(len(sol)))
			new_notes.append(i)

		# nonsampled notes are turned into rests
		last_note = None
		for i in range(len(sol)):
			if i in new_notes:
				last_note = sol[i]
			elif last_note:
				last_note.add_duration(.5)
				sol[i].set_duration(0)
			else:
				sol[i].set_pitch(0)

		return [note for note in sol if note.get_duration() != 0]


	def get_sample_G7_solution1(self):
		return util.make_notes([86, 84, 81, 82, 83, 81, 79, 78])

	def get_sample_G7_solution2(self):
		return util.make_notes([77, 81, 76, 79, 77, 69, 72, 74])





	################################
	#     Simulated annealing      #
	################################

	def search(self):
		"""
			implements a simple search algorithm: hill-climbing with metropolis variation

			soln is a list of Note objects

			TO DO - add a scheduling / temperature function
		"""
		# initialize: make a solution of size self.size
		if self.init_sol:
			assert(len(self.init_sol) == self.size)
			curr_soln = self.init_sol
		else:
			curr_soln = util.make_notes([self.chord.get_root().get_pitch() + 24] * self.size)
		if self.fixed_notes:
			for i in self.fixed_notes:
				curr_soln[i] = self.fixed_notes[i]

		assert(len(curr_soln) == self.size)
		best_soln = curr_soln

		n = 200
		curr_soln_val = 0
		best_soln_val = curr_soln_val

		for _ in range(n):

			# get neighbor node
			candidate_soln = self.get_neighbor_node(curr_soln)
			candidate_soln_val = self.ensemble_evaluate(candidate_soln)

			# accept with probability 1 if climbs up
			if candidate_soln_val > curr_soln_val:
				curr_soln = candidate_soln
				curr_soln_val = candidate_soln_val

			# accept with probability <1 if climbs down
			# should be proportional to size of change but not sure what distance metric makes sense rn
			elif random.random() < 0.1:
				curr_soln = candidate_soln
				curr_soln_val = candidate_soln_val

			if best_soln_val < curr_soln_val:
				best_soln = curr_soln
				best_soln_val = curr_soln_val

		print "Score of:", best_soln_val, "for", self.size, "notes"
		self.solution = best_soln


	def get_neighbor_node(self, soln, pitch_sd=3):
		"""
			implements a naive approach for retrieving neighbors

			1 s.d. corresponds to 3 half-steps ? we can tweak however
		"""

		# sample a single note
		i = random.choice(range(len(soln)))
		if self.fixed_notes:
			while (i in self.fixed_notes or soln[i].is_rest()):
				i = random.choice(range(len(soln)))

		# sample notes to replace this note
		pitch = soln[i].get_pitch()
		proposed_pitch = int(random.gauss(pitch, pitch_sd))

		# python is pass by ref right?
		proposed_soln = copy.copy(soln)
		proposed_soln[i] = Note(proposed_pitch, duration=.5)
		return proposed_soln

	################################
	# 		Genetic algorithms 	   #
	################################

	def GA(self):
		"""
			a GA approach could be interesting b/c crossovers may 1. combine interesting licks / patterns
			and 2. create interesting intervallic jumps / dives
		"""
		# globals
		generation_sz = 10
		generations = 10

		# intialize initial population
		population = self.generate_population(generation_sz)

		# repeat until an individual is uber fit (or sufficient time...)
		for _ in range(generations):

			successor_population = []
			# replace population with successor population
			for _ in range(generation_sz):

				# selection time
				# 	sample parents with probability that's proportional to fitness
				fitness = [self.get_fitness(individual) for individual in population]
				normalized_fitness = map(lambda x: x / float(sum(fitness)), fitness)

				# np.random allows specifying a distribution, but works on 1-d array only, hence indexing
				mom = population[np.random.choice(range(len(population)), p=normalized_fitness)]
				dad = population[np.random.choice(range(len(population)), p=normalized_fitness)]

				# sexy time (crossover)
				child = self.reproduce(mom, dad)

				# mutate
				# 	note should be randomly changed with some small probability
				mutated_child = self.mutate(child)

				successor_population.append(mutated_child)

			population = successor_population

		# return the fittest individual
		best_sol = sorted(population, key=lambda individual: self.get_fitness(individual), reverse=True)[0]
		print "Score of:", self.get_fitness(best_sol)
		self.solution = best_sol

	def generate_individual_for_population(self):
		"""
			list of Notes
		"""
		pitch_sd = 3 # \sigma = 3 1/2 steps
		pitches = [self.chord.get_root().get_pitch()+24] * 8
		pitches = map(lambda pitch: int(random.gauss(pitch, pitch_sd)), pitches)
		return util.make_notes(pitches)

	def generate_population(self, sz):
		"""
			list of list of Notes
		"""

		return [self.generate_individual_for_population() for _ in range(sz)]

	def get_fitness(self, individual):
		return self.ensemble_evaluate(individual)

	def reproduce(self, mom, dad):
		"""
			chose to retain only one child
		"""
		# pick crossover point
		i = random.choice(range(len(mom)))
		return mom[:i] + dad[i:]

	def mutate(self, child):
		"""
		 	should add a temperature function here also
		"""
		mutated_child = copy.copy(child)
		for note_index, note in enumerate(mutated_child):
			if random.random() < 0.05:
				pitch = note.get_pitch()
				new_pitch = int(random.gauss(pitch, 3))  # \sigma = 3 1/2 steps, again
				mutated_child[note_index] = util.make_notes([new_pitch])[0]
		return mutated_child

	################################
    # Feature Evaluation Functions #
    ################################

	def ensemble_evaluate(self, soln):
		"""
			evaluate on tonality, contour and register

		"""

		return self.tonality(soln) + self.contour(soln) + self.register(soln)


	def resolution_evaluate(self, prev_note, res_note):
		"""
		evaluate just the resolution pitch
		"""
		return self.tonality([res_note]) + self.distance([prev_note, res_note])


	def tonality(self, solution):
		"""
		how well does the solo use chord tones, tensions, and scales?
		we don't want all notes to be chord tones, but we do want
		*important* notes to be chord notes; we may hardcode important
		tones as a feature of subproblem, retrievable with a call to
		get_important_notes()
		"""
		score = 0
		tension = None
		chord = self.active_chord

		for note in solution:
			if tension and chord.is_tension_resolution((tension, note.as_letter())):
				score += 5
			tension = None
			letter = note.as_letter()
			if chord.is_third_or_seventh(letter):
				score += 3
			elif chord.is_chord_tone(letter):
				score += 2
			elif chord.is_in_scale(letter):
				score += 1
			elif chord.is_tension(letter):
				tension = letter
		return score



	def contour(self, solution):
		"""
		how well does the solo use contour? This includes an evaluation
		of intervallic diversity: *in general* we want a good mix of half
		steps and whole steps, along with larger leaps of 3rds-octaves. When
		considering just a stream of eighth notes (a bebop line), we penalize
		intervalls larger than octaves, and "too many" consecutive large 
		(third or larger) intervalls
		"""
		# assert(len(solution) >= 2)
		if len(solution) < 2:
			return 0

		score = 0

		# heuristics
		interval_variety = {1:0, 2:0, 3:1, 4:3, 5:3, 6:2, 7:1, 8:1}
		direction_variety = {1:0, 2:2, 3:3, 4:3, 5:2, 6:1, 7:1, 8:1}
		# interval_weights = [.5, .4, .3, .3, .3, .2, .2, .1]
		interval_weights = [1, .8, .6, .5, .3, .2, .1, 0, -.1, -.2, -.3, .2]

		sol = util.make_pitches(solution)
		up = "up"
		down = "down"
		same = "same"
		intervals = []   # intervals
		directions = []   # recent interval direction (up or down)

		# build intervals and directions from solution
		for i in [n+1 for n in range(len(solution) - 1)]:
			intervals.append(sol[i] - sol[i-1])
			if sol[i] < sol[i-1]:
				directions.append(down)
			elif sol[i] > sol[i-1]:
				directions.append(up)
			else:
				directions.append(same)

		abs_intervals = [abs(n) for n in intervals]

		# incentivize varied contour and intervalls
		if len(solution) >= 5:
			score += interval_variety[len(util.compress(abs_intervals))]
			score += direction_variety[len(util.compress(directions))]

		# slight penalization for repeating notes
		if directions.count(same) > 2:
			score -= directions.count(same)

		# slightly incentivize small intervals over large ones
		score += np.dot([abs_intervals.count(i+1) for i in range(12)], interval_weights)

		# disincentivize leaps larger than an octave
		for interval in abs_intervals:
			if interval in theory.large_leap:
				score -= 3

		# incentivize a downward or upward line
		pitch_diff = sum(intervals)
		if pitch_diff > 12:
			score += 2
		elif pitch_diff > 7:
			score += 2
		elif pitch_diff > 3:
			score += 1
		return score


	def register(self, solution):
		"""
		penalities notes outside the desired register
		"""
		score = 0
		for note in solution:
			if note.get_pitch() not in theory.register:
				score -= 100
		return score


	def distance(self, solution):
		"""
		very simple distance function for evaluation scoring. Simply
		encourages smaller steps over larger ones. Can be used for
		finding a very simple resolution pitch for a solution
		"""
		score = 0
		assert(len(solution) >= 2)
		intervals = []
		sol = util.make_pitches(solution)

		curr_p = sol[0]
		for next_p in sol[1:]:
			intervals.append(abs(curr_p - next_p))
		return sum([2/x if x != 0 else -.2 for x in intervals])


if __name__ == "__main__":
	G7 = util.build_chord('G', 'I', '7')
	C7 = util.build_chord('C', 'I', 'M7')
	sub = subproblem(G7)
	notes = search_solver(sub).get_solution()
	util.write_midi(solo=notes, chords=[G7])
