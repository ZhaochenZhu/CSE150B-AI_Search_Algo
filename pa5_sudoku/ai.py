from __future__ import print_function
from game import sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random, copy

class AI: 
    def __init__(self):
        pass

    def solve(self, problem):
        domains = init_domains()
        restrict_domain(domains, problem) 

        # TODO: implement backtracking search. 

        # TODO: delete this block ->
        # Note that the display and test functions in the main file take domains as inputs. 
        #   So when returning the final solution, make sure to take your assignment function 
        #   and turn the value into a single element list and return them as a domain map. 
        # for spot in sd_spots:
        #     domains[spot] = [1]
        # return domains
        # <- TODO: delete this block
        assign = {}
        decisions = []
        while True:
            assign,domains = self.Propagate(assign,domains)
            if not (-1,-1) in assign:
                if self.AllAssigned(assign):
                    return self.Solution(assign)
                else:
                    assign,decision_spot = self.MakeDecision(assign,domains)
                    decisions.append((copy.deepcopy(assign),copy.deepcopy(decision_spot),copy.deepcopy(domains)))
            else:
                if not decisions:
                    return None
                else:
                    assign,domains=self.BackTrack(decisions)

    # TODO: add any supporting function you need
    def Propagate(self, assign, domains):
        while True:
            modified = []
            for decision_spot in domains:
                if len(domains[decision_spot])==1 and decision_spot not in assign:
                    assign[decision_spot] = copy.deepcopy(domains[decision_spot][0])
                    modified.append(decision_spot)
            for decision_spot in assign:
                if len(domains[decision_spot])>1:
                    domains[decision_spot] = [assign[decision_spot]]
                    modified.append(decision_spot)
            for decision_spot in domains:
                if len(domains[decision_spot])==0:
                    assign[(-1,-1)] = -1
                    return assign,domains

            consistent = True
            for i in modified:
                value = assign[i]
                for j in sd_peers[i]:
                    if value in domains[j]:
                        domains[j].remove(value)
                        consistent = False
            if consistent:
                return assign,domains
    
    def AllAssigned(self, assign):
        for decision_spot in sd_spots:
            if not decision_spot in assign:
                return False
        return True

    def Solution(self, assign):
        solution = {}
        for decision_spot in assign:
            solution[decision_spot] = [assign[decision_spot]]
        return solution

    def MakeDecision(self, assign, domains):
        shortest_length = float('inf')
        shortest_spot = None
        for decision_spot in domains:
            if not decision_spot in assign:
                if len(decision_spot)<shortest_length:
                    shortest_spot = decision_spot
                    shortest_length = len(decision_spot)
        assign[shortest_spot] = domains[shortest_spot][0];
        return assign,shortest_spot


    def BackTrack(self,decisions):
        assign,decision_spot,domains = decisions.pop()
        a = assign[decision_spot]
        # print("assign:")
        # print(assign)
        # print("spot")
        # print(decision_spot)
        # print("domain")
        # print(domains)
        assign.pop(decision_spot)
        domains[decision_spot].remove(a)
        return assign,domains

    #### The following templates are only useful for the EC part #####

    # EC: parses "problem" into a SAT problem
    # of input form to the program 'picoSAT';
    # returns a string usable as input to picoSAT
    # (do not write to file)
    def sat_encode(self, problem):
        text = ""

        # TODO: write CNF specifications to 'text'

        return text

    # EC: takes as input the dictionary mapping 
    # from variables to T/F assignments solved for by picoSAT;
    # returns a domain dictionary of the same form 
    # as returned by solve()
    def sat_decode(self, assignments):
        # TODO: decode 'assignments' into domains
        
        # TODO: delete this ->
        domains = {}
        for spot in sd_spots:
            domains[spot] = [1]
        return domains
        # <- TODO: delete this
