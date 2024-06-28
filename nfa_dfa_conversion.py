import sys
from nfa import NFA
from dfa import DFA

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('not read')
        sys.exit(0)
    
    filename = sys.argv[1]
    nfa = NFA()
    nfa.read_file(filename)
    nfa.display()   
    dfa = DFA(nfa.StateSet, nfa.TerminalSet, nfa.DeltaFunctions, nfa.StartState, nfa.FinalState)
    dfa.dfa_conversion()
    dfa.reduced_dfa()
