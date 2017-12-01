# jazz-bot: search.py

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
    # Feature Evaluation Functions #
    ################################

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
			score -= directions.count(sames)

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
	P = search_solver(G7)
	print "First example:"
	print P.tonality(P.get_sample_G7_solution1())
	print P.contour(P.get_sample_G7_solution1())
	print
	print "Second example:"
	print P.tonality(P.get_sample_G7_solution2())
	print P.contour(P.get_sample_G7_solution2())
	# print P.chord.get_chord_tones()
	# util.write_midi(solo=P.get_sample_G7_solution(), chords=[P.chord])
