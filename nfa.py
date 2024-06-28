
import sys

class NFA:
    def __init__(self):
        self.StateSet = []
        self.TerminalSet = []
        self.DeltaFunctions = {}
        self.StartState = None
        self.FinalState = []

    def read_file(self, filename):
        with open(filename, 'r') as file:
            current_section = None
            for line in file:
                line = line.strip()
                if line.startswith("StateSet"):
                    current_section = "StateSet"
                    self.StateSet = line.split("{")[1].split("}")[0].split(",")
                    self.StateSet = [frozenset({state.strip()}) for state in self.StateSet]
                    
                elif line.startswith("TerminalSet"):
                    current_section = "TerminalSet"
                    self.TerminalSet = line.split("{")[1].split("}")[0].split(",")
                    self.TerminalSet = frozenset({state.strip() for state in self.TerminalSet})
                elif line.startswith("DeltaFunctions"):
                    current_section = "DeltaFunctions"
                    self.DeltaFunctions = {}
                elif line.startswith("Startstate"):
                    current_section = "StartState"
                    self.StartState = line.split("=")[1].strip()
                elif line.startswith("FinalState"):
                    current_section = "FinalState"
                    final_states = line.split("{")[1].split("}")[0].split(",")
                    self.FinalState = {state.strip() for state in final_states}
                elif line.strip() == "":
                    current_section = None
                else:
                    if current_section == "DeltaFunctions":
                        delta_line = line.split('=')
                        if len(delta_line) == 2:
                            keys = []
                            delta_line[0] = delta_line[0].replace("(", "").replace(")", "").split(',')
                            keys.append(frozenset({delta_line[0][0].strip()}))
                            keys.append(delta_line[0][1].strip())
                            keys = tuple(keys)
                            values = set(delta_line[1].split("{")[1].split("}")[0].split(","))
                            values = {value.strip() for value in values}
                            self.DeltaFunctions[keys] = values


    def display(self):
        print("                         --(ε-)NFA--")
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
        # print(self.DeltaFunctions)
        print()
        print("StartState:", self.StartState)
        print("FinalState:", self.FinalState)
        print()
        print("-----------------------------------------------------------------------------")
    