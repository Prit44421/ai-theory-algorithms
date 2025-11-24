from backtracking import backtracking
from ac1 import ac1

n=4

X=[i for i in range(1,n+1)]
D=[ [i for i in range(1,n+1)] for _ in range(n)]
C=[
    [[1,2],[[1,3],[2,4],[3,1],[4,2],[1,4],[4,1]]],
    [[2,3],[[1,3],[2,4],[3,1],[4,2],[1,4],[4,1]]],
    [[3,4],[[1,3],[2,4],[3,1],[4,2],[1,4],[4,1]]],
    [[1,3],[[1,2],[2,4],[2,1],[4,2],[1,4],[4,1],[2,3],[3,1],[3,4],[4,3]]],
    [[2,4],[[1,2],[2,4],[2,1],[4,2],[1,4],[4,1],[2,3],[3,1],[3,4],[4,3]]],
    [[1,4],[[1,2],[1,3],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,2],[4,3]]]
]



# solution=backtracking(X,D,C)
D[0]=[2]
solution=ac1(X,D,C)


print(solution)
if solution:
    for i in range(n):
        row=['.']*n
        row[solution[i][0]-1]='Q'
        print(' '.join(row))