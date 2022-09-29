#Written by: Zarrukh Bazarov, Jackson Kelsch, and Emily Walden 
#CSCE 480- Intro to AI - Homework 2: Cheating Casino
#Program Purpose: Uses AI methods to cheat in 3-card poker to generate positive revenue over time
#Program Assumptions: 
#   1)Player will play more than 4 rounds, which allows the AI to observe game 
#     stats and then start cheating.
#   2)Different “users” would play over the long run to add to the profit & stats over time.
#   3)Computer has unlimited wallet of funds. 
#   4)Profit is calculated only using gains from the user, not including money 
#     the cpu bet and gained back. 
#   5)Aces are used as low aces.

# https://pypi.org/project/deck-of-cards/
# ^ deck of cards import docs
#install using:    pip install deck-of-cards
from deck_of_cards import deck_of_cards
import random
from random import sample
import copy
#card.suit   0=spades, 1=hearts, 2=diamonds, 3=clubs
#card.rank   1=Ace, 11=Jack, 12=Queen, 13=King - 2-10 are just numerical cards

#sorts passed in hand in ascending rank
def sortRank(hand):
    hand.sort(key=lambda c: c.rank)
    return hand

#randomizes locations of cards in a hand - used to not hint at 3rd card when printing hidden
def randHandIndices(hand):
    c1 = hand[0]
    c2 = hand[1]
    c3 = hand[2]
    indices = [0, 1, 2]
    randIndices = sample(indices, 3) #sample() takes x(3) distinct random values from an array
    hand[randIndices[0]] = c1
    hand[randIndices[1]] = c2
    hand[randIndices[2]] = c3
    return hand

#takes a hand and prints 2 of the 3 cards with symbol format
def printHandHidden(hand):
    #symbols = '♠', '♥', '♦', '♣'
    count = 0
    for x in hand:
        if count == 2:
            print('\t[ hidden ]')
            return
        if x.suit == 0:
            x.suit = '♠'
        if x.suit == 1:
            x.suit = '♥'   
        if x.suit == 2:
            x.suit = '♦'
        if x.suit == 3:
            x.suit = '♣'
        if x.rank == 1:
            print('\t[', 'Ace',  x.suit, ']')
            count+=1
            continue
        if x.rank == 11:
            print('\t[', 'Jack',  x.suit, ']')
            count+=1
            continue
        if x.rank == 12:
            print('\t[', 'Queen',  x.suit, ']')
            count+=1
            continue
        if x.rank == 13:
            print('\t[', 'King',  x.suit, ']')
            count+=1
            continue
        print('\t[', x.rank,  x.suit, ']')
        count+=1

#takes a hand and prints all cards with symbol format
def printHand(hand):
    #symbols = '♠', '♥', '♦', '♣'
    for x in hand:
        if x.suit == 0:
            x.suit = '♠'
        if x.suit == 1:
            x.suit = '♥'   
        if x.suit == 2:
            x.suit = '♦'
        if x.suit == 3:
            x.suit = '♣'
        if x.rank == 1:
            print('\t[', 'Ace',  x.suit, ']')
            continue
        if x.rank == 11:
            print('\t[', 'Jack',  x.suit, ']')
            continue
        if x.rank == 12:
            print('\t[', 'Queen',  x.suit, ']')
            continue
        if x.rank == 13:
            print('\t[', 'King',  x.suit, ']')
            continue
        print('\t[', x.rank,  x.suit, ']')

#takes a hand and evaluates the value (weak or strong)
def evaluate(hand):
    c1 = hand[0]
    c2 = hand[1]
    c3 = hand[2]
    evaluation = 0
    if c1.rank == c2.rank or c1.rank == c3.rank or c2.rank == c3.rank: #checking for pair
        evaluation = 1
    if c1.suit == c2.suit and c2.suit == c3.suit: #checking for flush
        evaluation = 2
    if c1.rank == (c2.rank-1) and c2.rank == (c3.rank-1): #checking for straight
        evaluation = 3
    if c1.rank == c2.rank and c2.rank == c3.rank: #checking for triple
        evaluation = 4
    if c1.rank == (c2.rank-1) and c2.rank == (c3.rank-1) and c1.suit == c2.suit and c2.suit == c3.suit: #checking for straight flush
        evaluation = 5
    return evaluation

