'''
This is for Elevator Class, it has a constructor for initializing the attributes.
It has functions to operate the elevator.
'''
class Elevator:
    #initializer/constructor
    def __init__(self, id, currentFloor, accessFloors):
        self.id = id
        self.currentFloor = currentFloor
        self.accessFloors = accessFloors
        self.serviceList = []
        self.direction = None


    #This function moves the elevator using the removeFloor, it updates the current floor
    #and removes the floor it has serviced.
    def moveElevator(self):
        while(len(self.serviceList) != 0 ):
            self.removeFloor()

    #This function adds floor to the services list once user has selected a floor.
    #Depending on the direction they're going, it sorts the array accordingly.
    def addFloor(self, floor):
        self.serviceList.append(floor)
        if(self.direction == "up"):
            self.serviceList.sort()
        else:
            self.serviceList.sort(reverse=True)

        self.moveElevator()

    #This function is to remove the floor elevator has just serviced, removes it from 
    #the array and updates the currentFloor before removing the floor from service list.
    def removeFloor(self):
        if(len(self.serviceList) > 0):
            print("Reached this floor: ", self.serviceList[0] ,"removing from queue")
            self.currentFloor = self.serviceList[0]
            self.serviceList.pop(0)    
        else:
            pass
    

#This is for Control Panel class, it has a constructor for initializing it's attributes.
#it only has one function for getting the closest elevator to employee.
class ControlPanel:
    def __init__(self, elevator):
        self.elevator = elevator

    #This functions gets the closest elevator to employee.
    def getElevator(self):
        return self.elevator
        
#This is for the Employee class, it has a constructor for initializing it's attributes.
#it has no functions 
class Employee:
    def __init__(self, name, level):
        self.name = name.lower()
        self.level = level
    

#Helper function to initialize elevators.
def initializeElevators(eList):
    elev1 = Elevator(1, 3, [1, 2, 3])
    elev2 = Elevator(2, 3, [1, 2, 3])
    elev3 = Elevator(3, 3, [1, 2, 3, 4])
    elev2.direction = "down"
    elev3.direction = "down"
    elev1.direction = "up"
    elev3.serviceList = [1, 2]
    elev2.serviceList = [2, 3]
    elev1.serviceList = [2, 3]

    eList.append(elev1)
    eList.append(elev2)
    eList.append(elev3)

#Helper function to initialize Employees.
def initializeEmployees(list):
    emp1 = Employee("Mia", "p6")
    emp2 = Employee("Joe", "p7")
    list.append(emp1)
    list.append(emp2)

#Helper function to initialize control systems for elevators.
def initializeControlSystem(cList, eList):
    cs1 = ControlPanel(eList[0])
    cs2 = ControlPanel(eList[1])
    cs3 = ControlPanel(eList[2])
    cList.append(cs1)
    cList.append(cs2)
    cList.append(cs3)

#Helper function to find which elevator can access the VIP suite.
#As there might be more elevators, it is important to find which elevator can service 4 floors
#4th floor being the VIP Suite.
def vipElevator(elevList):
    for b in elevList:
        if(len(b.accessFloors) == 4):
            return b

'''
Helper function to compute the closest elevator.
first, it checks for which floor employee is on, then it checks for the direction the employee wants to go in
In for loop, it iterates between step two and three
    second, it computes the difference between the floor elevator is on and the floor employee wants to go.
    third, it finds the shortest distance and sets the new difference, it updates if there is a smaller difference.
    fourth, it then compares the length of these elevators service list if the difference is same.
'''
def computeClosestElevator(onFloor, dir, elevList):
    tempArr = []
    diff = 1000

    if(onFloor == 4):
        elev = vipElevator(elevList)
        return elev
        
    for e in elevList:
        if(e.direction == dir or e.direction == None):
            tempArr.append(e)

    tempElev = tempArr[0]
    for x in tempArr:
        if(x.currentFloor > onFloor):
             distance = x.currentFloor - onFloor
        else:
            distance = onFloor - x.currentFloor

        if(distance <= diff):
            diff = distance
            if(len(x.serviceList) <= len(tempElev.serviceList)):
                tempElev= x

    print("assigning Elev #:", tempElev.id)
    return tempElev

'''
This function gets user input regarding the employee, which floor they want to go on and which floor they are on.
It also asks for the direction.
First, it checks if the floor they want to go on is valid.
Second, it iterates over the Employee list to find the employee and validate user name entry.
Third, it checks which floor to want to go and if they have the rank to visit it.
Fourth, if the floor entry is accessible, it checks their rank. 
Lastly, accordingly it finds the closest elevator using computeClosestElevator.
'''
def getUserInput(onFloor, direction, elevList, empList):
    i = 0
    while(i != -1):
        
        emp = input("enter employee name: ").lower()
        direction = input("up/down ").lower()
        floor = int(input("Enter a floor between 1 to 4 (4 being VIP Suite)."))
        onFloor = int(input("Enter the floor you're on? "))
        print("type of floor is: ", type(floor))
        if(floor not in range(1, 5)):
            print("Invalid floor")
            floor = int(input("Enter a floor between 1 to 4 (4 being VIP Suite)."))

        for x in empList:
            if(x.name == emp):
                tempEmp = x
                if(floor == 4 and x.level!="p7"):
                    print("employee level does not permit to access the VIP Suite. Please select another floor.")
                elif(floor == 4 and x.level =="p7"):
                    elev = vipElevator(elevList)
                    return elev
                else:
                    i = -1
                    break
            
    
    tempElevator = computeClosestElevator(onFloor, direction, elevList)
    return tempElevator

 
#This is the main function where it calls all the functions above and operates the Elevator system
def main():
    elevList = []
    initializeElevators(elevList)

    empList = []
    initializeEmployees(empList)

    controlSystems = []
    initializeControlSystem(controlSystems, elevList)

    onFloor = 0
    direction = ""
    tempElev = getUserInput(onFloor, direction, elevList, empList)
    
    for c in controlSystems:
        if(tempElev.id == c.elevator.id):
            tempElev = c.getElevator()
            print("Temp elev in getElevator() is: ", tempElev.id)

    tempElev.addFloor(onFloor)
    print(tempElev.serviceList)

#this is to call the main function implicitly whenever the program is ran as a script and not as a module.
if __name__ == "__main__":
    main()
