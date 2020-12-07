import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness, convert_dictionary
import sys
from os.path import basename, normpath
import glob
import copy
import multiprocessing


def solve(G, s, output_path):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """
    #initialize the set of subproblems
    cool = BranchAndBoundSolver(G, s)
    cool.solve()
    solution = cool.best
    rooms = len(solution)
    D, k = convert_dictionary(solution), rooms
    if rooms != 0:
        assert is_valid_solution(D, G, s, k)
        happiness = calculate_happiness(D, G)
        print("Total Happiness: {}".format(calculate_happiness(D, G)))
        write_output_file(D, output_path)
    else:
        print("Could not solve: {}".format(output_path))

class BranchAndBoundSolver():

    def __init__(self, G, s):
        print("new graph being worked on")
        self.G = G
        self.s = s
        self.max = -999
        self.best = {}
        self.num_students = nx.number_of_nodes(G)




    #runs the main solving loop in a branch and bound fashion
    def solve(self):
        sub_problems = [{}]
        while sub_problems:
            #next items assignments to iterate through
            branches = self.expand(sub_problems.pop())

            for br in branches:
                if self.valid_stress(br):
                    if self.students_in(br) == self.num_students:
                        self.update_best(br)
                    else:
                        sub_problems.append(br)

    # return subproblems but with the next student added to each room
    def expand(self, br):
        student = self.students_in(br)
        # creates a branch of the search tree for each possible addition
        branches = [copy.deepcopy(br) for i in range(len(br))]

        # adds a branch in which a student gets added to each room
        for i in range(len(br)):
            branches[i][i].append(student)

        #creates a new room for the student n the final branch
        if len(br) < 5:
            branches.append(copy.deepcopy(br))
            branches[len(br)][len(br)] = [student]

        return branches

    def students_in(self, br):
        stus = 0
        for room, kids in br.items():
            stus += len(kids)
        return stus

    def valid_stress(self, p):
        return is_valid_solution(convert_dictionary(p), self.G, self.s, len(p))

    def update_best(self, p):
        h = calculate_happiness(convert_dictionary(p), self.G)
        if h > self.max:
            self.max = h
            self.best = p


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

#if __name__ == '__main__':
 #   assert len(sys.argv) == 2
  #  path = sys.argv[1]
  #  G, s = read_input_file(path)
  #  D, k = solve(G, s)
  #  assert is_valid_solution(D, G, s, k)
# print("Total Happiness: {}".format(calculate_happiness(D, G)))


#For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
if __name__ == '__main__':
    inputs = glob.glob('inputs/Medium1/*')
    for input_path in inputs:
        output_path = 'outputs/medium/' + basename(normpath(input_path))[:-3] + '.out'
        G, s = read_input_file(input_path)
        solve(G,s, output_path)
