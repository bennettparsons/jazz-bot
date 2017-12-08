#!/usr/local/bin/python

"""
	short script to compare "score" per note in our 2 implementations
"""

import numpy as np
import os # subprocess is probably preferable for working with child processes, but this is a bit quicker

def score(alg):
	with open(alg+"-results.txt", "r") as f:
		results = f.readlines() # list of lines

		# Score of: 16.6 for 5 notes
		scores = []
		num_notes = []

		for result in results:
			scores.append(float(result.split()[2]))
			num_notes.append(int(result.split()[4]))

		# print "Average score / note for " + alg + ":"
		# print sum(scores) / sum(num_notes) # float / int 
		return sum(scores) / sum(num_notes) # float / int  


# this script will take some time
if __name__ == "__main__":
	SA_scores = []
	GA_scores = []

	
	os.system("for i in `seq 1 100`; do (python -W ignore blues-bot.py -a SA); done > SA-results.txt")
	SA_scores.append(score("SA")) 
	
	os.system("for i in `seq 1 100`; do (python -W ignore blues-bot.py -a GA); done > GA-results.txt")
	GA_scores.append(score("GA"))

	print "Avg score / note for SA:"
	print np.average(SA_scores)

	print "Avg score / note for GA:"
	print np.average(GA_scores)

	print "Of course, SA and GA can be tuned. This is for rough intuition on the particular parameters we've been working with."
		
