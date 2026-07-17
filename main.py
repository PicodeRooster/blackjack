from cards import *
from participants import *
from rich import print
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

#Prompt for a bet amount between 0 and 500, and no more than the wallet holds.
def input_bet(wallet):
    while True:
        try:
            amount = int(get_input('Input your amount: '))
            break
        except ValueError:
            print("That's not a valid number!")
            
        if amount < 0 or amount > 500:
            print("Amount must be between 0 and 500!")
            continue

        if amount > wallet:
            print(f"You don't have enough for {amount}!")
            print(f"Current funds: {wallet}")
            continue
        
        player.current_bet = player.current_bet + amount
        player.wallet = wallet - amount

def ask_yes_no(prompt):
    #Keep asking until the user gives a valid Y/N answer, then return 'y' or 'n'.
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "n"):
            return answer
        print("Please input Y or N in upper or lowercase.")

def player_economy_ui():
    print("---")
    print(f"Current bet: {player.current_bet}")
    print(f"Wallet: {player.wallet}")

def pregame(wallet, bet_amount):
    print("Welcome to Blackjack!", ":slot_machine:")
    print("To begin, place your bet.", ":money-mouth_face:")
    print("[bold white][5] [10] [25] [50][/bold white] [bold blue][100] [200] [300][/bold blue] [bold red][400] [500][/bold red]")

    bet_amount = input_bet(wallet)
    wallet -= bet_amount
    player_economy_ui()

    # Give the player a chance to change their bet before starting
    if ask_yes_no('Would you like to modify the bet? [Y/N] ') == "y":
        print("[bold white][5] [10] [25] [50][/bold white] [bold blue][100] [200] [300][/bold blue] [bold red][400] [500][/bold red]")
        # refund the old bet first, since it's no longer wagered
        wallet += bet_amount
        bet_amount = input_bet(wallet)
        wallet -= bet_amount
        player_economy_ui(bet_amount, wallet)

    # Confirm start, allowing the player to keep adjusting until they say yes
    while True:
        player_economy_ui(bet_amount, wallet)
        if ask_yes_no('Start game? [Y/N] ') == "y":
            break
        else:
            bet_amount = input_bet(wallet)
            player.wallet = wallet - bet_amount
            player_economy_ui()

    return wallet, bet_amount 

game_opts = ["SPLIT", "DOUBLE", "DEAL", "BET", "STAND"]
def show_game_opts(*args):
    return f"{args}"

#pregame(player.wallet, player.current_bet)
print(player.wallet)
breakpoint
def start_of_round():        
    print("---")
    print("Dealer's hand:")
    print(f"???, {dealer.current_hand['card 2']['suit']}{dealer.current_hand['card 2']['rank']}")
        
    print("---")
    print("Your hand:")
    print(f"{player.current_hand['card 1']['suit']}{player.current_hand['card 1']['rank']},{player.current_hand['card 2']['suit']}{player.current_hand['card 2']['rank']}")

    player_economy_ui(player.current_hand, player.wallet)

    print("---")
    print("[bold green][BET][/bold green] [bold cyan][DEAL][/bold cyan] [bold #ff8700][STAND][/bold #ff8700] [bold #d70087][DOUBLE][/bold #d70087] [bold red1][QUIT][bold red1]")