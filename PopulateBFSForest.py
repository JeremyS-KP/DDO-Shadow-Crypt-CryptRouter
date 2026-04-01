from collections import deque
import heapq
import itertools
import sys
import json
import sqlite3
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
    pointedRoomListInstance3[12].setEastPointer(pointedRoomListInstance3[14]) # east points to Green Columns room
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
# Begin Code for Populating BFS Tree
initializeInstance3()
initializeInstance2()
initializeInstance1()
instanceList = [instance1, instance2, instance3]
connectionObj = sqlite3.connect("cryptPaths.db") # creates/opens SQLite database file 
cursor = connectionObj.cursor() # this is how we will execute SQL statements in python
tableNames = ["instance1Paths", "instance2Paths", "instance3Paths"]
# this code initializes each table for each instance, sending the query to the cryptPaths.db file
# for each table, there will only ever be one 'optimized' path for each possible path => we can make the primary key the multivalue attribute of the starting room and final room
cursor.execute("""
        CREATE TABLE IF NOT EXISTS instance1Paths (
               startingRoom TEXT,
               finalRoom TEXT,
               path TEXT,
               PRIMARY KEY (startingRoom, finalRoom)
               )
               """)
cursor.execute("""
        CREATE TABLE IF NOT EXISTS instance2Paths (
               startingRoom TEXT,
               finalRoom TEXT,
               path TEXT,
               PRIMARY KEY (startingRoom, finalRoom)
               )
               """)
cursor.execute("""
        CREATE TABLE IF NOT EXISTS instance3Paths (
               startingRoom TEXT,
               finalRoom TEXT,
               path TEXT,
               PRIMARY KEY (startingRoom, finalRoom)

               )
               """)
connectionObj.commit()
for i, instance in enumerate(instanceList): # GOAL: Find every path to every room from current room
    # print(instance) debug print: ensures loop is retrieving correct instance data
    for startingRoom in instance.getRoomsInInstance():
        for finalRoom in instance.getRoomsInInstance():
            tempPath = prioBFS(instance, startingRoom, finalRoom)
            roomSequence = [(str(room), direction) for room, direction in tempPath]
            cursor.execute("""
                INSERT INTO """ + tableNames[i] + """(startingRoom, finalRoom, path) VALUES (?, ?, ?)""", (str(startingRoom), str(finalRoom), json.dumps(roomSequence))
            )
            # print(roomSequence) debug print: ensures loop is retrieving correct roomSequence data
        # print(room) debug print: ensures loop is retrieving correct room data
    # print("\n") debug print: adds newline so that debug output is more readable
connectionObj.commit()
