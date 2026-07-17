from rich import print
import random
import re
import sys

def exit_game():
    print('Thanks for playing!')
    sys.exit()

#Quit the game at any time
def get_input(prompt):
    value = input("Type an option from above:")
    if value.strip().upper() == "QUIT":
        exit_game()
    return value

playing_cards = {
    "SUITS" : [":heart_suit:", ":spade_suit:", ":diamond_suit:", ":club_suit:"],
    "VALUES" : {
        1: "Ace",
        2 : "2",
        3 : "3",
        4 : "4",
        5 : "5",
        6 : "6",
        7 : "7",
        8 : "8",
        9 : "9",
        10: "10",
        11: "Ace",
        "Jack": "10",
        "Queen": "10", 
        "King" : "10"
    }
}

# Empty deck list variable
deck = []

# Building deck
for suit in playing_cards["SUITS"]:
    for key, value in playing_cards["VALUES"].items():
        if key == (1, 11):
            deck.append({"suit": suit, "rank": value, "value": key})
        elif isinstance(key, tuple):
            for name in key:
                deck.append({"suit": suit, "rank": name, "value": value})
        else:
            deck.append({"suit": suit, "rank": value, "value": key})

#Create a shuffled deck for each player
random.shuffle(deck)
dealer_deck = deck
random.shuffle(deck)
player_deck = deck

dealer = {
        "deck" : dealer_deck,
        "rounds_won": 0,
        "current_hand": [] 
}
    
player = {
        "deck" : player_deck,
        "rounds_won": 0,
        "wallet": 5000,
        "current_bet": 0,
        "current_hand": []
}

#Prompt for a bet amount between 0 and 500, and no more than the wallet holds.
def input_bet(wallet):
    while True:
        try:
            amount = int(get_input('Input your amount: '))
        except ValueError:
            print("That's not a valid number!")
            continue

        if amount < 0 or amount > 500:
            print("Amount must be between 0 and 500!")
            continue

        if amount > wallet:
            print(f"You don't have enough for {amount}!")
            print(f"Current funds: {wallet}")
            continue
        
        player['current_bet'] = player['current_bet'] + amount
        player['wallet'] = wallet - amount

def ask_yes_no(prompt):
    #Keep asking until the user gives a valid Y/N answer, then return 'y' or 'n'.
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "n"):
            return answer
        print("Please input Y or N in upper or lowercase.")

def player_economics_ui():
    print("---")
    print(f"Current bet: {player['current_bet']}")
    print(f"Wallet: {player['wallet']}")

def pregame(wallet, bet_amount):
    print("Welcome to Blackjack!", ":slot_machine:")
    print("To begin, place your bet.", ":money-mouth_face:")
    print("[bold white][5] [10] [25] [50][/bold white] [bold blue][100] [200] [300][/bold blue] [bold red][400] [500][/bold red]")

    bet_amount = input_bet(wallet)

    wallet -= bet_amount
    player_economics_ui()

    # Give the player a chance to change their bet before starting
    if ask_yes_no('Would you like to modify the bet? [Y/N] ') == "y":
        print("[bold white][5] [10] [25] [50][/bold white] [bold blue][100] [200] [300][/bold blue] [bold red][400] [500][/bold red]")
        # refund the old bet first, since it's no longer wagered
        wallet += bet_amount
        bet_amount = input_bet(wallet)
        wallet -= bet_amount
        player_economics_ui(bet_amount, wallet)

    # Confirm start, allowing the player to keep adjusting until they say yes
    while True:
        player_economics_ui(bet_amount, wallet)
        if ask_yes_no('Start game? [Y/N] ') == "y":
            break
        else:
            wallet += bet_amount
            bet_amount = input_bet(wallet)
            wallet -= bet_amount

    return wallet, bet_amount

def deal_new_hand():
    dealer_hand = {
        "card 1": dealer['deck'].pop(),
        "card 2": dealer['deck'].pop()
    }

    player_hand = {
        "card 1": player['deck'].pop(),
        "card 2": player['deck'].pop()
    }

    dealer['current_hand'] = dealer_hand
    player["current_hand"] = player_hand
    
def deal_new_cards(obj):
    #Check how many cards are currently in hand
    key_count = []
    for key in obj.keys():
        numbers = re.findall('\d+', key)
        key_count.append(numbers)
    cc = key_count[-1:][0]
    card_count = "".join(str(x) for x in cc) + 1
    key_name = f"card {card_count}"
    obj['current_hand'][key_name] = obj['deck'].pop()        
 
def game_options(split, bet):
    #Use game_options( boolean, boolean). If user has a total of 10, they see the SPLIT option. If user's wallet has enough to continue betting, they see the deal option.
    #The options are gone if the function is inputted with False for either one.
    if split == True and bet == True:
        options = ["BET", "DEAL", "STAND", "SPLIT", "DOUBLE"]
    elif split == False and bet == True:
        options = ["BET", "DEAL", "STAND", "DOUBLE"]
    elif split == True and bet == False:
        options = ["DEAL", "STAND", "SPLIT", "DOUBLE"]
    else:
        options = ["DEAL", "STAND", "DOUBLE"]

    return options

def track_values():
    deal_new_hand()
    for value in player['current_hand'].values():
        print(value['value'])
    

track_values()
breakpoint
for suit in playing_cards["SUITS"]:
    for key, value in playing_cards["VALUES"].items():
        if key == (1, 11):
            deck.append({"suit": suit, "rank": value, "value": key})
        elif isinstance(key, tuple):
            for name in key:
                deck.append({"suit": suit, "rank": name, "value": value})
        else:
            deck.append({"suit": suit, "rank": value, "value": key})
'''
if __name__ == "__main__":
    wallet, bet_amount = pregame()
'''    