import networkx as nx
from parse import read_input_file, write_output_file
from utils import *
import sys
from os.path import basename, normpath
import glob
import copy
from solver import GreedySolver, convert_list

if __name__ == '__main__':
    inputs = glob.glob('inputs/large/*')
    for input_path in inputs:
        output_path = 'outputs/large/' + basename(normpath(input_path))[:-3] + '.out'
        G, s = read_input_file(input_path)
        cool = GreedySolver(G, s)
        cool.solve()
        solution = cool.rooms
        rooms = len(solution)
        D, k = convert_dictionary(convert_list(solution)), rooms
        assert is_valid_solution(D, G, s, k)
        happiness = calculate_happiness(D, G)
        print("{} Total Happiness: {}".format(output_path, happiness))
        write_output_file(D, output_path)
