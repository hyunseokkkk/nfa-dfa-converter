class DFA:

    def __init__(self, state_set, terminal_set, delta_functions, start_state, final_state):
        self.StateSet = state_set
        self.TerminalSet = terminal_set
        self.DeltaFunctions = delta_functions
        self.StartState = start_state
        self.FinalState = final_state


    def epsilon_closure(self, state):
            visited = set()  # 방문한 상태를 기록 
            stack = [state]  # 스택으로 입실론-closure를 찾아냄

            while stack:
                current_state = stack.pop()  #스택에서 상태를 받아옴
                if current_state not in visited:
                    visited.add(current_state)  #해당 상태를 visited로 
                    
                    #입실론으로 갈 수 있는 모든 상태 탐색
                    epsilon_transitions = self.DeltaFunctions.get((frozenset({current_state}), 'ε'), set())
                    for next_state in epsilon_transitions:
                        if next_state not in visited:
                            stack.append(next_state)  # 해당 상태가 visited되지 않았다면 stack에 추가 후 다시 loop
            return visited

    def dfa_conversion(self):
        dfa_states = []  # DFA 상태 저장 리스트
        dfa_delta = {}   # DFA 함수 저장 딕셔너리
        dfa_start_state = self.epsilon_closure(self.StartState)  # 시작 상태의 입실론-closure를 구함
        # print(frozenset(dfa_start_state))
        stack = [frozenset(dfa_start_state)]  # 스택으로 DFA 상태를 구함, 시작 상태로 초기화
        while stack:
            current_dfa_state = stack.pop()  # 스택에서 DFA 상태를 pop
            if current_dfa_state not in dfa_states:
                dfa_states.append(current_dfa_state)  # dfa_states리스트에 저장
                
                # 모든 가능한 DFA 상태를 탐색
                for symbol in self.TerminalSet:
                    next_dfa_state = set() 
                   
                    # 입실론-closure까지 고려하여 상태를 저장
                    for nfa_state in current_dfa_state:#현재 상태에서 갈 수 있는 모든 상태
                        transitions = self.DeltaFunctions.get((frozenset({nfa_state}), symbol), set())
              
                        for transition_state in transitions:#그 중 입실론-closure까지 고려하여 합집합
                            next_dfa_state |= self.epsilon_closure(transition_state)
                    
                    if next_dfa_state:
                        next_dfa_state = frozenset(next_dfa_state) 
                        if next_dfa_state not in dfa_states:
                            stack.append(next_dfa_state)  #이렇게 만들어진 새로운 상태가 dfa_state리스트에 없다면 스택에 저장하고 다시 loop
                        dfa_delta[(current_dfa_state, symbol)] = next_dfa_state  # DFA 상태 전이 함수 업데이트
        
        # dfa_state에서 finalState를 포함한 상태를 dfa_final_state로 저장
        dfa_final_states = [state for state in dfa_states if any(s in self.FinalState for s in state)]
        
        self.StateSet = dfa_states
        self.DeltaFunctions = dfa_delta
        self.StartState = frozenset(dfa_start_state)
        self.FinalState = dfa_final_states
        
        print("                         --DFA--")
        self.display()
        
    def reduced_dfa(self):
        
        #상태를 finalstate와 그렇지 않은 상태로 나누기
        P = [set(self.FinalState), set(self.StateSet) - set(self.FinalState)]#실제 최소화된 dfa상태가 저장될 리스트
        stack = [set(self.FinalState), set(self.StateSet) - set(self.FinalState)]#
        
        while stack:
            A = stack.pop()
            for symbol in self.TerminalSet:
                X = {state for state in self.StateSet if self.DeltaFunctions.get((state, symbol)) in A}# A(새로운 상태 집합) 에 도달할 수 있는 state들
                
                for Y in P.copy():#P의 세트 Y와 X의 차집합, 교집합을 이용해 그룹 분리 
                    intersection = X & Y
                    difference = Y - X
                    
                    if intersection and difference:#차집합과 교집합이 둘 다 존재 -> 서로 다른 두 그룹
                        P.remove(Y)
                        P.append(intersection)
                        P.append(difference)
                        
                        if Y in stack:#계속해서 loop를 하기 위해 stack에도 차집합, 교집합 추가
                            stack.remove(Y)
                            stack.append(intersection)
                            stack.append(difference)
                        else:
                            if len(intersection) <= len(difference):
                                stack.append(intersection)
                            else:
                                stack.append(difference)
        
        new_states = [tuple(s) for s in P]#minimized dfa states
        new_start_state = next(s for s in new_states if self.StartState in s)#시작 상태
        new_final_states = [s for s in new_states if any(fs in s for fs in self.FinalState)]#종료 상태
        new_delta = {}
        
        #delta_function 구하기
        for state in new_states:
            tmp = next(iter(state))#minimized dfa 상태의 첫 번째 원소(대표 상태)
            for symbol in self.TerminalSet:#그 원소가 symbol을 바라봤을 때의 값
                next_state = self.DeltaFunctions.get((tmp, symbol))
                if next_state:
                    value = [s for s in new_states if next_state in s]#그 값이 minimized dfa 상태 중 어떤 상태에 속하는지 확인 후 해당되는 상태를 value에 저장
                    new_delta[(state, symbol)] = value #minimized dfa function
        
        self.StateSet = new_states
        self.DeltaFunctions = new_delta
        self.StartState = new_start_state
        self.FinalState = new_final_states
        
        print("                         --minimized_dfa--")
        self.display()
        
            
    def display(self):
        print("StateSet:")
        for state in self.StateSet:
            print(state)
        print()
        print("TerminalSet:")
        print(self.TerminalSet)
        print()
        print("DeltaFunctions:")
        for keys, values in self.DeltaFunctions.items():
            print(keys, ':' , values)
        print()
        print("StartState:", self.StartState)
        print()

        print("FinalState:")
        for fs in self.FinalState:
            print(fs)
        print("-----------------------------------------------------------------------------")