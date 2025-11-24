path1=[6,2,1,3,4,5]
path2=[1,3,5,4,6,2]
position_of_slice=3

"""
Dear Sir/mam i was not able to complete my answer on theory part because of time constraints


My representation is as follows:
I will represent the tour as an array
where ith element of the array would represent the position of ith city in tour 

like for example if i take a tour [6,2,1,3,4,5]
the position of city 1 is 3
city1: 3
city2: 2
city3: 4
city4: 5
city5: 6
city6: 1

so my representation would be [3,2,4,5,6,1]


now lets suppose we have two parents in my representation 

p1= [6,2,1,3,4,5]
p2= [1,6,2,4,3,5]

and i want to slice from 3 

so 
i would have this 4 arrays 

p1_part1=[6,2,1]
p1_part2=[3,4,5]
p2_part1=[1,6,2]
p2_part2=[4,3,5]


than i would sort each of them 

p1_part1_s=[1,2,6]
p1_part2_s=[3,4,5]
p2_part1_s=[1,2,6]
p2_part2_s=[3,4,5]

now to reconstruct childs in path representation
i would follow this 

for part1 
i will take ith element of part1_s than would find its index in part1 and add that index in part1 of my child

like for p1_part1_s
1st element is 1
i would find 1 in p1_part1 which is at index 3
so i would add 3 in child 1
and so on for all evements of p1_part1_s


for part2 
everything will remain same as part 1 but the index added to part2 would be index +pos

like for p1_part2_s
1st element is 3
i would find 3 in p1_part2 which is at index 1
so i would add 1+pos in child 1
and so on for all evements of p1_part1_s


"""



def path_to_my(parent):
    pos=[]
    for i in range(len(parent)):
        pos.append(parent.index(i+1)+1)
    return pos


def my_to_path(parent,pos):
    part1=parent[:pos]
    part2=parent[pos:]

    part1_s=sorted(part1)
    part2_s=sorted(part2)

    child=[]

    for i in part1_s:
        child.append(part1.index(i)+1)
    
    for i in part2_s:
        child.append(part2.index(i)+1+pos)
    
    return child



def crossover(parent1,parent2,pos):

    new_parent1=path_to_my(parent1)
    new_parent2=path_to_my(parent2)

    child1_my=new_parent1[:pos]+new_parent2[pos:]
    child2_my=new_parent2[:pos]+new_parent1[pos:]

    child1=my_to_path(child1_my,pos)
    child2=my_to_path(child2_my,pos)

    return child1,child2



# print(path_to_my(path2))



childs=crossover(path1,path2,position_of_slice)
print(f"parent1: {path1} \nparent2: {path2}")
print(f"child1:{childs[0]} \nchild2: {childs[1]}")