#takes hands and the bet to determine who won
def compareHands(uEval, cEval, bet, uHand, cHand ): 
    result = ''
    if uEval > cEval:
        print("\n\tUser wins!", "\n\tYou won: $", bet, '\n')
        result = 'l'
    if cEval > uEval:
        print("\n\tCPU wins\n")
        result = 'w'
    if cEval == uEval:            #check for high card
        #print('The match is a draw')
        if uHand[2] > cHand[2]:
            print("\n\tUser wins from highest card", "\n\tYou won: $", bet, '\n')
            result = 'l'
        if uHand[2] < cHand[2]:
            print("\n\tCPU wins from highest card\n")
            result = 'w'
        if uHand[2] == cHand[2]:
            print('\n\tThe match is a draw\n')
            result = 'd'
    return result 
            
        
#returns relevant hand for better visualization at endgame
def handAnalyze(eval, player, hand):
    if eval == 1:
        print(player , "has a -pair-")
    if eval == 2:
        print(player , "has a -flush-")
    if eval == 3:
        print(player , "has a -straight-")
    if eval == 4:
        print(player , "has a -triple-")
    if eval == 5:
        print(player , "has a -straight flush-")
    if eval == 0:
        if hand[2].rank == 1:
            print(player ,"'s high card is: " , "Ace(1)")
        elif hand[2].rank == 11:
            print(player ,"'s high card is: " , "Jack(11)")
        elif hand[2].rank == 12:
            print(player ,"'s high card is: " , "Queen(12)")
        elif hand[2].rank == 13:
            print(player ,"'s high card is: " , "King(13)")
        else:
            print(player ,"'s high card is: " , hand[2].rank)
            
'''the three functions below (checkRatio, checkProfit, checkHistory) will be used to determine if the cpu should cheat this round'''
#checks win ratio, makes sure that win ratio does not drop below 60%
def checkWinRatio(history):
    cheat = False 
    if len(history) >=4:
        winRatio = history.count('w') / len(history)
        if  winRatio < .60:
            cheat = True
    return cheat
    
#checks profit, makes sure it does not go negative
def checkProfit(profit, history):
    cheat = False 
    if len(history)>=4 and profit<0:
        cheat = True
    return cheat
    
#checks history of games, makes sure cpu is not winning over and over
def checkHistory(history):
    cheat = False
    if len(history)>=4:
        if not(history[len(history)-1]=='w' and history[len(history)-2]=='w' and history[len(history)-3]=='w'):
            cheat = True
    return cheat

