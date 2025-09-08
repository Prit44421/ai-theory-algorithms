"""N-Queen move generators.

Representation:
    Partial constructive search: node length = number of placed queens. node[i]=column of queen in row i.
    Complete assignment (for local search): permutation or any list of columns length n.

Functions:
    is_safe_partial(node,row,col) -> check safety placing (row,col) given partial node.
    expand_next_row(node,n)       -> children by placing next row queen (constructive).
    swap_columns_complete(node)   -> 2-opt style swap of two rows' columns.
    move_single_queen(node)       -> move one queen within its row (all alt columns).
    adjacent_column_shift(node)   -> shift each queen +/-1 column (wrap) (local mild change).
    diagonal_swap(node)           -> swap two queens if they share a diagonal (focus attacking pairs).
"""


def is_safe_partial(node,row,col):
    for r in range(row):
        c=node[r]
        if c==col or abs(r-row)==abs(c-col):
            return False
    return True


def expand_next_row(node,n):
    """Original incremental placement for row=len(node)."""
    row=len(node)
    if row>=n:
        return []
    children=[]
    for col in range(n):
        if is_safe_partial(node,row,col):
            new=node[:]
            new.append(col)
            children.append(new)
    return children


def swap_columns_complete(node):
    """Assumes complete assignment (permutation). Swap two rows' columns (for local search)."""
    children=[]
    n=len(node)
    for i in range(n):
        for j in range(i+1,n):
            new=node[:]
            new[i],new[j]=new[j],new[i]
            children.append(new)
    return children


def move_single_queen(node):
    """For complete assignment: move one queen to any other column in its row."""
    children=[]
    n=len(node)
    for r in range(n):
        for c in range(n):
            if c!=node[r]:
                new=node[:]
                new[r]=c
                children.append(new)
    return children


def adjacent_column_shift(node):
    """Generate neighbors by shifting each queen one column left or right (wrap)."""
    children=[]
    n=len(node)
    for r in range(n):
        for delta in (-1,1):
            nc=(node[r]+delta)%n
            if nc!=node[r]:
                new=node[:]
                new[r]=nc
                children.append(new)
    return children


def diagonal_swap(node):
    """Swap only pairs of queens that currently attack each other diagonally."""
    n=len(node)
    children=[]
    for i in range(n):
        for j in range(i+1,n):
            if abs(i-j)==abs(node[i]-node[j]):
                new=node[:]
                new[i],new[j]=new[j],new[i]
                children.append(new)
    return children
