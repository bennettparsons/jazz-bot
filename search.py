# jazz-bot: search.py

import random, copy
import util
from problems import subproblem
import numpy as np

class search_solver(subproblem):
	"""
	defines evaluation functions for a local search solution to the
	subproblem, and solves the problem using local search
	"""

	def __init__(self, chord):
		self.chord = chord
		self.solution = self.get_solution()

	def get_solution(self):
		"""
		generate a solution: a sequence of notes that obeys the 
		requirements of the subproblem and can be subjected to 
		the feature evaluation functions
		"""
		return self.get_sample_G7_solution2()

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
		# initialize
		curr_soln = util.make_notes([self.chord.get_root().get_pitch()+24] * 8) # TBU

		n = 100
		climbed = 1 # flag if an iteration changes, so don't have to recompute the evaluation
		curr_soln_val = 0

		for _ in range(n):

			if climbed:
				curr_soln_val = self.ensemble_evaluate(curr_soln)
			climbed = 0

			# get neighbor node
			candidate_soln = self.get_neighbor_node(curr_soln)

			# accept with probability 1 if climbs up
			if self.ensemble_evaluate(candidate_soln) > curr_soln_val:
				curr_soln = candidate_soln
				climbed = 1
				continue

			# accept with probability <1 if climbs down
			# should be proportional to size of change but not sure what distance metric makes sense rn
			if random.random() < 0.1:
				curr_soln = candidate_soln
				climbed = 1

		return curr_soln


	def get_neighbor_node(self, soln, pitch_sd=3):
		"""
			implements a naive approach for retrieving neighbors

			1 s.d. corresponds to 3 half-steps ? we can tweak however
		"""

		# sample a single note
		i = random.choice(range(len(soln)))

		# sample notes to replace this note
		pitch = soln[i].get_pitch()
		proposed_pitch = int(random.gauss(pitch, pitch_sd))

		# python is pass by ref right?
		proposed_soln = copy.copy(soln)
		proposed_soln[i] = util.make_notes([proposed_pitch])[0] # ew
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
		generations = 1000

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
		return sorted(population, key=lambda individual: self.get_fitness(individual), reverse=True)[0]

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
			simply additive for the time being
		"""

		return self.tonality(soln) + self.contour(soln)


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

		for note in solution:
			if tension and self.chord.is_tension_resolution((tension, note.as_letter())):
				score += 5
			tension = None
			letter = note.as_letter()
			if self.chord.is_third_or_seventh(letter):
				score += 3
			elif self.chord.is_chord_tone(letter):
				score += 2
			elif self.chord.is_in_scale(letter):
				score += 1
			elif self.chord.is_tension(letter):
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
		score = 0

		# heuristics
		interval_variety = {1:0, 2:0, 3:1, 4:3, 5:3, 6:2, 7:1, 8:1}
		direction_variety = {1:0, 2:2, 3:3, 4:3, 5:2, 6:1, 7:1, 8:1}
		interval_weights = [.5, .4, .3, .3, .3, .2, .2, .1]

		sol = util.make_pitches(solution)
		up = "up"
		down = "down"
		same = "same"
		intervals = []   # intervals
		directions = []   # recent interval direction (up or down)

		# build intervals and directions from solution
		for i in [n+1 for n in range(7)]:
			intervals.append(sol[i] - sol[i-1])
			if sol[i] < sol[i-1]:
				directions.append(down)
			elif sol[i] > sol[i-1]:
				directions.append(up)
			else:
				directions.append(same)

		print intervals
		print directions

		abs_intervals = [abs(n) for n in intervals]

		# incentivize varied contour and intervalls
		score += interval_variety[len(util.compress(abs_intervals))]
		score += direction_variety[len(util.compress(directions))]

		# slight penalization for repeating notes
		if directions.count(same) > 2:
			score -= directions.count(same)

		# slightly incentivize small intervals over large ones
		score += np.dot([abs_intervals.count(i+1) for i in range(8)], interval_weights)

		# incentivize a downward or upward line
		pitch_diff = sum(intervals)
		if pitch_diff > 12:
			score += 3
		elif pitch_diff > 7:
			score += 2
		elif pitch_diff > 3:
			score += 1
		return score



if __name__ == "__main__":
	G7 = util.build_chord('G', 'I', '7')
	C7 = util.build_chord('C', 'I', 'M7')
	P1 = search_solver(G7)
	P2 = search_solver(C7)
	util.write_midi(solo=P1.GA() + P2.GA(), chords=[P1.chord, P2.chord])
