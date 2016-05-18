import random
import pdb

class Card:
	def __init__(self, suit, num):
		self.suit = suit
		self.num = num
	
	def __str__(self):
		if self.num == 1:
			rep = "Ace"
		elif self.num == 11:
			rep = "Jack"
		elif self.num == 12:
			rep = "Queen"
		elif self.num == 13:
			rep = "King"
		else:
			rep = str(self.num)
			
		return rep + " of " + self.suit
		
	#Returns golf value of card
	def getValue(self):
		if self.num == 1:
			return -4
		if self.num == 13:
			return 0
		if self.num >= 10:
			return 10
		else:
			return self.num

class Deck:
	def __init__(self):
		self.deck = []
	
		for n in range(4):
			for num in range(14)[1:]:
				if n == 0:
					suit = "clubs"
				elif n == 1:
					suit = "diamonds"
				elif n==2:
					suit = "hearts"
				elif n==3:
					suit = "spades"
				self.deck.append(Card(suit, num))
		self.unrevealed = self.deck[:]
	
	def __str__(self):
		final = "Cards: " + str(len(self.deck)) + "\n"
		for c in self.deck:
			final += str(c) + "\n"
		return final
		
	#Returns mean of all unrevealed cards
	def getMean(self):
		sum = 0
		for card in self.unrevealed:
			sum += card.getValue()
		if len(self.deck) == 0:
			return 0
		return float(sum)/float(len(self.unrevealed))
		
	#Draws a card, reveals it, and removes it from deck
	def draw(self):
		card = self.deck.pop()
		self.unrevealed.remove(card)
		return card
	
	def shuffle(self):
		random.shuffle(self.deck)
		
	def getCards(self):
		return self.deck[:]
		
class Player:
	def __init__(self, name, deck, info_value=5, draw=True, end=5, pair=2, info_mod=.5):
		self.actual = []
		self.revealed = []
		self.name = name
		self.brain = AI(info_value, draw, end, pair, info_mod)
		for i in range(6):
			card = deck.draw()
			self.actual.append(card)
			if i == 0 or i == 1:
				self.revealed.append(card)
			else:
				self.revealed.append("-")
				deck.unrevealed.append(card)
				
	def __str__(self):
		final = self.name
		for i in range(3):
			final += "\n"
			final += "\n"
			if self.revealed[i*2] == "-":
				final += "     -------     "
			else:
				final += str(self.revealed[i*2]) + " "*(17-len(str(self.revealed[i*2])))
			final += " | "
			if self.revealed[i*2+1] == "-":
				final += "     -------     "
			else:
				final += str(self.revealed[i*2+1]) + " "*(17-len(str(self.revealed[i*2+1])))
		return final + "\n"
	
	#Returns list of laid out cards with unrevealed masked
	def getRevealed(self):
		return self.revealed
		
	#Gets score of a row, the actual score
	def getRowScore(self, row):
		c1 = self.actual[2*row]
		c2 = self.actual[2*row + 1]
		
		if c1.num == c2.num and c1.num != 1:
			return 0
		return c1.getValue() + c2.getValue()
		
	#Gets the actual score of a player
	def getScore(self):
		score = 0
		for i in range(3):
			score += self.getRowScore(i)
		return score
		
	#Estimates the score of a player by filling in mean for masked cards
	def estimateScore(self, mean):
		count = 0
		for card in self.revealed:
			if card == "-":
				count += mean
			else:
				count += card.getValue()
		return count
		
	#Returns number of revealed cards
	def numRevealed(self):
		return 6-self.revealed.count("-")
		
	#Reveals a card
	def reveal(self, i, deck):
		self.revealed[i] = self.actual[i]
		deck.unrevealed.remove(self.actual[i])
		
	#Sets the given card to the specified spot in player
	def set(self, card, i, game):
		if self.actual[i] in game.deck.unrevealed:
			game.deck.unrevealed.remove(self.actual[i])
		temp = self.actual[i]
		self.revealed[i] = card
		self.actual[i] = card
		game.discard = temp
		
	#Uses brain to make a move
	def makeMove(self, game):
		self.brain.makeMove(game, self)
	
