# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
from game import Agent
from math import inf

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foodList = newFood.asList()
        foodDist = []
        ghostDist = []
        # Evaluation score
        score = 0

        # Manhattan distance to every food
        for f in foodList:
            foodDist.append(manhattanDistance(newPos, f))

        # Manhattan distance to every ghost
        for g in newGhostStates:
            ghostDist.append(manhattanDistance(newPos, g.getPosition()))

        # Higher scores for closest dots
        for dist in foodDist:
            if dist <= 2:
                score += 1
            elif 2 < dist <= 10:
                score += 0.5
            else:
                score += 0.25

        # Low score if a ghost is near
        for i in newGhostStates:
            # Considering a dangerous ghost radius equals 4
            if min(ghostDist) < 4:
                score -= 1

        # Add score to total evaluation
        return childGameState.getScore() + score


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        # MAX-VALUE function
        def maxvalue(gameState, depth):
            depth += 1  # Every MAX move is the start of the new depth
            pacActions = gameState.getLegalActions(0)
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            V = -inf
            for action in pacActions:
                nextState = gameState.getNextState(0, action)
                V = max(V, minvalue(nextState, depth, 1))
            return V

        # MIN-VALUE function
        def minvalue(gameState, depth, agentIndex):
            no_ghosts = gameState.getNumAgents() - 1  # Agent 0 is pacman
            ghostActions = gameState.getLegalActions(agentIndex)
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            V = +inf
            for action in ghostActions:
                nextState = gameState.getNextState(agentIndex, action)
                if agentIndex == no_ghosts:  # If every ghost made a move, pacman plays
                    V = min(V, maxvalue(nextState, depth))
                else:  # One MIN layer suggests ALL ghosts make a move
                    V = min(V, minvalue(nextState, depth, agentIndex + 1))
            return V

        # MINIMAX-DECISION
        def minimax(gameState):
            # Start the game
            pacActions = gameState.getLegalActions(0)
            score = -inf
            move = None
            for action in pacActions:
                nextState = gameState.getNextState(0, action)
                value = minvalue(nextState, 0, 1)
                if value > score:
                    move = action
                    score = value
            return move

        return minimax(gameState)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # MAX-VALUE function
        def maxvalue(gameState, depth, a,  b):
            depth += 1  # Every MAX move is the start of the new depth
            pacActions = gameState.getLegalActions(0)
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            V = -inf
            for action in pacActions:
                nextState = gameState.getNextState(0, action)
                V = max(V, minvalue(nextState, depth, a, b, 1))
                if V > b:
                    return V
                a = max(a, V)  # Update a
            return V

        # MIN-VALUE function
        def minvalue(gameState, depth, a, b, agentIndex):
            no_ghosts = gameState.getNumAgents() - 1
            ghostActions = gameState.getLegalActions(agentIndex)
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            V = +inf
            for action in ghostActions:
                nextState = gameState.getNextState(agentIndex, action)
                if agentIndex == no_ghosts:
                    V = min(V, maxvalue(nextState, depth, a, b))
                    if V < a:
                        return V
                    b = min(b, V)
                else: # One MIN layer suggests ALL ghosts make a move
                    V = min(V, minvalue(nextState, depth, a, b, agentIndex + 1))
                    if V < a:
                        return V
                    b = min(b, V)  # Update b
            return V

        # ALPHA-BETA PRUNING
        def alphabeta(gameState):
            # Start the game
            pacActions = gameState.getLegalActions(0)
            score = -inf
            a = -inf
            b = +inf
            move = None
            for action in pacActions:
                nextState = gameState.getNextState(0, action)
                value = minvalue(nextState, 0, a, b, 1)
                if value > score:
                    move = action
                    score = value
                if value > b:
                    return move
                a = max(a, value)  # Update a
            return move
        
        return alphabeta(gameState)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        # MAX-VALUE function
        def maxvalue(gameState, depth):
            depth += 1 # Every MAX move is the start of a new depth
            pacActions = gameState.getLegalActions(0)
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            V = -inf
            for action in pacActions:
                nextState = gameState.getNextState(0, action)
                V = max(V, minvalue(nextState, depth, 1))
            return V

        # MIN-VALUE function including CHANCE LEVEL
        def minvalue(gameState, depth, agentIndex):
            no_ghosts = gameState.getNumAgents() - 1
            ghostActions = gameState.getLegalActions(agentIndex)
            no_ghostActions = len(ghostActions)
            total_chance = 0
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            for action in ghostActions:
                nextState = gameState.getNextState(agentIndex, action)
                if agentIndex == no_ghosts:
                    chance = maxvalue(nextState, depth)
                else:
                    chance = minvalue(nextState, depth, agentIndex + 1)
                total_chance += chance
            return total_chance/no_ghostActions

        # EXPECTIMAX DECISION
        def expectimax(gameState):
            # Start the game
            pacActions = gameState.getLegalActions(0)
            score = -inf
            move = None
            for action in pacActions:
                nextState = gameState.getNextState(0, action)
                value = minvalue(nextState, 0, 1)
                if value > score:
                    move = action
                    score = value
            return move

        return expectimax(gameState)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    ~~~ Same evaluation function as in q1, plus the feature of computing scared times
    for ghosts, after pacman eats a capsule ~~~
    """
    "*** YOUR CODE HERE ***"
    # Useful information
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    foodList = newFood.asList()
    foodDist = []
    ghostDist = []
    ScaredTimes = sum(newScaredTimes)
    # Evaluation score
    score = 0

    # Manhattan distance to every food
    for f in foodList:
        foodDist.append(manhattanDistance(newPos, f))

    # Manhattan distance to every ghost
    for g in newGhostStates:
        ghostDist.append(manhattanDistance(newPos, g.getPosition()))

    # Higher scores for closest dots
    for dist in foodDist:
        if dist <= 2:
            score += 1
        elif 2 < dist <= 10:
            score += 0.5
        else:
            score += 0.25

    # Low score if a ghost is near
    for i in newGhostStates:
        if ScaredTimes > 0:
            score += 20
        # Considering a dangerous ghost radius equals 4
        if min(ghostDist) < 4:
            score -= 1

    return currentGameState.getScore() + score

# Abbreviation
better = betterEvaluationFunction
