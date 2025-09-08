"""Map Coloring move generators.

State Representation:
  List[int] of length N where index corresponds to a region and value is the color id (0 = uncolored).

Core Functions:
  standard_expand(node, adjacency, colors):
      Select first uncolored region (smallest index) and create children assigning each legal color.
  mrv_expand(node, adjacency, colors):
      Use Minimum Remaining Values heuristic: pick uncolored region with fewest legal colors.
  recolor_single(node, adjacency, colors):
      For complete assignments (no zeros), change color of one region to any alternative legal color.
  swap_conflicted(node, adjacency):
      For a complete assignment, swap colors between two conflicted regions (keeps palette size constant).
  conflicted_regions(node, adjacency):
      Helper: return indices that currently violate constraints.

All functions return a list of new state lists.
"""
from itertools import combinations


def legal_colors_for(region, node, adjacency, colors):
    used = {node[n] for n in adjacency[region] if node[n] != 0}
    return [c for c in colors if c not in used]


def standard_expand(node, adjacency, colors):
    if 0 not in node:
        return []
    region = node.index(0)
    children = []
    for c in legal_colors_for(region, node, adjacency, colors):
        new = node[:]
        new[region] = c
        children.append(new)
    return children


def mrv_expand(node, adjacency, colors):
    if 0 not in node:
        return []
    # compute domain sizes
    candidates = []
    for r, v in enumerate(node):
        if v == 0:
            legal = legal_colors_for(r, node, adjacency, colors)
            candidates.append((len(legal), r, legal))
    if not candidates:
        return []
    candidates.sort(key=lambda x: (x[0], x[1]))
    _, region, legal = candidates[0]
    children = []
    for c in legal:
        new = node[:]
        new[region] = c
        children.append(new)
    return children


def conflicted_regions(node, adjacency):
    conflicts = set()
    for r, neighbors in adjacency.items():
        for n in neighbors:
            if node[r] != 0 and node[r] == node[n]:
                conflicts.add(r)
                conflicts.add(n)
    return sorted(conflicts)


def recolor_single(node, adjacency, colors):
    if 0 in node:
        return []  # expect complete assignment
    children = []
    for r in range(len(node)):
        current = node[r]
        for c in colors:
            if c != current:
                # tentative
                ok = True
                for n in adjacency[r]:
                    if node[n] == c:
                        ok = False
                        break
                if ok:
                    new = node[:]
                    new[r] = c
                    children.append(new)
    return children


def swap_conflicted(node, adjacency):
    conf = conflicted_regions(node, adjacency)
    children = []
    for i, j in combinations(conf, 2):
        if node[i] != node[j]:  # swap only different colors
            new = node[:]
            new[i], new[j] = new[j], new[i]
            children.append(new)
    return children
