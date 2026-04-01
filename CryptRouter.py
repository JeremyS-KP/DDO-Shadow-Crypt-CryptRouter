import sys
import sqlite3
import json
import os

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
def plainText(inputStr):
    return inputStr.replace("\033[32m", "").replace("\033[31m", "").replace("\033[33m", "").replace("\033[34m", "").replace("\033[1m", "").replace("\033[0m", "").replace("\033[38;2;255;165;0m", "").replace("\033[4m", "")

start = "Start"
ramp = "Ramp"
greenColumns = green("Green Columns")
greenMaze = green("Green Maze")
greenDais = green("Green Dais")
greenPuzzle = green("Green Puzzle")
greenUnderwater = green("Green Underwater")
redColumns = red("Red Columns")
redMaze = red("Red Maze")
redDais = red("Red Dais")
redPuzzle = red("Red Puzzle")
redUnderwater = red("Red Underwater")
yellowColumns = yellow("Yellow Columns")
yellowMaze = yellow("Yellow Maze")
yellowDais = yellow("Yellow Dais")
yellowPuzzle = yellow("Yellow Puzzle")
yellowUnderwater = yellow("Yellow Underwater")
blueColumns = blue("Blue Columns")
blueMaze = blue("Blue Maze")
blueDais = blue("Blue Dais")
bluePuzzle = blue("Blue Puzzle")
blueUnderwater = blue("Blue Underwater")

if getattr(sys, 'frozen', False):
    baseDir = os.path.dirname(sys.executable)
else:
    baseDir = os.path.dirname(os.path.abspath(__file__))

dbPath = os.path.join(baseDir, "cryptPaths.db")
connectionObj = sqlite3.connect(dbPath)
cursor = connectionObj.cursor()

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
def roomNotInTopologyChar(input):
    return input.strip().lower() == 'x'
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
    
def printResult(jsonLoad, finalRoom):
    dirString = ""
    # create a map for plain strings to their colored (technically, non-string) variants
    stringColorMap = {
        plainText(greenColumns): greenColumns,
        plainText(greenMaze): greenMaze,
        plainText(greenDais): greenDais,
        plainText(greenPuzzle): greenPuzzle,
        plainText(greenUnderwater): greenUnderwater,
        plainText(redColumns): redColumns,
        plainText(redMaze): redMaze,
        plainText(redDais): redDais,
        plainText(redPuzzle): redPuzzle,
        plainText(redUnderwater): redUnderwater,
        plainText(yellowColumns): yellowColumns,
        plainText(yellowMaze): yellowMaze,
        plainText(yellowDais): yellowDais,
        plainText(yellowPuzzle): yellowPuzzle,
        plainText(yellowUnderwater): yellowUnderwater,
        plainText(blueColumns): blueColumns,
        plainText(blueMaze): blueMaze,
        plainText(blueDais): blueDais,
        plainText(bluePuzzle): bluePuzzle,
        plainText(blueUnderwater): blueUnderwater,
        "Start": bold("Start"),
        "Ramp": bold("Ramp")
    }
    # parse the jsonLoad
    for tuple in jsonLoad:
        # by design, for all tuples in a path will be formatted (room, direction)
        room = tuple[0] # meaning the 0th element in the tuple will be the room
        direction = tuple[1] # meaning the 1st element in the tuple will be the direction (=None when it is the beginning room)
        if direction == None: # this means this is the starting room
            print("\nRoom: " + bold(stringColorMap.get(room))) # display to the user where they start
        else:
            dirString += (direction[0]).upper() # record the first letter of the direction and keep it for later
            print("Go " + underline(direction.upper()) + " to " + bold(stringColorMap.get(room)))
            if room != finalRoom:
                print("then")
    print("or more simply: " + bold(dirString)) # print a string with the sequence of directions for the user (standard convention in-game)
        
            
