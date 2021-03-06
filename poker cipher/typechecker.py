'''This module should be used to test the parameter and return types of your
functions. Before submitting your assignment, run this type-checker. This
typechecker expects to find files cipher_functions.py, secret1.txt, and
deck1.txt.

If errors occur when you run this typechecker, fix them before you submit
your assignment.

If no errors occur when you run this typechecker, then the type checks passed.
This means that the function parameters and return types match the assignment
specification, but it does not mean that your code works correctly in all
situations. Be sure to test your code before submitting.
'''

import cipher_functions

sample_deck = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 3, 6, 9, 12, 15,
               18, 21, 24, 27, 2, 5, 8, 11, 14, 17, 20, 23, 26]

# typecheck the cipher_functions.py functions

# Type check cipher_functions.clean_message
result = cipher_functions.clean_message('abc')
assert isinstance(result, str), \
    '''clean_message should return a str, but returned {0}''' \
    .format(type(result))


# Type check cipher_functions.swap_cards
result = cipher_functions.swap_cards(sample_deck, 1)
assert result is None, \
    '''swap_cards should return None, but returned {0}''' \
    .format(type(result))


# Type check cipher_functions.move_joker_1
result = cipher_functions.move_joker_1(sample_deck)
assert result is None, \
    '''move_joker_1 should return None, but returned {0}''' \
    .format(type(result))


# Type check cipher_functions.move_joker_2
result = cipher_functions.move_joker_2(sample_deck)
assert result is None, \
    '''move_joker_2 should return None, but returned {0}''' \
    .format(type(result))


# Type check cipher_functions.triple_cut
result = cipher_functions.triple_cut(sample_deck)
assert result is None, \
    '''triple_cut should return None, but returned {0}''' \
    .format(type(result))


# Type check cipher_functions.insert_top_to_bottom
result = cipher_functions.insert_top_to_bottom(sample_deck)
assert result is None, \
    '''insert_top_to_bottom should return None, but returned {0}''' \
    .format(type(result))


# Type check cipher_functions.get_card_at_top_index
result = cipher_functions.get_card_at_top_index(sample_deck)
assert isinstance(result, int), \
    '''get_card_at_top_index should return an int, but returned {0}''' \
    .format(type(result))


# Type check cipher_functions.get_next_value
result = cipher_functions.get_next_value(sample_deck)
assert isinstance(result, int), \
    '''get_next_value should return an int, but returned {0}''' \
    .format(type(result))


# Type check cipher_functions.get_next_keystream_value
result = cipher_functions.get_next_keystream_value(sample_deck)
assert isinstance(result, int), \
    '''get_next_keystream_value should return an int, but returned {0}''' \
    .format(type(result))


# Type check cipher_functions.encrypt_letter
result = cipher_functions.encrypt_letter('A', 1)
assert isinstance(result, str) and len(result) == 1, \
    '''encrypt_letter should return a single character, but returned {0}''' \
    .format(type(result))


# Type check cipher_functions.decrypt_letter
result = cipher_functions.decrypt_letter('B', 1)
assert isinstance(result, str) and len(result) == 1, \
    '''decrypt_letter should return a single character, but returned {0}''' \
    .format(type(result))


# Type check cipher_functions.process_message
result = cipher_functions.process_message(sample_deck, 'ABC', 'e')
assert isinstance(result, str), \
    '''process_message should return a string, but returned {0}''' \
    .format(type(result))


# Type check cipher_functions.process_messages
result = cipher_functions.process_messages(sample_deck, ['A', 'B', 'C'], 'd')
assert isinstance(result, list), \
    '''process_messages should return a list, but returned {0}''' \
    .format(type(result))


# Type check cipher_functions.read_deck
result = cipher_functions.read_deck(open('deck1.txt'))
assert isinstance(result, list), \
    '''read_deck should return a list, but returned {0}''' \
    .format(type(result))


# Type check cipher_functions.read_messages
result = cipher_functions.read_messages(open('secret1.txt'))
assert isinstance(result, list), \
    '''read_messages should return a list, but returned {0}''' \
    .format(type(result))


# main is not typechecked because it acquires user-input
# It takes no parameters and returns None
