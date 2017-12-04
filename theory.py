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
seventh = [10,11]

large_leap = [n+13 for n in range(50)]

# play notes from this range for solo
register = [n+56 for n in range(45)]

######################################
# Feature Evaluation Function Params #
######################################


# indexed by solution size
params = {
"tonality":
	[
		{	# size = 1
			"tension": 1,
			"third_or_seventh": 2,
			"chord_tone": 2,
			"scale": 1.8
		},
		{	# size = 2
			"tension": 1,
			"third_or_seventh": 2,
			"chord_tone": 2,
			"scale": 1.8
		},
		{	# size = 3
			"tension": 1,
			"third_or_seventh": 2,
			"chord_tone": 2,
			"scale": 1.8
		},
		{	# size = 4
			"tension": 1,
			"third_or_seventh": 2,
			"chord_tone": 2,
			"scale": 1.8
		},
		{	# size = 5
			"tension": 1,
			"third_or_seventh": 2,
			"chord_tone": 2,
			"scale": 1.8
		},
		{	# size = 6
			"tension": 1,
			"third_or_seventh": 2,
			"chord_tone": 2,
			"scale": 1.8
		},
		{	# size = 7
			"tension": 5,
			"third_or_seventh": 4,
			"chord_tone": 3,
			"scale": 2
		},
		{	# size = 8
			"tension": 5,
			"third_or_seventh": 4,
			"chord_tone": 3,
			"scale": 2
		},
	],
"contour": 
	[
		{},
		{	# size = 2
			"interval_variety": {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0},
			"direction_variety": {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0},
			"interval_weights": [1.2, 1.2, 1.4, 1.4, 1.2, .8, 1, .5, .5, -.2, -.3, .2],
			"same": [0],
			"large_leap": -3,
			"line": (0,0,0)
		},
		{	# size = 3
			"interval_variety": {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0},
			"direction_variety": {1:.5, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0},
			"interval_weights": [1.2, 1.2, 1.4, 1.4, 1.2, .8, 1, .5, .5, -.2, -.3, .2],
			"same": [0,0],
			"large_leap": -3,
			"line": (0,0,.4)
		},
		{	# size = 4
			"interval_variety": {1:0, 2:.5, 3:.5, 4:0, 5:0, 6:0, 7:0, 8:0},
			"direction_variety": {1:.5, 2:8, 3:.5, 4:0, 5:0, 6:0, 7:0, 8:0},
			"interval_weights": [1.2, 1.2, 1.4, 1.4, 1.2, .8, 1, .5, .5, -.2, -.3, .2],
			"same": [0,0,0],
			"large_leap": -3,
			"line": (0,.4,.7)
		},
		{	# size = 5
			"interval_variety": {1:0, 2:.5, 3:.5, 4:.3, 5:0, 6:0, 7:0, 8:0},
			"direction_variety": {1:.5, 2:.7, 3:.4, 4:.1, 5:0, 6:0, 7:0, 8:0},
			"interval_weights": [1.2, 1.2, 1.4, 1.4, 1.2, .8, 1, .5, .5, -.2, -.3, .2],
			"same": [0,0,0,1],
			"large_leap": -3,
			"line": (0,1,1)
		},
		{	# size = 6
			"interval_variety": {1:0, 2:0, 3:.6, 4:.5, 5:.3, 6:0, 7:0, 8:0},
			"direction_variety": {1:.5, 2:1.2, 3:1.3, 4:1, 5:.5, 6:0, 7:0, 8:0},
			"interval_weights": [1.2, 1.2, 1.4, 1.4, 1.2, .8, 1, .5, .5, -.2, -.3, .2],
			"same": [0,0,.5,1,2],
			"large_leap": -3,
			"line": (1,1,1)
		},
		{	# size = 7
			"interval_variety": {1:0, 2:0, 3:.8, 4:2.4, 5:2.6, 6:1, 7:0, 8:0},
			"direction_variety": {1:0, 2:2, 3:3, 4:3, 5:2, 6:1, 7:1, 8:0},
			"interval_weights": [1, .8, .6, .5, .3, .2, .1, 0, -.1, -.2, -.3, .2],
			"same": [0,0,1,2,3,4],
			"large_leap": -3,
			"line": (1.5,2,2)
		},
		{	# size = 8
			"interval_variety": {1:0, 2:0, 3:1, 4:3, 5:3, 6:2, 7:1, 8:0},
			"direction_variety": {1:0, 2:2, 3:3, 4:3, 5:2, 6:1, 7:1, 8:0},
			"interval_weights": [1, .8, .6, .5, .3, .2, .1, 0, -.1, -.2, -.3, .2],
			"same": [0,0,1,2,4,6,8],
			"large_leap": -3,
			"line": (1.8,2,1.8)
		},
	],
"distance":
	[{},{},{},{},{},{},{},{}]
}










