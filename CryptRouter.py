from collections import deque
import heapq
import itertools
import sys
# https://ddowiki.com/page/The_Shadow_Crypt/Instance_Paths - refer to this link for topology of instances
class Pointer:
    def __init__(self, roomBeingPointedTo, direction):
        self.roomBeingPointedTo = roomBeingPointedTo
        self.direction = direction
    def getDirection(self):
        return self.direction
    def getRoomBeingPointedTo(self):
        return self.roomBeingPointedTo
    def setRoomBeingPointedTo (self, room):
        if isinstance(room, Room):
            self.roomBeingPointedTo = room
        else:
            raise TypeError("Data must be of Room type")
    def setDirection (self, direction):
        validDirections = {"north", "east", "south", "west"}
        if(isinstance(direction, str)):
            if direction.lower() in validDirections:
                self.direction = direction
            else:
                raise AttributeError("Not a valid direction")
        else:
            raise TypeError("Directions can only be Strings")
    def __str__(self):
        return "This pointer points to " + str(self.roomBeingPointedTo) + self.direction

class Room:

    def __init__(self, color, structure):
        self.color = color
        self.structure = structure
        self.northPointer = None # need to keep track of where a given rooms north exit leads.
        self.eastPointer = None # need to keep track of where a given rooms east exit leads.
        self.southPointer = None # need to keep track of where a given rooms south exit leads.
        self.westPointer = None # need to keep track of where a given rooms north exit leads.
        self.neighboringRooms = set() # Need to maintain a neighboringRoom set to manage routing among rooms.

    # room attribute retrieval methods
    def getColor(self):
        return self.color
    
    def getType(self):
        return self.structure
    
    def getNorthPointer(self):
        return self.northPointer
    
    def getEastPointer(self):
        return self.eastPointer
    
    def getSouthPointer(self):
        return self.southPointer
    
    def getWestPointer(self):
        return self.westPointer
    
    def getNeighboringRooms(self):
        return self.neighboringRooms
    
    # room attribute mutator methods
    
    def setNorthPointer(self, room):
        # logic is to update the northmost room and keep record within the set.
        if self.northPointer not in self.neighboringRooms:
            self.northPointer = Pointer(room, "north")
            self.neighboringRooms.add(self.northPointer)
        else:
            self.neighboringRooms.remove(self.northPointer)
            self.northPointer = Pointer(room, "north")
            self.neighboringRooms.add(self.northPointer)

    def setEastPointer(self, room):
        # logic is to update the eastmost room and keep record within the set.
        if self.eastPointer not in self.neighboringRooms:
            self.eastPointer = Pointer(room, "east")
            self.neighboringRooms.add(self.eastPointer)
        else:
            self.neighboringRooms.remove(self.eastPointer)
            self.eastPointer = Pointer(room, "east")
            self.neighboringRooms.add(self.eastPointer)

    def setSouthPointer(self, room):
        # logic is to update the southmost room and keep record within the set.
        if self.southPointer not in self.neighboringRooms:
            self.southPointer = Pointer(room, "south")
            self.neighboringRooms.add(self.southPointer)
        else:
            self.neighboringRooms.remove(self.southPointer)
            self.southPointer = Pointer(room, "south")
            self.neighboringRooms.add(self.southPointer)

    def setWestPointer(self, room):
        # logic is to update the westmost room and keep record within the set.
        if self.westPointer not in self.neighboringRooms:
            self.westPointer = Pointer(room, "west")
            self.neighboringRooms.add(self.westPointer)
        else:
            self.neighboringRooms.remove(self.westPointer)
            self.westPointer = Pointer(room, "west")
            self.neighboringRooms.add(self.westPointer)
            
    def __str__(self):
        # toString method for printing the objects
        finalStr = ""
        if(self.color.lower() == "colorless" ):
            finalStr = str(self.structure)
        else:
            finalStr = str(self.color + " " + self.structure)
        return finalStr
    
class Instance:
    def __init__(self, roomsInInstance=None):
        if roomsInInstance is None:
            self.roomsInInstance = set()
        else:
            if isinstance(roomsInInstance, set) and all(isinstance(e, Room) for e in roomsInInstance):
                self.roomsInInstance = roomsInInstance
            else:
                raise TypeError("Set must contain only Room instances")
            
    def getRoomsInInstance(self):
        return self.roomsInInstance
    
    def setRoomsInInstance(self,roomSet):
        if isinstance(roomSet, set):
            self.roomsInInstance = roomSet
        else:
            print("Given data type must be a set")
    def addRoomObjToInstance(self, room): 
        if len(self.roomsInInstance ) < 12:
            if isinstance(room, Room):
                self.roomsInInstance.add(room)
            else:
                raise TypeError("Elements added to the set of rooms must also be rooms")
        else:
            raise ValueError("Set cannot have more than 12 rooms")
    def addRoomToInstance(self, color, structure):
        if len(self.roomsInInstance) < 12:
            tempRoom = Room(color, structure)
            self.roomsInInstance.add(tempRoom)
        else:
            raise ValueError("Set cannot have more than 12 rooms")
    def __str__ (self):
        tempString = ""
        for room in self.roomsInInstance:
            tempString += str(room) + "\n"
        finalString = "Rooms in this instance: " + tempString
        return finalString




# next step: creating objects for each possible room (without pointers, just yet)

"""
GENERAL INSTANCE SETUP
"""

pointedRoomListInstance1  = [Room("Colorless", "Start")] # starting room = index 0
pointedRoomListInstance2  = [Room("Colorless", "Start")] # starting room = index 0
pointedRoomListInstance3  = [Room("Colorless", "Start")] # starting room = index 0