class Game:
	def __init__(self, player_infos):
		self.deck = Deck()
		self.deck.shuffle()
		
		self.players = []
		for p in player_infos:
			self.players.append(Player(p[0], self.deck, p[1], p[2], p[3], p[4], p[5]))
			
		random.shuffle(self.players)
		
		self.discard = self.deck.draw()
		
		top = -10
		for i in range(len(self.players)):
			if self.players[i].getRowScore(0) > top:
				top = self.players[i].getRowScore(0)
				first = i
		self.turn = first
		
	def __str__(self):
		final = "Discard: " + str(self.discard) + "\n"
		for p in self.players:
			final += str(p)
		return final + "\n"
		
	#Plays a game, prints if debug is true
	def play(self, debug=False):
		stopOn = -1
		moves = 0
		while stopOn != self.turn and len(self.deck.getCards()) > 0:
			if moves > 1000:
				print("Stopping loop")
				moves = 0
				self.discard = self.deck.draw()
			if debug:
				print(str(self))
				input()
				print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
			self.players[self.turn].makeMove(self)
			if not ("-" in self.players[self.turn].revealed) and stopOn == -1:
				stopOn = self.turn
			self.turn += 1
			if self.turn >= len(self.players):
				self.turn = 0
			moves += 1
	
	#estimates the number of turns remaining in the game
	def turnsLeft(self):
		num = 0
		pos = -1
		for i in range(len(game.players)):
			p = game.player[i]
			if p.numRevealed() > num:
				num = p.numRevealed()
				pos = i
			
	#Finds and returns info of winner after game has ended
	def postGame(self):
		min = 10000
		final = "Scores:\n"
		for p in self.players:
			final += p.name + ": " + str(p.getScore()) + "\n"
			if p.getScore() < min:
				pMin = p
				min = p.getScore()
		final += "WINNER: " + pMin.name + "\n"
		return final
		
	#yea
	def findWinner(self):
		min = 10000
		minPos = -1
		for i in range(len(self.players)):
			p = self.players[i]
			if p.getScore() < min:
				min = p.getScore()
				minPos = i
		return [minPos, min]

class AI:
	def __init__(self, info_value, draw, end, pair, mod):
		self.info_value = info_value
		self.draw = draw
		self.end = end
		self.pair = pair
		self.mod = mod
		
	#Determines if they would like to end the game based on their wanting to end
	def wantToEnd(self, game, player):
		mean = game.deck.getMean()
		own = player.estimateScore(mean)
		min = 100
		for player in game.players:
			if player.estimateScore(mean) < min:
				min = player.estimateScore(mean)
		return own+self.end <= min
		
	#Given a card and a player, pairs off the given card if able
	def pairOff(self, test, game, player):
		for i in range(len(player.revealed)):
			card = player.revealed[i]
			if card != "-" and card.num == test.num and card.getValue() > 0:
				if i%2 == 0:
					offset = i+1
				else:
					offset = i-1
				other = player.revealed[offset]
				if other == "-":
					player.set(test, offset, game)
					return True
				elif other.getValue() + card.getValue() > 0:
					player.set(test, offset, game)
					return True
				else:
					pass
		return False
		
	#If the card given is lower than mean, takes it and plays it
	def lower(self, test, game, player, info_offset):
		if test.getValue() < game.deck.getMean()+info_offset:
			if player.numRevealed() < 5:
				for i in range(len(player.revealed)):
					card = player.revealed[i]
					if card == "-":
						player.set(test, i, game)
						return True
			elif self.wantToEnd(game, player):
				for i in range(len(player.revealed)):
					card = player.revealed[i]
					if card == "-":
						player.set(test, i, game)
						return True
			else:
				max = -5
				maxPos = -1
				for i in range(len(player.revealed)):
					card = player.revealed[i]
					if i % 2 == 0:
						offset = i + 1
					else: 
						offset = i-1
					other = player.revealed[offset]
					if card != "-" and (other == "-" or card.num != other.num):
						if card.getValue() > max:
							max = card.getValue()
							maxPos = i
					if max > test.getValue():
						player.set(test, maxPos, game)
						return True
					else:
						return False
		else:
			return False
			
	#Tries to pair a small card with another small, even if no pair
	def smaller(self, test, game, player):
		if test.getValue() <= player.brain.pair:
			for i in range(len(player.revealed)):
				card = player.revealed[i]
				if card != "-" and card.getValue() <= player.brain.pair:
					if i%2 == 0:
						offset = i+1
					else:
						offset = i-1
					other = player.revealed[offset]
					if other == "-" or other.getValue() > player.brain.pair:
						player.set(test, offset, game)
						return True
		return False
	
	#Structure for drawing a card from deck
	def takeCard(self, game, player):
		card = game.deck.draw()
		if self.pairOff(card, game, player):
			return True
		if self.smaller(card, game, player):
			return True
		if self.lower(card, game, player, player.brain.info_value):
			return True
		game.discard = card
		return False
		
	#Make the move
	def makeMove(self, game, player):
		#self.info_value -= self.mod
		#if self.info_value < 0:
		#	self.info_value = 0
		
		if self.pairOff(game.discard, game, player):
			return 1
		
		if self.smaller(game.discard, game, player):
			return 1
		
		if self.lower(game.discard, game, player, 0):
			return 1
					
		take = self.draw or (player.numRevealed == 5 and not wantToEnd(game, player))
		if take:
			if self.takeCard(game, player):
				return 2
			else:
				return 0
		else:
			for i in range(len(player.revealed)):
				card = player.revealed[i]
				if card == "-":
					player.reveal(i, game.deck)
					return 3