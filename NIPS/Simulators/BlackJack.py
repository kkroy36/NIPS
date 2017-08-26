from random import randint
class Game(object):
    '''class for new blackjack game'''
    
    def __init__(self):
        '''class constructor'''
        self.cards = self.makeCardDeck()
        self.initPSum = self.drawTwo(tot=True)
        self.initDCards = self.drawTwo()
        self.start = (self.initPSum,self.initDCards[0])
        self.actions = ["hit","stand"]
        self.features = ["playerSum","dealerFaceCard"]

    def bust(self,state):
        '''checks if player has bust'''
        pSum = state[0]
        if pSum > 21:
            return True
        return False
    
    def factored(self,state):
        '''returns factored state'''
        return [float(item) for item in list(state)]

    def won(self,state):
        '''checks who won'''
        pSum = state[0]
        dSum = sum([float(item) for item in self.initDCards])
        if pSum >= dSum:
            return True
        else:
            return False

    def takeAction(self,state,action):
        '''performs action and returns state'''
        if state == "winner" or state == "loser":
            return state
        if action not in self.actions:
            return state
        if action == "hit":
            card = self.drawCard()
            pSum = state[0]
            npSum = float(pSum)+float(card)
            if self.bust((npSum,state[1])):
                return "loser"
            if npSum == 21:
                return "winner"
            return (npSum,state[1])
        else:
            if self.won(state):
                return "winner"
            else:
                return "loser"

    def makeCardDeck(self):
        '''makes a deck of cards'''
        cards = []
        cards += [10 for i in range(16)]
        cards += [11 for i in range(4)]
        for i in range(1,10):
            cards += [i for j in range(4)]
        return cards

    def drawCard(self):
        '''draws a random card'''
        N = len(self.cards)
        i = randint(0,N-1)
        card = self.cards[i]
        self.cards.remove(card)
        return card

    def drawTwo(self,tot=False):
        '''draws two cards for player'''
        card1 = self.drawCard()
        card2 = self.drawCard()
        total = float(card1)+float(card2)
        if tot:
            return total
        else:
            return (card1,card2)

    def __repr__(self):
        '''prints this during call to print'''
        rStr = ""
        rStr += "Initial player sum: "+str(self.start[0])
        rStr += "\nDealer face card: "+str(self.start[1])
        rStr += "\nDealer hidden card: "+str(self.initDCards[1])
        rStr += "\nwinner must get to 21 or close\n"
        return rStr