"""
INSTANCE ONE SETUP
"""
def initializeInstance1():
    global instance1
    # add the rooms in instance one initially to a list so that they can be indexed [exhaustively, theres no pattern just how it is]
    pointedRoomListInstance1.append(Room("Green", "Columns")) # INDEX 1
    pointedRoomListInstance1.append(Room("Red", "Columns")) # INDEX 2
    pointedRoomListInstance1.append(Room("Blue", "Columns")) # INDEX 3
    pointedRoomListInstance1.append(Room("Yellow", "Maze")) # INDEX 4
    pointedRoomListInstance1.append(Room("Green", "Maze")) # INDEX 5
    pointedRoomListInstance1.append(Room("Blue", "Maze")) # INDEX 6
    pointedRoomListInstance1.append(Room("Yellow", "Puzzle")) # INDEX 7
    pointedRoomListInstance1.append(Room("Yellow", "Dais")) # INDEX 8
    pointedRoomListInstance1.append(Room("Green", "Dais")) # INDEX 9
    pointedRoomListInstance1.append(Room("Red", "Dais")) # INDEX 10
    pointedRoomListInstance1.append(Room("Red", "Underwater")) # INDEX 11
    pointedRoomListInstance1.append(Room("Blue", "Underwater")) # INDEX 12
    pointedRoomListInstance1.append(Room("Colorless", "Ramp")) # INDEX 13

    # pointers for starting room ( edges ) INDEX 0
    pointedRoomListInstance1[0].setNorthPointer(pointedRoomListInstance1[0]) # north points to Starting room
    pointedRoomListInstance1[0].setEastPointer(pointedRoomListInstance1[2]) # east points to Red Columns room
    pointedRoomListInstance1[0].setSouthPointer(pointedRoomListInstance1[4]) # south points to Yellow Maze room
    pointedRoomListInstance1[0].setWestPointer(pointedRoomListInstance1[1]) # west points to Green Columns room

    # pointers for Green Columns room ( edges ) INDEX 1
    pointedRoomListInstance1[1].setNorthPointer(pointedRoomListInstance1[5]) # north points to Green Maze room
    pointedRoomListInstance1[1].setEastPointer(pointedRoomListInstance1[1]) # east points to Green Columns room
    pointedRoomListInstance1[1].setSouthPointer(pointedRoomListInstance1[1]) # south points to Green Columns room
    pointedRoomListInstance1[1].setWestPointer(pointedRoomListInstance1[4]) # west points to Yellow Maze room

    # pointers for Red Columns room ( edges ) INDEX 2
    pointedRoomListInstance1[2].setNorthPointer(pointedRoomListInstance1[3]) # north points to Blue Columns
    pointedRoomListInstance1[2].setEastPointer(pointedRoomListInstance1[6]) # east points to Blue Maze room
    pointedRoomListInstance1[2].setSouthPointer(pointedRoomListInstance1[11]) # south points to Red Underwater room
    pointedRoomListInstance1[2].setWestPointer(pointedRoomListInstance1[12]) # west points to Blue Underwater room

    # pointers for Blue Columns room ( edges ) INDEX 3
    pointedRoomListInstance1[3].setNorthPointer(pointedRoomListInstance1[9]) # north points to Green Dais room
    pointedRoomListInstance1[3].setEastPointer(pointedRoomListInstance1[7]) # east points to Yellow Puzzle room
    pointedRoomListInstance1[3].setSouthPointer(pointedRoomListInstance1[10]) # south points to Red Dais room
    pointedRoomListInstance1[3].setWestPointer(pointedRoomListInstance1[11]) # west points to Red Underwater room
    
    # pointers for Yellow Maze room ( edges ) INDEX 4
    pointedRoomListInstance1[4].setNorthPointer(pointedRoomListInstance1[5]) # north points to Green Maze room
    pointedRoomListInstance1[4].setEastPointer(pointedRoomListInstance1[8]) # east points to Yellow Dais room
    pointedRoomListInstance1[4].setSouthPointer(pointedRoomListInstance1[6]) # south points to Blue Maze room
    pointedRoomListInstance1[4].setWestPointer(pointedRoomListInstance1[0]) # west points to Starting room
    
    # pointers for Green Maze room ( edges ) INDEX 5
    pointedRoomListInstance1[5].setNorthPointer(pointedRoomListInstance1[2]) # north points to Red Columns room
    pointedRoomListInstance1[5].setEastPointer(pointedRoomListInstance1[0]) # east points to Starting room
    pointedRoomListInstance1[5].setSouthPointer(pointedRoomListInstance1[12]) # south points to Blue Underwater room
    pointedRoomListInstance1[5].setWestPointer(pointedRoomListInstance1[9]) # west points to Green Dais room

    # pointers for Blue Maze room ( edges ) INDEX 6
    pointedRoomListInstance1[6].setNorthPointer(pointedRoomListInstance1[2]) # north points to Red Columns Room
    pointedRoomListInstance1[6].setEastPointer(pointedRoomListInstance1[10]) # east points to Red Dais room
    pointedRoomListInstance1[6].setSouthPointer(pointedRoomListInstance1[7]) # south points to Yellow Puzzle room
    pointedRoomListInstance1[6].setWestPointer(pointedRoomListInstance1[9]) # west points to Green Dais room
    
    # pointers for Yellow Puzzle room ( edges ) INDEX 7
    pointedRoomListInstance1[7].setNorthPointer(pointedRoomListInstance1[4]) # north points to Yellow Maze room
    pointedRoomListInstance1[7].setEastPointer(pointedRoomListInstance1[10]) # east points to Red Dais room
    pointedRoomListInstance1[7].setSouthPointer(pointedRoomListInstance1[12]) # south points to Blue Underwater room 
    pointedRoomListInstance1[7].setWestPointer(pointedRoomListInstance1[6]) # west points to Blue Maze room

    # pointers for Yellow Dais room ( edges ) INDEX 8
    pointedRoomListInstance1[8].setNorthPointer(pointedRoomListInstance1[11]) # north points to Red Underwater room
    pointedRoomListInstance1[8].setEastPointer(pointedRoomListInstance1[1]) # east points to Green Columns room
    pointedRoomListInstance1[8].setSouthPointer(pointedRoomListInstance1[3]) # south points to Blue Columns room
    pointedRoomListInstance1[8].setWestPointer(pointedRoomListInstance1[10]) # west points to Red Dais room

    # pointers for Green Dais room ( edges ) INDEX 9
    pointedRoomListInstance1[9].setNorthPointer(pointedRoomListInstance1[5]) # north points to Green Maze room
    pointedRoomListInstance1[9].setEastPointer(pointedRoomListInstance1[3]) # east points to Blue Columns room
    pointedRoomListInstance1[9].setSouthPointer(pointedRoomListInstance1[6]) # south points to Blue Maze room
    pointedRoomListInstance1[9].setWestPointer(pointedRoomListInstance1[7]) # west points to Yellow Puzzle room

    # pointers for Red Dais room ( edges ) INDEX 10
    pointedRoomListInstance1[10].setNorthPointer(pointedRoomListInstance1[4]) # north points to Yellow Maze room
    pointedRoomListInstance1[10].setEastPointer(pointedRoomListInstance1[11]) # east points to Red Underwater room
    pointedRoomListInstance1[10].setSouthPointer(pointedRoomListInstance1[12]) # south points to Blue Underwater room
    pointedRoomListInstance1[10].setWestPointer(pointedRoomListInstance1[13]) # west points to Ramp room

    # pointers for Red Underwater room ( edges ) INDEX 11
    pointedRoomListInstance1[11].setNorthPointer(pointedRoomListInstance1[2]) # north points to Red Columns room
    pointedRoomListInstance1[11].setEastPointer(pointedRoomListInstance1[7]) # east points to Yellow Puzzle room
    pointedRoomListInstance1[11].setSouthPointer(pointedRoomListInstance1[3]) # south points to Blue Columns room
    pointedRoomListInstance1[11].setWestPointer(pointedRoomListInstance1[8]) # west points to Yellow Dais room

    # pointers for Blue Underwater room ( edges ) INDEX 12
    pointedRoomListInstance1[12].setNorthPointer(pointedRoomListInstance1[8]) # north points to Yellow Dais room
    pointedRoomListInstance1[12].setEastPointer(pointedRoomListInstance1[0]) # east points to Start room
    pointedRoomListInstance1[12].setSouthPointer(pointedRoomListInstance1[1]) # south points to Green Columns room
    pointedRoomListInstance1[12].setWestPointer(pointedRoomListInstance1[5]) # west points to Green Maze room

    pointedRoomListInstance1[13].setEastPointer(pointedRoomListInstance1[8]) # Ramp has only one pointer pointing to Yellow Dais

    pointedRoomSetInstance1 = set(pointedRoomListInstance1) # Convert List to Set for purposes of the instance class
    instance1 = Instance(pointedRoomSetInstance1) # instantiate instance.

