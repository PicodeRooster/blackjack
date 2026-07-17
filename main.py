from Archive.participants import *
import random
from rich import print
import sys

chips = f"[bold white][5] [10] [25] [50][/bold white] [bold blue][100] [200] [300][/bold blue] [bold red][400] [500][/bold red]"
game_options = ["SPLIT", "DOUBLE", "DEAL", "BET", "STAND", "QUIT"]

class Cards:
    def __init__(self):
        self.cards = {
            "SUITS" : [":heart_suit:", ":spade_suit:", ":diamond_suit:", ":club_suit:"],
            # (display rank, blackjack value) — one entry per card, so 13 per suit.
            # Ace starts at 11; get_hand_total downgrades it to 1 when the hand would bust.
            "RANKS" : [
            ("Ace", 11),
            ("2", 2),
            ("3", 3),
            ("4", 4),
            ("5", 5),
            ("6", 6),
            ("7", 7),
            ("8", 8),
            ("9", 9),
            ("10", 10),
            ("Jack", 10),
            ("Queen", 10),
            ("King", 10),
        ]
    }
    
    def build_deck(self): 
        deck = []
        for suit in self.cards["SUITS"]:
            for rank, value in self.cards["RANKS"]:
                deck.append({"suit": suit, "rank": rank, "value": value})
        
        random.shuffle(deck)
        return deck

playing_cards = Cards()
print(playing_cards.build_deck())

class Participant:
    def __init__(self, deck):
        self.deck = deck
        self.current_hand = {}
        self.rounds_won = 0
            
    def deal_new_cards(self):
        card_count = len(self.current_hand) + 1
        self.current_hand[f"card {card_count}"] = self.deck.pop()
    
    def deal_new_hand(self):
        self.current_hand = {
            "card 1": self.deck.pop(),
            "card 2": self.deck.pop()
        }
        
    def get_hand_total(self):
        total = 0
        ace_count = 0

        for card in self.current_hand.values():
            total += card["value"]  # numeric value: Ace=11, face cards=10
            if card["value"] == 11:
                ace_count += 1

        # Downgrade Aces from 11 to 1, one at a time, if we're busting
        while total > 21 and ace_count > 0:
            total -= 10  # 11 -> 1 is a difference of 10
            ace_count -= 1

        return total

class Player(Participant):
    def __init__(self, deck, wallet=5000):
        super().__init__(deck)
        self.wallet = wallet
        self.current_bet = 0

class Dealer(Participant):
    def must_hit(self, hand_total):
        return hand_total < 17

#Note: The word "shoe" is a casino term. It just means "the shared deck between the dealer and the player in Blackjack"
shoe = playing_cards.build_deck()
dealer = Dealer(shoe)
player = Player(shoe)

def exit_game():
    print('Thanks for playing!')
    sys.exit()

#Quit the game at any time
def get_input(prompt):
    value = input(prompt)
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

    # Ask about modifying the bet first, then whether to start.
    # Keep looping until the player starts the game or the wallet is empty.
    while player.wallet > 0:
        print(chips)
        if ask_yes_no('Would you like to modify the bet? [Y/N] ') == "y":
            # add the new amount on top of the current bet, and take that extra out of the wallet
            added = input_bet()
            player.current_bet += added
            player.wallet -= added
            player_economy_ui()

        if ask_yes_no('Start game? [Y/N] ') == "y":
            break

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

def game():
    player.deal_new_cards()
    check values for player
    if card 1 and card 2 have the same 'value', show SPLIT option
    if get_hand_total(player) < 21, show game_options
    if get_hand_total(player) == 21, BLACKJACK
    if STAND and get_hand_total(player) < 21:
        if must_hit(dealer, get_hand_total(dealer)) == FALSE
            deal new card for dealer until at least 17 True
        if player hand total > 21:
            BUST, dealer wins
            remove chips from wallet
        if dealer hand total > 21:
            player wins
            add chips to wallet
        if dealer hand total > player hand total:
            dealer wins round
            remove chips from wallet
        if dealer hand total < player hand total:
            player winds round
            add chips to wallet
        if dealer hand total == player hand total:
            PUSH
            end round
            do nothing

    


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