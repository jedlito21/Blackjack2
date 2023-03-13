import random
import json

chips = None

# hodnota karty
def value_of_card(card):
    rank = card['Rank']
    if rank.isnumeric():
        return int(rank)
    elif rank == "Jack" or rank == "Queen" or rank == "King":
        return 10
    elif rank == "Ace":
        return 11


# počítání ruky
def count_hand(hand):
    count = 0
    aces = 0
    for card in hand:
        if value_of_card(card) == 11:
            aces = aces + 1
        count = count + value_of_card(card)
    for _ in range(aces):
        if count > 21:
            count = count - 10
    return count

# dealování karet
def deal_card(turn):
    card = random.choice(pack)
    turn.append(card)
    pack.remove(card)

# ukázání karet dealera a hráče
def reveal(hand, hidden):
    string = ""
    for i, card in enumerate(hand):
        if i == 0 and hidden:
            continue
        else:
            string = string + card['Rank'] + " " + card['Suit'] + " "
    return string

players = []
def json_write(nickname, chips):
    with open("leaderboard.json", "r") as file:
        load = json.load(file)
        arr = load[nickname] if nickname in load else []

    with open("leaderboard.json", "w") as f:
        arr.append(chips)
        players = {nickname: arr}
        load.update(players)
        f.write(json.dumps(load))

def json_read():
    with open("leaderboard.json", "r") as f:
        load = json.load(f)
        for key, value in load.items():
            print(key, " - ", max(value))
# výhry a prohry
def win(chips):
    print('\n____________________________________________________\nDealer cards: ', reveal(dealer_cards, True), 'and Unknown')
    print('Your cards: ', reveal(player_cards, False), '\nYour sum is: ', count_hand(player_cards))
    print("_____________________________________\nYOU WON!")
    chips = chips + bet
    print(chips)
    return chips

def loose(chips):
    print('\n____________________________________________________\nDealer cards: ', reveal(dealer_cards, True), 'and Unknown')
    print('Your cards: ', reveal(player_cards, False), '\nYour sum is: ', count_hand(player_cards))
    print("_____________________________________\nYOU LOST!")
    chips = chips - bet
    print(chips)
    return chips

def draw():
    print('\n____________________________________________________\nDealer cards: ', reveal(dealer_cards, True), 'and Unknown')
    print('Your cards: ', reveal(player_cards, False), '\nYour sum is: ', count_hand(player_cards))
    print("_____________________________________\nDRAW")
    print(chips)

def blackjack(chips):
    print('\n____________________________________________________\nDealer cards: ', reveal(dealer_cards, True), 'and Unknown')
    print('Your cards: ', reveal(player_cards, False), '\nYour sum is: ', count_hand(player_cards))
    print("_____________________________________\nBLACKJACK!")
    chips = chips + bet + round(bet / 2)
    print(chips)
    return chips

# menu
MENU = "██████  ██       █████   ██████ ██   ██      ██  █████   ██████ ██   ██\n██   ██ ██      ██   ██ ██      ██  ██       ██ ██   ██ ██      ██  ██ \n██████  ██      ███████ ██      █████        ██ ███████ ██      █████  \n██   ██ ██      ██   ██ ██      ██  ██  ██   ██ ██   ██ ██      ██  ██ \n██████  ███████ ██   ██  ██████ ██   ██  █████  ██   ██  ██████ ██   ██ \n"
choices = "__________________________________________________________________________\n1 - Play\n2 - Ladder\n3 - Rules\n4 - About\n5 - End game\n"

loop = False
gameloop = True


