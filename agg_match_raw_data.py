from enum import Enum

class Player(Enum):
	playerA = "A"
	playerB = "B"

KEYWORD_SERVE = "SERVE"
KEYWORD_FAULT = "FAULT"
KEYWORD_ARROW = "->"


'''
serve table is a buffer to aggregate serve data. It has this format:
+-------+-------+-------+-------+-------+-------+
|		| Fault	| B1	| B2	| B3	| B4	|
+-------+-------+-------+-------+-------+-------+
| A1  	|(count)|(count)|(count)|(count)|(count)|
+-------+-------+-------+-------+-------+-------+
| A2 	|(count)|(count)|(count)|(count)|(count)|
+-------+-------+-------+-------+-------+-------+

shot table is a buffer to aggregate shot data. Take shot_a as example,
it has this format. e.g. the first row records count of moves from A1 to
all possible zones in player B's side:
+-------+-------+-------+-------+-------+-------+
|		| Fault	| B1	| B2	| B3	| B4	|
+-------+-------+-------+-------+-------+-------+
| A1	|(count)|(count)|(count)|(count)|(count)|
+-------+-------+-------+-------+-------+-------+
| A2	|(count)|(count)|(count)|(count)|(count)|
+-------+-------+-------+-------+-------+-------+
| A3	|(count)|(count)|(count)|(count)|(count)|
+-------+-------+-------+-------+-------+-------+
| A4	|(count)|(count)|(count)|(count)|(count)|
+-------+-------+-------+-------+-------+-------+
all counts are initialized as zero.
'''
serve_a = [ [0] * 5 for _ in range(2)]
serve_b = [ [0] * 5 for _ in range(2)]
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
	line = line.replace(" ", "") # remove all spaces
	splitted = line.split(",", 3)
	if (splitted[0] == KEYWORD_SERVE):
		recordInServeTable(splitted[1])
	elif (KEYWORD_ARROW in splitted[0]):
		recordInShotTable(splitted[0])

def recordInServeTable(from_to_str):
	from_player, from_zone, to_zone = parseFromToStr(from_to_str)
	print ("recording serve table, %s player from %d to %d" % (from_player, from_zone, to_zone))
	if (from_player == Player.playerA):
		serve_a[from_zone][to_zone] += 1
	else:
		serve_b[from_zone][to_zone] += 1

def recordInShotTable(from_to_str):
	from_player, from_zone, to_zone = parseFromToStr(from_to_str)
	print ("recording shot table, %s player from %d to %d" % (from_player, from_zone, to_zone))
	if (from_player == Player.playerA):
		shot_a[from_zone][to_zone] += 1
	else:
		shot_b[from_zone][to_zone] += 1

def parseFromToStr(from_to_str):
	from_to_str_arr = from_to_str.split(KEYWORD_ARROW, 2)
	from_player = Player(from_to_str_arr[0][:1])
	from_zone = int(from_to_str_arr[0][1:]) - 1
	to_zone = 0 if (from_to_str_arr[1] == KEYWORD_FAULT) else int(from_to_str_arr[1][1:])
	return from_player, from_zone, to_zone

def printServeTable(player, table):
	from_player = player
	to_player = Player.playerA if (player == Player.playerB) else Player.playerB

	print("- Serve table for %s" % from_player)
	print("FROM_ZONE,FAULT,%s1,%s2,%s3,%s4" % (
		to_player.value, to_player.value, to_player.value, to_player.value))
	for index in range(0, len(table)):
		printTableRow(table[index], index, from_player, to_player)

def printShotTable(player, table):
	from_player = player
	to_player = Player.playerA if (player == Player.playerB) else Player.playerB

	print("- Shot table for %s" % from_player)
	print("FROM_ZONE,FAULT,%s1,%s2,%s3,%s4" % (
		to_player.value, to_player.value, to_player.value, to_player.value))
	for index in range(0, len(table)):
		printTableRow(table[index], index, from_player, to_player)

def printTableRow(row, rowIndex, from_player, to_player):
	from_zone = from_player.value + str(rowIndex + 1)
	print("%s,%d,%d,%d,%d" % (from_zone,
		row[0],row[1],row[2],row[3]))

if __name__ == "__main__":
	main()