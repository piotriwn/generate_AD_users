import random

OFFICE_LIST = ["London", "Cambridge", "Bristol", "Liverpool", "New York", "Dallas", "San Francisco", "Chicago", "Ottawa", "Vancouver", "Quebec", "Mombai", "Delhi", "Bangalore"]

class Employee:
    def __init__(self, name, surname, username):
        self.name = name
        self.surname = surname
        self.username = username
        self.emailAlias = None
        self.managerLevel = None
        self.manager = None
        self.office = None

    def showProperties(self):
        return f"{self.name:<15} {self.surname:<20} {self.username:<10} {self.emailAlias:<40} {self.managerLevel:<3} {self.manager:<10} {self.office}"


def createUserObjects(k):
    employeeList = []
    for _ in range(int(k)):
        randName = random.choice(namesList)
        randSur = random.choice(surnamesList)
        username = randName[0:3] + randSur[0:3] + "01"
        employeeList.append(Employee(randName, randSur, username))
    employeeList.sort(key = lambda x: x.username)
    #print(employeeList[2].name)
    return employeeList

def checkUsernameUniq(employeeList):
    previousName = None
    k = 0
    for i in range(len(employeeList)):
        if previousName == employeeList[i].username:
            k+=1
        elif k > 0:
            while (k>0):
                employeeList[i-k-1].username = f"{employeeList[i-k-1].name[:3]}{employeeList[i-k-1].surname[:3]}{k+1:02d}"
                k -= 1
        else:
            pass
        previousName = employeeList[i].username
    return None

def modifyEmailAlias(employeeList):
    for emp in employeeList:
        if emp.username[-2:] != "01":
            emp.emailAlias = f"{emp.name}.{emp.surname}{emp.username[-2:]}@contoso.com"
        else:
            emp.emailAlias = f"{emp.name}.{emp.surname}@contoso.com"
    return None
    

def defineManagers(employeeList):
    random.shuffle(employeeList)
    employeeList[0].managerLevel = 1
    employeeList[0].manager = ""  # re-assign explicitly, so that CEO has none above
    level = 2
    i = 1
    while i < len(employeeList):
        numberOfEmpAtLevel = int(level**(1/2)) * random.randint(3,6) * sum(1 for emp in employeeList if emp.managerLevel == level-1) # i came up with this formula, it's arbitrary
        j= 0
        while (j < numberOfEmpAtLevel) and (i+j < len(employeeList)):
            employeeList[i+j].managerLevel = level
            employeeList[i+j].manager = (random.choice( [x for x in employeeList if x.managerLevel == level-1] )).username
            j+= 1
        level += 1
        i += numberOfEmpAtLevel
    return None

def assignToOffice(employeeList): # ugh, very inefficent (O(n2) I suppose), will have to be reconsidered
# another consideration - input List has to be sorted by emp.managerLevel attribute (it is since it is executed in main func after defineManagers())
    for emp in employeeList:
        if emp.managerLevel <= 3:
            emp.office = random.choice(OFFICE_LIST)
        else:
            emp.office = next(x.office for x in employeeList if x.username == emp.manager)
    return None

def printStatistics(employeeList):
    print(f"# CEO = {sum(1 for x in employeeList if x.managerLevel == 1)}\n# Level 2 = {sum(1 for x in empList if x.managerLevel == 2)}\n# Level 3 = {sum(1 for x in empList if x.managerLevel == 3)}\n# Level 4 = {sum(1 for x in empList if x.managerLevel == 4)}\n# Level 5 = {sum(1 for x in empList if x.managerLevel == 5)}\n# Level 6 = {sum(1 for x in empList if x.managerLevel == 6)}\n# Level 7 = {sum(1 for x in empList if x.managerLevel == 7)}")


# In some areas, it is also convention to use a “BOM” at the start of UTF-8 encoded files; the name is misleading since UTF-8 is not byte-order dependent. The mark simply announces that the file is encoded in UTF-8. Use the ‘utf-8-sig’ codec to automatically skip the mark if present for reading such files.

with open("names2000.csv", 'r', encoding="utf-8-sig") as namesFile:
    with open("surnames1000.csv",'r', encoding="utf-8-sig") as surnamesFile:
        namesList = namesFile.readlines()
        surnamesList = surnamesFile.readlines()
        namesList = [name.strip() for name in namesList]
        surnamesList = [surnname.strip() for surnname in surnamesList]
        
        k = input("Provide the number of AD user objects to be created: ")
        
        empList = createUserObjects(k)
        checkUsernameUniq(empList)
        modifyEmailAlias(empList)
        defineManagers(empList)
        assignToOffice(empList)


        for i in range(100):
            print(sorted(empList,key = lambda x: x.managerLevel)[i].showProperties())

        # printStatistics(empList)

        



