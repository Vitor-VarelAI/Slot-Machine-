import random
import os
import time
from colorama import init, Fore, Back, Style

# Initialize Colorama
init(autoreset=True)

# Constants
REELS = 5
SYMBOLS = ['M', 'O', 'N', 'E', 'Y', 'A', 'B', 'C', 'D']
BONUS_SYMBOL = 'B'
BONUS_SPINS = 3
INITIAL_BALANCE = 100.0
MIN_BET = 1.0
MAX_BET = 500.0

# Add color coding to symbols
SYMBOL_COLORS = {
    'M': Fore.RED,
    'O': Fore.GREEN,
    'N': Fore.BLUE,
    'E': Fore.YELLOW,
    'Y': Fore.MAGENTA,
    'A': Fore.CYAN,
    'B': Fore.WHITE + Back.RED,
    'C': Fore.WHITE,
    'D': Fore.LIGHTBLUE_EX
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_user_input():
    return input("Enter command (s: Spin, a: Decrease bet, d: Increase bet, 1-5: Quick bet, e: Exit): ").lower()

def spin_reels_with_animation():
    spinning_reels = []
    for _ in range(REELS):
        reel = []
        for _ in range(3):
            reel.append(random.choice(SYMBOLS))
        spinning_reels.append(reel)
    
    for _ in range(10):  # Number of animation frames
        clear_screen()
        print(Fore.CYAN + "╔════════════════════════════════════════════╗")
        print(Fore.CYAN + "║           VARELA E ROMA MACHINE            ║")
        print(Fore.CYAN + "╠════════════════════════════════════════════╣")
        print(Fore.CYAN + "║" + display_spinning_reels(spinning_reels).center(44) + "║")
        print(Fore.CYAN + "╚════════════════════════════════════════════╝")
        
        # Shift symbols in each reel
        for reel in spinning_reels:
            reel.pop(0)
            reel.append(random.choice(SYMBOLS))
        
        time.sleep(0.1)
    
    return [reel[1] for reel in spinning_reels]  # Return the middle row

def spin_reels_with_animation():
    title = "VARELA E ROMA MACHINE"
    padding = " " * ((44 - len(title)) // 2)
    
    for _ in range(20):  # Number of animation frames
        clear_screen()
        print(Fore.CYAN + "╔════════════════════════════════════════════╗")
        
        # Animate the title
        if _ % 2 == 0:
            print(Fore.CYAN + "║" + padding + title + padding + "║")
        else:
            print(Fore.CYAN + "║" + " " * 44 + "║")
        
        print(Fore.CYAN + "╠════════════════════════════════════════════╣")
        print(Fore.CYAN + "║" + " " * 44 + "║")
        print(Fore.CYAN + "║" + "[ ] [ ] [ ] [ ] [ ]".center(44) + "║")
        print(Fore.CYAN + "║" + " " * 44 + "║")
        print(Fore.CYAN + "╚════════════════════════════════════════════╝")
        
        time.sleep(0.1)
    
    # Generate and return the final reels
    return [random.choice(SYMBOLS) for _ in range(REELS)]

def display_slot_machine(balance, last_win, bet, reels=None):
    clear_screen()
    print(Fore.CYAN + "╔════════════════════════════════════════════╗")
    print(Fore.CYAN + "║           VARELA E ROMA MACHINE            ║")
    print(Fore.CYAN + "╠════════════════════════════════════════════╣")
    if reels:
        print(Fore.CYAN + "║" + display_reels(reels).center(44) + "║")
    else:
        print(Fore.CYAN + "║" + "[ ] [ ] [ ] [ ] [ ]".center(44) + "║")
    print(Fore.CYAN + "╠════════════════════════════════════════════╣")
    print(Fore.CYAN + f"║ Balance: ${balance:<8.2f}                      ║")
    print(Fore.CYAN + f"║ Last Win: ${last_win:<8.2f}                     ║")
    print(Fore.CYAN + f"║ Current Bet: ${bet:<8.2f}                   ║")
    print(Fore.CYAN + "╠════════════════════════════════════════════╣")
    print(Fore.CYAN + "║ [S] Spin | [A] Decrease | [D] Increase | [E] Exit ║")
    print(Fore.CYAN + "║ Quick Bet: [1] $20 | [2] $50 | [3] $80 | [4] $150 | [5] $500 ║")
    print(Fore.CYAN + "╚════════════════════════════════════════════╝")

def display_reels(reels):
    reel_display = ""
    for i in range(3):  # Display 3 rows
        reel_display += "| "
        for symbol in reels:
            if i == 1:  # Middle row shows the actual symbols
                reel_display += f"{SYMBOL_COLORS[symbol]}{symbol}{Style.RESET_ALL} | "
            else:
                reel_display += "  | "
        reel_display += "\n"
    return reel_display

def play_slot_machine():
    balance = INITIAL_BALANCE
    last_win = 0.0
    bet = 5.0

    while True:
        display_slot_machine(balance, last_win, bet)
        
        key = get_user_input()
        if key == 's':
            if balance < bet:
                print(Fore.RED + "Insufficient balance to place bet!")
                input("Press Enter to continue...")
                continue

            balance -= bet
            reels = spin_reels_with_animation()
            display_slot_machine(balance, last_win, bet, reels)
            result = check_win_condition(reels)

            if result == 'bonus':
                old_balance = balance
                balance = play_bonus_round(balance)
                last_win = balance - old_balance
            elif result == 'jackpot':
                last_win = bet * 100
                print(Fore.YELLOW + Style.BRIGHT + "JACKPOT!!! You spelled 'MONEY'!")
            elif result == 'win':
                last_win = bet * 5
                print(Fore.GREEN + "You Win! 'YO' or three or more of a 'MONEY' letter!")
            else:
                last_win = 0
                print(Fore.RED + "No Win")

            balance += last_win
            print(Fore.CYAN + f"Result: {result.capitalize()}! You won ${last_win:.2f}")
            input("Press Enter to continue...")
        elif key == 'e':
            print(Fore.YELLOW + f"Thanks for playing! Your final balance: ${balance:.2f}")
            break
        elif key == 'a':
            bet = max(MIN_BET, bet - 0.5)
        elif key == 'd':
            bet = min(MAX_BET, bet + 0.5)
        elif key in ['1', '2', '3', '4', '5']:
            bet_increase = {
                '1': 20, '2': 50, '3': 80, '4': 150, '5': 500
            }
            bet = min(MAX_BET, bet_increase[key])
        else:
            print(Fore.RED + "Invalid input. Please try again.")
            input("Press Enter to continue...")

def check_win_condition(reels):
    reel_str = "".join(reels)
    if BONUS_SYMBOL in reels:
        return 'bonus'
    if all(letter in reel_str for letter in 'MONEY'):
        return 'jackpot'
    if 'YO' in reel_str or any(reel_str.count(letter) >= 3 for letter in 'MONEY'):
        return 'win'
    return 'lose'

if __name__ == "__main__":
    play_slot_machine()