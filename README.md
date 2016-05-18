Simulation of the card game Golf - description here: http://www.bicyclecards.com/how-to-play/six-card-golf/

A friend challenged me to build a bot that could beat him. The bot, which is written from the AI class in golf.py, had several variables
that controlled different priorities, actions in a decision tree, and behaviors. golfBattle.py plays a collection of bots against each
other, then outputs the raw data into a text file in a format readable by R, for later statistical analysis. In this way I was able to
optimize the behavior of the bot.

Conclusions:
1. Golf is mostly luck (Even the best bots only have a win rate of ~28% in a game of 4)
2. Information has very little value - one should take only cards that improve your score, regardless of info
3. Flipping is rarely a good idea. Better to draw.