#cheat function will use a evalNeeded that is greater than opponent's eval score
#evalNeeded should be a randomly selected number greater than opponents evaluation and less than or equal to 5 (highest evaluation)
def cheat(hand, evalNeeded):
    c1 = hand[0]
    c2 = hand[1]
    c3 = hand[2]
    if evalNeeded == 1: #creates pair
        if (c1.suit != c2.suit):
            c2.rank = int(c1.rank)
        elif (c2.suit != c3.suit):
            c3.rank = int(c2.rank)
        elif (c1.suit != c3.suit):
            c3.rank = int(c1.rank)
    if evalNeeded == 2: #creates flush using C1's suit
        '''cannot have a pair here'''
        if c1.rank == c2.rank or c1.rank == c3.rank or c2.rank == c3.rank:
            evalNeeded = random.randint(3,5)
        else:
            c2.suit = c1.suit
            c3.suit = c1.suit
    if evalNeeded == 3: #creates a straight
        '''cannot be the same suit aka old evaluation number can not be 2''' 
        if c1.suit == c2.suit and c2.suit == c3.suit:
            evalNeeded = 5
        else:
            if c1.rank <12:
                c2.rank = copy.deepcopy(int(c1.rank))+1
                c3.rank = copy.deepcopy(int(c2.rank))+1
            else:
                c2.rank = copy.deepcopy(int(c3.rank))-1
                c1.rank = copy.deepcopy(int(c2.rank))-1
    if evalNeeded == 4: #creates a triple based off of C1's rank
        '''cant have 2 of the same suit here'''
        if (c1.suit == c2.suit)or(c2.suit == c3.suit):
            evalNeeded=5
        else:
            c2.rank = int(c1.rank)  
            c3.rank = int(c1.rank)
    if evalNeeded == 5: #creates a straight flush
        c2.suit = c1.suit
        c3.suit = c1.suit
        if c1.rank <12:
            c2.rank = copy.deepcopy(int(c1.rank))+1
            c3.rank = copy.deepcopy(int(c2.rank))+1
        else:
            c2.rank = copy.deepcopy(int(c3.rank))-1
            c1.rank = copy.deepcopy(int(c2.rank))-1
    if evalNeeded == 6: #creates a straight flush using highest card if possible 
        c2.suit = c1.suit
        c3.suit = c1.suit
        if c3.rank >2:
            c2.rank = copy.deepcopy(int(c3.rank))-1
            c1.rank = copy.deepcopy(int(c2.rank))-1
        else:
            c2.rank = copy.deepcopy(int(c1.rank))+1
            c3.rank = copy.deepcopy(int(c2.rank))+1
    return hand
              

#create new card deck
cardDeck = deck_of_cards.DeckOfCards()
playing = True


#initialize profit & win/loss/total game, & history variables for stat tracking
profit = 0
totalGames = 0
cpuBet = 0 
userBet = 0
history = []

print('\n\tWELCOME! Good Luck!')
#main game loop
while playing == True:
    winnerDeclared = False
    cheatingBoolean = False
    cardDeck.reset_deck() #resets the deck each game
    bet = 0
    totalGames = totalGames+1
    print('\t ROUND NUMBER', totalGames, '\n')
    #initial user bet
    print("Place a bet: ")
    bet = input()
    userBet = int(bet)
    print('\n')
    if int(bet) != 0:
        print("CPU matches your bet")
        cpuBet = int(bet)
        bet = int(bet) + int(bet)
        
    #grab users cards, add to its hand
    uCard1 = cardDeck.give_random_card()
    uCard2 = cardDeck.give_random_card()
    uCard3 = cardDeck.give_random_card()
    uHand = [uCard1, uCard2, uCard3]
    uHand = sortRank(uHand)
    
    #grab CPU cards, add to its hand
    cCard1 = cardDeck.give_random_card()
    cCard2 = cardDeck.give_random_card()
    cCard3 = cardDeck.give_random_card()
    cHand = [cCard1, cCard2, cCard3]
    cHand = sortRank(cHand)

    
