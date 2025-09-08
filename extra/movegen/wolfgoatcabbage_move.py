"""Wolf-Goat-Cabbage move generators.

State: [F,W,G,C] bits (0 left, 1 right).
Functions:
    unsafe(state)    -> constraint check.
    legal_children(node) -> all legal one-crossing moves.
    prioritize_goat_first(node) -> heuristic ordering preferring moving goat if legal.
"""


def unsafe(state):
    F,W,G,C=state
    if W==G and W!=F: return True
    if G==C and G!=F: return True
    return False


def legal_children(node):
    children=[]
    F=node[0]
    # farmer alone
    ns=node[:]
    ns[0]=1-F
    if not unsafe(ns):
        children.append(ns)
    for i in range(1,4):
        if node[i]==F:
            ns=node[:]
            ns[0]=1-F
            ns[i]=1-node[i]
            if not unsafe(ns):
                children.append(ns)
    uniq=[]
    seen=set()
    for c in children:
        t=tuple(c)
        if t not in seen:
            seen.add(t)
            uniq.append(c)
    return uniq


def prioritize_goat_first(node):
    """Return children with those moving the goat (index 2) first if present."""
    kids=legal_children(node)
    def key(s):
        # detect if goat moved relative to parent
        return 0 if s[2]!=node[2] else 1
    kids.sort(key=key)
    return kids
