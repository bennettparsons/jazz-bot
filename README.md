# Blues-bot
Trainingless jazz improvisor, using heuristics and local search algorithms

## Requirements

* Only been tested on MacOS, but should work on Linux as well
* Python MidiUtil library: install with `pip install MIDIUtil`

## Running the Code

* Clone [this](https://github.com/bennettparsons/jazz-bot) repository
* Run `python blues-bot.py -h` to start getting bluesy!
* Output will be a MIDI file

## Algorithms

This bot improvises over a given form consisting of one chord per measure. A solo is generated one measure at a time, using local search guided by hand crafted [heuristic functions](#feature-evaluation-functions). `search.py` implements two local search algorithms: simulated annealing and a genetic algorithm.

## Feature Evaluation Functions
We currently use two feature evaluation functions, which act on "solutions" to a given measure. Their sum is used as the evaluation function guiding local search. The weightings of the parameters discussed below vary with the "size" of the subproblem (i.e. how many notes will be played in the measure). These weights are hard-coded in `theory.py`

### Tonality
How well does the solo use chord tones (3rds and 7ths) as well as tensions? These ratings will be determined largely from the accepted jazz theory of how to solo over particularly kinds of chords. The hierarchy is roughly as follows:

1. 3rds and 7ths of chord
2. tension (provided it resolves correctly) 
3. any chord tone
4. any note within the scale
5. any note not in the above

### Contour
How well does the solo capture the concept of a musical line? There should not be very many large intervallic leaps, and there should be an interesting mix of rising and falling lines. Our implementation does the following, with no particular hierarchy:

* incentivize varied contour (rising and falling notes) and intervals
* slightly incentivize small intervals over large ones
* slight penalization for repeating notes
* disincentivize leaps larger than an octave
* incentivize a general downward or

## Code
`util.py` contains helper functions for manipulating musical objects and for interfacing with the `MidiUtil` library

`theory.py` contains definitions and dictionaries for the theory concepts the code relies on as well as hard-coded values for our feature evaluation functions

`structures.py` contains classes for a \texttt{Note} and a \texttt{Chord} that are amenable for MIDI


`problems.py` contains a class for our proposed problem representation, i.e. a sequence of subproblems which are measures of one and only one chord

`search.py` contains the implementation of our search algorithms as well as the heuristics they rely on