#NOTE= code below was modified to test cheat function- i will change this later
    #evaluate winner before cheating
    uEval = evaluate(uHand)
    cEval = evaluate(cHand)

    #determining if the cpu should cheat to win the game. then calls the cheat function if the conditions are met. 
    if ((checkWinRatio(history)==True)or(checkProfit(profit, history)==True))and(checkHistory(history)==True):
            cheatingBoolean = True
            if uEval!=5:
                randEvalNeeded = random.randint(uEval+1,5) #randomized evaluation that is used to create a higher ranking hand than the user's
                cHand = cheat(cHand,randEvalNeeded)
            if uEval ==5:
                cHand = cheat(cHand,6) #if the user has a straight flush (highest rank) then the highest card the cpu has is used to create a high straight flush
        
    #evaluate again after AI
    uHand = sortRank(uHand)
    cHand = sortRank(cHand)
    uEval = evaluate(uHand)
    cEval = evaluate(cHand)

    #randomize card locations to not spoil 3rd card (non ascending order)
    uHand = randHandIndices(uHand)
    cHand = randHandIndices(cHand)
    
    print("\n\tYour cards: ")
    printHandHidden(uHand)  
    print("\t----------")
    print("\tDealer's cards: ")
    printHandHidden(cHand)
    print("\t----------\n",'\tCurrent bet: ', bet, '\n\t----------\n' )

    #re-sort hands for final print
    uHand = sortRank(uHand)
    cHand = sortRank(cHand)

    #second round of betting
    print("Place no additional bet or raise:(0 for none) ")
    betIn = input()
    bet = int(bet) + int(betIn)
    userBet = userBet + int(betIn)

    #if the AI is cheating, following will be executed for raising/matching
    #if the AI is cheating, it would not 'fold'
    if(cheatingBoolean == True):    #if the AI is cheating
        if(cEval==1):   #if the Evaluation/CPU's hand has a pair
            compChoices=['match','raiseFirstOption']  #it can either match or raise, 2 options total
            raiseChoices = [1.20, 1.40] #raiseFirstOption is raising only 20% or 40% from the bet
            choice = random.choice(compChoices)
            if choice == "match":
                cpuBet = cpuBet + int(betIn)
                bet = int(bet) + int(betIn)
                print('CPU matches your bet')
            if choice == "raiseFirstOption":
                raiseBet = random.choice(raiseChoices)*bet # raiseBet is (random % from 20% or 40%) * (the bet)
                roundedRaiseBet = int(round(raiseBet,-2)) #rounding the raise bet to nearest 100 number and casting as integer
                cpuBet = cpuBet + int(betIn) + roundedRaiseBet
                bet = int(bet) + int(betIn) + roundedRaiseBet
                print("CPU has raised by ", roundedRaiseBet)
                print("\n\t----------\n",'\tCurrent bet: ', bet, '\n\t----------\n' )
                print('You must match the CPU raise or fold(match or fold):')
                usrIn = input()
                if str(usrIn) == 'match':
                    bet = int(bet) + roundedRaiseBet
                    userBet = userBet + roundedRaiseBet
                    print("\n\t----------\n",'\tCurrent bet: ', bet, '\n\t----------\n' )
                if str(usrIn) == 'fold':
                    print('\n\tYou fold, CPU has won\n')
                    gameResult = 'w'
                    winnerDeclared = True
        if(cEval==2 or cEval==3): #if the Evaluation/CPU's hand has a FLUSH or STRAIGHT
            choice="raiseSecondOption"     #raising 50% or 60% or 70% of the bet
            raiseChoices= [1.50, 1.60, 1.70]
            raiseBet = random.choice(raiseChoices)*bet #raiseBet is (random % from 50,60 or 70) * (the bet)
            roundedRaiseBet = int(round(raiseBet, -2)) #rounding the raise bet to nearest 100 number and casting as integer
            cpuBet = cpuBet + int(betIn) + roundedRaiseBet
            bet = int(bet) + int(betIn) + roundedRaiseBet
            print("CPU has raised by ", roundedRaiseBet)
            print("\n\t----------\n",'\tCurrent bet: ', bet, '\n\t----------\n' )
            print('You must match the CPU raise or fold(match or fold):')
            usrIn = input()
            if str(usrIn) == 'match':
                bet = int(bet) + roundedRaiseBet
                userBet = userBet + roundedRaiseBet
                print("\n\t----------\n",'\tCurrent bet: ', bet, '\n\t----------\n' )
            if str(usrIn) == 'fold':
                print('\n\tYou fold, CPU has won\n')
                gameResult = 'w'
                winnerDeclared = True
        if(cEval==4 or cEval == 5):  #if the Evaluation/CPU's hand has TRIPPLE or STRAIGHT-FLUSH
            choice="raiseThirdOption"    #raising 80% or 90% or 100% of the bet
            raiseChoices = [1.80, 1.90, 2]
            raiseBet = random.choice(raiseChoices)*bet # raiseBet is (random % from 80, 90 or 100) * (the bet)
            roundedRaiseBet = int(round(raiseBet, -2))  # rounding the raise bet to nearest 100 number and casting as integer
            cpuBet = cpuBet + int(betIn) + roundedRaiseBet
            bet = int(bet) + int(betIn) + roundedRaiseBet
            print("CPU has raised by ", roundedRaiseBet)
            print("\n\t----------\n",'\tCurrent bet: ', bet, '\n\t----------\n' )
            print('You must match the CPU raise or fold(match or fold):')
            usrIn = input()
            if str(usrIn) == 'match':
                bet = int(bet) + roundedRaiseBet
                userBet = userBet + roundedRaiseBet
                print("\n\t----------\n",'\tCurrent bet: ', bet, '\n\t----------\n' )
            if str(usrIn) == 'fold':
                print('\n\tYou fold, CPU has won\n')
                gameResult = 'w'
                winnerDeclared = True

    if (cheatingBoolean == False):              #IF we are NOT cheating, then the CPU decides to raise or match randomly
        #cpu bets, matching/raising
        compChoices = ['raise', 'match', 'raise', 'match', 'fold']
        raiseChoices = [10, 50, 100, 200]   #CPU decides randomly between these amounts, how much to raise
        choice = random.choice(compChoices)
        if choice == 'match':
            cpuBet = cpuBet + int(betIn)
            bet = int(bet) + int(betIn)
            print('CPU matches your bet')
        if choice == 'fold':
            print('\n\tCPU folds, you win!',"\n\tYou won: $", bet, '\n')
            gameResult = 'l'
            winnerDeclared = True
        if choice == 'raise':
            raiseBet = random.choice(raiseChoices)
            cpuBet = cpuBet + int(betIn) + raiseBet
            bet = int(bet) + int(betIn) + raiseBet
            print("CPU has raised by ", raiseBet)
            print("\n\t----------\n",'\tCurrent bet: ', bet, '\n\t----------\n' )
            print('You must match the CPU raise or fold(match or fold):' )
            usrIn = input()
            if str(usrIn) == 'match':
                bet = int(bet) + raiseBet
                userBet = userBet + raiseBet
                print("\n\t----------\n",'\tCurrent bet: ', bet, '\n\t----------\n' )
            if str(usrIn) == 'fold':
                print('\n\tYou fold, CPU has won\n')
                gameResult = 'w'
                winnerDeclared = True

    #print full hands (reveal 3rd card)
    print("\n\tYour cards: ")
    printHand(uHand)
    print("\t----------")
    print("\tDealer's cards: ")
    printHand(cHand)
    print("\t----------\n",'\tCurrent bet: ', bet, '\n\t----------\n' )


        
    #print out hand values in string format, determine if need highest card
    handAnalyze(uEval, "User", uHand)
    handAnalyze(cEval, "CPU", cHand)

    #update stat tracking for wins & losses 
    if winnerDeclared == False: #if winnerdeclared is true, that means user or cpu folded
        gameResult = compareHands(uEval, cEval, bet, uHand, cHand)
    history.append(gameResult)
    #update stat tracking for profit
    if  gameResult == 'w':
        profit = profit + userBet
    elif gameResult == 'l':
        profit = profit - cpuBet 

    print("Total games played: " + str(totalGames))
    print("\nCPU Stats: " + "\nTotal Profit/Loss amount: " + str(profit))
    print("\nHistory of Wins/Losses: " + str(history))
    #ask for another round or exit
    print("\nPlay another round? (y/n) ")
    again = input()
    if again == 'n':
        playing = False


    #for x in uHand:
    #    print(x.name)
    #for x in cHand:
    #    print(x.name)