'''
Wordle- Guess a five-letter secret word in at most six attempts.
'''
from __future__ import annotations
import random
# py -m pip install colorama
from colorama import Fore, Back, Style, init
init(autoreset=True) #Ends color formatting after each print statement
from wordle_wordlist import get_word_list
import time


def get_feedback(guess: str, secret_word: str) -> str:
    '''Generates a feedback string based on comparing a 5-letter guess with the secret word. 
       The feedback string uses the following schema: 
        - Correct letter, correct spot: uppercase letter ('A'-'Z')
        - Correct letter, wrong spot: lowercase letter ('a'-'z')
        - Letter not in the word: '-'

       For example:
        - get_feedback("lever", "EATEN") --> "-e-E-"
        - get_feedback("LEVER", "LOWER") --> "L--ER"
        - get_feedback("MOMMY", "MADAM") --> "M-m--"
        - get_feedback("ARGUE", "MOTTO") --> "-----"

        Args:
            guess (str): The guessed word
            secret_word (str): The secret word
        Returns:
            str: Feedback string, based on comparing guess with the secret word
    '''
    #edge cases
    guessUpper = guess.upper()
    guessList = list(guessUpper)
    secretList = list(secret_word)
    feedBack = []

    if len(guess)!=5 or guessUpper not in get_word_list():
        return 'This is an invalid word. Guess again!'
    else:
        for i in range(len(guessList)):
            if guessList[i] == secretList[i]:
                secretList[i] = '*'
                feedBack.append(guessList[i])
            else:
                feedBack.append("-")

        for i in range(len(guessList)):
            if feedBack[i] == "-":
                if guessList[i] in secretList:
                    if secretList[secretList.index(guessList[i])] == guessList[secretList.index(guessList[i])]:
                        feedBack[i] = "-"
                    else:
                        feedBack[i] = guessList[i].lower()
                        secretList[secretList.index(guessList[i])] = "*" 
                else:
                    feedBack[i] = "-"

    return ''.join(feedBack)

word_list_global = set(get_word_list().copy())
invalid_indexes = {'A':set(), 'B':set(), 'C':set(), 'D':set(), 'E':set(), 'F':set(), 'G':set(), 'H':set(), 'I':set(), 
                   'J':set(), 'K':set(), 'L':set(), 'M':set(), 'N':set(), 'O':set(), 'P':set(), 'Q':set(), 'R':set(), 
                   'S':set(), 'T':set(), 'U':set(), 'V':set(), 'W':set(), 'X':set(), 'Y':set(), 'Z':set()}
invalid_index_copy = invalid_indexes.copy()
scrabble_dict = {'A': 9, 'B': 2, 'C': 2, 'D': 4, 'E': 12, 'F': 2,
    'G': 3, 'H': 2, 'I': 9, 'J': 1, 'K': 1, 'L': 4, 'M': 2, 'N': 6,
    'O': 8, 'P': 2, 'Q': 1, 'R': 6, 'S': 4, 'T': 6, 'U': 4, 'V': 2,
    'W': 2, 'X': 1, 'Y': 2, 'Z': 1 }
confirmed_list = ['-','-','-','-','-']
valid_letters = set()
starting_word = 'REACT'
def get_AI_guess(word_list: list[str], guesses: list[str], feedback: list[str]) -> str:
    '''Analyzes feedback from previous guesses (if any) to make a new guess
        Args:
            word_list (list): A list of potential Wordle words
            guesses (list): A list of string guesses, could be empty
            feedback (list): A list of feedback strings, could be empty
        Returns:
         str: a valid guess that is exactly 5 uppercase letters
    '''
    global word_list_global, invalid_indexes, invalid_index_copy, scrabble_dict, confirmed_list, valid_letters
    deleted = set()
    max_score = 0
    final_word = ''
    
    if len(guesses) == 0: #first guess
        #reset global variables for each new secret word
        word_list_global = set(word_list)
        invalid_indexes = {'A':set(), 'B':set(), 'C':set(), 'D':set(), 'E':set(), 'F':set(), 'G':set(), 'H':set(), 'I':set(), 
                   'J':set(), 'K':set(), 'L':set(), 'M':set(), 'N':set(), 'O':set(), 'P':set(), 'Q':set(), 'R':set(), 
                   'S':set(), 'T':set(), 'U':set(), 'V':set(), 'W':set(), 'X':set(), 'Y':set(), 'Z':set()}
        confirmed_list = ['-', '-', '-', '-', '-']
        valid_letters = set()

        return starting_word
    elif len(guesses) >= 1: #second guess beyond
        for i in range(5):
            guess_char = guesses[-1][i]
            feedback_char = feedback[-1][i]
            if feedback_char == '-' and len(invalid_indexes[guess_char]) == 0 and guess_char not in confirmed_list and guess_char not in feedback[-1]: #update invalid_indexes with every index for letters not in word
                invalid_indexes[guess_char].update([0,1,2,3,4])
            elif ord(feedback_char) >= 65 and ord(feedback_char) <= 90: #if upper case, add to confirmed list
                confirmed_list[i] = feedback_char
                valid_letters.add(guess_char)
            else: #if lowercase, update invalid indexes
                if feedback_char != '-':
                    valid_letters.add(guess_char)
                invalid_indexes[guesses[-1][i]].add(i)
    '''
    print(f"valid letters: {valid_letters}")
    print(feedback[-1])
    print(invalid_indexes)
    print(confirmed_list)
    '''
    if feedback[0] == '-----' and len(guesses) == 1:
        return 'POUCH'
    
    for word in word_list_global:
        score = 0
        valid = True
        for index in range(len(word)):
            if (confirmed_list[index] != '-' and confirmed_list[index] != word[index]):
                deleted.add(word)
                break
            elif (index in invalid_indexes[word[index]]):
                deleted.add(word)
                break
            else:
                score += scrabble_dict[word[index]]        
        for c in valid_letters:
            if c not in word:
                deleted.add(word)
                valid = False
        if score > max_score and valid:
            max_score = score
            final_word = word

    word_list_global = word_list_global.difference(deleted)
    '''
    print(f"guess: {guesses[-1]}")
    print(f"deleted list: {deleted}")
    print(f"remaining word list: {word_list_global}")
    '''
    return final_word


