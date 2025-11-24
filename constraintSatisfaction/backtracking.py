def is_consistent(ai,a,C):
    a=a+[ai]
    for c in C:
        domain=c[0]
        if max(domain)<=len(a):
            # we would have to arrange them same as in domain
            values=[a[i-1] for i in domain]
            if values not in c[1]:
                return False
    return True


def select_value(D_new,a,C):
    while len(D_new)>0:
        ai=D_new[0]
        D_new=D_new[1:]
        if is_consistent(ai,a,C):
            return ai,D_new
    return None,D_new


def backtracking(X,D,C):
    a=[]
    i=1
    D_new=D[i-1].copy()
    D_copy=[d.copy() for d in D]
    while 0<i<=len(X):
        ai,D_new=select_value(D_new,a,C)
        print("Checking",ai,a)
        if not ai:
            i=i-1
            if i==0:
                return None
            D_new=D_copy[i-1]
            a=a[:-1]
        else:
            a+=[ai]
            i+=1
            if i<=len(X):
                D_copy[i-2]=D_new.copy()
                D_new=D[i-1].copy()
    return a