# Functions for running an encryption or decryption.

# The values of the two jokers.
JOKER1 = 27
JOKER2 = 28


# Write your functions here:
def clean_message(message):
    '''(str) -> str
    Return a copy of the message that includes only its alphabetical characters
    ,where each of those characters has been converted to uppercase.
    >>> clean_message("")
    ''
    >>> clean_message("A?@ #3gp")
    'AGP'''
    # Initialize the variable result.
    result = ""
    # If the character in message is alphabetical then add its upper case to
    # result
    for ch in message:
        if ch.isalpha():
            result += ch.upper()
    return result


def encrypt_letter(up_ch, key_stream):
    '''(str, int) -> str
    Apply the keystream value to the character to encrypt the character, and
    return the result.'''
    # Assume the input char is capitalize letter only
    # The ASCII value of A-Z is 65 - 90
    encrypt = ord(up_ch) - 65 + key_stream
    return chr((encrypt % 26) + 65)


def decrypt_letter(up_ch, key_stream):
    '''(str, int) -> str
    Apply the keystream value to the character to decrypt the character, and
    return the result.'''
    # Assume the input char is capitalize
    # The ASCII value of A-Z is 65 - 90
    decrypt = ord(up_ch) - 65 - key_stream
    return chr((decrypt % 26) + 65)


def swap_cards(deck, index):
    '''(list of int, int) -> NoneType
    Swap the card at the index with the card that follows it.Treat the deck as
    circular: if the card at the index is on the bottom of the deck, swap that
    card with the top card.'''
    # (Note that in this and all functions that do something to the deck, the
    # function doesn't return anything. The deck is to be mutated.)
    # Handle the situation where the index is on the bottom of the deck
    if index == len(deck)-1:
        index = -1
    # Swap
    temp = deck[index]
    deck[index] = deck[index+1]
    deck[index+1] = temp


def move_joker_1(deck):
    '''(list of int) -> NoneType
    Find JOKER1 and swap it with the card that follows it. Treat the deck as
    circular.'''
    # Assuming only one JOKER1 in the input deck
    # Find the location of JOKER1
    location = deck.index(JOKER1)
    # Swap
    swap_cards(deck, location)


def move_joker_2(deck):
    '''(list of int) -> NoneType
    Find JOKER2 and move it two cards down. Treat the deck as circular.'''
    # Assuming only one JOKER2 in the input deck
    # Find the location of JOKER2
    location = deck.index(JOKER2)
    if location == len(deck)-1:
        location = -1
    # Swap
    swap_cards(deck, location)
    swap_cards(deck, location + 1)


def triple_cut(deck):
    '''(list of int) -> NoneType
    This is step 3 of the algorithm. Find the two jokers and do a triple
    cut.'''
    # Find the location of JOKER1 and JOKER2
    index_J1 = deck.index(JOKER1)
    index_J2 = deck.index(JOKER2)
    # Find the first Joker
    if index_J1 > index_J2:
        start = index_J2
        end = index_J1 + 1
    else:
        start = index_J1
        end = index_J2 + 1
    # Perform triple cut
    deck[:] = deck[end:] + deck[start:end] + deck[:start]


def insert_top_to_bottom(deck):
    '''(list of int) -> NoneType
    This is step 4 of the algorithm. Look at the bottom card of the deck; move
    that many cards from the top of the deck to the bottom, inserting them just
    above the bottom card. Special case: if the bottom card is JOKER2, use
    JOKER1 as the number of cards.'''
    # Get the amount of cards moving
    move = deck[-1]
    # If the bottom card is joker2, use joker1 as the number of cards
    if move == JOKER2:
        move = JOKER1
    # Insert the first n cards in front of the bottom card where n is the value
    # of the bottom card
    deck[:] = deck[move:-1] + deck[:move] + [deck[-1]]


def get_card_at_top_index(deck):
    '''(list of int) -> int
    This is step 5 of the algorithm. Look at the top card. Using that value as
    an index, return the card in that deck at that index. Special case: if the
    top card is JOKER2, use JOKER1 as the index.'''
    # Find the top card
    index = deck[0]
    # Change to JOKER1 if the top card is JOKER2
    if index == JOKER2:
        index = JOKER1
    return deck[index]


def get_next_value(deck):
    '''(list of int) -> int
    This is the function that does all five steps of the algorithm. Return the
    next potential keystream value'''
    # Performs all five steps
    move_joker_1(deck)
    move_joker_2(deck)
    triple_cut(deck)
    insert_top_to_bottom(deck)
    return get_card_at_top_index(deck)


def get_next_keystream_value(deck):
    '''(list of int) -> int
    This is the function that repeats all five steps of the algorithm (call
    get_next_value to get potential keystream values!) until a valid keystream
    value (a number in the range 1-26) is produced.'''
    result = JOKER1
    # Find a value between 1-26 or else keep looking
    while result == JOKER1 or result == JOKER2:
        result = get_next_value(deck)
    return result


def process_message(deck, msg, mode):
    '''(list of int, str, str) -> str
    The first parameter represents a deck of cards. The second represents a
    message to encrypt or decrypt based on the third parameter, which is either
    'e' (to encrypt) or 'd' (to decrypt). Return the encrypted or decrypted
    message. Note that the message might contain non-letters.'''
    # Get the clean message
    message = clean_message(msg)
    result = ""
    # Encrypt/decrypt the letter depening on mode with key stream value
    for i in range(len(message)):
        key_stream = get_next_keystream_value(deck)
        if mode == "e":
            result += encrypt_letter(message[i], key_stream)
        if mode == "d":
            result += decrypt_letter(message[i], key_stream)
    return result


def process_messages(deck, msgs, mode):
    '''(list of int, list of str, str) -> str
    The first parameter represents a deck of cards. The second represents a
    message to encrypt or decrypt based on the third parameter, which is
    either 'e' (to encrypt) or 'd' (to decrypt). Return the encrypted or
    decrypted message. Note that the message might contain non-letters.'''
    result = ""
    # Use process message to process each message in the list
    for element in msgs:
        result += process_message(deck, element, mode)
    return result


def read_messages(file):
    '''(file open for reading) -> list of str
    Read and return the contents of the file as a list of messages. Strip the
    newline from each line.'''
    # Note: you don't have to provide example calls for functions that read
    # files.
    # Remove the \n newline charater while reading.
    msgs = file.readlines()
    content = []
    for msg in msgs:
        content.append(msg.replace("\n", ""))
    file.close()
    return content


def read_deck(file):
    '''(file open for reading) -> list of int
    The parameter represents an open deck file, which contains the numbers 1
    through 28 in some order. Read and return the contents of the file. Do
    not hard-code the number 28 anywhere; just read all of the integers
    from the deck file.'''
    # Note: you don't have to provide example calls for functions that read
    # files.
    # Get the string of the deck
    content = read_messages(file)
    # Process the string into numbers
    deck = []
    for element in content:
        for num in element.split(" "):
            if num.isdigit():
                deck.append(int(num))
    return deck
