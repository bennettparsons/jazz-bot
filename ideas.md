## Can we generate music without a training set?

To accomplish this, we have to create models that enforce --- or simply encourage, since no rules and music are hard set --- musical patterns. Below are a list of features we could imagine selecting for using some kind of probabilistic model and/or evaluation function:

* tonality: this is quite broad in jazz, but we should start out with a tonal model, which uses chord tones (especially 3rds and 7ths) and tensions to navigate the changes of a form. We'll just stick to the blues form.
* melodic coherency: in jazz, most licks involve sequences of sequential notes. It would be bad if our improviser produces lots of really large intervallic leaps.
* rhythmic coherency: this one is difficult, since varied rhythms and syncopations are a huge aspect of soloing. However, we could start with trying to string together a logical sequence of eighth notes
* phrase structure: some balance of short and long phrases. Should not always have same phrase length!
* (add more!)

Assuming we have some success with the above, we could imagine tweaking those elements, and introducing some others to try and match different styles, or even come up with our own! For instance, we could pull back on tonality and coherency to try and emulate free jazz, or introduce a new element that determines how sparse the improvisation is, maybe to try and capture the feel of a ballad.

### Cool Idea: Center Around a Lick
What would be really neat is if we could input a small lick and have it produces variations on it. We could set up a pretty straight forward model for this capable of performing the following operations on the lick: repitition, ornamentation, inversion, extension, transposition, embellishment, etc. This is particularly useful, because most improvisations do this to the melody anyway!

If we find that generated solos not using this idea turn out to be uncompelling, we could try to infuse a random generation of a particular lick which the solo could be based off of. This could even be a means toward composition of an entire piece.
