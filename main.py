from cards import *
from participants import *
from rich import print
import sys

chips = f"[bold white][5] [10] [25] [50][/bold white] [bold blue][100] [200] [300][/bold blue] [bold red][400] [500][/bold red]"
game_options = ["SPLIT", "DOUBLE", "DEAL", "BET", "STAND", "QUIT"]

def exit_game():
    print('Thanks for playing!')
    sys.exit()

#Quit the game at any time
def get_input(prompt):
    value = input("Type an option from above:")
    if value.strip().upper() == "QUIT":
        exit_game()
    return value

#Prompt for a bet amount between 0 and 500, and no more than the wallet holds.
def input_bet():
    while True:
        try:
            print(chips)
            amount = int(get_input('Input your amount: '))
            
            if amount < 0 or amount > 500:
                print("Amount must be between 0 and 500!")
                continue
            
            if amount > player.wallet:
                print(f"You don't have enough for {amount}!")
                print(f"Current funds: {player.wallet}")
                continue 

            player.current_bet = player.current_bet + amount
            player.wallet = player.wallet - amount
            return amount
        
        except ValueError:
            print("That's not a valid number!")
            continue           

def ask_yes_no(prompt):
    #Keep asking until the user gives a valid Y/N answer, then return 'y' or 'n'.
    while True:
        answer = get_input(prompt).strip().lower()
        if answer in ("y", "n"):
            return answer
        print("Please input Y or N in upper or lowercase.")

def player_economy_ui():
    print("---")
    print(f"Current bet: {player.current_bet}")
    print(f"Wallet: {player.wallet}")

def pregame():
    print("Welcome to Blackjack!", ":slot_machine:")
    print("To begin, place your bet.", ":money-mouth_face:")

    player.current_bet = input_bet()
    player.wallet -= player.current_bet
    player_economy_ui()

    # Give the player a chance to change their bet before starting
    if ask_yes_no('Would you like to modify the bet? [Y/N] ') == "y":
        print(chips)
        # refund the old bet first, since it's no longer wagered
        player.wallet += player.current_bet
        player.current_bet = input_bet()
        player.wallet -= player.current_bet
        player_economy_ui()
        print(chips)

    # Confirm start, allowing the player to keep adjusting until they say yes
    while True:
        player_economy_ui()
        print(chips)
        if ask_yes_no('Start game? [Y/N] ') == "y":
            player.current_bet = input_bet()
            player.wallet = player.wallet - player.current_bet 
            player_economy_ui()
            
            break
        else:
            ask_yes_no('Would you like to modify the bet? [Y/N] ')
            print(chips)
            return 

    return player.wallet 

def start_of_round():        
    print("---")
    print("Dealer's hand:")
    print(f"???, {dealer.current_hand['card 2']['suit']}{dealer.current_hand['card 2']['rank']}")
        
    print("---")
    print("Your hand:")
    print(f"{player.current_hand['card 1']['suit']}{player.current_hand['card 1']['rank']},{player.current_hand['card 2']['suit']}{player.current_hand['card 2']['rank']}")

    player_economy_ui()

    print("---")
    print("[bold green][BET][/bold green] [bold cyan][DEAL][/bold cyan] [bold #ff8700][STAND][/bold #ff8700] [bold #d70087][DOUBLE][/bold #d70087] [bold red1][QUIT][bold red1]")

pregame()

'''

One usage note: call it as player.deal_new_hand() and dealer.deal_new_hand() at the start of a round — not deal_new_cards() for the first deal, since deal_new_hand resets current_hand to a fresh 2-card hand, while deal_new_cards assumes a hand already exists and adds one card to it (for hits).


def confirm_initial_bet(wallet, amount):
    player_economy_ui
    print(chips)

    while True:
        try:
            answer = ask_yes_no('Would you like to modify the bet? [Y/N] ')
            if ask_yes_no('Start game? [Y/N] ') == "y":
                amount = input_bet(wallet)

            player.wallet = wallet - amount
            player_economy_ui()
            
            else:
                ask_yes_no('Would you like to modify the bet? [Y/N] ')
                print(chips)
                break
        else:
        

        except:

'''            
    