print(MENU)
while gameloop == True:
    menu_text = input(choices)
    gameloop = False
    if menu_text == "1":
        # nastavení nicku a žetonů
        chips = 1000
        nickname = input('Type your nickname: ')
        loop = True
    elif menu_text == "2":
        print("_____________________________________\nLEADERBOARD\n_____________________________________\n")
        print(json_read())
        gameloop = True
    elif menu_text == "3":
        print("_____________________________________\nRULES\n\n•At start you get 2 cards\n•Your goal is to get sum of 21 or less\n•If you have more than 21 you loose\n•If you have 21 or less and the dealer has less than you, you win\n•If dealer has more than you but it's 21 or less, you loose\n_____________________________________\n\n")
        gameloop = True
    elif menu_text == "4":
        print("_____________________________________\nABOUT\nThis game was made as a school project for aplication development by Tomas Jedlicka\n_____________________________________\n")
        gameloop = True
    elif menu_text == "5":
        quit()
    else:
        print("________________________\nYou chose wrong number!\n________________________\n")
        gameloop = True

    # loop hry
    while loop:
        # hráč nebo dealer jsou ve hře
        player = True
        dealer = True
        print('Your chips: ', chips)
        # vytvořený balík karet
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        colors = ["♥", "♦", "♠", "♣"]
        pack = [{"Rank": rank, "Suit": color} for rank in ranks for color in colors]
        random.shuffle(pack)

        # ukládání karet
        player_cards = []
        dealer_cards = []

        for _ in range(2):
            deal_card(player_cards)
            deal_card(dealer_cards)

        while player or dealer:
            loop = False
            try:
                p = True
                while p:
                    bet = int(input("Place your bet: "))
                    if bet > chips:
                        print("You cannot bet more than you have")
                    elif bet < 0:
                        print("You can not bet negative amount of chips!")
                    else:
                        p = False
            except ValueError:
                print('\n____________________________________________________\nPlease enter integer only!\n____________________________________________________\n')
                continue
            print('\n____________________________________________________\nDealer cards: ', reveal(dealer_cards, True), 'and Unknown')
            print('Your cards: ', reveal(player_cards, False), '\nYour sum is: ', count_hand(player_cards))
            if count_hand(player_cards) == 21:
                print('\n____________________________________________________\nDealer cards: ', reveal(dealer_cards, True), 'and Unknown')
                print('Your cards: ', reveal(player_cards, False), '\nYour sum is: ', count_hand(player_cards))
                chips = blackjack(chips)
                json_write(nickname, chips)
                player = False
                next_round = input("Do you wanna play again?  1 - Yes / Any other character - No")
                if next_round == "1":
                    loop = True
                else:
                    loop = False
                    gameloop = True
            else:
                while player:
                    if len(player_cards) == 2:
                        if bet < (chips / 2):
                            double_down = " / 3 - double down"
                            dd = True
                        else:
                            double_down = ""
                            dd = False
                    else:
                        double_down = ""
                    take_card = input("____________________________________________________\nDo you want to take a card?  1 - yes / 2 - no" + double_down + "\n___________________________________________________\n")
                    if take_card == "1":
                        deal_card(player_cards)
                        print('\n____________________________________________________\nDealer cards: ', reveal(dealer_cards, True), 'and Unknown')
                        print('Your cards: ', reveal(player_cards, False), '\nYour sum is: ', count_hand(player_cards))
                        if count_hand(player_cards) > 21:
                            player = False
                        else:
                            continue

                    elif take_card == "2":
                        player = False
                        loop = False
                        gameloop = True

                    elif take_card == "3":
                        if dd == True:
                            deal_card(player_cards)
                            bet = bet * 2
                            player = False
                        else:
                            print("\n____________________________________________________\nYou picked wrong number!\n____________________________________________________\n")
                while count_hand(dealer_cards) <= 16:
                    deal_card(dealer_cards)
                dealer = False
                if count_hand(player_cards) <= 21:
                    if count_hand(player_cards) > count_hand(dealer_cards):
                        chips = win(chips)
                        json_write(nickname, chips)
                    elif count_hand(player_cards) == count_hand(dealer_cards):
                        draw()
                        json_write(nickname, chips)
                    else:
                        chips = loose(chips)
                        json_write(nickname, chips)
                else:
                    chips = loose(chips)
                    json_write(nickname, chips)
                if chips <= 0:
                    print("You have no more chips!")
                    loop = False
                    gameloop = True
                else:
                    next_round = input("Do you wanna play again?  1 - Yes / Any other character - No")
                    if next_round == "1":
                        loop = True
                    else:
                        loop = False
                        gameloop = True