import random, sys

#suits
HEARTS = chr(9289)
DIAMONDS = chr(9830)
SPADES = chr(9824)
CLUBS = chr(9827)
BACKING = 'backing'

def main():
    print('''Blackjack!
    Rules:
        Try to get as close to 21 without going over.
        Face cards are worth 10.
        Aces are worth 1 or 11.
        Blackjack pays 3 to 2.
        (H)it to take another card
        (S)tand to stop taking cars
        On your first play, you may (D)ouble down and double your bet for one single card
        In case of a tie, bet is returned to player
        Dealer stands on 17''')

    money = input('How much would you like to play with today? >')
    if money.isdigit() == False:
        money = input("Please enter a number greater than 0. >")
    elif int(money) < 0:
        money = input("Please enter a number greater than 0. >")
    else:
        money = int(money)
    
    while True:
        if money <= 0:
            print("Thanks for playing! Better luck next time.")
            sys.exit()
        
        print('Money: ', money)
        bet = getBet(money)

        deck = getDeck()
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]

        print('Bet: ', bet)
        while True:
            displayHands(playerHand, dealerHand, False)
            print()

            if getHandValue(playerHand) > 21:
                break

            if len(playerHand) == 2 and getHandValue(playerHand) == 21:
                winning = 1.5 * bet
                blackjack = True

            move = getMove(playerHand, money - bet)
            
            if move == 'D':
                additionalBet = getBet(min(bet, (money - bet)))
                bet += additionalBet
                print("Player doubles down")
            
            if move in ('H', 'D'):
                newCard = deck.pop()
                rank, suit = newCard
                print('You drew the {} of {}'.format(rank, suit))
                playerHand.append(newCard)

                if getHandValue(playerHand) > 21:
                    continue

            if move in ('S', 'D'):
                break
        
        if getHandValue(playerHand) <= 21:
            while getHandValue(dealerHand) < 17:
                print('Dealer hits.')
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)

                if getHandValue(dealerHand) > 21:
                    break
                input('Press Enter to continue.')
                print('\n\n')
            displayHands(playerHand, dealerHand, True)

        playerValue = getHandValue(playerHand)
        dealerValue = getHandValue(dealerHand)

        if blackjack == True:
            money += winning
            print("Blackjack! you win {}!".format(winning))        
        elif dealerValue > 21:
            print('Dealer busts. You win ${}!'.format(bet))
            money += bet
        elif (playerValue > 21) or (playerValue < dealerValue):
            print('You lost.')
            money -= bet
        elif playerValue > dealerValue:
            print('You won ${}!'.format(bet))
            money += bet
        elif playerValue == dealerValue:
            print('Push. Nobody wins.')
        
        input('Press enter to continue')
        print('\n\n')



def getBet(maxBet):
    while True:
        bet = input('How much would you like to bet this hand? (1-{}, or QUIT) >'.format(maxBet)).upper().strip()
        if bet == 'QUIT':
            print('Thanks for playing!')
            sys.exit()
        if not bet.isdecimal():
            continue
        
        bet = int(bet)
        if 1 <= bet <= maxBet:
            return bet

def getDeck():
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))
        for rank in ('J', 'K', 'Q', 'A'):
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck

def displayHands(playerHand, dealerHand, showDealerHand):
    #Hides dealers first card if showDealerHand == False
    if showDealerHand:
        print('DEALER: ', getHandValue(dealerHand))
        displayCards(dealerHand)
    else:
        print('DEALER: ???')
        displayCards([BACKING] + dealerHand[1:])
    
    print('PLAYER: ', getHandValue(playerHand))
    displayCards(playerHand)

def getHandValue(cards):
    value = 0
    numberAces = 0

    for card in cards:
        rank = card[0]
        if rank == 'A':
            numberAces += 1
        elif rank in ('K', 'Q', 'J'):
            value += 10
        else:
            value += int(rank)
    
    value += numberAces
    for i in range(numberAces):
        if value + 10 <= 21:
            value += 10
    
    return value

def displayCards(cards):
    rows = ['','','','','']

    for i, card in enumerate(cards):
        rows[0] += ' __   '
        if card == BACKING:
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '| ##| '
        else:
            rank, suit = card
            rows[1] += '|{} | '.format(rank.ljust(2))
            rows[2] += '| {} | '.format(suit)
            rows[3] += '|_{}| '.format(rank.rjust(2, '_'))

    for row in rows:
        print(row)

def getMove(playerHand, money):
    while True:
        moves = ['(H)it', '(S)tand']

        if len(playerHand) == 2 and money > 0:
            moves.append('(D)ouble down')
        
        movePrompt = ', '.join(moves) + '> '
        move = input(movePrompt).upper()
        if move in ('H', 'S'):
            return move
        if move == 'D' and '(D)ouble down' in moves:
            return move
        
if __name__ == '__main__':
    main()
