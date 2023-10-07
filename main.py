#!/usr/bin/python3
import string
import random            
import shutil  


def print_border():

    terminal_width = shutil.get_terminal_size().columns
    print("=" * terminal_width)


def print_centered_text(text, end="\n"):
    # Get the terminal width
    terminal_width = shutil.get_terminal_size().columns

    # Calculate the number of spaces needed to center the text
    padding = (terminal_width - len(text)) // 2

    # Print the centered text with padding
    return (" " * padding + text)


def print_heading():
    print_border()
    print(print_centered_text("Guess the Quote!"))    

def print_instructions():
    instructions = """
    You have to guess the quote!
    Each letter (A-Z) is mapped to a number (1-26)
    For the quote, some letters are given, but some are missing!
    For each round, you can guess one letter by choosing which word, and what letter position
    Eg., You want to guess 'E' for the 2nd Letter of 1st Word
    You will guess, Word: 1 Pos: 2 Guess: E
    If you answer correctly, the letter stays, otherwise, you lose a life!
    You have three lives!!
    Guess the quote with the given clues!
    """

    print_border()
    print(print_centered_text("How to Play?"))
    instructions = instructions.split("\n")
    for instruction in instructions:
        print(print_centered_text(instruction))
    print_border()


def generate_challenge():
    # Map english letters to random unique numbers from 1-26
    letters = list(string.ascii_uppercase)
    randomized_letters = random.sample(letters, 26)

    quotes = [
        "Live with purpose and passion",
        "Dream big, work hard, succeed",
        "Love deeply, laugh often, live",
        "Chase dreams, catch stars, shine",
        "Create, inspire, make a difference",
        "Stay curious, keep exploring life",
        "Believe in yourself, achieve greatness",
        "Find joy in life's journey",
        "Kindness matters, spread love daily",
        "Embrace challenges, grow stronger always",
        "Live fully, love freely, smile"
    ]
    quote = random.sample(quotes, 1)[0].upper()

    duplicate_chars = list(set([char for char in quote if quote.count(char) > 1 and char in string.ascii_uppercase]))

    # Challenge Quote Construction
    challenge_quote = list(quote)

    quote_len = len(quote)
    random_sequence = random.sample(list(range(quote_len)), quote_len)


    for index in random_sequence:

        char = quote[index]
        
        if char == " ":
            continue

        if char == "," or char == "'":
            continue

        if char not in duplicate_chars:
            challenge_quote[index] = '_'
        else:
            duplicate_chars.remove(char)
    
    return quote, challenge_quote, randomized_letters



def print_hint(quote, challenge_quote, randomized_letters):
    
    number_sequence = ""
    for index in range(len(quote)):
        original_char = quote[index]
        hidden_char = challenge_quote[index]

        if hidden_char == " ":
            number_sequence += "   "
        
        elif hidden_char == "," or hidden_char == "'":
            number_sequence += "   "
        
        else:
            number_sequence += (" %02d" % (randomized_letters.index(original_char)+1))
        
    print(print_centered_text(number_sequence))


def guess(quote, challenge_quote):
    
    words = quote.split()

    print(print_centered_text("Guess your letter!"))
    print() 

    try:
        word = int(input(print_centered_text(f"Word Number (1 - {len(words)}): ")))
    
    
        if word < 1 or word > len(words):
            print(print_centered_text("Invalid Input! Game Over!!!"))
            exit()
    except ValueError:
        print(print_centered_text("Invalid Input! Game Over!!!"))
        exit()

    try:   
        pos = int(input(print_centered_text(f"Letter Position within the word (1 - {len(words[word-1])}): ")))
        if pos < 1 or pos > len(words[word-1]):
            print(print_centered_text("Invalid Input! Game Over!!!"))
            exit()
    except ValueError:
        print(print_centered_text("Invalid Input! Game Over!!!"))
        exit()
    
    guess = input(print_centered_text("Guess the letter (A-Z): ")).upper()

    if guess not in string.ascii_uppercase:
        print(print_centered_text("Invalid Input! Game Over!!!"))
        exit()

    chall_pos = 0
    chall_word_pos = 1

    for index in range(len(challenge_quote)):
        if word == chall_word_pos:
            chall_pos += pos
            break
        elif challenge_quote[index] == " ":
            chall_word_pos += 1
        chall_pos += 1
    
    if challenge_quote[chall_pos-1] != '_':
        print(print_centered_text("You can only guess hidden letters! One Life Lost!!"))
        return -1

    actual = words[word-1][pos-1]
    if guess != actual:
        print(print_centered_text("Wrong Answer! One Life Lost!!"))
        return -1
    
    else:
        challenge_quote[chall_pos-1] = guess
        print(print_centered_text("Correct Answer!"))
        return 0    


def check_game_over(quote, challenge_quote, lives):

    if lives == 0:
        print(print_centered_text("No Life Remaining! Game Over!!!"))
        print(print_centered_text("The quote was: " + quote))
        exit()

    if quote == ''.join(challenge_quote):
        print(print_centered_text("You Win!!!!"))
        print(print_centered_text("The quote is: " + quote))
        exit()    



if __name__ == "__main__":

    # Print the heading
    print_heading()

    # Print hints
    print_instructions()

    # Generate Challenge
    qt, chl_qt, randm_lttrs = generate_challenge()
    

    # Run the game
    round  = 1
    lives = 3

    while qt != chl_qt:

        print(print_centered_text(f"Round {round}: Remaining Lives: {lives}"))
        print_border()

        print(print_centered_text('  '.join(chl_qt)))
        print_hint(qt, chl_qt, randm_lttrs)

        print_border()

        lives += guess(qt, chl_qt)

        check_game_over(qt, chl_qt, lives)

        round += 1

        print_border()





