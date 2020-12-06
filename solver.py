import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness, convert_dictionary
import sys
from os.path import basename, normpath
import glob


def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """
    #initialize the set of subproblems
    problems = []
    cool = BranchAndBoundSolver(G, s)
    return cool.solve()


class BranchAndBoundSolver():

    def __init__(self, G, s):
        self.G = G
        self.s = s
        self.max = -999
        self.best = {}
        self.best_rooms = 0
        self.num_students = nx.number_of_nodes(G)
        self.rooms = 1

    def add_room(self):
        self.rooms += 1

    def get_stress_limit(self):
        return self.s/self.rooms

    def solve(self):
        while self.rooms < 5:
            self.solve_helper()
            self.rooms += 1
        return self.best, self.best_rooms

    #runs the main solving loop in a branch and bound fashion
    def solve_helper(self):
        sub_problems = [{}]
        while sub_problems:
            #next items assignments to iterate through
            branches = self.expand(sub_problems.pop())
            for br in branches:
                if self.valid_stress(br):
                    if len(br) == self.num_students:
                        self.update_best(br)
                    else:
                        sub_problems.append(br)

    # return subproblems but with the next student added to each room
    def expand(self, br):
        student = len(br)
        # creates a branch of the search tree for each possible addition
        branches = [br.copy() for i in range(self.rooms)]

        # adds student to room
        for i in range(len(branches)):
            branches[i][student] = i

        return branches

    def valid_stress(self, p):
        return is_valid_solution(p, self.G, self.s, self.rooms)

    def update_best(self, p):
        h = calculate_happiness(p, self.G)
        if h > self.max:
            self.max = h
            self.best = p
            self.best_rooms = self.rooms

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G, s = read_input_file(path)
    D, k = solve(G, s)
    assert is_valid_solution(D, G, s, k)
    print("Total Happiness: {}".format(calculate_happiness(D, G)))
     #write_output_file(D, 'outputs/small-1.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('inputs/*')
#     for input_path in inputs:
#         output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         happiness = calculate_happiness(D, G)
#         write_output_file(D, output_path)
