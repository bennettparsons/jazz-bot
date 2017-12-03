# How are we going to build this?

## What is a Note

Attributes:

* Midi Pitch Value
* Duration (rhythmic value)

Note that we can easily convert between Midi pitch numbers and note letter name / octave pairs.

Member Functions:

```
transpose(steps, up=True)
change_duration(n)     # multiply duration by factor of n
```

## What is a Chord?

Attributes:

* num_pitches
* type (major, minor, dominant, dimished, min6, etc.)
* list of consituent pitches
* inversion?

Member Functions:

```
get_root()
get_fifth()
get_chord_tones()
get_tensions()
get_clashing()
get_scale()
invert(steps, up=True)
transpose(steps, up=True)
```


## What is a State?

Since there will certainly be some kind of underlying probabilistic model, we will need some notion of a "state". This is also a requisite for general RL. Below are some possible representations of state:

1. Simplest
	* Chord + Note
	* Each state will be dependent on previous k
	* Advantages: concise, easy to work with
	* disadvantages: probably to many possible states to accurately explore

2. More Abstract
	* Chord + short sequence of notes
	* notes must be related in some way:
		- arpeggiation
		- embellishment of a pitch (neighbor tones)
		- a short, distinctive lick
		- target pitch (this could be the defining feature)

3. Most Abstract
	* Chord + Musical Idea
	* idea is probably just a phrase
	* phrase would have many attributes:
		- length
		- density
		- type of cadence
		- melodic contour
	* this would help high level coherency of produced solos

4. Combine the Above?
	* would it be possible to have a hierarchal state model?
	* surely states of type 3. are composed of those of type 2. and 1.
	* how could we leverage this hierarchy to influence learning?

### Discussion

#### Idea 1

words

#### Idea 2

words

#### Idea 3

This makes most sense with Idea 4.

#### Idea 4
We could have 3 phases of learning, which builds the solo in the same way one would build a house: start with the foundation, add important supporting features, then fill in the details. This would enable us to leverage different musical ideas, and separate them logically. More specifically, we could apply different evalutation functions to each phase: enforce different phrase lengths, and varied contours in phase 3, enforce different kinds of embellishment in phase 2, and choose accurate, tonal notes for phase 1. Thus, we discretize the solo into logical, musical chunks, and compose one chunk at a time given a set of requirements. For instance, one phase will have to decide how to write a particular phrase given the set phrase length, cadence type, and contour dictated by the previous phase, and the last phase will have to select the appropriate approach tones to get from one chord tone to the next.

This is a very interesting theoretical approach. Since we are simulating improvisation, it may not make sense to think in these grand terms. At the same time, the best solos evolve to be coherent when viewed through any lens. This approach blurs the distinction between improvisation and composition.

## Putting it all Together: Algorithms

THIS IS THE IMPORTANT PART!!!

### initial thoughts

After thinking about this more, I think we need to make a decision between using markov/MDPs or RL. Basically the question is this: should we try to build the model ourselves by just thinking about music theory (ie assign probabilities and rewards to transitions -- there will be a lot of these though) or should we try to learn these from scratch using smart evaluation functions that will return an appropriate reward for a given transition. Might actually help if we discretize the space hierarchically using something like [Idea 4](#idea-4).

### combination of above in hierarchal approach

I worry that using straight RL will not give our bot enough variation. RL is an optimization technique, which tries to compute the optimal policy. There is no optimal policy in music. So we could apply RL to only certain layers in the hierchal approach. That is, when we do the first layer which just maps out the structure and important goal tones of the solo, we could just use some simple, sufficiently random markov model we come up with ourselves. Then, given this data, we could use RL to smartly build phrases subject to these given parameters.

### but what's the SIMPLEST approach we can start with?

Let's first solve the following simple subproblem: compose a melody over one measure (one chord). Use just eighth notes, no rests. Write a continuous melody that seeks to maintain the following attributes (or equivalently, minimize penalties): 1) plays chord tones 2) roughly scalar (not large intervallic leaps) 3) smooth contour (rising and falling). But how?

#### Straight up Qlearning

Model off Berekely pacman qlearning setup, and try to write smart reward functions. A state is just a single eighth note. Use dynamic programming. Make sure to use a "soft max" when extracting a policy from qvals so that we end up mapping states to a distribution of actions, rather than a single action.

* Reward functions take in only current state and next state

#### Probabilistic: build as we go

Somehow easier solution (smaller complexity). Choose start state (may be fixed by hierarchy/Black Box). Using reward functions, calculate soft max policy for next states to transition to. Sample from this distribution. Repeat, except at each step, leverage entire past. Once we reach the end of the measure, just return what we have.

* Reward functions take in current state and entire past

##### Advantages (vs. RL)

* can condition on entire past
* faster
* more probabilistic - higher variance

##### Disadvantages

* can't improvise in real time; the biggest advantage of RL is that once it learns the model, it could conceivably improvise in really time, just by sampling from the learned, probabilistic policy function
* not "complete"; doesn't find optimal solution according to our reward functions
* this actually might be good though, since we know we cannot perfectly capture the notion of "good" music with our handmade rewards

#### Local Search

Use the solution return by the probabilistic approach as the input to a local search problem. Engineer smart neighbor function. Can use straight hill climbing, beam search or simulated annealing. Could even imagine applying a genetic algorithm with a smart cross-over function

* reward functions act on entire realization of melody (for the measure)

##### Advantages (vs. probabilitic)

* pretty much strictly better, since it starts with that solution
* the real win is that it is more natural to define reward functions that act on entire realization of a melody. Two notes don't really mean anything by themselves. But with 8 whole eighth notes, you can start to extract some more meaningful musical qualities.

## Feature Evaluation Functions

Here we discuss ways to implement some of the feature functions we allude to in `ideas.md`. One simple way of aggregating feature functions would be to carry around a weighting of states

### Tonality

On the simplest blues form, we just use dominant chords. Check out [this](https://www.jazzadvice.com/v7-to-i-10-options-for-expanding-your-dominant-7th-vocabulary/) site for ideas on how to weight specific 

## Output to MIDI?

Should be pretty simple using [this](https://pypi.python.org/pypi/MIDIUtil/) python midi library. Look at [this guy's code](https://github.com/ckdotca/JSB2/blob/master/JSB2.py) for inspiration on how to use this library to generate chords and melodies.

UPDATE: it's definitely easy (see `midi_test.py`)

# Thoughts

* Specifically, randomness in neighbor function needs to be fixed; we should also start off the local search with a more intuitive solution: done!
* Still need to link measures together by finishing to implement fixed notes: done!
* Still need to introduce more variation through different evaluation functions (maybe multiple weights of tonality)
* Rhythm!!!
* could pre-process fixed notes to make a larger line

## knobs

* I think, 200 iterations seems to be pretty good for the basic hill climbing
* initializing next solution with previous is a pretty good idea! With this, we can add to the subproblems a heuristic that encourages or discourages similarity to the previous bar (or parts of the bar)
* resolution feature is good, but needs notion of history: keeps returning the same solution! Could introduce a history that disincentivizes repition, or just sample out certain possible resolutions in classic, random fashion
* making it more tonal is pretty sick

## specific TODOs:

* fix resolution so that it is probabilistic
* implement rhythm: could just sample from outputted eighth notes?
* notion of choruses: denseness of rhythms should be a function of this, as well as feature functions e.g. tonality, whether or not to initialize with previous solution (this should reset at certain points)

