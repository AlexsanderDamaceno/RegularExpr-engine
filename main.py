class State:

	def __init__(self , isEnd):
		self.IsEnd = isEnd 
		self.Transitions = {}
		self.EpsilonTransitions = [] 

class  NFA: 
     def __init__(self , start ,  end): 
        self.start = start 
        self.end   = end



def addTransition(source , destination  , symbol):
      source.Transitions[symbol] = destination

def addEpsilonTransition(source , destination): 
      source.EpsilonTransitions.append(destination)

 
def FromEpsilon():
      source      =  State(False) 
      destination =  State(true)
      addEpsilonTransition(source , destination)  
      return NFA(source , destination)   


def FromSymbol(symbol):
      source      =  State(False) 
      destination =  State(True)
      addTransition(source , destination , symbol)
      return NFA(source , destination)         


def concat(nfa1 , nfa2):
	  addEpsilonTransition(nfa1.end   ,  nfa2.start)
	  nfa1.end.isEnd = False
	  return NFA(nfa1.start , nfa2.end)

def union(nfa1 , nfa2): 
    start  = State(False) 
    addEpsilonTransition(start ,  nfa1.start)
    addEpsilonTransition(start  , nfa2.start)
    nfa1.end.IsEnd  = False

    end = State(True) 
    addEpsilonTransition(nfa1.end , end)
    addEpsilonTransition(nfa2.end , end)
    nfa2.isEnd = False
    return NFA(start , end)


def closure(nfa1):
  start  = State(False)
  end    = State(True)
  addEpsilonTransition(start , end)
  addEpsilonTransition(start , nfa1.start)
  addEpsilonTransition(nfa1.end , end)
  addEpsilonTransition(nfa1.end , nfa1.start)
  nfa1.end.isEnd = False 
  return  NFA(start , end)


def ToNFA(postfixExp):
  if postfixExp == ' ':
  	return FromEpsilon()

  stack = [] 

  for token in postfixExp: 
         if token == '*': 
             stack.append(closure(stack.pop()))	
         elif token == '|':
              right = stack.pop()
              left  = stack.pop()
              stack.append(union(left , right))
         elif token ==  '.':
              right = stack.pop() 
              left  = stack.pop()
              stack.append(concat(left , right))
         else: 
              stack.append(FromSymbol(token))     
               	

  return stack.pop()



def addNextState(state , nextStates , visited):
  	if len(state.EpsilonTransitions):
  	    for state in state.EpsilonTransitions:
  	        if not (state in visited):
  	        	visited.append(state)
  	        	addNextState(state ,  nextStates , visited)
  	else:
                nextStates.append(state)



def search(nfa , word):
     currentStates = []
     addNextState(nfa.start , currentStates , [])
     for token in word: 
	  	  nextStates = []
	  	  for state  in currentStates:
              
	  	  	    nextState =   state.Transitions.get(token)
	  	  	    if nextState: 
	  	  	       addNextState(nextState , nextStates , [])
	  	  currentStates = nextStates

     for x in currentStates:
       if x.IsEnd == True:
      	  return True
     
     

     return False 	 



              


nfa = ToNFA('ab*|')
print(search(nfa , 'bbbbb'))