def lookUp(instance, startingRoom, finalRoom):
    # Create a map for instance numbers to names in the db file
    instanceDBMap = {
                1 : "instance1Paths",
                2 : "instance2Paths",
                3 : "instance3Paths"
            }
    # retrieve the path from the db file using a select statement for the table mapping to the instance number
    cursor.execute("""
                    SELECT path
                    FROM """ + instanceDBMap.get(instance) + """
                    WHERE startingRoom = ? and finalRoom = ?
                    """, (startingRoom, finalRoom))
    fromDB = cursor.fetchone()
    result = json.loads(fromDB[0]) # convert from db compatible datum to parsable data for the printResult function
    printResult(result, finalRoom)
    
        


firstIteration = True
foundInstance = False
yesSet = {"y", "yes"}
print("\nWelcome to Crypt-Router! Ver 2.000\n\nThis is a software to help you navigate your way throughout the Shadow Crypt Dungeon in DDO.\n")
while True:
    needInstructions = False
    CurrentInstance = None
    while firstIteration:
        firstTimer = input("Is this your first time using Crypt-Router? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit.\n"+ orange("Enter Here: ")).lower()
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
    while firstIteration:
        startInput = input("\n\nReady to Find your way? type 'yes' or 'y' if so & 'no' or 'n' if not, or press 'enter' to exit.\n"+ orange("Enter Here: ")).lower()
        if(yesNoAssociation(startInput)):         
            if startInput in yesSet:
                break
            else:
                print("Closing Program ... Thank you for using Crypt Router!")
                sys.exit()
        elif isExitChar(startInput):
            sys.exit()
        else:
            print("Invalid Input, please try again.") 
    while True:
        if not foundInstance:
            userKnowInstance = input("\nDo you know which instance you are in? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit\n"+ orange("Enter Response: ")).lower() # primary question for this while loop
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
                        userInstance = input("\nWhich instance are you in? (r/g/b/red/green/blue) or press enter to exit\n"+ orange("Enter Response: ")).lower() # primary questions for this while loop
                        if instanceAssociation(userInstance): # verifies if any of the user's responses correlate to valid instances
                            userInstance = userInstance.strip().lower() # use to make case insensitive
                            # print(userInstance)
                            # print(isinstance(userInstance, str))
                            if userInstance == "r" or  userInstance == "red":
                                if firstIteration:
                                    instance1Rooms = [start, greenColumns, redColumns, blueColumns, yellowMaze, greenMaze, blueMaze, yellowPuzzle, yellowDais, greenDais, redDais, redUnderwater, blueUnderwater, ramp]
                                inInstance1 = True
                                # print("DEBUG: instance 1 initialized.")
                                break # if valid instance, no need to continue while loop
                            elif userInstance == "g" or userInstance ==  "green":
                                if firstIteration:
                                    instance2Rooms = [start, greenColumns, blueColumns, greenMaze, redMaze, blueMaze, yellowPuzzle, greenPuzzle, redPuzzle, yellowDais, blueDais, yellowUnderwater, redUnderwater, ramp]
                                inInstance2 = True
                                # print("DEBUG: instance 2 initialized.")
                                break # if valid instance, no need to continue while loop
                            elif userInstance == "b" or userInstance == "blue":
                                if firstIteration:
                                    instance3Rooms = [start, greenColumns, yellowColumns, redColumns, yellowMaze, blueMaze, greenPuzzle, redPuzzle, bluePuzzle, greenDais, redDais, yellowUnderwater, greenUnderwater, blueUnderwater, ramp]
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
                        userDD = input("\nDo you Have Death's Door charges or Dimension Door Spell? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit\n"+ orange("Enter Response: ")).lower() # allows for alternative to check instance ( returns player to starting room )
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
                                instance1Rooms = [start, greenColumns, redColumns, blueColumns, yellowMaze, greenMaze, blueMaze, yellowPuzzle, yellowDais, greenDais, redDais, redUnderwater, blueUnderwater, ramp]
                                instance2Rooms = [start, greenColumns, blueColumns, greenMaze, redMaze, blueMaze, yellowPuzzle, greenPuzzle, redPuzzle, yellowDais, blueDais, yellowUnderwater, redUnderwater, ramp]
                                instance3Rooms = [start, greenColumns, yellowColumns, redColumns, yellowMaze, blueMaze, greenPuzzle, redPuzzle, bluePuzzle, greenDais, redDais, yellowUnderwater, greenUnderwater, blueUnderwater, ramp]
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
                CurrentInstance = 1
                # populate a list with the valid map-form string identifiers of the room in given instance
                roomsInInstance1 = ["s", "gc", "rc", "bc", "ym", "gm", "bm", "yp", "yd", "gd", "rd", "ru", "bu", "r"]
                stringToNameMap1 = {
                    "s": "Start",
                    "gc": "Green Columns",
                    "rc": "Red Columns",
                    "bc": "Blue Columns",
                    "ym": "Yellow Maze",
                    "gm": "Green Maze",
                    "bm": "Blue Maze",
                    "yp": "Yellow Puzzle",
                    "yd": "Yellow Dais",
                    "gd": "Green Dais",
                    "rd": "Red Dais",
                    "ru": "Red Underwater",
                    "bu": "Blue Underwater",
                    "r": "Ramp"
                }
                
                while True:
                    print("\n\n[Shadow Crypt " + bold(red("Red")) + " Instance]\n")
                    for room in instance1Rooms: # display rooms for user
                        print(room)  
                    while True: # dialogue loop for starting room
                        raw = input("\nWhich of these rooms are you currently in? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\n"+ orange("Enter Room: ")).lower() # collect input
                        normalized = raw.strip().lower().replace(" ", "") # normalize input
                        startingRoomString = roomTerms(normalized) # check to see if valid room term
                        if startingRoomString in stringToNameMap1:
                            startingRoom = stringToNameMap1.get(startingRoomString)
                            break
                        elif isExitChar(raw): # check raw input to see if it is the exit character
                            sys.exit()
                        else:
                            print("invalid room, please try again\n") # inform the user of the error of their ways
                            continue # restart the while loop
                    print("\n\n[Shadow Crypt " + bold(red("Red")) + " Instance]\n")
                    for room in instance1Rooms: # display rooms for user
                        print(room)
                    while True: # dialogue loop for destination room
                        raw = input("\nWhich of these rooms are you trying to reach? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\n"+ orange("Enter Room: ")).lower() # collect input
                        normalized = raw.strip().lower().replace(" ", "") # normalize input
                        destinationRoomString = roomTerms(normalized) # check to see if valid room term
                        if destinationRoomString in stringToNameMap1:
                            destinationRoom = stringToNameMap1.get(destinationRoomString)
                            break
                        elif isExitChar(raw): # check raw input to see if it is the exit character
                            sys.exit()
                        else:
                            print("invalid room, please try again\n") # inform the user of the error of their ways
                            continue # restart the while loop
                    # Path LOOK UP HERE !!!
                    lookUp(CurrentInstance, startingRoom, destinationRoom)
                    # Path LOOK UP HERE !!!
                    while True:
                        again = input("\nNeed to get to another room? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit\n"+ orange("Enter Response: ")).lower()
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
                CurrentInstance = 2
                firstIteration = False
                # populate a list with the valid map-form string identifiers of the room in given instance
                roomsInInstance2 = ["s", "gc", "bc", "gm", "rm", "bm", "yp", "gp", "rp", "yd", "bd", "yu", "ru", "r"]
                stringToNameMap2 = {
                    "s": "Start",
                    "gc": "Green Columns",
                    "bc": "Blue Columns",
                    "gm": "Green Maze",
                    "rm": "Red Maze",
                    "bm": "Blue Maze",
                    "yp": "Yellow Puzzle",
                    "gp": "Green Puzzle",
                    "rp": "Red Puzzle",
                    "yd": "Yellow Dais",
                    "bd": "Blue Dais",
                    "yu": "Yellow Underwater",
                    "ru": "Red Underwater",
                    "r": "Ramp"
                }
                while True:
                    print("\n\n[Shadow Crypt " + bold(green("Green")) + " Instance]\n")
                    for room in instance2Rooms: # display rooms for user
                        print(room)
                    while True: # dialogue loop for starting room
                        raw = input("\nWhich of these rooms are you currently in? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\n"+ orange("Enter Room: ")).lower() # collect input
                        normalized = raw.strip().lower().replace(" ", "") # normalize input
                        startingRoomString = roomTerms(normalized) # check to see if valid room term
                        if startingRoomString in stringToNameMap2:
                            startingRoom = stringToNameMap2.get(startingRoomString)
                            break
                        elif isExitChar(raw): # check raw input to see if it is the exit character
                            sys.exit()
                        else:
                            print("invalid room, please try again\n") # inform the user of the error of their ways
                            continue # restart the while loop
                    print("\n\n[Shadow Crypt " + bold(green("Green")) + " Instance]\n")
                    for room in instance2Rooms: # display rooms for user
                        print(room)
                    while True: # dialogue loop for destination room
                        raw = input("\nWhich of these rooms are you trying to reach? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\n"+ orange("Enter Room: ")) # collect input
                        normalized = raw.strip().lower().replace(" ", "") # normalize input
                        destinationRoomString = roomTerms(normalized) # check to see if valid room term
                        if destinationRoomString in stringToNameMap2: # easy element check from set copy of map-form list
                            destinationRoom = stringToNameMap2.get(destinationRoomString)
                            break # break dialogue loop, no more need to continue this query
                        elif isExitChar(raw): # check raw input to see if it is the exit character
                            sys.exit()
                        else:
                            print("invalid room, please try again\n") # inform the user of the error of their ways
                            continue # restart the while loop
                    #PATH LOOKUP HERE !!!
                    lookUp(CurrentInstance, startingRoom, destinationRoom)
                    #PATH LOOKUP HERE !!!
                    while True:
                        again = input("\nNeed to get to another room? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit\n"+ orange("Enter Response: ")).lower()
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
                CurrentInstance = 3
                firstIteration = False
                # populate a list with the valid map-form string identifiers of the room in given instance
                roomsInInstance3 = ["s", "gc", "yc", "rc", "ym", "bm", "gp", "rp", "bp", "gd", "rd", "yu", "gu", "bu", "r"]
                stringToNameMap3 = {
                    "s": "Start",
                    "gc": "Green Columns",
                    "yc": "Yellow Columns",
                    "rc": "Red Columns",
                    "ym": "Yellow Maze",
                    "bm": "Blue Maze",
                    "gp": "Green Puzzle",
                    "rp": "Red Puzzle",
                    "bp": "Blue Puzzle",
                    "gd": "Green Dais",
                    "rd": "Red Dais",
                    "yu": "Yellow Underwater",
                    "gu": "Green Underwater",
                    "bu": "Blue Underwater",
                    "r": "Ramp"
                }
                while True:
                    print("\n\n[Shadow Crypt " + bold(blue("Blue")) + " Instance]\n")
                    for room in instance3Rooms: # display rooms for user
                        print(room)
                    while True: # dialogue loop for starting room
                        raw = input("\nWhich of these rooms are you currently in? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\n"+ orange("Enter Room: ")) # collect input
                        normalized = raw.strip().lower().replace(" ", "") # normalize input
                        startingRoomString = roomTerms(normalized) # check to see if valid room term
                        if startingRoomString in stringToNameMap3: # easy element check from set copy of map-form list
                            startingRoom = stringToNameMap3.get(startingRoomString) # because room is mapped to string, easy room retrieval
                            break # break dialogue loop, no more need to continue this query
                        elif isExitChar(raw): # check raw input to see if it is the exit character
                            sys.exit()
                        else:
                            print("invalid room, please try again\n") # inform the user of the error of their ways
                            continue # restart the while loop
                    print("\n\n[Shadow Crypt " + bold(blue("Blue")) + " Instance]\n")
                    for room in instance3Rooms: # display rooms for user
                        print(room)
                    while True: # dialogue loop for destination room
                        raw = input("\nWhich of these rooms are you trying to reach? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\n"+ orange("Enter Room: ")) # collect input
                        normalized = raw.strip().lower().replace(" ", "") # normalize input
                        destinationRoomString = roomTerms(normalized) # check to see if valid room term
                        if destinationRoomString in stringToNameMap3: # easy element check from set copy of map-form list
                            destinationRoom = stringToNameMap3.get(destinationRoomString) # because room is mapped to string, easy room retrieval
                            break # break dialogue loop, no more need to continue this query
                        elif isExitChar(raw): # check raw input to see if it is the exit character
                            sys.exit()
                        else:
                            print("invalid room, please try again\n") # inform the user of the error of their ways
                            continue # restart the while loop
                    # PATH LOOKUP HERE !!!
                    lookUp(CurrentInstance, startingRoom, destinationRoom)
                    # PATH LOOKUP HERE !!!
                    while True:
                        again = input("\nNeed to get to another room? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit\n"+ orange("Enter Response: ")).lower()
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
            elif(isUnsure):
                firstIteration = False
                while isUnsure:
                    CurrentInstance = 1
                    print("So let's try instance 1 first!\n")
                    # populate a list with the valid map-form string identifiers of the room in given instance
                    stringToNameMap1 = {
                        "s": "Start",
                        "gc": "Green Columns",
                        "rc": "Red Columns",
                        "bc": "Blue Columns",
                        "ym": "Yellow Maze",
                        "gm": "Green Maze",
                        "bm": "Blue Maze",
                        "yp": "Yellow Puzzle",
                        "yd": "Yellow Dais",
                        "gd": "Green Dais",
                        "rd": "Red Dais",
                        "ru": "Red Underwater",
                        "bu": "Blue Underwater",
                        "r": "Ramp"
                    }
                    print("\n\n[Shadow Crypt " + bold(red("Red")) + " Instance]\n")
                    for room in instance1Rooms: # display rooms for user
                        print(room)
                    while True: # dialogue loop for starting room 
                        roomNotFound = False
                        raw = input("\nWhich of these rooms are you currently in? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\nIf you cannot find your room, type 'x'\n"+ orange("Enter Room: ")) # collect input
                        normalized = raw.strip().lower().replace(" ", "") # normalize input
                        startingRoomString = roomTerms(normalized) # check to see if valid room term
                        if startingRoomString in stringToNameMap1: # easy element check from set copy of map-form list
                            startingRoom = stringToNameMap1.get(startingRoomString) # because room is mapped to string, easy room retrieval
                            break # break dialogue loop, no more need to continue this query
                        elif isExitChar(raw): # check raw input to see if it is the exit character
                            sys.exit()
                        if roomNotInTopologyChar(raw):
                            roomNotFound = True
                            break
                        else:
                            print("invalid room, please try again\n") # inform the user of the error of their ways
                            continue # restart the while loop
                    if not roomNotFound:
                        print("\n\n[Shadow Crypt " + bold(red("Red")) + " Instance]\n")
                        for room in instance1Rooms: # display rooms for user
                            print(room)  
                        while True: # dialogue loop for destination room
                            raw = input("\nWhich of these rooms are you trying to reach? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\nIf you cannot find your room, type 'x'\n"+ orange("Enter Room: ")) # collect input
                            normalized = raw.strip().lower().replace(" ", "") # normalize input
                            destinationRoomString = roomTerms(normalized) # check to see if valid room term
                            if destinationRoomString in stringToNameMap1: # easy element check from set copy of map-form list
                                destinationRoom = stringToNameMap1.get(destinationRoomString) # because room is mapped to string, easy room retrieval
                                break # break dialogue loop, no more need to continue this query
                            elif isExitChar(raw): # check raw input to see if it is the exit character
                                sys.exit()
                            elif roomNotInTopologyChar(raw):
                                roomNotFound = True
                                break
                            else:
                                print("invalid room, please try again\n") # inform the user of the error of their ways
                                continue # restart the while loop
                        if not roomNotFound:
                            # PATH LOOKUP HERE!!!
                            lookUp(CurrentInstance, startingRoom, destinationRoom)
                            # PATH LOOKUP HERE!!!
                            while True:
                                workInput = input("\nDid that work? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit\n"+ orange("Enter Response: ")).lower()
                                if yesNoAssociation(workInput):
                                    if workInput in yesSet:
                                        foundInstance = True
                                        while True:
                                            again = input("\nNeed to get to another room? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit\n"+ orange("Enter Response: ")).lower()
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
                    if foundInstance:   
                        break
                    # out of precaution, set variables in scope to none
                    CurrentInstance = 2
                    print("\nnext, let's try instance 2!")
                    # populate a list with the valid map-form string identifiers of the room in given instance
                    roomsInInstance2 = ["s", "gc", "bc", "gm", "rm", "bm", "yp", "gp", "rp", "yd", "bd", "yu", "ru", "r"]
                    stringToNameMap2 = {
                        "s": "Start",
                        "gc": "Green Columns",
                        "bc": "Blue Columns",
                        "gm": "Green Maze",
                        "rm": "Red Maze",
                        "bm": "Blue Maze",
                        "yp": "Yellow Puzzle",
                        "gp": "Green Puzzle",
                        "rp": "Red Puzzle",
                        "yd": "Yellow Dais",
                        "bd": "Blue Dais",
                        "yu": "Yellow Underwater",
                        "ru": "Red Underwater",
                        "r": "Ramp"
                    }
                    print("\n\n[Shadow Crypt " + bold(green("Green")) + " Instance]\n")
                    for room in instance2Rooms: # display rooms for user
                        print(room)
                    while True: # dialogue loop for starting room
                        roomNotFound = False
                        raw = input("\nWhich of these rooms are you currently in? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\nIf you cannot find your room, type 'x'\n"+ orange("Enter Room: ")) # collect input
                        normalized = raw.strip().lower().replace(" ", "") # normalize input
                        startingRoomString = roomTerms(normalized) # check to see if valid room term
                        if startingRoomString in stringToNameMap2: # easy element check from set copy of map-form list
                            startingRoom = stringToNameMap2.get(startingRoomString) # because room is mapped to string, easy room retrieval
                            break # break dialogue loop, no more need to continue this query
                        elif isExitChar(raw): # check raw input to see if it is the exit character
                            sys.exit()
                        elif roomNotInTopologyChar(raw):
                            roomNotFound = True
                            break
                        else:
                            print("invalid room, please try again\n") # inform the user of the error of their ways
                            continue # restart the while loop
                    if not roomNotFound:
                        print("\n\n[Shadow Crypt " + bold(green("Green")) + " Instance]\n")
                        for room in instance2Rooms: # display rooms for user
                            print(room)
                        while True: # dialogue loop for destination room
                            raw = input("\nWhich of these rooms are you trying to reach? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\nIf you cannot find your room, type 'x'\n"+ orange("Enter Room: ")) # collect input
                            normalized = raw.strip().lower().replace(" ", "") # normalize input
                            destinationRoomString = roomTerms(normalized) # check to see if valid room term
                            if destinationRoomString in stringToNameMap2: # easy element check from set copy of map-form list
                                destinationRoom = stringToNameMap2.get(destinationRoomString) # because room is mapped to string, easy room retrieval
                                break # break dialogue loop, no more need to continue this query
                            elif isExitChar(raw): # check raw input to see if it is the exit character
                                sys.exit()
                            elif roomNotInTopologyChar(raw):
                                roomNotFound = True
                                break
                            else:
                                print("invalid room, please try again\n") # inform the user of the error of their ways
                                continue # restart the while loop
                        if not roomNotFound:
                            # PATH LOOKUP HERE !!!
                            lookUp(CurrentInstance, startingRoom, destinationRoom)
                            # PATH LOOKUP HERE !!!
                            while True:
                                workInput = input("\nDid that work? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit\n"+ orange("Enter Response: ")).lower()
                                if yesNoAssociation(workInput):
                                    if workInput in yesSet:
                                        foundInstance = True
                                        while True:
                                            again = input("\nNeed to get to another room? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit\n"+ orange("Enter Response: ")).lower()
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
                    if foundInstance:
                        break
                    # out of precaution, set variables in scope to non
                    CurrentInstance =  3
                    print("\nThat's Okay! last but not least, let's try instance 3!")
                    # populate a list with the valid map-form string identifiers of the room in given instance
                    roomsInInstance3 = ["s", "gc", "yc", "rc", "ym", "bm", "gp", "rp", "bp", "gd", "rd", "yu", "gu", "bu", "r"]
                    stringToNameMap3 = {
                        "s": "Start",
                        "gc": "Green Columns",
                        "yc": "Yellow Columns",
                        "rc": "Red Columns",
                        "ym": "Yellow Maze",
                        "bm": "Blue Maze",
                        "gp": "Green Puzzle",
                        "rp": "Red Puzzle",
                        "bp": "Blue Puzzle",
                        "gd": "Green Dais",
                        "rd": "Red Dais",
                        "yu": "Yellow Underwater",
                        "gu": "Green Underwater",
                        "bu": "Blue Underwater",
                        "r": "Ramp"
                    }
                    print("\n\n[Shadow Crypt " + bold(blue("Blue")) + " Instance]\n")
                    for room in instance3Rooms: # display rooms for user
                        print(room)
                    while True: # dialogue loop for starting room
                        roomNotFound = False
                        raw = input("\nWhich of these rooms are you currently in? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\nIf you cannot find your room, type 'x'\n"+ orange("Enter Room: ")) # collect input
                        normalized = raw.strip().lower().replace(" ", "") # normalize input
                        startingRoomString = roomTerms(normalized) # check to see if valid room term
                        if startingRoomString in stringToNameMap3: # easy element check from set copy of map-form list
                            startingRoom = stringToNameMap3.get(startingRoomString) # because room is mapped to string, easy room retrieval
                            break # break dialogue loop, no more need to continue this query
                        elif isExitChar(raw): # check raw input to see if it is the exit character
                            sys.exit()
                        elif roomNotInTopologyChar(raw):
                            roomNotFound = True
                            isUnsure = False
                            wasUnsure = True
                            break
                        else:
                            print("invalid room, please try again\n") # inform the user of the error of their ways
                            continue # restart the while loop
                    if not roomNotFound:
                        print("\n\n[Shadow Crypt " + bold(blue("Blue")) + " Instance]\n")
                        for room in instance3Rooms: # display rooms for user
                            print(room)
                        while True: # dialogue loop for destination room
                            raw = input("\nWhich of these rooms are you trying to reach? (or press enter to exit)\nValid inputs: i.e. gc, rc, yellow maze, etc. s/start for starting room, r/ramp for final room <case insensitive>\nIf you cannot find your room, type 'x'\n"+ orange("Enter Room: ")) # collect input
                            normalized = raw.strip().lower().replace(" ", "") # normalize input
                            destinationRoomString = roomTerms(normalized) # check to see if valid room term
                            if destinationRoomString in stringToNameMap3: # easy element check from set copy of map-form list
                                destinationRoom = stringToNameMap3.get(destinationRoomString) # because room is mapped to string, easy room retrieval
                                break # break dialogue loop, no more need to continue this query
                            elif isExitChar(raw): # check raw input to see if it is the exit character
                                sys.exit()
                            elif roomNotInTopologyChar(raw):
                                roomNotFound = True
                                isUnsure = False
                                wasUnsure = True
                                break
                            else:
                                print("invalid room, please try again\n") # inform the user of the error of their ways
                                continue # restart the while loop
                        if not roomNotFound:
                            # PATH LOOKUP HERE !!!
                            lookUp(CurrentInstance, startingRoom, destinationRoom)
                            # PATH LOOKUP HERE !!!
                            while True:
                                workInput = input("\nDid that work? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit\n"+ orange("Enter Response: ")).lower()
                                if yesNoAssociation(workInput):
                                    if workInput in yesSet:
                                        foundInstance = True
                                        while True:
                                            again = input("\nNeed to get to another room? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit\n"+ orange("Enter Response: ")).lower()
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
                restartQuery = input("\nWould you like to restart the program and try again? type 'yes' or 'y' if so & 'no' or 'n' if not, or press enter to exit\n"+ orange("Enter Response: ")).lower()
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
        