"""
INSTANCE 2 SETUP
"""
def initializeInstance2():
    global instance2
    pointedRoomListInstance2.append(Room("Green", "Columns")) # INDEX 1
    pointedRoomListInstance2.append(Room("Blue", "Columns")) # INDEX 2
    pointedRoomListInstance2.append(Room("Green", "Maze")) # INDEX 3
    pointedRoomListInstance2.append(Room("Red", "Maze")) # INDEX 4
    pointedRoomListInstance2.append(Room("Blue", "Maze")) # INDEX 5
    pointedRoomListInstance2.append(Room("Yellow", "Puzzle")) # INDEX 6
    pointedRoomListInstance2.append(Room("Green", "Puzzle")) # INDEX 7
    pointedRoomListInstance2.append(Room("Red", "Puzzle")) # INDEX 8
    pointedRoomListInstance2.append(Room("Yellow", "Dais")) # INDEX 9
    pointedRoomListInstance2.append(Room("Blue", "Dais")) # INDEX 10
    pointedRoomListInstance2.append(Room("Yellow", "Underwater")) # INDEX 11
    pointedRoomListInstance2.append(Room("Red", "Underwater")) # INDEX 12
    pointedRoomListInstance2.append(Room("Colorless", "Ramp")) # INDEX 13

    # pointers for starting room ( edges ) INDEX 0
    pointedRoomListInstance2[0].setNorthPointer(pointedRoomListInstance2[4]) # north points to Red Maze room
    pointedRoomListInstance2[0].setEastPointer(pointedRoomListInstance2[1]) # east points to Green Columns room
    pointedRoomListInstance2[0].setSouthPointer(pointedRoomListInstance2[8]) # south points to Red Puzzle room
    pointedRoomListInstance2[0].setWestPointer(pointedRoomListInstance2[2]) # west points to Blue Columns room

    # pointers for Green Columns room ( edges ) INDEX 1
    pointedRoomListInstance2[1].setNorthPointer(pointedRoomListInstance2[2]) # north points to Blue Columns room
    pointedRoomListInstance2[1].setEastPointer(pointedRoomListInstance2[3]) # east points to Green Maze room
    pointedRoomListInstance2[1].setSouthPointer(pointedRoomListInstance2[1]) # south points to Green Columns room
    pointedRoomListInstance2[1].setWestPointer(pointedRoomListInstance2[9]) # west points to Yellow Dais room

    # pointers for Blue Columns room ( edges ) INDEX 2
    pointedRoomListInstance2[2].setNorthPointer(pointedRoomListInstance2[3]) # north points to Green Maze room
    pointedRoomListInstance2[2].setEastPointer(pointedRoomListInstance2[12]) # east points to Red Underwater room
    pointedRoomListInstance2[2].setSouthPointer(pointedRoomListInstance2[6]) # south points to Yellow Puzzle room
    pointedRoomListInstance2[2].setWestPointer(pointedRoomListInstance2[1]) # west points to Green Columns room
    
    # pointers for Green Maze room ( edges ) INDEX 3
    pointedRoomListInstance2[3].setNorthPointer(pointedRoomListInstance2[11]) # north points to Yellow Underwater room
    pointedRoomListInstance2[3].setEastPointer(pointedRoomListInstance2[4]) # east points to Red Maze room
    pointedRoomListInstance2[3].setSouthPointer(pointedRoomListInstance2[10]) # south points to Blue Dais room
    pointedRoomListInstance2[3].setWestPointer(pointedRoomListInstance2[12]) # west points to Red Underwater room

    # pointers for Red Maze room ( edges ) INDEX 4
    pointedRoomListInstance2[4].setNorthPointer(pointedRoomListInstance2[4]) # north points to Red Maze room
    pointedRoomListInstance2[4].setEastPointer(pointedRoomListInstance2[9]) # east points to Yellow Dais room
    pointedRoomListInstance2[4].setSouthPointer(pointedRoomListInstance2[2]) # south points to Blue Columns room
    pointedRoomListInstance2[4].setWestPointer(pointedRoomListInstance2[12]) # west points to Red Underwater room

    # pointers for Blue Maze room ( edges ) INDEX 5
    pointedRoomListInstance2[5].setNorthPointer(pointedRoomListInstance2[12]) # north points to Red Underwater room
    pointedRoomListInstance2[5].setEastPointer(pointedRoomListInstance2[9]) # east points to Yellow Dais room
    pointedRoomListInstance2[5].setSouthPointer(pointedRoomListInstance2[3]) # south points to Green Maze room
    pointedRoomListInstance2[5].setWestPointer(pointedRoomListInstance2[10]) # west points to Blue Dais room
    
    # pointers for Yellow Puzzle room ( edges ) INDEX 6
    pointedRoomListInstance2[6].setNorthPointer(pointedRoomListInstance2[7]) # north points to Green Puzzle Room
    pointedRoomListInstance2[6].setEastPointer(pointedRoomListInstance2[5]) # east points to Blue Maze room
    pointedRoomListInstance2[6].setSouthPointer(pointedRoomListInstance2[6]) # south points to Yellow Puzzle room
    pointedRoomListInstance2[6].setWestPointer(pointedRoomListInstance2[0]) # west points to Starting room

    # pointers for Green Puzzle room ( edges ) INDEX 7
    pointedRoomListInstance2[7].setNorthPointer(pointedRoomListInstance2[10]) # north points to Blue Dais room
    pointedRoomListInstance2[7].setEastPointer(pointedRoomListInstance2[6]) # east points to Yellow Puzzle room
    pointedRoomListInstance2[7].setSouthPointer(pointedRoomListInstance2[7]) # south points to Green Puzzle room 
    pointedRoomListInstance2[7].setWestPointer(pointedRoomListInstance2[4]) # west points to Red Maze room

    # pointers for Red Puzzle room ( edges ) INDEX 8
    pointedRoomListInstance2[8].setNorthPointer(pointedRoomListInstance2[7]) # north points to Green Puzzle room
    pointedRoomListInstance2[8].setEastPointer(pointedRoomListInstance2[11]) # east points to Yellow Underwater room
    pointedRoomListInstance2[8].setSouthPointer(pointedRoomListInstance2[8]) # south points to Red Puzzle room
    pointedRoomListInstance2[8].setWestPointer(pointedRoomListInstance2[9]) # west points to Yellow Dais room

    # pointers for Yellow Dais room ( edges ) INDEX 9
    pointedRoomListInstance2[9].setNorthPointer(pointedRoomListInstance2[5]) # north points to Blue Maze room
    pointedRoomListInstance2[9].setEastPointer(pointedRoomListInstance2[0]) # east points to Starting room
    pointedRoomListInstance2[9].setSouthPointer(pointedRoomListInstance2[8]) # south points to Red Puzzle room
    pointedRoomListInstance2[9].setWestPointer(pointedRoomListInstance2[7]) # west points to Green Puzzle room

    # pointers for Blue Dais room ( edges ) INDEX 10
    pointedRoomListInstance2[10].setNorthPointer(pointedRoomListInstance2[2]) # north points to Blue Columns room
    pointedRoomListInstance2[10].setEastPointer(pointedRoomListInstance2[11]) # east points to Yellow Underwater room
    pointedRoomListInstance2[10].setSouthPointer(pointedRoomListInstance2[11]) # south points to Yellow Underwater room
    pointedRoomListInstance2[10].setWestPointer(pointedRoomListInstance2[0]) # west points to Starting room

    # pointers for Yellow Underwater room ( edges ) INDEX 11
    pointedRoomListInstance2[11].setNorthPointer(pointedRoomListInstance2[0]) # north points to Starting room
    pointedRoomListInstance2[11].setEastPointer(pointedRoomListInstance2[3]) # east points to Green Maze room
    pointedRoomListInstance2[11].setSouthPointer(pointedRoomListInstance2[10]) # south points to Blue Dais room
    pointedRoomListInstance2[11].setWestPointer(pointedRoomListInstance2[13]) # west points to Ramp room

    # pointers for Red Underwater room ( edges ) INDEX 12
    pointedRoomListInstance2[12].setNorthPointer(pointedRoomListInstance2[8]) # north points to Red Puzzle room
    pointedRoomListInstance2[12].setEastPointer(pointedRoomListInstance2[5]) # east points to Blue Maze room
    pointedRoomListInstance2[12].setSouthPointer(pointedRoomListInstance2[9]) # south points to Yellow Dais room
    pointedRoomListInstance2[12].setWestPointer(pointedRoomListInstance2[5]) # west points to Blue Maze room

    pointedRoomListInstance2[13].setEastPointer(pointedRoomListInstance2[6]) # Ramp has only one pointer pointing to Yellow Puzzle room

    pointedRoomSetInstance2 = set(pointedRoomListInstance2) # Convert List to Set for purposes of the instance class
    instance2 = Instance(pointedRoomSetInstance2) # instantiate instance.

