"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 74].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.18].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())


  nextState = (nextx, nexty)
  action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]

  successors.append( ( nextState, action, cost) )
  """
  "*** YOUR CODE HERE ***"
  frontier = util.Stack()
  start = problem.getStartState()
  explored = set()
  
  #Put the successor of start_state in frontier
  for start_leaf in problem.getSuccessors(start):
      frontier.push([start,start_leaf[0],start_leaf[1]])

  # Put all expanded path in sub_result
  # at the end, according to the goal state to select the real path from it
  sub_result = []
  explored.add(start)

  while (not frontier.isEmpty()):
      state = frontier.pop()
      state_node = state[1] #this is the successor node of state which is exploring now
      if (problem.isGoalState(state_node)):
          sub_result.append(state)
          break
      if (state_node not in explored):
          explored.add(state_node)
          sub_result.append(state)
          successors = problem.getSuccessors(state_node)
          for successor in successors:
              frontier.push([state_node,successor[0],successor[1]])
 # successor[0]: nextstate; successor[1] action 

  path = []
  while (state_node != start):
      for result in sub_result:
          if (result[1] == state_node):
              state_node = result[0]
              path.append(result[2])
              break
                
  path.reverse()
  return path
  util.raiseNotDefined()
          


def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 74]"
  "*** YOUR CODE HERE ***"
  frontier = util.Queue()
  start = problem.getStartState()
  explored = set()

  for start_leaf in problem.getSuccessors(start):
      frontier.push([start,start_leaf[0],start_leaf[1]])

  sub_result = []
  explored.add(start)

  while (not frontier.isEmpty()):
      state = frontier.pop()
      state_node = state[1]
      if (problem.isGoalState(state_node)):
          sub_result.append(state)
          break
      if (state_node not in explored):
          explored.add(state_node)
          sub_result.append(state)
          successors = problem.getSuccessors(state_node)
          for successor in successors:
              frontier.push([state_node,successor[0],successor[1]])
 # successor[0]: nextstate; successor[1] action 

  path = []
  while (state_node != start):
      for result in sub_result:
          if (result[1] == state_node):
              state_node = result[0]
              path.append(result[2])
              break
                
  path.reverse()
  return path
  util.raiseNotDefined()
          

      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  frontier = util.PriorityQueue()
  start = problem.getStartState()
  explored = set()
  item = []

  for start_leaf in problem.getSuccessors(start):
      item = [start, start_leaf[0],start_leaf[1],start_leaf[2]] #[0]nextnode,[1]action,[2]cost
      frontier.push(item, start_leaf[2])
  explored.add(start)
  
  sub_result = []
  path = []

  while (not frontier.isEmpty()):
      state = frontier.pop()  #only pop item
      sub_result.append([state[0], state[1], state[2]])
      state_node = state[1]
      if (problem.isGoalState(state_node)):
          break
      if (state_node not in explored):
          explored.add(state_node)
          for successor in problem.getSuccessors(state_node):
            cost = state[3] + successor[2]
            frontier.push([state_node, successor[0], successor[1], cost], cost)

  while (state_node != start):
      for result in sub_result:
          if (result[1] == state_node):
              state_node = result[0]
              path.append(result[2])
              break

  path.reverse()
  return path
  util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  frontier = util.PriorityQueue()
  start = problem.getStartState()
  explored = set()
  item = []

  for start_leaf in problem.getSuccessors(start):
      priority = start_leaf[2] + heuristic(start_leaf[0], problem) #loss this code will make mistake
      item = [start, start_leaf[0],start_leaf[1],start_leaf[2]] #[0]nextnode,[1]action,[2]cost
      frontier.push(item, priority)

  explored.add(start)
  sub_result = []
 

  while (not frontier.isEmpty()):
      state = frontier.pop()
      state_node = state[1]
      sub_result.append([state[0], state[1], state[2]])
      if (problem.isGoalState(state_node)):
          break
      if (state_node not in explored):
          explored.add(state_node)
          for successor in problem.getSuccessors(state_node):
              cost = state[3] + successor[2]
              frontier.push([state_node, successor[0], successor[1], cost], cost + heuristic(successor[0], problem))

  path = []
  while (state_node != start):
      for result in sub_result:
          if (result[1] == state_node):
              state_node = result[0]
              path.append(result[2])
              break
  path.reverse()
  return path
  util.raiseNotDefined()
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
