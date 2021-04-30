import random
import csv
import re
import copy

OFFICE_DICT = {"England" : ("London", "Cambridge", "Bristol", "Liverpool"), "United States" : ("New York", "Dallas", "San Francisco", "Chicago"), "Canada": ("Ottawa", "Vancouver", "Quebec"), "India": ("Mombai", "Delhi", "Bangalore")}

# country and office groups will be created automatically based on OFFICE_DICT
# this contains other groups to be created
# in addition I'll write a function that creates some random security groups and add random members
GROUPS = ["IT Support", "Developers", "HR", "Administrators", "Board", "VIP", "Office license", "Domain Users"]
# these will have only 1 owner and any employee can be a member
GROUPS_SUBSET = ["IT Support", "Developers", "HR"]

class Employee:
    def __init__(self, name, surname, username):
        self.name = name
        self.surname = surname
        self.username = username
        self.emailAlias = None
        self.managerLevel = None
        self.manager = None
        self.office = None
        self.OULevel1 = None # country
        self.OULevel2 = None # office
        self.password = "Zaq12wsx"
        self.groups = []
        self.groupsOwner = []
        self.propertyList = None
        self.propertyNameList = None

    def showProperties(self):
        return f"{self.name:<15} {self.surname:<20} {self.username:<10} {self.emailAlias:<40} {self.managerLevel:<3} {self.manager:<10} {self.office:<15} {self.OULevel1:<15} {self.OULevel2:<15} {self.password:<10} {self.groups}"

    def writePropertiesToList(self):
        self.propertyList = [self.name, self.surname, self.username, self.emailAlias, self.managerLevel, self.manager, self.office, self.OULevel1, self.OULevel2, self.password, self.groups, self.groupsOwner]

    def writePropertyNameList(self):
        self.propertyNameList = ["Name", "Surname", "Username", "Email alias", "Managerial level", "Manager", "Office", "OU Level 1 - Country", "OU Level 2 - Office", "Password", "Groups", "Owner of groups"]


def createUserObjects(k):
    employeeList = []
    for _ in range(int(k)):
        randName = random.choice(namesList)
        randSur = random.choice(surnamesList)
        username = randName[0:3] + randSur[0:3] + "01"
        employeeList.append(Employee(randName, randSur, username))
    employeeList.sort(key = lambda x: x.username)
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
# another consideration - input List has to be sorted by emp.managerLevel attribute (it is since it is executed in main func after defineManagers(), but I'll add it still there, still python's timsort is very efficient - best case scenario O(n))
    employeeList.sort(key = lambda x: x.managerLevel)
    for emp in employeeList:
        if emp.managerLevel <= 3:
            country = random.choice(list(OFFICE_DICT.keys()))
            office = random.choice(OFFICE_DICT[country])
            emp.office = office
            emp.OULevel1 = country
            emp.OULevel2 = office
        else:
            empRef = next(x for x in employeeList if x.username == emp.manager)
            emp.OULevel1 = empRef.OULevel1
            emp.OULevel2 = empRef.OULevel2
            emp.office = empRef.office
    return None

def createRandomGroups(k):
    k = int(k)
    groupsDict = {}
    randomGroupsNumber = random.randint(int(k/40), int(k/10))
    for i in range(randomGroupsNumber): # number of groups to be created is arbitrary
        groupsDict[f"GroupNo{i+1}"] = []
    for item in GROUPS:
        groupsDict[item] = []
    return groupsDict


def assignToGroups(employeeList, groupsDict):
    # employeeList has to be sorted by emp.managerLevel attribute
    employeeList.sort(key = lambda x: x.managerLevel)
    # groupsOneOwner = GROUPS_SUBSET[:]
    numberOfGroups = len(groupsDict)
    for emp in employeeList:
        emp.groups.append("Office license")
        emp.groups.append("Domain Users")
        groupsDict["Office license"].append(emp.username)
        groupsDict["Domain Users"].append(emp.username)
        if emp.managerLevel <= 4:
            emp.groups.append("VIP")
            groupsDict["VIP"].append(emp.username)
            if emp.managerLevel <= 3:
                emp.groups.append("Administrators")
                groupsDict["Administrators"].append(emp.username)
                if emp.managerLevel <= 2:
                    emp.groups.append("Board") 
                    groupsDict["Board"].append(emp.username)
        for group in groupsDict:
            if (group not in ["Administrators", "Board", "VIP", "Office license"]) and (random.randint(0, numberOfGroups) in [0,1]): # give everyone 2/numberOfGroups chance to be a member of every group
                emp.groups.append(group)
                groupsDict[group].append(emp.username) 
    return None


def assignOwners(employeeList, groupsDict):
    randomGroupRegex = re.compile(r'GroupNo\w+')
    groupNameList = [x for x in groupsDict.keys()]
    for group in groupNameList:
        if randomGroupRegex.search(group):
            random.choice(employeeList).groupsOwner.append(group)
        elif group in  ["Administrators", "Board", "VIP"]:
            random.choice([x for x in empList if x.managerLevel == 2]).groupsOwner.append(group)
        elif group in ["IT Support", "Developers", "HR"]:
            random.choice([x for x in empList if x.managerLevel in [2,3]]).groupsOwner.append(group)
    return None
            


def printStatistics(employeeList):
    print(f"# CEO = {sum(1 for x in employeeList if x.managerLevel == 1)}\n# Level 2 = {sum(1 for x in empList if x.managerLevel == 2)}\n# Level 3 = {sum(1 for x in empList if x.managerLevel == 3)}\n# Level 4 = {sum(1 for x in empList if x.managerLevel == 4)}\n# Level 5 = {sum(1 for x in empList if x.managerLevel == 5)}\n# Level 6 = {sum(1 for x in empList if x.managerLevel == 6)}\n# Level 7 = {sum(1 for x in empList if x.managerLevel == 7)}")


# In some areas, it is also convention to use a “BOM” at the start of UTF-8 encoded files; the name is misleading since UTF-8 is not byte-order dependent. The mark simply announces that the file is encoded in UTF-8. Use the ‘utf-8-sig’ codec to automatically skip the mark if present for reading such files.

with open("names2000.csv", 'r', encoding="utf-8-sig") as namesFile:
    with open("surnames1000.csv",'r', encoding="utf-8-sig") as surnamesFile:
        with open("employees.csv", mode='w', newline='') as employeeData:
            with open("groups.csv", mode="w", newline='') as groupData:
                employeeWriter = csv.writer(employeeData, delimiter=";", quoting=csv.QUOTE_NONE)
                groupWriter = csv.writer(groupData, delimiter=";", quoting=csv.QUOTE_NONE)

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
                groupsDict = createRandomGroups(k)
                assignToGroups(empList, groupsDict)
                assignOwners(empList, groupsDict)

                # format before printing
                for emp in empList:
                    emp.groups = ','.join(emp.groups).replace("[", "").replace("]", "").replace("'", "")
                    emp.groupsOwner = ','.join(emp.groupsOwner).replace("[", "").replace("]", "").replace("'", "")

                empList[0].writePropertyNameList()
                employeeWriter.writerow( empList[0].propertyNameList )
                for emp in empList:
                    emp.writePropertiesToList()
                    employeeWriter.writerow(emp.propertyList)

                # format before printing
                for groupKey, groupVal in groupsDict.items():
                    groupsDict[groupKey] = ','.join(groupVal).replace("[", "").replace("]", "").replace("'", "")

                groupWriter.writerow(["Group Name", "Members"])
                groupWriter.writerows(groupsDict.items())