# jazz-bot: qlearning.py

import util

# stolen from Berklee! also check out BERKLEE-ValueIterationAgents.py 
#	to see if we can adapt that to our problem
class mdp:

    def getStates(self):
        """
        Return a list of all states in the MDP.
        Not generally possible for large MDPs.
        """
        abstract

    def getStartState(self):
        """
        Return the start state of the MDP.
        """
        abstract

    def getPossibleActions(self, state):
        """
        Return list of possible actions from 'state'.
        """
        abstract

    def getTransitionStatesAndProbs(self, state, action):
        """
        Returns list of (nextState, prob) pairs
        representing the states reachable
        from 'state' by taking 'action' along
        with their transition probabilities.

        Note that in Q-Learning and reinforcment
        learning in general, we do not know these
        probabilities nor do we directly model them.
        """
        abstract

    def getReward(self, state, action, nextState):
        """
        Get the reward for the state, action, nextState transition.

        Not available in reinforcement learning.
        """
        abstract

    def isTerminal(self, state):
        """
        Returns true if the current state is a terminal state.  By convention,
        a terminal state has zero future rewards.  Sometimes the terminal state(s)
        may have no possible actions.  It is also common to think of the terminal
        state as having a self-loop action 'pass' with zero reward; the formulations
        are equivalent.
        """
        abstract

# this is what we actually want to fill out!
class mdp_solver(subproblem):
	"""
	defines evaluation functions for an mdp approach to the 
	subproblem, and solves the problem using value iteration
	"""

	def get_state(self):
		"""
		return current state: within this subproblem, state 
		is simply the current note
		"""

	def get_qvalue(self, state, action):


	################################
    # Feature Evaluation Functions #
    ################################

    def tonality(self):
    	"""
    	put implementation notes here
    	"""
    	pass

    def contour(self):
    	"""
    	put implementation notes here
    	"""
    	pass