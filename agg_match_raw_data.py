from enum import Enum

class Player(Enum):
	playerA = "A"
	playerB = "B"

class Action(Enum):
	FAULT = 0
	Diagonal_Near = 1
	Adjacent_Near = 2
	Diagonal_Far = 3
	Adjacent_Far = 4

KEYWORD_SERVE = "SERVE"
KEYWORD_GAME_START = "GAME_START"
KEYWORD_FAULT = "FAULT"
KEYWORD_ARROW = "->"

start_parsing = False
last_action = Action.Diagonal_Near

'''
serve table is a buffer to aggregate serve data. It has this format:
+-------+-------+---------------+---------------+
|		| Fault	| Diagonal_Near	| Diagonal_Far	|
+-------+-------+---------------+---------------+
| Left  |(count)|	(count)		|	(count)		|
+-------+-------+---------------+---------------+
| Right |(count)|	(count)		|	(count)		|
+-------+-------+---------------+---------------+

shot table is a buffer to aggregate shot data. It has this format:
+-----------------------+-------+---------------+---------------+---------------+---------------+
|						| Fault	| Diagonal_Near	| Adjacent_Near	| Diagonal_Far	| Adjacent_Far	|
+-----------------------+-------+---------------+---------------+---------------+---------------+
| Counter_Diagonal_Near	|(count)|	(count)		|	(count)		|	(count)		|	(count)		|
+-----------------------+-------+---------------+---------------+---------------+---------------+
| Counter_Adjacent_Near	|(count)|	(count)		|	(count)		|	(count)		|	(count)		|
+-----------------------+-------+---------------+---------------+---------------+---------------+
| Counter_Diagonal_Far	|(count)|	(count)		|	(count)		|	(count)		|	(count)		|
+-----------------------+-------+---------------+---------------+---------------+---------------+
| Counter_Adjacent_Far	|(count)|	(count)		|	(count)		|	(count)		|	(count)		|
+-----------------------+-------+---------------+---------------+---------------+---------------+
all counts are initialized as zero.
'''
serve_a = [ [0] * 3 for _ in range(2)]
serve_b = [ [0] * 3 for _ in range(2)]
shot_a = [ [0] * 5 for _ in range(4)]
shot_b = [ [0] * 5 for _ in range(4)]

def main():
	with open("badminton_match.txt", "r") as game_data:
		for line in game_data:
			recordLine(line.strip())
	print("------------------------result------------------------")
	printServeTable(Player.playerA, serve_a)
	printServeTable(Player.playerB, serve_b)
	printShotTable(Player.playerA, shot_a)
	printShotTable(Player.playerB, shot_b)


def recordLine(line):
	global start_parsing
	line = line.replace(" ", "") # remove all spaces
	if (not start_parsing):
		if (line == KEYWORD_GAME_START):
			start_parsing = True
			return
	splitted = line.split(",", 3)
	if (splitted[0] == KEYWORD_SERVE):
		recordInServeTable(splitted[1])
	elif (KEYWORD_ARROW in splitted[0]):
		recordInShotTable(splitted[0])

def recordInServeTable(from_to_str):
	global last_action
	from_player, from_zone, to_zone = parseFromToStr(from_to_str)
	print ("recording serve table, %s player from %d to %d" % (from_player, from_zone, to_zone))
	
	table = serve_a if (from_player == Player.playerA) else serve_b
	row_in_table = from_zone - 1
	column_in_table = 0

	if (isFault(to_zone)):
		last_action = Action.FAULT
		column_in_table = 0
	if (isNear(to_zone)):
		last_action = Action.Diagonal_Near
		column_in_table = 1
	else:
		last_action = Action.Diagonal_Far
		column_in_table = 2

	table[row_in_table][column_in_table] += 1

def recordInShotTable(from_to_str):
	global last_action
	from_player, from_zone, to_zone = parseFromToStr(from_to_str)
	print ("recording shot table, %s player from %d to %d" % (from_player, from_zone, to_zone))
	
	table = shot_a if (from_player == Player.playerA) else shot_b
	row_in_table = last_action.value - 1
	column_in_table = 0

	if (isFault(to_zone)):
		last_action = Action.FAULT
		column_in_table = Action.FAULT.value
	elif (isDiagonal(from_zone, to_zone) and isNear(to_zone)):
		last_action = Action.Diagonal_Near
		column_in_table = Action.Diagonal_Near.value
	elif (not isDiagonal(from_zone, to_zone) and isNear(to_zone)):
		last_action = Action.Adjacent_Near
		column_in_table = Action.Adjacent_Near.value
	elif (isDiagonal(from_zone, to_zone) and not isNear(to_zone)):
		last_action = Action.Diagonal_Far
		column_in_table = Action.Diagonal_Far.value
	elif (not isDiagonal(from_zone, to_zone) and not isNear(to_zone)):
		last_action = Action.Adjacent_Far
		column_in_table = Action.Adjacent_Far.value

	table[row_in_table][column_in_table] += 1

def isDiagonal(from_zone, to_zone):
	return (from_zone - to_zone) % 2 == 0

def isNear(to_zone):
	return to_zone == 1 or to_zone == 2

def isFault(to_zone):
	return to_zone == 0

def parseFromToStr(from_to_str):
	from_to_str_arr = from_to_str.split(KEYWORD_ARROW, 2)
	from_player = Player(from_to_str_arr[0][:1])
	from_zone = int(from_to_str_arr[0][1:])
	to_zone = 0 if (from_to_str_arr[1] == KEYWORD_FAULT) else int(from_to_str_arr[1][1:])
	return from_player, from_zone, to_zone

def printServeTable(player, table):
	from_player = player
	to_player = Player.playerA if (player == Player.playerB) else Player.playerB

	print("- Serve table for %s" % from_player)
	print("FROM_ZONE,FAULT,Diagonal_Near,Diagonal_Far")
	print("Left,%d,%d,%d" % (table[0][0], table[0][1], table[0][2]))
	print("Right,%d,%d,%d" % (table[1][0], table[1][1], table[1][2]))

def printShotTable(player, table):
	from_player = player
	to_player = Player.playerA if (player == Player.playerB) else Player.playerB

	print("- Shot table for %s" % from_player)
	print("Counter,FAULT,Diagonal_Near,Adjacent_Near,Diagonal_Far,Adjacent_Far")
	for index in range(0, len(table)):
		printTableRow(table[index], index, from_player, to_player)

def printTableRow(row, rowIndex, from_player, to_player):
	counter = Action(rowIndex+1).name
	print("%s,%d,%d,%d,%d,%d" % (counter,row[0],row[1],row[2],row[3],row[4]))

if __name__ == "__main__":
	main()