"""
Encrypt or decrypt the contents of a message file using a deck of cards.
"""

import cipher_functions

DECK_FILENAME = 'deck1.txt'
MSG_FILENAME = 'message1.txt'
MODE = 'e'  # 'e' for encryption, 'd' for decryption.


def main():
    """ () -> NoneType

    Perform the encryption using the deck from a file called DECK_FILENAME and
    the messages from a file called MSG_FILENAME. If MODE is 'e', encrypt;
    otherwise, decrypt.
    """
    #####################################################################
    ##
    ##Test1 Encrypt
    ##
    #####################################################################
    d_file = open(DECK_FILENAME, 'r')
    m_file = open(MSG_FILENAME, 'r')
    deck = cipher_functions.read_deck(d_file)
    msg = cipher_functions.read_messages(m_file)
    result = ""
    result += cipher_functions.process_messages(deck, msg, MODE)
    print (result)
    #####################################################################
    ##
    ##Test2 decrypt
    ##
    #####################################################################
    d_file = open(DECK_FILENAME, 'r')
    deck = cipher_functions.read_deck(d_file)
    s_file = open("secret1.txt", 'r')
    s_msg = cipher_functions.read_messages(s_file)
    result = cipher_functions.process_message(deck, s_msg, 'd')
    print (result)
    #####################################################################
    ##
    ##Test3 decrypt
    ##
    #####################################################################
    d_file = open(DECK_FILENAME, 'r')
    deck = cipher_functions.read_deck(d_file)
    s_file = open("secret2.txt", 'r')
    s_msg = cipher_functions.read_messages(s_file)
    result = cipher_functions.process_messages(deck, s_msg, 'd')
    print (result)    
    ####################################################################
    #
    #Test4 decrypt
    #
    ####################################################################
    d_file = open(DECK_FILENAME, 'r')
    deck = cipher_functions.read_deck(d_file)
    s_file = open("secret3.txt", 'r')
    s_msg = cipher_functions.read_messages(s_file)
    result = cipher_functions.process_messages(deck, s_msg, 'd')
    print (result)    
    #####################################################################
    ##
    ##Test5 decrypt
    ##
    #####################################################################
    d_file = open(DECK_FILENAME, 'r')
    deck = cipher_functions.read_deck(d_file)
    s_file = open("secret4.txt", 'r')
    s_msg = cipher_functions.read_messages(s_file)
    result = cipher_functions.process_messages(deck, s_msg, 'd')
    print (result)    
    #####################################################################
    ##
    ##Test6 decrypt
    ##
    #####################################################################
    d_file = open(DECK_FILENAME, 'r')
    deck = cipher_functions.read_deck(d_file)
    s_file = open("secret5.txt", 'r')
    s_msg = cipher_functions.read_messages(s_file)
    result = cipher_functions.process_messages(deck, s_msg, 'd')
    print (result)    
    #####################################################################
    ##
    ##Test7 decrypt
    ##
    #####################################################################  
    d_file = open(DECK_FILENAME, 'r')
    deck = cipher_functions.read_deck(d_file)
    s_file = open("secret6.txt", 'r')
    s_msg = cipher_functions.read_messages(s_file)
    result = cipher_functions.process_message(deck, s_msg, 'd')
    print (result)
    #####################################################################
    ##
    ##Test8 decrypt
    ##
    ####################################################################  
    d_file = open(DECK_FILENAME, 'r')
    deck = cipher_functions.read_deck(d_file)
    s_file = open("secret7.txt", 'r')
    s_msg = cipher_functions.read_messages(s_file)
    result = cipher_functions.process_message(deck, s_msg, 'd')
    print (result)          
    
main()