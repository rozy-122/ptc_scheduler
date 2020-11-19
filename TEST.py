
ifile=open("data/students", "r")
lines=ifile.readlines()

students = [tuple(line.strip("\n").split(",")) for line in lines]
students = students[1:]
"""
for i in range(len(students)):
    students[i][0] = students[i][0].strip(" ")
    students[i][1] = students[i][1].strip(" ")
print(students)

#[len()])

#with open("data/students", "r") as f:
  #  mylist = [tuple(map(float, i.split(','))) for i in f]
"""