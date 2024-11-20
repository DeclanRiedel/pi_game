from mpmath import mp
import os
import json

# Set precision for Pi generation
mp.dps = 1000001  # Set slightly higher for safety

def generate_pi_digits():
    """Generate Pi digits if they don't exist"""
    if not os.path.exists('pi_digits.txt'):
        print("Generating Pi digits (this may take a moment)...")
        pi_str = str(mp.pi)[2:]  # Remove "3."
        with open('pi_digits.txt', 'w') as f:
            f.write(pi_str)
        return pi_str
    else:
        with open('pi_digits.txt', 'r') as f:
            return f.read().strip()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_high_score():
    try:
        with open('pi_high_score.json', 'r') as f:
            return json.load(f)['high_score']
    except:
        return 0

def save_high_score(score):
    with open('pi_high_score.json', 'w') as f:
        json.dump({'high_score': score}, f)

def draw_hangman(mistakes):
    stages = [
        """
           -----
           |   |
               |
               |
               |
               |
        """,
        """
           -----
           |   |
           O   |
               |
               |
               |
        """,
        """
           -----
           |   |
           O   |
           |   |
               |
               |
        """,
        """
           -----
           |   |
           O   |
          /|   |
               |
               |
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
               |
               |
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
          /    |
               |
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
          / \\  |
               |
        """
    ]
    return stages[mistakes]

def draw_game_screen(hangman, pi_digits, current_position, mistakes, max_mistakes, high_score):
    clear_screen()
    
    # Calculate the sliding window (show 40 digits, centered on current position)
    start_pos = max(0, current_position - 20)
    end_pos = start_pos + 40
    
    # Create display string showing only entered digits plus current position
    display_digits = ['_'] * (end_pos - start_pos)
    for i in range(start_pos, min(current_position, end_pos)):
        display_digits[i - start_pos] = pi_digits[i]
    
    # Add current position marker
    if current_position < end_pos:
        current_relative_pos = current_position - start_pos
        display_digits[current_relative_pos] = '■'
    
    print(hangman)
    print("\n3." + ''.join(display_digits))
    print(f"\nCurrent Score: {current_position} digits")
    print(f"High Score: {high_score} digits")
    print(f"Lives remaining: {max_mistakes - mistakes}")
    print("\nEnter next digit: ", end='', flush=True)

def play_pi_game():
    pi_digits = generate_pi_digits()
    current_position = 0
    mistakes = 0
    max_mistakes = 6
    high_score = load_high_score()
    max_digits = 1000000  # 1 million digits limit
    
    print("Welcome to the Pi Memorization Game!")
    print("Loading...")
    
    while mistakes < max_mistakes:
        if current_position >= max_digits:
            clear_screen()
            print("🎉 CONGRATULATIONS! 🎉")
            print(f"You've reached the maximum score of {max_digits} digits!")
            print(f"You are truly a Pi master!")
            break
            
        draw_game_screen(draw_hangman(mistakes), pi_digits, current_position, 
                        mistakes, max_mistakes, high_score)
        
        guess = input().strip()
        
        if not guess.isdigit() or len(guess) != 1:
            continue
            
        if guess == pi_digits[current_position]:
            current_position += 1
            if current_position > high_score:
                high_score = current_position
                save_high_score(high_score)
        else:
            mistakes += 1
            
        if mistakes >= max_mistakes:
            clear_screen()
            print(draw_hangman(mistakes))
            print(f"\nGame Over! Final score: {current_position} digits")
            print(f"High Score: {high_score} digits")
            print(f"\nThe next few digits were: {pi_digits[current_position:current_position+10]}...")
            break

def main():
    while True:
        play_pi_game()
        play_again = input("\nWould you like to play again? (y/n): ").lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
