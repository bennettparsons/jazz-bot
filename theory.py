# jazz-bot.py: music_theory.py

keys = {'A':45, 'Bb':46, 'B':47, 'C':48, 'Db':49, 'D':50,
 		'Eb':51, 'E':52, 'F':53, 'Gb':54, 'G':55, 'Ab':56}

numerals = {'I':0, 'bII':1, 'II':2, 'III':4, 'IV':5, 'bV':6,
			'V':7, 'bVI':8, 'VI': 9, 'bVII':10, 'VII': 11}

qualities = {'M': [0,4,7], 'm': [0,3,7], 'M7': [0,4,7,11], 
		'm7': [0,3,7,10], '7': [0,4,7,10]}

tensions = {
			'M': [], 
			'm': [], 
			'M7': [], 
			'm7': [], 
			'7': [(1,0), (3,4), (6,5), (8,9)]  # b9, #9, #11, b13
		   }

scales = {
		  'M': [], 
		  'm': [], 
		  'M7': [], 
		  'm7': [], 
		  '7': [0,2,4,5,7,9,10,11]   # bebop scale
		 }

# useful intervals
second = [1,2]
third = [3,4]
fourth = [5]
tritone = [6]
fifth = [7]
sixth = [8,9]
sevneth = [10,11]

large_leap = [n+13 for n in range(50)]

# play notes from this range for solo
register = [n+56 for n in range(45)]
