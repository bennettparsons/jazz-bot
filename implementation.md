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

Since there will certainly be some kind of underlying probabilistic model, we will need some notion of a ``state''. This is also a requisite for general RL. Below are some possible representations of state:

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

After thinking about this more, I think we need to make a decision between using markov/MDPs or RL. Basically the question is this: should we try to build the model ourselves by just thinking about music theory (ie assign probabilities and rewards to transitions -- there will be a lot of these though) or should we try to learn these from scratch using smart evaluation functions that will return an appropriate reward for a given transition. Might actually help if we discretize the space hierarchically using something like [Idea 4](Idea-4).

## Output to MIDI?

Should be pretty simple using [this](https://pypi.python.org/pypi/MIDIUtil/) python midi library. Look at [this guy's code](https://github.com/ckdotca/JSB2/blob/master/JSB2.py) for inspiration on how to use this library to generate chords and melodies.