def colorize_output(result:str, guess:str)->str:
    print(Back.LIGHTBLACK_EX + "  ", end="")
    for i in range(len(result)):
        if result[i] == '-':
            print(Fore.WHITE + Back.BLACK + guess[i], end='')
        elif ord(result[i]) >= 65 and ord(result[i]) <= 90:
            print(Fore.WHITE + Back.GREEN + guess[i], end='')
        else:
            print(Fore.WHITE + Back.YELLOW + guess[i], end='')
    print(Back.LIGHTBLACK_EX + "  ")
    #print()

# TODO: Define and implement your own functions!
def start_game():
    print("WELCOME TO WORDLE")
    num_guesses = 0
    secret_word = word_generator()
    winner = False
    guesses = []
    feedback = []
    while num_guesses < 6 and winner == False:
        guess = input("Please enter your guess: ")
        result = get_feedback(guess, secret_word)
        if result != 'This is an invalid word. Guess again!':
            guesses.append(guess.upper())
            num_guesses += 1
            feedback.append(result)
            print(Back.LIGHTBLACK_EX + "         ")
            for i in range(len(feedback)):
                colorize_output(feedback[i], guesses[i])
            print(Back.LIGHTBLACK_EX + "         ")
        else:
            print(result)
            
        if result == secret_word:
            winner = True
    if winner == False:
        print("YOU LOST THE GAME!!")
        print(f"The secret word was {secret_word}.")
    else:
        print(f"YOU WON THE GAME IN {num_guesses} GUESSES!")
    
    start_over = input("Do you want to play again? Y/N ")
    if start_over.upper() == 'Y':
        return start_game()
    else:
        print("THANKS FOR PLAYING!")
    

def word_generator():
    return get_word_list()[random.randint(0, len(get_word_list())-1)]




if __name__ == "__main__":
    print("WELCOME TO WORDLE!")
    print("Here are the game modes:")
    print("[1] Normal Wordle")
    print("[2] Starting Word Tester")
    print("[3] Observe AI Gameplay")
    print("[4] Manual Debug (for developers)")
    game_mode = input("What game mode would you like to play? ")
    while game_mode != '1' and game_mode != '2' and game_mode != '3' and game_mode != '4':
        print("Please enter a number from 1-3 to select your game mode")
        game_mode = input("What game mode would you like to play? ")
    
    if game_mode == '1': #normal wordle
        start_game()
    elif game_mode == '2': #starting word tester
        starting_word = input("Please select a 5-letter starting word: ").upper()
        while len(starting_word) != 5 or starting_word.upper() not in get_word_list():
            print(f'{starting_word} is an invalid word!')
            starting_word = input("Please select a 5-letter starting word: ").upper()
        
        total_guesses = 0
        max_guesses = 0
        min_guesses = len(get_word_list())
        for i in range(100):    
            for word in get_word_list():
                guess_count = 0
                #print(f"secret word: {word}")
                guesses = []
                feedback_list = []
                guessed = False
                AI_guess = ''
                while AI_guess != word:
                    AI_guess = get_AI_guess(get_word_list(), guesses, feedback_list)
                    guesses.append(AI_guess)
                    feedback_list.append(get_feedback(AI_guess, word))
                    guess_count += 1

                    if AI_guess == word:
                        if guess_count > max_guesses:
                            max_guesses = guess_count
                        elif guess_count < min_guesses:
                            min_guesses = guess_count
                        total_guesses += guess_count
                        break
            print(i)
        print(f"max guesses: {max_guesses}")
        print(f"min guesses: {min_guesses}")
        print(f"average guesses: {total_guesses / (len(get_word_list()*100))}")
    elif game_mode == 3: #watch AI play wordle
        guess_count = 0
        secret_word = word_generator()
        #secret_word = 'ABASE'
        print(f"secret word: {secret_word}")
        guesses = []
        feedback_list = []
        guessed = False

        while guess_count < 6:
            AI_guess = get_AI_guess(get_word_list(), guesses, feedback_list)
            guesses.append(AI_guess)
            feedback_list.append(get_feedback(AI_guess, secret_word))
            guess_count += 1

            print(feedback_list[-1])
            time.sleep(2)

            if AI_guess == secret_word:
                break
    else: #debug to test one word at a time
        secret_word = input("Please select a 5-letter secret word: ").upper()
        while len(secret_word) != 5 or secret_word.upper() not in get_word_list():
            print(f'{secret_word} is an invalid word!')
            secret_word = input("Please select a 5-letter secret word: ").upper()
        guess_count = 0
        print(f"secret word: {secret_word}")
        guesses = []
        feedback_list = []
        guessed = False

        while guess_count < 6:
            AI_guess = get_AI_guess(get_word_list(), guesses, feedback_list)
            guesses.append(AI_guess)
            feedback_list.append(get_feedback(AI_guess, secret_word))
            guess_count += 1

            if AI_guess == secret_word:
                break
        print(f"guess list: {guesses}")
        print(f"feedback list: {feedback_list}")