"""
INSTANCE 3 SETUP
"""
def initializeInstance3():
    global instance3
    pointedRoomListInstance3.append(Room("Yellow", "Columns")) # INDEX 1
    pointedRoomListInstance3.append(Room("Red", "Columns")) # INDEX 2
    pointedRoomListInstance3.append(Room("Yellow", "Maze")) # INDEX 3
    pointedRoomListInstance3.append(Room("Blue", "Maze")) # INDEX 4
    pointedRoomListInstance3.append(Room("Green", "Puzzle")) # INDEX 5
    pointedRoomListInstance3.append(Room("Red", "Puzzle")) # INDEX 6
    pointedRoomListInstance3.append(Room("Blue", "Puzzle")) # INDEX 7
    pointedRoomListInstance3.append(Room("Green", "Dais")) # INDEX 8
    pointedRoomListInstance3.append(Room("Red", "Dais")) # INDEX 9
    pointedRoomListInstance3.append(Room("Yellow", "Underwater")) # INDEX 10
    pointedRoomListInstance3.append(Room("Green", "Underwater")) # INDEX 11
    pointedRoomListInstance3.append(Room("Blue", "Underwater")) # INDEX 12
    pointedRoomListInstance3.append(Room("Colorless", "Ramp")) # INDEX 13
    pointedRoomListInstance3.append(Room("Green", "Columns")) # INDEX 14

    # pointers for starting room  ( edges ) INDEX 0
    pointedRoomListInstance3[0].setNorthPointer(pointedRoomListInstance3[11]) # north points to Green Underwater room
    pointedRoomListInstance3[0].setEastPointer(pointedRoomListInstance3[7]) # east points to Blue Puzzle room
    pointedRoomListInstance3[0].setSouthPointer(pointedRoomListInstance3[6]) # south points to Red Puzzle room
    pointedRoomListInstance3[0].setWestPointer(pointedRoomListInstance3[10]) # west points to Yellow Underwater room

    # pointers for Yellow Columns room ( edges ) INDEX 1
    pointedRoomListInstance3[1].setNorthPointer(pointedRoomListInstance3[3]) # north points to Yellow Maze room
    pointedRoomListInstance3[1].setEastPointer(pointedRoomListInstance3[0]) # east points to Starting room
    pointedRoomListInstance3[1].setSouthPointer(pointedRoomListInstance3[1]) # south points to Yellow Columns room
    pointedRoomListInstance3[1].setWestPointer(pointedRoomListInstance3[10]) # west points to Yellow Underwater room

    # pointers for Red Columns room ( edges ) INDEX 2
    pointedRoomListInstance3[2].setNorthPointer(pointedRoomListInstance3[0]) # north points to Starting room
    pointedRoomListInstance3[2].setEastPointer(pointedRoomListInstance3[5]) # east points to Green Puzzle room
    pointedRoomListInstance3[2].setSouthPointer(pointedRoomListInstance3[3]) # south points to Yellow Maze room
    pointedRoomListInstance3[2].setWestPointer(pointedRoomListInstance3[4]) # west points to Blue Maze room
    
    # pointers for Yellow Maze room ( edges ) INDEX 3
    pointedRoomListInstance3[3].setNorthPointer(pointedRoomListInstance3[11]) # north points to Green Underwater room
    pointedRoomListInstance3[3].setEastPointer(pointedRoomListInstance3[6]) # east points to Red Puzzle room
    pointedRoomListInstance3[3].setSouthPointer(pointedRoomListInstance3[0]) # south points to Starting room
    pointedRoomListInstance3[3].setWestPointer(pointedRoomListInstance3[9]) # west points to Red Dais room

    # pointers for Blue Maze room ( edges ) INDEX 4
    pointedRoomListInstance3[4].setNorthPointer(pointedRoomListInstance3[8]) # north points to Green Dais room
    pointedRoomListInstance3[4].setEastPointer(pointedRoomListInstance3[2]) # east points to Red Columns room
    pointedRoomListInstance3[4].setSouthPointer(pointedRoomListInstance3[0]) # south points to Starting room
    pointedRoomListInstance3[4].setWestPointer(pointedRoomListInstance3[7]) # west points to Blue Puzzle room
    
    # pointers for Green Puzzle room ( edges ) INDEX 5
    pointedRoomListInstance3[5].setNorthPointer(pointedRoomListInstance3[8]) # north points to Green Dais room
    pointedRoomListInstance3[5].setEastPointer(pointedRoomListInstance3[13]) # east points to Ramp room
    pointedRoomListInstance3[5].setSouthPointer(pointedRoomListInstance3[1]) # south points to Yellow Columns room
    pointedRoomListInstance3[5].setWestPointer(pointedRoomListInstance3[7]) # west points to Blue Puzzle room

    # pointers for Red Puzzle room ( edges ) INDEX 6
    pointedRoomListInstance3[6].setNorthPointer(pointedRoomListInstance3[8]) # north points to Green Dais room
    pointedRoomListInstance3[6].setEastPointer(pointedRoomListInstance3[1]) # east points to Yellow Columns room
    pointedRoomListInstance3[6].setSouthPointer(pointedRoomListInstance3[12]) # south points to Blue Underwater room
    pointedRoomListInstance3[6].setWestPointer(pointedRoomListInstance3[2]) # west points to Red Columns room

    # pointers for Blue Puzzle room ( edges ) INDEX 7
    pointedRoomListInstance3[7].setNorthPointer(pointedRoomListInstance3[2]) # north points to Red Columns room
    pointedRoomListInstance3[7].setEastPointer(pointedRoomListInstance3[9]) # east points to Red Dais room
    pointedRoomListInstance3[7].setSouthPointer(pointedRoomListInstance3[3]) # south points to Yellow Maze room 
    pointedRoomListInstance3[7].setWestPointer(pointedRoomListInstance3[12]) # west points to Blue Underwater room

    # pointers for Green Dais room ( edges ) INDEX 8
    pointedRoomListInstance3[8].setNorthPointer(pointedRoomListInstance3[10]) # north points to Yellow Underwater room
    pointedRoomListInstance3[8].setEastPointer(pointedRoomListInstance3[11]) # east points to Green Underwater room
    pointedRoomListInstance3[8].setSouthPointer(pointedRoomListInstance3[4]) # south points to Blue Maze room
    pointedRoomListInstance3[8].setWestPointer(pointedRoomListInstance3[6]) # west points to Red Puzzle room

    # pointers for Red Dais room ( edges ) INDEX 9
    pointedRoomListInstance3[9].setNorthPointer(pointedRoomListInstance3[10]) # north points to Yellow Underwater room
    pointedRoomListInstance3[9].setEastPointer(pointedRoomListInstance3[5]) # east points to Green Puzzle room
    pointedRoomListInstance3[9].setSouthPointer(pointedRoomListInstance3[6]) # south points to Red Puzzle room
    pointedRoomListInstance3[9].setWestPointer(pointedRoomListInstance3[12]) # west points to Blue Underwater room

    # pointers for Yellow Underwater room ( edges ) INDEX 10
    pointedRoomListInstance3[10].setNorthPointer(pointedRoomListInstance3[1]) # north points to Yellow Columns room
    pointedRoomListInstance3[10].setEastPointer(pointedRoomListInstance3[2]) # east points to Red Columns room
    pointedRoomListInstance3[10].setSouthPointer(pointedRoomListInstance3[4]) # south points to Blue Maze room
    pointedRoomListInstance3[10].setWestPointer(pointedRoomListInstance3[8]) # west points to Green Dais room

    # pointers for Green Underwater room ( edges ) INDEX 11
    pointedRoomListInstance3[11].setNorthPointer(pointedRoomListInstance3[11]) # north points to Green Underwater room
    pointedRoomListInstance3[11].setEastPointer(pointedRoomListInstance3[3]) # east points to Yellow Maze room
    pointedRoomListInstance3[11].setSouthPointer(pointedRoomListInstance3[9]) # south points to Red Dais room
    pointedRoomListInstance3[11].setWestPointer(pointedRoomListInstance3[4]) # west points to Blue Maze room

    # pointers for Blue Underwater room ( edges ) INDEX 12
    pointedRoomListInstance3[12].setNorthPointer(pointedRoomListInstance3[12]) # north points to Blue Underwater room
    pointedRoomListInstance3[12].setEastPointer(pointedRoomListInstance3[5]) # east points to Green Puzzle room
    pointedRoomListInstance3[12].setSouthPointer(pointedRoomListInstance3[5]) # south points to Green Puzzle room
    pointedRoomListInstance3[12].setWestPointer(pointedRoomListInstance3[9]) # west points to Red Dais room

    # Ramp Room has no important pointers INDEX 13.

    # pointers for Green Columns Room ( edges ) INDEX 14
    # this room does exist and contradicts the general topology of the dungeon, however I did not make the dungeon.
    pointedRoomListInstance3[14].setNorthPointer(pointedRoomListInstance3[0]) # north points to Starting Room
    pointedRoomListInstance3[14].setEastPointer(pointedRoomListInstance3[0]) # east points to Starting Room
    pointedRoomListInstance3[14].setSouthPointer(pointedRoomListInstance3[0]) # south points to Starting Room
    pointedRoomListInstance3[14].setWestPointer(pointedRoomListInstance3[0]) # west points to Starting Room

    pointedRoomListInstance3[13].setEastPointer(pointedRoomListInstance3[5]) # Ramp has only one pointer pointing to Green Puzzle room
    

    pointedRoomSetInstance3 = set(pointedRoomListInstance3) # Convert List to Set for purposes of the instance class
    instance3 = Instance(pointedRoomSetInstance3) # instantiate instance.

"""
Modified maze-avoidance BFS Algorithm
"""

def prioBFS(instance, start_room, goal_room=None):
    visited = set()
    predecessor = dict()
    pq = []
    counter = itertools.count()  # unique sequence counter
    # Push starting node with priority 0 and unique count
    heapq.heappush(pq, (0, next(counter), start_room))
    visited.add(start_room)
    predecessor[start_room] = (None, None)

    while pq:
        current_priority, _, current_room = heapq.heappop(pq)

        if goal_room is not None and current_room == goal_room:
            path = []
            while current_room is not None:
                prev_room, pointer = predecessor[current_room]
                path.append((current_room, pointer.getDirection() if pointer else None))
                current_room = prev_room
            path.reverse()
            return path

        for pointer in current_room.getNeighboringRooms():
            neighbor_room = pointer.getRoomBeingPointedTo()
            if neighbor_room not in visited:
                priority = 0 if neighbor_room.getType().lower() != "maze" else 4
                visited.add(neighbor_room)
                predecessor[neighbor_room] = (current_room, pointer)
                heapq.heappush(pq, (priority, next(counter), neighbor_room))
"""
The discussion becomes DFS or BFS? is efficiency/memory capacity an issue for the user & if not what are the benefits of BFS?

Answer:
        BFS > DFS in this case because it ensures the same path & the shortest path every iteration
        despite the obvious memory constraints.

Why is memory contrainst not a concern?

Answer:
        The Shadow Crypt topology is not obvious to the user & BFS allows for fewer-hope paths to be found more efficiently 
        (comparitively speaking to DFS), meaning that this tool is more likely to be used in cases where the user mistakenly
        takes the wrong path and allows for the user to correct-course much quicker, and often times this will be by means of
        only a few hops.

NEW CONCERN: 
        Often times, the maze walls within the Shadow Crypt will change based on certain (often unbeknownst to the user) quest objectives.
        The implications of this is that these walls changing can create untraversable rooms giving invalid paths to the player.

MY SOLUTION:
        Implement a priority system within the breadth-first search algorithm prioritizing literally any other room to traverse to
        than the maze. This does not mean that mazes will not be ecountered in certain paths, however it makes it much less likely
        for the user to encounter any path constrainment.
"""


def bold(inputStr):
    return "\033[1m" + inputStr + "\033[0m"
def blue(inputStr):
    return "\033[34m" + inputStr + "\033[0m"
def green(inputStr):
    return "\033[32m" + inputStr + "\033[0m"
def red(inputStr):
    return "\033[31m" + inputStr + "\033[0m"
def yellow(inputStr):
    return "\033[33m" + inputStr + "\033[0m"
def orange(inputStr):
    return "\033[38;2;255;165;0m" + inputStr + "\033[0m"
def underline(inputStr):
    return "\033[4m" + inputStr + "\033[0m"
def colorize(color, input):
    if color.lower() == "yellow":
        return yellow(input)
    elif color.lower() == "green":
        return green(input)
    elif color.lower() == "blue":
        return blue(input)
    elif color.lower() == "red":
        return red(input)
    else:
        return bold(input)
        

def printPath(path):
    # print("Shortest path from source room to destination room in " + str(instancePathName) + " is:\n")
    directionLetterList = []  # Initialize outside to avoid scope issues
    
    if path:
        iter = 0
        for room, direction in path:
            if direction is None:
                print(f"Room: {colorize(room.getColor(), str(room))}")
            else:
                if iter < len(path) - 1:
                    print("Go " + underline(direction.upper()) + " to " + colorize(room.getColor(), str(room)) +"\nthen")
                else:
                    print("Go " + underline(direction.upper()) + " to " + colorize(room.getColor(), str(room)))
                # Append only if direction is a non-empty string
                if direction:
                    directionLetterList.append(direction[0])
            iter+= 1
        # If no path found or empty, handle gracefully
        if not directionLetterList:
            print("Congratulations, you're already here!")
    else:
        print("No path found")
    
    # Only if directionLetterList is populated
    s = ""
    for letter in directionLetterList:
        s += letter.upper()
    if s:
        print("or more simply: " + s)
    print("\n")


