
# https://pypi.org/project/deck-of-cards/
# ^ deck of cards import docs
#install using:    pip install deck-of-cards
from deck_of_cards import deck_of_cards
import random

#takes a hand and prints 2 of the 3 cards with symbol format
def printHandHidden(hand):
    #symbols = '♠', '♥', '♦', '♣'
    count = 0
    for x in hand:
        if count == 2:
            print('[ hidden ]')
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
            print('[', 'Ace',  x.suit, ']')
            count+=1
            continue
        if x.rank == 11:
            print('[', 'Jack',  x.suit, ']')
            count+=1
            continue
        if x.rank == 12:
            print('[', 'Queen',  x.suit, ']')
            count+=1
            continue
        if x.rank == 13:
            print('[', 'King',  x.suit, ']')
            count+=1
            continue
        print('[', x.rank,  x.suit, ']')
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
            print('[', 'Ace',  x.suit, ']')
            continue
        if x.rank == 11:
            print('[', 'Jack',  x.suit, ']')
            continue
        if x.rank == 12:
            print('[', 'Queen',  x.suit, ']')
            continue
        if x.rank == 13:
            print('[', 'King',  x.suit, ']')
            continue
        print('[', x.rank,  x.suit, ']')

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
    if c1.rank == (c2.rank+1) and c2.rank == (c3.rank+1): #checking for straight
        evaluation = 3
    if c1.rank == c2.rank and c2.rank == c3.rank: #checking for triple
        evaluation = 4
    if c1.rank == (c2.rank+1) and c2.rank == (c3.rank+1) and c1.suit == c2.suit and c2.suit == c3.suit: #checking for straight flush
        evaluation = 5
    return evaluation

#takes hands and the bet to determine who won
def compareHands(uEval, cEval, bet):
    if uEval > cEval:
        print("User wins!", "you won: $", bet)
    if cEval > uEval:
        print("CPU wins")
    if cEval == uEval:            
        print('The match is a draw')


#create new card deck
cardDeck = deck_of_cards.DeckOfCards()
playing = True

#main game loop
while playing == True:
    cardDeck.shuffle_deck() #resets the deck each game
    bet = 0
    #initial user bet
    print("Place a bet: ")
    bet = input()
    print('\n')

    #grab users cards, add to its hand
    uCard1 = cardDeck.give_first_card()
    uCard2 = cardDeck.give_first_card()
    uCard3 = cardDeck.give_first_card()
    uHand = [uCard1, uCard2, uCard3]
    print("Your cards: ")
    printHandHidden(uHand)
    #grab CPU cards, add to its hand
    cCard1 = cardDeck.give_first_card()
    cCard2 = cardDeck.give_first_card()
    cCard3 = cardDeck.give_first_card()
    cHand = [cCard1, cCard2, cCard3]
    print("----------")
    print("Dealer's cards: ")
    printHandHidden(cHand)
    print("----------\n", 'Current bet: ', bet, '\n---------' )

    #second round of betting
    print("Place no additional bet or raise:(0 for none) ")
    betIn = input()
    bet = int(bet) + int(betIn)

    #loop for cpu bets, matching/raising
    compChoices = ['match', 'match', 'raise', 'raise' 'fold']     #weighting this with duplicates, probably a much better way to do this, using AI components
    raiseChoices = [10, 50, 100, 200]
    bettingWar = True
    while bettingWar == True:
        choice = random.choice(compChoices)
        if choice == 'match' or choice == 'fold':
            bettingWar = False
            if choice == 'match':
                bet = int(bet) + int(betIn)
                print('CPU matches your bet')
            if choice == 'fold':
                print('CPU folds, you win!')
        if choice == 'raise':
            raiseBet = random.choice(raiseChoices)
            bet = int(bet) + raiseBet
            print("CPU has raised by ", raiseBet)
            print("----------\n", 'Current bet: ', bet, '\n---------' )
            print('You must match the CPU raise or fold(match or fold):' )
            usrIn = input()
            if str(usrIn) == 'match':
                bet = int(bet) + raiseBet
                print("----------\n", 'Current bet: ', bet, '\n---------' )
            if str(usrIn) == 'fold':
                print('You fold, CPU has won')

    #print full hands (reveal 3rd card)
    print("Your cards: ")
    printHand(uHand)
    print("----------")
    print("Dealer's cards: ")
    printHand(cHand)
    print("----------\n", 'Current bet: ', bet, '\n---------' )

    #evaluate winner
    uEval = evaluate(uHand)
    cEval = evaluate(cHand)
    compareHands(uEval, cEval, bet)

    #ask for another round or exit
    print("Play another round? (y/n) ")
    again = input()
    if again == 'n':
        playing = False


    #for x in uHand:
    #    print(x.name)
    #for x in cHand:
    #    print(x.name)