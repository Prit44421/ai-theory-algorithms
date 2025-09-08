"""Example usage patterns for SAT move generators.
Run directly to see sample neighbor sets.
"""
from . import sat_move

# Provide a dummy evaluator (lower better)
def dummy_eval(node):
    # just count ones
    return sum(node)

if __name__ == '__main__':
    node=[0,0,0]
    print('Flip all:',sat_move.flip_all(node))
    print('Flip pair:',sat_move.flip_pair(node))
    print('Greedy better:',sat_move.flip_until_true(node,dummy_eval))