"""
#TEST CASES



initializeInstance1()
initializeInstance2()
initializeInstance3()

start1 = pointedRoomListInstance1[2]
goal1 = pointedRoomListInstance1[13]
path1 = prioBFS(instance1, start1, goal1)
start2 = pointedRoomListInstance2[0]
goal2 = pointedRoomListInstance2[13]
path2 = prioBFS(instance2, start2, goal2)
start3 = pointedRoomListInstance3[7]
goal3 = pointedRoomListInstance3[13]
path3 = prioBFS(instance3, start3, goal3)



#printPath(path1, "instance 1 [RED]")
#printPath(path2, "instance 2 [GREEN]")
#printPath(path3, "instance 3 [BLUE]")


"""

def yesNoAssociation(input):
    if(isinstance(input, str)):
        input = input.lower()
        validResponses = {"y", "n", "yes", "no"}
        if input in validResponses:
            return True
        else:
            if input == "":
                return False
            else:   
                # print("please enter either of y/n/yes/no (case insensitive)")
                return False
    else:
        print("please enter either of y/n/yes/no (case insensitive)")
        return False
def instanceAssociation(input):
    input = input.lower()
    validResponses = {"r", "g", "b", "red", "green", "blue"}
    if(input in validResponses):
        return True
    else:
        return False
    
def isExitChar(input):
    if input == "":
        print("Closing Program ... Thank you for using Crypt Router!")
        return True
    else:
        return False
def roomTerms(input):
    start = {"s","start"}
    yellowCol = {"yc", "yellowcolumns"}
    greenCol = {"gc","greencolumns"}
    redCol = {"rc","redcolumns"}
    blueCol = {"bc","bluecolumns"}
    yellowMaze = {"ym","yellowmaze"}
    greenMaze = {"gm","greenmaze"}
    redMaze = {"rm","redmaze"}
    blueMaze = {"bm","bluemaze"}
    yellowPuz = {"yp","yellowpuzzle"}
    greenPuz = {"gp","greenpuzzle"}
    redPuz = {"rp","redpuzzle"}
    bluePuz = {"bp","bluepuzzle"}
    yellowDais = {"yd","yellowdais"}
    greenDais = {"gd","greendais"}
    redDais = {"rd","reddais"}
    blueDais = {"bd","bluedais"}
    yellowUW = {"yu","yellowunderwater"}
    greenUW = {"gu","greenunderwater"}
    redUW = {"ru","redunderwater"}
    blueUW = {"bu","blueunderwater"}
    ramp = {"r","ramp"}
    if input in start:
        return "s"
    elif input in yellowCol:
        return "yc"
    elif input in greenCol:
        return "gc"
    elif input in redCol:
        return "rc"
    elif input in blueCol:
        return "bc"
    elif input in yellowMaze:
        return "ym"
    elif input in greenMaze:
        return "gm"
    elif input in redMaze:
        return "rm"
    elif input in blueMaze:
        return "bm"
    elif input in yellowPuz:
        return "yp"
    elif input in greenPuz:
        return "gp"
    elif input in redPuz:
        return "rp"
    elif input in bluePuz:
        return "bp"
    elif input in yellowDais:
        return "yd"
    elif input in greenDais:
        return "gd"
    elif input in redDais:
        return "rd"
    elif input in blueDais:
        return "bd"
    elif input in yellowUW:
        return "yu"
    elif input in greenUW:
        return "gu"
    elif input in redUW:
        return "ru"
    elif input in blueUW:
        return "bu"
    elif input in ramp:
        return "r"
    else:
        return "invalid room"
