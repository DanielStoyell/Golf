from golf import *
import itertools
import time
import math

botList = [["0", -2, True, -2, 1, 0]]
wins = [0]
games = [0]
sum_scores = [0]
i = 1
for filler in range(1):
	for v in [-2, -1 ,0, 1, 2]:
		for e in [-1, 0, 1, 2]:
			for p in [0, 1, 2]:
				for o in [0]:
					botList.append([str(i), v, True, 4*e, p, o])
					wins.append(0)
					games.append(0)
					sum_scores.append(0)
					i += 1

ran = 0
old = 0
start = time.clock()
for match in itertools.combinations(botList, 4):
	game = Game(match)
	game.play(False)
	winner = game.findWinner()
	pos = int(match[winner[0]][0])
	wins[pos] += 1
	for i in range(len(game.players)):
		pos = int(match[i][0])
		games[pos] += 1
		sum_scores[pos] += game.players[i].getScore()
	ran += 1
	if ran % 10000 == 0:
		gamesPerSec = float(ran - old)/(time.clock() - start)
		old = ran
		start = time.clock()
		percent = ((float(ran)/float(521855))*100.0)
		print("Progress: " + str(percent)[:4] + "% | Games: " + str(ran) + " | Games/second: " + str(gamesPerSec)[:5])
	
avgs = []
for i in range(len(games)):
	avgs.append(float(sum_scores[i]/games[i]))
	wins[i] = (float(wins[i])/float(games[i]))*100

ranked = [x for (y,x) in sorted(zip(wins,botList))]
winners = [y for (y,x) in sorted(zip(wins,botList))]
avgs = [x for (y,x) in sorted(zip(wins, avgs))]
output = "ID WinPercent avg_score info_value info_mod draw end pair\n"
for i in range(len(winners)):
	if ranked[i][2]:
		draw = 1
	else:
		draw = 0
	output += str(ranked[i][0]) + " " + str(winners[i])[:4] + " " + str(avgs[i])[:4] + " " + str(ranked[i][1]) + " " + str(ranked[i][5]) + " " + str(draw) + " " + str(ranked[i][3]) + " " + str(ranked[i][4]) + "\n"
	
f = open('results.txt', 'w')
f.write(output)
f.close()

print("\nData upload complete, ready for analysis")