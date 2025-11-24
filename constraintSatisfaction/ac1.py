
def is_consistent(Y,ai,X,x,C):
    for c in C:
        domain=c[0]
        if X<Y:
            if [X,Y]==domain:
            # we would have to arrange them same as in domain
                values=[x,ai]
                if values not in c[1]:
                    return False
        else:
            if [Y,X]==domain:
                values=[ai,x]
                if values not in c[1]:
                    return False
    return True


def select_value(Y,Dy,X,x,C):
    while len(Dy)>0:
        ai=Dy[0]
        Dy=Dy[1:]
        if is_consistent(Y,ai,X,x,C):
            return ai
    return None
    




def revise(X,Y,D,C):
    Dx=D[X-1]
    Dy=D[Y-1]
    revised=False
    for x in Dx.copy():
        ay=select_value(Y,Dy,X,x,C)
        if not ay:
            Dx.remove(x)
            # print("Removing",x,"from domain of",X)
            revised=True
        else:
            # print(x,"is consistent for",X)
            pass
    D[X-1]=Dx
    return revised,D

 
def ac1(X,D,C):
    revised=True
    while revised:
        revised=False
        for x in X:
            for y in X:
                # print("Revising",x,"and",y)
                if x!=y:
                    revx, D = revise(x,y,D,C)
                    revy, D = revise(y,x,D,C)
                    revised=revx or revy or revised
                    # print("After revising",x,"and",y, "Domains:",D)
    return D

    