firstIteration = True
yesSet = {"y", "yes"}
print("\nWelcome to Crypt-Router! Ver 1.02\n\nThis is a software to help you navigate your way throughout the Shadow Crypt Dungeon in DDO.\n")
while True:
    needInstructions = False
    while firstIteration:
        firstTimer = input("Is this your first time using Crypt-Router? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit.\n"+ orange("Enter Here: "))
        if yesNoAssociation(firstTimer):
            if firstTimer in yesSet:
                needInstructions = True
                break
            else:
                break
        elif isExitChar(firstTimer):
            sys.exit()
        else:
            print("Invalid input, try again.")
    if needInstructions:    
        welcStr = "\nAs you may or may not know, Shadow Crypt is one of the most experience-dense quests along the entire heroic leveling arc."
        welcStr += "\nDespite that, many players still do not run Shadow Crypt with regularity throughout their heroic leveling experience."
        welcStr += "\nThis can primarily be attributed to the fact that there is virtually no way to know where you are going in the dungeon, even with a map."
        welcStr += "\nWhile there are resources online with solo/duo paths for 8 or 12 gears to help you complete the quest,\nthere's not much of a contingency plan for a wrong turn."
        welcStr += "\nThat's where Crypt-Router comes in! in the event that you either do not have access to the known paths or have found yourself in a room found separate from the path"
        welcStr += "\nyou can use Crypt-Router to find your way back to a specific room from any of the rooms you may find yourself in in any given instance"
        welcStr += "\n\n How do I use Crypt-Router?"
        welcStr += "\n\n\t - First, you will begin by letting the program know if you know what instance you are in or not."
        welcStr += "\n\n\t - Second, you will be asked which instance you are in if you know your current instance; if not, the program will help figure out your instance\n\t along side you."
        welcStr += "\n\n\t - Third, you will give the program which room you are currently in\n\t ( of which can be written out as given to you or abbrieviated by <first-letter-of-color><first-letter-of-structure> )"
        welcStr += "\n\n\t - Fourth, similarly to the last step you will let the program know which room you want to go to. Note: If you need a specific gear color,\n\t go to a room of that color."
        welcStr += "\n\nIMPORTANT NOTE:\t if you encounter a maze that you cannot traverse through, enter another room (sometimes more than one room away)\n\t and restart the program from there"
        welcStr += ". However, the progam operates in such a way that most of the times you can avoid mazes altogether."
        welcStr += "\n\nAfter these steps, you will have been given a path formatted by which room you need to go to and which direction to go as well as\nuppercase directional format as traditionally used on DDO wiki. i.e EWSNE"
        
        print(welcStr)
    
    while True:
        startInput = input("\n\nReady to Find your way? type 'yes' or 'y' if so & 'no' or 'n' if not.\n"+ orange("Enter Here: "))
        if(yesNoAssociation(startInput)):
            if startInput in yesSet:
                break
            else:
                print("Closing Program ... Thank you for using Crypt Router!")
                sys.exit()
        else:
            print("Invalid Input, please try again.")
    while True:
        userKnowInstance = input("\nDo you know which instance you are in? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit\n"+ orange("Enter Response: ")) # primary question for this while loop
        flagDD = None # initialize as None
        exitedInnerLoop = False
        inInstance1 = False
        inInstance2 = False
        inInstance3 = False
        isUnsure = False
        wasUnsure = False
        if yesNoAssociation(userKnowInstance): # checks to see if the response is a valid affirmative/negative response
            userKnowInstance = userKnowInstance.strip().lower() # use to make case insensitive
            while True: # use a while loop to loop back for mistaken instance responses
                if userKnowInstance in yesSet: # basically, cannot proceed if they do not know their instance.
                    flagDD = False # because we know our instance DD becomes irrelevant
                    userInstance = input("\nWhich instance are you in? (r/g/b/red/green/blue) or press enter to exit\n"+ orange("Enter Response: ")) # primary questions for this while loop
                    if instanceAssociation(userInstance): # verifies if any of the user's responses correlate to valid instances
                        userInstance = userInstance.strip().lower() # use to make case insensitive
                        # print(userInstance)
                        # print(isinstance(userInstance, str))
                        if userInstance == "r" or  userInstance == "red":
                            if firstIteration:
                                initializeInstance1()
                            inInstance1 = True
                            # print("DEBUG: instance 1 initialized.")
                            break # if valid instance, no need to continue while loop
                        elif userInstance == "g" or userInstance ==  "green":
                            if firstIteration:
                                initializeInstance2()
                            inInstance2 = True
                            # print("DEBUG: instance 2 initialized.")
                            break # if valid instance, no need to continue while loop
                        elif userInstance == "b" or userInstance == "blue":
                            if firstIteration:
                                initializeInstance3()
                            inInstance3 = True
                            # print("DEBUG: instance 3 initialized.")
                            break # if valid instance, no need to continue while loop
                    elif isExitChar(userInstance):
                        # let outter loop know that there was an exit within the inner loop so that the outter loop can automatically break
                        sys.exit()
                    else:
                        print("please enter a valid instance")
                        continue # if invalid instance, ask again for a valid instance
                else:
                    userDD = input("\nDo you Have Death's Door charges or Dimension Door Spell? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit\n"+ orange("Enter Response: ")) # allows for alternative to check instance ( returns player to starting room )
                    if(yesNoAssociation(userDD) and userDD in yesSet):
                        flagDD = True
                        print("Please use Deaths Door/Dimension door to return to the starting room, and go east to learn which instance you are in.\n")
                        break
                    elif isExitChar(userDD):
                        exitedInnerLoop = True
                        break
                    else:
                        # initialize all 3 instances and offer them a path to try, if path does not properly get from A to B, then try next instance, and so on.
                        if firstIteration:
                            initializeInstance1()
                            initializeInstance2()
                            initializeInstance3()
                        isUnsure = True
                        break
        elif isExitChar(userKnowInstance):
            #check if there was a break within the outter loop or inner loop
            sys.exit()
        else:
            print("\ninvalid input, please try again.")
            continue
        if flagDD: # if the user had dimension door, restart the loop because now they should know their instance.
            continue
        while True:
            if(inInstance1):
                firstIteration = False
                # populate a list with the valid map-form string identifiers of the room in given instance
                roomsInInstance1 = ["s","gc", "rc", "bc", "ym", "gm", "bm", "yp", "yd", "gd", "rd", "ru", "bu", "r"]
                abrvSet = set(roomsInInstance1) # transform map-form string list into set for element checks
                stringToObjMap = dict(zip(roomsInInstance1, pointedRoomListInstance1)) # create map
                print("\n\n[Shadow Crypt " + bold(red("Red")) + " Instance]\n")
                while True:
                    for room in pointedRoomListInstance1: # display rooms for user
                        strng = ""
                        roomColor = room.getColor().lower()
                        if roomColor == "yellow":
                            strng = yellow(str(room))
                        elif roomColor == "green":
                            strng = green(str(room))
                        elif roomColor == "red":
                            strng = red(str(room))
                        elif roomColor == "blue":
                            strng = blue(str(room))
                        else:
                            strng = bold(str(room))
                        print(strng)    
                    while True: # dialogue loop for starting room
                        raw = input("\nWhich of these rooms are you currently in? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\n"+ orange("Enter Room: ")) # collect input
                        normalized = raw.strip().lower().replace(" ", "") # normalize input
                        startingRoomString = roomTerms(normalized) # check to see if valid room term
                        if startingRoomString in abrvSet: # easy element check from set copy of map-form list
                            startingRoom = stringToObjMap.get(startingRoomString) # because room is mapped to string, easy room retrieval
                            break # break dialogue loop, no more need to continue this query
                        elif isExitChar(raw): # check raw input to see if it is the exit character
                            sys.exit()
                        else:
                            print("invalid room, please try again\n") # inform the user of the error of their ways
                            continue # restart the while loop
                    print("\n\n[Shadow Crypt " + bold(red("Red")) + " Instance]\n")
                    for room in pointedRoomListInstance1: # display rooms for user
                        strng = ""
                        roomColor = room.getColor().lower()
                        if roomColor == "yellow":
                            strng = yellow(str(room))
                        elif roomColor == "green":
                            strng = green(str(room))
                        elif roomColor == "red":
                            strng = red(str(room))
                        elif roomColor == "blue":
                            strng = blue(str(room))
                        else:
                            strng = bold(str(room))
                        print(strng)
                    while True: # dialogue loop for destination room
                        raw = input("\nWhich of these rooms are you trying to reach? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\n"+ orange("Enter Room: ")) # collect input
                        normalized = raw.strip().lower().replace(" ", "") # normalize input
                        destinationRoomString = roomTerms(normalized) # check to see if valid room term
                        if destinationRoomString in abrvSet: # easy element check from set copy of map-form list
                            destinationRoom = stringToObjMap.get(destinationRoomString) # because room is mapped to string, easy room retrieval
                            break # break dialogue loop, no more need to continue this query
                        elif isExitChar(raw): # check raw input to see if it is the exit character
                            sys.exit()
                        else:
                            print("invalid room, please try again\n") # inform the user of the error of their ways
                            continue # restart the while loop
                    path = prioBFS(instance1, startingRoom, destinationRoom) # perform priority BFS, store path as a list
                    print("\nHere is your path from " + str(startingRoom) + " to " + str(destinationRoom) + "\n") # reiterate to the user their chosen rooms
                    printPath(path) # display path to user
                    while True:
                        again = input("\nNeed to get to another room? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit\n"+ orange("Enter Response: "))
                        if(yesNoAssociation(again)):
                            if again in yesSet:
                                break
                            else:
                                print("Closing Program ... Thank you for using Crypt Router!")
                                sys.exit()
                        elif isExitChar(again):
                            sys.exit()
                        else:
                            print("invalid response, try again")
                            continue
            elif(inInstance2):
                firstIteration = False
                # populate a list with the valid map-form string identifiers of the room in given instance
                roomsInInstance2 = ["s","gc", "bc", "gm", "rm", "bm", "yp", "gp", "rp", "yd", "bd", "yu", "ru", "r"]
                abrvSet = set(roomsInInstance2) # transform map-form string list into set for element checks
                stringToObjMap = dict(zip(roomsInInstance2, pointedRoomListInstance2)) # create map
                print("\n\n[Shadow Crypt " + bold(green("Green")) + " Instance]\n")
                for room in pointedRoomListInstance2: # display rooms for user
                    strng = ""
                    roomColor = room.getColor().lower()
                    if roomColor == "yellow":
                        strng = yellow(str(room))
                    elif roomColor == "green":
                        strng = green(str(room))
                    elif roomColor == "red":
                        strng = red(str(room))
                    elif roomColor == "blue":
                        strng = blue(str(room))
                    else:
                        strng = bold(str(room))
                    print(strng)
                while True: # dialogue loop for starting room
                    raw = input("\nWhich of these rooms are you currently in? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\n"+ orange("Enter Room: ")) # collect input
                    normalized = raw.strip().lower().replace(" ", "") # normalize input
                    startingRoomString = roomTerms(normalized) # check to see if valid room term
                    if startingRoomString in abrvSet: # easy element check from set copy of map-form list
                        startingRoom = stringToObjMap.get(startingRoomString) # because room is mapped to string, easy room retrieval
                        break # break dialogue loop, no more need to continue this query
                    elif isExitChar(raw): # check raw input to see if it is the exit character
                        sys.exit()
                    else:
                        print("invalid room, please try again\n") # inform the user of the error of their ways
                        continue # restart the while loop
                print("\n\n[Shadow Crypt " + bold(green("Green")) + " Instance]\n")
                for room in pointedRoomListInstance2: # display rooms for user
                    strng = ""
                    roomColor = room.getColor().lower()
                    if roomColor == "yellow":
                        strng = yellow(str(room))
                    elif roomColor == "green":
                        strng = green(str(room))
                    elif roomColor == "red":
                        strng = red(str(room))
                    elif roomColor == "blue":
                        strng = blue(str(room))
                    else:
                        strng = bold(str(room))
                    print(strng)
                while True: # dialogue loop for destination room
                    raw = input("\nWhich of these rooms are you trying to reach? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\n"+ orange("Enter Room: ")) # collect input
                    normalized = raw.strip().lower().replace(" ", "") # normalize input
                    destinationRoomString = roomTerms(normalized) # check to see if valid room term
                    if destinationRoomString in abrvSet: # easy element check from set copy of map-form list
                        destinationRoom = stringToObjMap.get(destinationRoomString) # because room is mapped to string, easy room retrieval
                        break # break dialogue loop, no more need to continue this query
                    elif isExitChar(raw): # check raw input to see if it is the exit character
                        sys.exit()
                    else:
                        print("invalid room, please try again\n") # inform the user of the error of their ways
                        continue # restart the while loop
                path = prioBFS(instance2, startingRoom, destinationRoom) # perform priority BFS, store path as a list
                print("\nHere is your path from " + str(startingRoom) + " to " + str(destinationRoom) + "\n") # reiterate to the user their chosen rooms
                printPath(path) # display path to user
                while True:
                    again = input("\nNeed to get to another room? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit"+ orange("Enter Response: "))
                    if(yesNoAssociation(again)):
                        if again in yesSet:
                            break
                        else:
                            print("Closing Program ... Thank you for using Crypt Router!")
                            sys.exit()
                    elif isExitChar(again):
                        sys.exit()
                    else:
                        print("invalid response, try again")
                        continue
            elif(inInstance3):
                firstIteration = False
                # populate a list with the valid map-form string identifiers of the room in given instance
                roomsInInstance3 = ["s","yc", "rc", "ym", "bm", "gp", "rp", "bp", "gd", "rd", "yu", "gu", "bu", "r", "gc"]
                abrvSet = set(roomsInInstance3) # transform map-form string list into set for element checks
                stringToObjMap = dict(zip(roomsInInstance3, pointedRoomListInstance3)) # create map
                print("\n\n[Shadow Crypt " + bold(blue("Blue")) + " Instance]\n")
                for room in pointedRoomListInstance3: # display rooms for user
                    strng = ""
                    roomColor = room.getColor().lower()
                    if roomColor == "yellow":
                        strng = yellow(str(room))
                    elif roomColor == "green":
                        strng = green(str(room))
                    elif roomColor == "red":
                        strng = red(str(room))
                    elif roomColor == "blue":
                        strng = blue(str(room))
                    else:
                        strng = bold(str(room))
                    print(strng)
                while True: # dialogue loop for starting room
                    raw = input("\nWhich of these rooms are you currently in? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\n"+ orange("Enter Room: ")) # collect input
                    normalized = raw.strip().lower().replace(" ", "") # normalize input
                    startingRoomString = roomTerms(normalized) # check to see if valid room term
                    if startingRoomString in abrvSet: # easy element check from set copy of map-form list
                        startingRoom = stringToObjMap.get(startingRoomString) # because room is mapped to string, easy room retrieval
                        break # break dialogue loop, no more need to continue this query
                    elif isExitChar(raw): # check raw input to see if it is the exit character
                        sys.exit()
                    else:
                        print("invalid room, please try again\n") # inform the user of the error of their ways
                        continue # restart the while loop
                print("\n\n[Shadow Crypt " + bold(blue("Blue")) + " Instance]\n")
                for room in pointedRoomListInstance3: # display rooms for user
                    strng = ""
                    roomColor = room.getColor().lower()
                    if roomColor == "yellow":
                        strng = yellow(str(room))
                    elif roomColor == "green":
                        strng = green(str(room))
                    elif roomColor == "red":
                        strng = red(str(room))
                    elif roomColor == "blue":
                        strng = blue(str(room))
                    else:
                        strng = bold(str(room))
                    print(strng)
                while True: # dialogue loop for destination room
                    raw = input("\nWhich of these rooms are you trying to reach? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\n"+ orange("Enter Room: ")) # collect input
                    normalized = raw.strip().lower().replace(" ", "") # normalize input
                    destinationRoomString = roomTerms(normalized) # check to see if valid room term
                    if destinationRoomString in abrvSet: # easy element check from set copy of map-form list
                        destinationRoom = stringToObjMap.get(destinationRoomString) # because room is mapped to string, easy room retrieval
                        break # break dialogue loop, no more need to continue this query
                    elif isExitChar(raw): # check raw input to see if it is the exit character
                        sys.exit()
                    else:
                        print("invalid room, please try again\n") # inform the user of the error of their ways
                        continue # restart the while loop
                path = prioBFS(instance3, startingRoom, destinationRoom) # perform priority BFS, store path as a list
                print("\nHere is your path from " + str(startingRoom) + " to " + str(destinationRoom) + "\n") # reiterate to the user their chosen rooms
                printPath(path) # display path to user
                while True:
                    again = input("\nNeed to get to another room? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit\n"+ orange("Enter Response: "))
                    if(yesNoAssociation(again)):
                        if again in yesSet:
                            break
                        else:
                            print("Closing Program ... Thank you for using Crypt Router!")
                            sys.exit()
                    elif isExitChar(again):
                        sys.exit()
                    else:
                        print("invalid response, try again")
                        continue
                print(inInstance3)    
            elif(isUnsure):
                firstIteration = False
                while isUnsure:
                    print("So let's try instance 1 first!\n")
                    # populate a list with the valid map-form string identifiers of the room in given instance
                    roomsInInstance1 = ["s","gc", "rc", "bc", "ym", "gm", "bm", "yp", "yd", "gd", "rd", "ru", "bu", "r"]
                    abrvSet = set(roomsInInstance1) # transform map-form string list into set for element checks
                    stringToObjMap = dict(zip(roomsInInstance1, pointedRoomListInstance1)) # create map
                    print("\n\n[Shadow Crypt " + bold(red("Red")) + " Instance]\n")
                    
                    for room in pointedRoomListInstance1: # display rooms for user
                        strng = ""
                        roomColor = room.getColor().lower()
                        if roomColor == "yellow":
                            strng = yellow(str(room))
                        elif roomColor == "green":
                            strng = green(str(room))
                        elif roomColor == "red":
                            strng = red(str(room))
                        elif roomColor == "blue":
                            strng = blue(str(room))
                        else:
                            strng = bold(str(room))
                        print(strng)
                    while True: # dialogue loop for starting room
                        raw = input("\nWhich of these rooms are you currently in? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\n"+ orange("Enter Room: ")) # collect input
                        normalized = raw.strip().lower().replace(" ", "") # normalize input
                        startingRoomString = roomTerms(normalized) # check to see if valid room term
                        if startingRoomString in abrvSet: # easy element check from set copy of map-form list
                            startingRoom = stringToObjMap.get(startingRoomString) # because room is mapped to string, easy room retrieval
                            break # break dialogue loop, no more need to continue this query
                        elif isExitChar(raw): # check raw input to see if it is the exit character
                            sys.exit()
                        else:
                            print("invalid room, please try again\n") # inform the user of the error of their ways
                            continue # restart the while loop
                    print("\n\n[Shadow Crypt " + bold(red("Red")) + " Instance]\n")
                    for room in pointedRoomListInstance1: # display rooms for user
                        strng = ""
                        roomColor = room.getColor().lower()
                        if roomColor == "yellow":
                            strng = yellow(str(room))
                        elif roomColor == "green":
                            strng = green(str(room))
                        elif roomColor == "red":
                            strng = red(str(room))
                        elif roomColor == "blue":
                            strng = blue(str(room))
                        else:
                            strng = bold(str(room))
                        print(strng)
                    while True: # dialogue loop for destination room
                        raw = input("\nWhich of these rooms are you trying to reach? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\n"+ orange("Enter Room: ")) # collect input
                        normalized = raw.strip().lower().replace(" ", "") # normalize input
                        destinationRoomString = roomTerms(normalized) # check to see if valid room term
                        if destinationRoomString in abrvSet: # easy element check from set copy of map-form list
                            destinationRoom = stringToObjMap.get(destinationRoomString) # because room is mapped to string, easy room retrieval
                            break # break dialogue loop, no more need to continue this query
                        elif isExitChar(raw): # check raw input to see if it is the exit character
                            sys.exit()
                        else:
                            print("invalid room, please try again\n") # inform the user of the error of their ways
                            continue # restart the while loop
                    path = prioBFS(instance1, startingRoom, destinationRoom) # perform priority BFS, store path as a list
                    print("\nHere is your path from " + str(startingRoom) + " to " + str(destinationRoom) + "\n") # reiterate to the user their chosen rooms
                    printPath(path) # display path to user
                    while True:
                        workInput = input("\nDid that work? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit\n"+ orange("Enter Response: "))
                        if yesNoAssociation(workInput):
                            if workInput in yesSet:
                                while True:
                                    again = input("\nNeed to get to another room? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit\n"+ orange("Enter Response: "))
                                    if(yesNoAssociation(again)):
                                        if again in yesSet:
                                            break
                                        else:
                                            print("Closing Program ... Thank you for using Crypt Router!")
                                            sys.exit()
                                    elif isExitChar(again):
                                        sys.exit()
                                    else:
                                        print("invalid response, try again")
                                        continue
                                isUnsure = False
                                inInstance1 = True
                                break
                            else:
                                break
                        elif isExitChar(workInput):
                            sys.exit()
                        else:
                            print("\ninvalid response, please try again\n")
                            continue
                    # out of precaution, set variables in scope to none
                    stringToObjMap = None
                    abrvSet = None
                    print("\nnext, let's try instance 2!")
                    # populate a list with the valid map-form string identifiers of the room in given instance
                    roomsInInstance2 = ["s","gc", "bc", "gm", "rm", "bm", "yp", "gp", "rp", "yd", "bd", "yu", "ru", "r"]
                    abrvSet = set(roomsInInstance2) # transform map-form string list into set for element checks
                    stringToObjMap = dict(zip(roomsInInstance2, pointedRoomListInstance2)) # create map
                    print("\n\n[Shadow Crypt " + bold(green("Green")) + " Instance]\n")
                    for room in pointedRoomListInstance2: # display rooms for user
                        strng = ""
                        roomColor = room.getColor().lower()
                        if roomColor == "yellow":
                            strng = yellow(str(room))
                        elif roomColor == "green":
                            strng = green(str(room))
                        elif roomColor == "red":
                            strng = red(str(room))
                        elif roomColor == "blue":
                            strng = blue(str(room))
                        else:
                            strng = bold(str(room))
                        print(strng)
                    while True: # dialogue loop for starting room
                        raw = input("\nWhich of these rooms are you currently in? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\n"+ orange("Enter Room: ")) # collect input
                        normalized = raw.strip().lower().replace(" ", "") # normalize input
                        startingRoomString = roomTerms(normalized) # check to see if valid room term
                        if startingRoomString in abrvSet: # easy element check from set copy of map-form list
                            startingRoom = stringToObjMap.get(startingRoomString) # because room is mapped to string, easy room retrieval
                            break # break dialogue loop, no more need to continue this query
                        elif isExitChar(raw): # check raw input to see if it is the exit character
                            sys.exit()
                        else:
                            print("invalid room, please try again\n") # inform the user of the error of their ways
                            continue # restart the while loop
                    print("\n\n[Shadow Crypt " + bold(green("Green")) + " Instance]\n")
                    for room in pointedRoomListInstance2: # display rooms for user
                        strng = ""
                        roomColor = room.getColor().lower()
                        if roomColor == "yellow":
                            strng = yellow(str(room))
                        elif roomColor == "green":
                            strng = green(str(room))
                        elif roomColor == "red":
                            strng = red(str(room))
                        elif roomColor == "blue":
                            strng = blue(str(room))
                        else:
                            strng = bold(str(room))
                        print(strng)
                    while True: # dialogue loop for destination room
                        raw = input("\nWhich of these rooms are you trying to reach? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\n"+ orange("Enter Room: ")) # collect input
                        normalized = raw.strip().lower().replace(" ", "") # normalize input
                        destinationRoomString = roomTerms(normalized) # check to see if valid room term
                        if destinationRoomString in abrvSet: # easy element check from set copy of map-form list
                            destinationRoom = stringToObjMap.get(destinationRoomString) # because room is mapped to string, easy room retrieval
                            break # break dialogue loop, no more need to continue this query
                        elif isExitChar(raw): # check raw input to see if it is the exit character
                            sys.exit()
                        else:
                            print("invalid room, please try again\n") # inform the user of the error of their ways
                            continue # restart the while loop
                    path = prioBFS(instance2, startingRoom, destinationRoom) # perform priority BFS, store path as a list
                    print("\nHere is your path from " + str(startingRoom) + " to " + str(destinationRoom) + "\n") # reiterate to the user their chosen rooms
                    printPath(path) # display path to user
                    while True:
                        workInput = input("\nDid that work? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit\n"+ orange("Enter Response: "))
                        if yesNoAssociation(workInput):
                            if workInput in yesSet:
                                while True:
                                    again = input("\nNeed to get to another room? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit\n"+ orange("Enter Response: "))
                                    if(yesNoAssociation(again)):
                                        if again in yesSet:
                                            break
                                        else:
                                            print("Closing Program ... Thank you for using Crypt Router!")
                                            sys.exit()
                                    elif isExitChar(again):
                                        sys.exit()
                                    else:
                                        print("invalid response, try again")
                                        continue
                                isUnsure = False
                                inInstance2 = True
                                break
                            else:
                                break
                        elif isExitChar(workInput):
                            sys.exit()
                        else:
                            print("\ninvalid response, please try again\n")
                            continue
                    # out of precaution, set variables in scope to none
                    stringToObjMap = None
                    abrvSet = None
                    print("\nThat's Okay! last but not least, let's try instance 3!")
                    # populate a list with the valid map-form string identifiers of the room in given instance
                    roomsInInstance3 = ["s","yc", "rc", "ym", "bm", "gp", "rp", "bp", "gd", "rd", "yu", "gu", "bu", "r", "gc"]
                    abrvSet = set(roomsInInstance3) # transform map-form string list into set for element checks
                    stringToObjMap = dict(zip(roomsInInstance3, pointedRoomListInstance3)) # create map
                    print("\n\n[Shadow Crypt " + bold(blue("Blue")) + " Instance]\n")
                    for room in pointedRoomListInstance3: # display rooms for user
                        strng = ""
                        roomColor = room.getColor().lower()
                        if roomColor == "yellow":
                            strng = yellow(str(room))
                        elif roomColor == "green":
                            strng = green(str(room))
                        elif roomColor == "red":
                            strng = red(str(room))
                        elif roomColor == "blue":
                            strng = blue(str(room))
                        else:
                            strng = bold(str(room))
                        print(strng)
                    while True: # dialogue loop for starting room
                        raw = input("\nWhich of these rooms are you currently in? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\n"+ orange("Enter Room: ")) # collect input
                        normalized = raw.strip().lower().replace(" ", "") # normalize input
                        startingRoomString = roomTerms(normalized) # check to see if valid room term
                        if startingRoomString in abrvSet: # easy element check from set copy of map-form list
                            startingRoom = stringToObjMap.get(startingRoomString) # because room is mapped to string, easy room retrieval
                            break # break dialogue loop, no more need to continue this query
                        elif isExitChar(raw): # check raw input to see if it is the exit character
                            sys.exit()
                        else:
                            print("invalid room, please try again\n") # inform the user of the error of their ways
                            continue # restart the while loop
                    print("\n\n[Shadow Crypt " + bold(blue("Blue")) + " Instance]\n")
                    for room in pointedRoomListInstance3: # display rooms for user
                        strng = ""
                        roomColor = room.getColor().lower()
                        if roomColor == "yellow":
                            strng = yellow(str(room))
                        elif roomColor == "green":
                            strng = green(str(room))
                        elif roomColor == "red":
                            strng = red(str(room))
                        elif roomColor == "blue":
                            strng = blue(str(room))
                        else:
                            strng = bold(str(room))
                        print(strng)
                    while True: # dialogue loop for destination room
                        raw = input("\nWhich of these rooms are you trying to reach? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\n"+ orange("Enter Room: ")) # collect input
                        normalized = raw.strip().lower().replace(" ", "") # normalize input
                        destinationRoomString = roomTerms(normalized) # check to see if valid room term
                        if destinationRoomString in abrvSet: # easy element check from set copy of map-form list
                            destinationRoom = stringToObjMap.get(destinationRoomString) # because room is mapped to string, easy room retrieval
                            break # break dialogue loop, no more need to continue this query
                        elif isExitChar(raw): # check raw input to see if it is the exit character
                            sys.exit()
                        else:
                            print("invalid room, please try again\n") # inform the user of the error of their ways
                            continue # restart the while loop
                    path = prioBFS(instance3, startingRoom, destinationRoom) # perform priority BFS, store path as a list
                    print("\nHere is your path from " + str(startingRoom) + " to " + str(destinationRoom) + "\n") # reiterate to the user their chosen rooms
                    printPath(path) # display path to user
                    while True:
                        workInput = input("\nDid that work? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit\n"+ orange("Enter Response: "))
                        if yesNoAssociation(workInput):
                            if workInput in yesSet:
                                while True:
                                    again = input("\nNeed to get to another room? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit\n"+ orange("Enter Response: "))
                                    if(yesNoAssociation(again)):
                                        if again in yesSet:
                                            break
                                        else:
                                            print("Closing Program ... Thank you for using Crypt Router!")
                                            sys.exit()
                                    elif isExitChar(again):
                                        sys.exit()
                                    else:
                                        print("invalid response, try again")
                                        continue
                                isUnsure = False
                                inInstance3 = True
                                break
                            else:
                                isUnsure = False
                                wasUnsure = True
                                break
                        elif isExitChar(workInput):
                            sys.exit()
                        else:
                            print("\ninvalid response, please try again\n")
                            continue
                break
        if wasUnsure:
            print("\nI'm sorry that didn't work.")
            while True:
                restartQuery = input("\nWould you like to restart the program and try again? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit\n"+ orange("Enter Response: "))
                if yesNoAssociation(restartQuery):
                    if(restartQuery in yesSet):
                        break
                    else:
                        sys.exit()
                elif isExitChar(restartQuery):
                    sys.exit()
                else:
                    print("\ninvalid input, please try again.")
                    continue
        print("\n\n")
        break
