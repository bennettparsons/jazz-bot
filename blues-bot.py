#!/usr/local/bin/python

"""

	script to run the blues bot!

"""

import argparse
import util, theory
from search import subproblem, search_solver
from problems import problem

def build_cli():
	parser = argparse.ArgumentParser(description='Run the blues bot!', epilog='By Bennett Parsons, Jeremy Welborn')

	parser.add_argument('-a', '--algorithm', action='store', choices=['SA', 'GA'], default='SA',
						help='run with simulated annealing (SA) or a genetic algorithm (GA)')
	parser.add_argument('-k', '--key', action='store', default='C',
						choices=['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab'],
						help='specify the key, like C or Db')
	parser.add_argument('-p', '--progression', action='store', nargs='+', 
						default="I 7 I 7 I 7 I 7 IV 7 IV 7 I 7 I 7 V 7 IV 7 I 7 V 7",
						help='specify a sequence of numerals and qualities for the progression, separated by spaces')
	parser.add_argument('-n', '--number_choruses', action='store', default='1', type=int,
						help='specify the number of choruses to compose')
	parser.add_argument('-f', '--filename', action='store', default='blues-bot-solo',
						help='specify the midi file to write to')

	return parser 
	



if __name__ == '__main__':

	args = build_cli().parse_args()

	# extract from command-line
	alg = args.algorithm
	key = args.key
	prog = args.progression.split()
	prog_tuples = [(prog[i], prog[i+1]) for i in range(0, len(prog), 2)]
	n = args.number_choruses
	filename = args.filename

	# build a blues solo, write it 
	progression = util.build_progression(key, prog_tuples)

	util.write_midi(solo=problem(progression, alg=alg, choruses=n, res_chord=progression[0]).get_solo(),
					# chords=progression*n + [util.build_chord('D', 'I', '7')])
					chords=progression*n + [progression[0]], outfile=filename+'.mid')

	

	
	