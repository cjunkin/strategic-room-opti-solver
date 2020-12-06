def expand(br):

    student = students_in(br)
    # creates a branch of the search tree for each possible addition
    branches = [br.copy() for i in range(len(br) + 1)]

    # adds a branch in which a student gets added to each room
    for i in range(len(br)):
        branches[i][i].append(student)

    # creates a new room for the student n the final branch
    branches[len(br)][len(br)] = [student]
    return branches

def students_in( br):
    stus = 0
    for room, kids in br.items():
        stus += len(kids)
    return stus

x = expand({})
print(x)
print(expand(x[0]))