"""

ADDITIONAL DOCUMENTATION
 instances in shadow crypt can vary by having set/immutable pointers to different rooms given certain directions. 
 instances have will have a total of 14 distinct rooms

 Instance #1 has the rooms as follows:

 - Starting Room

 - Green Columns
 - Red Columns
 - Blue Columns
 - Yellow Maze
 - Green Maze
 - Blue Maze
 - Yellow Puzzle
 - Yellow Dais
 - Green Dais
 - Red Dais
 - Red Underwater
 - Blue Underwater

 - Ramp Room

 Instance #2 has the rooms as follows:

 - Starting Room

 - Green Columns 
 - Blue Columns
 - Green Maze
 - Red Maze
 - Blue Maze
 - Yellow Puzzle
 - Green Puzzle
 - Red Puzzle
 - Yellow Dais
 - Blue Dais
 - Yellow Underwater
 - Red Underwater

 - Ramp Room

 Instance #3 has the rooms as follows: (Wiki Diagram indicates 13)

 - Starting Room

 - Yellow Columns 
 - Red Columns 
 - Yellow Maze 
 - Blue Maze 
 - Green Puzzle 
 - Red Puzzle 
 - Blue Puzzle 
 - Green Dais 
 - Red Dais 
 - Yellow Underwater 
 - Green Underwater 
 - Blue Underwater 

 - Green Columns (not intended?)

 - Ramp Room

PROTO instance population -- didnt work because each instance is unique and lacks any computer reproduceable pattern.

# Columns on 1, 6, 11, and 16 ( n % 5 = 1)
# Mazes on 2, 7, 12, and 17 ( n % 5 = 2)
# Puzzles on 3, 8, 13, and 18 ( n % 5 = 3)
# Dais on 4, 9, 14, and 19 ( n % 5 = 4)
# Underwater on 5, 10, 15, and 20 ( n % 5 = 0)
# Yellow Ranges from 1 - 5
# Green Ranges from 6 - 10
# Red Ranges from 11 - 15
# Blue Ranges from 16 - 20

colorList = ["Yellow", "Green", "Red", "Blue"]
structureList = ["Columns", "Maze", "Puzzle", "Dais", "Underwater"]

unpointedGeneralRoomList  = [Room("Colorless", "Start")] # starting room = index 0

for color in colorList:
    for structure in structureList:
        unpointedGeneralRoomList.append(Room(color, structure))
"""