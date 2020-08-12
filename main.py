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


def OneorMore(nfa1):
  start  = State(False)
  end    = State(True)
  addEpsilonTransition(start , nfa1.start)
  addEpsilonTransition(nfa1.end , end)
  addEpsilonTransition(nfa1.end , nfa1.start)
  nfa1.end.isEnd = False 
  return  NFA(start , end)


def zeroOrOne(nfa1):
   start  = State(False)
   end    = State(True)
   
   addEpsilonTransition(start , end);
   addEpsilonTransition(start , nfa1.start)
   addEpsilonTransition(nfa1.end , end)
   nfa1.end.isEnd = False 
   return NFA(start , end)


def ToNFA(postfixExp):
  if postfixExp == ' ':
  	return FromEpsilon()

  stack = [] 

  for token in postfixExp: 
         if   token == '*': 
              stack.append(closure(stack.pop()))	
         elif token == '+':
              stack.append(OneorMore(stack.pop()))
         elif token == '?':
              stack.append(zeroOrOne(stack.pop()))
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





def InsertConcatOperator(regex):
   
   new_regex = ''
   index = 0 
  
   for i in range(len(regex)):

        new_regex += regex[i]

        if regex[i] == '|' or regex[i] == '(':
            continue
                
        if i  < (len(regex) - 1):
           if (regex[i+1] == '|' or regex[i+1] == '*' or regex[i+1] == '+' or regex[i+1] == '?' or regex[i+1] == ')'):
                  continue 
           new_regex += '.'
         
  
   return new_regex 


def ToPostfix(regex):
    prec = {}
    prec['*'] = 2 
    prec['+'] = 2
    prec['?'] = 2
    prec['.'] = 1
    prec['|'] = 0
    
   
   
    postfixregex  = []
    stack =  []
    for token  in regex: 
          
          if token == '.' or token == '|' or token == '*' or token == '+' or token == '?':                                                                                                                                            
            while not len(stack) <= 0 and stack[len(stack) -1] != '(' and  prec.get(stack[len(stack)-1]) >= prec[token]:
                    postfixregex.append(stack.pop())
            stack.append(token)


          if  token.isalnum():
             postfixregex.append(token)
             continue



          if token == '(':
              stack.append(token)
          if token == ')': 
            
              token = stack.pop()
              
              while token  != '(':
                  postfixregex.append(token)            
                  token = stack.pop()

        

    while   len(stack) > 0:
         postfixregex.append(stack.pop())
    
    return ''.join(postfixregex) 



def make_rangeInt(a , b): 
    str_range  = '('
    for value in range(int(a) , int(b) +1):  

        str_range += str(value)
        
        if value == int(b): 
           break

        str_range += '|'


    str_range += ')'

    return str_range 



def make_rangeChar(a , b): 
    str_range  = '('
    for value in range(ord(a) , ord(b) + 1):  
      
        str_range += chr(value)
        
        if value == ord(b): 
           break

        str_range += '|'


    str_range += ')'

    return str_range 




 
def OpenRange(regex):
   newregex = ''
   index = 0

   while index < len(regex): 
      if regex[index] == '[':
       
       if  regex[index+1].isdigit():
         newregex += make_rangeInt(regex[index+1]  , regex[index+3])
       else:
        newregex += make_rangeChar(regex[index+1] , regex[index+3])
       index += 5
      else:
        newregex += regex[index]
        index += 1
   return newregex

  

  


 
while 1:

 print("Enter regex: ")
 regex = input();

 nfa   = ToNFA(ToPostfix(InsertConcatOperator(OpenRange(regex))))

 print("Enter test string: ")
 teststr = input()
 print(search(nfa , teststr))
 print('\n')
