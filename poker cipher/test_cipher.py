import unittest
from cipher_functions import *

class Testclean_mesage(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(clean_message(""),"")
    def test_lowercase(self):
        self.assertEqual(clean_message("a?@ #3gp"),"AGP")
    def test_mixed(self):
        self.assertEqual(clean_message("ijdQ)@als AIwrqr*$("),"IJDQALSAIWRQR")

class Testencrypt_letter(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(encrypt_letter("L", 12),"X")
    def test_overflow(self):
        self.assertEqual(encrypt_letter("E",25), "D")
        
class Testdecrypt_letter(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(decrypt_letter("X", 12),"L")
    def test_overflow(self):
        self.assertEqual(decrypt_letter("D",25), "E")

class Testswap_cards(unittest.TestCase):
    def test_basic(self):
        deck = [1,2,3,4,5,6,7,8,9]
        expected = [1,2,3,4,5,7,6,8,9]
        swap_cards(deck,5)
        self.assertEqual(deck,expected)
    def test_last_element(self):
        deck = [1,2,3,4,5,6,7,8,9]
        expected = [9,2,3,4,5,6,7,8,1]
        swap_cards(deck,8)        
        self.assertEqual(deck,expected)

class testmove_joker_1(unittest.TestCase):
    def test_basic(self):
        deck = [1,2,3,4,5,JOKER1,6,7,8,9]
        expected = [1,2,3,4,5,6,JOKER1,7,8,9]
        move_joker_1(deck)
        self.assertEqual(deck,expected)
    def test_last_element(self):
        deck = [1,2,3,4,5,6,7,8,9,JOKER1]
        expected = [JOKER1,2,3,4,5,6,7,8,9,1]
        move_joker_1(deck)        
        self.assertEqual(deck,expected)    

class testmove_joker_2(unittest.TestCase):
    def test_basic(self):
        deck = [1,2,3,4,5,JOKER2,6,7,8,9]
        expected = [1,2,3,4,5,6,7,JOKER2,8,9]
        move_joker_2(deck)
        self.assertEqual(deck,expected)
    def test_second_last_element(self):
        deck = [1,2,3,4,5,6,7,8,9,JOKER2,10]
        expected = [JOKER2,2,3,4,5,6,7,8,9,10,1]
        move_joker_2(deck)        
        self.assertEqual(deck,expected)         
    def test_last_element(self):
        deck = [1,2,3,4,5,6,7,8,9,JOKER2]
        expected = [2,JOKER2,3,4,5,6,7,8,9,1]
        move_joker_2(deck)
        self.assertEqual(deck,expected)
        
class testtriple_cut(unittest.TestCase): 
    def test_joker1first(self):
        deck = [1, 4, 7, 10, 13, 16, 19, 22, 25, 3, 6, 27, 9, 12, 15, 18, 21, 24, 2, 28, 5, 8, 11, 14, 17, 20, 23, 26]
        expected = [5, 8, 11, 14, 17, 20, 23, 26, 27, 9, 12, 15, 18, 21, 24, 2, 28, 1, 4, 7, 10, 13, 16, 19, 22, 25, 3, 6]
        triple_cut(deck)
        self.assertEqual(deck,expected)    
    def test_joker2first(self):
        deck = [1, 4, 7, 10, 13, 16, 19, 22, 25, 3, 6, 28, 9, 12, 15, 18, 21, 24, 2, 27, 5, 8, 11, 14, 17, 20, 23, 26]
        expected = [5, 8, 11, 14, 17, 20, 23, 26, 28, 9, 12, 15, 18, 21, 24, 2, 27, 1, 4, 7, 10, 13, 16, 19, 22, 25, 3, 6]
        triple_cut(deck)
        self.assertEqual(deck,expected)
    def test_sidebyside(self):
        deck = [1, 4, 7, 10, 13, 16, 19, 22, 25, 3, 6, 28, 27, 5, 8, 11, 14, 17, 20, 23, 26]
        expected = [5, 8, 11, 14, 17, 20, 23, 26, 28, 27, 1, 4, 7, 10, 13, 16, 19, 22, 25, 3, 6]
        triple_cut(deck)
        self.assertEqual(deck,expected)        
class testinsert_top_to_bottom(unittest.TestCase): 
    def test_basic(self):
        deck = [5, 8, 11, 14, 17, 20, 23, 26, 28, 9, 12, 15, 18, 21, 24, 2, 27, 1, 4, 7, 10, 13, 16, 19, 22, 25, 3, 6]
        expected = [23, 26, 28, 9, 12, 15, 18, 21, 24, 2, 27, 1, 4, 7, 10, 13, 16, 19, 22, 25, 3, 5, 8, 11, 14, 17, 20, 6]
        insert_top_to_bottom(deck)
        self.assertEqual(deck,expected)
    def test_joker2_end(self):
        deck = [5, 8, 11, 14, 17, 20, 23, 26, 6, 9, 12, 15, 18, 21, 24, 2, 27, 1, 4, 7, 10, 13, 16, 19, 22, 25, 3, 28]
        expected = [5, 8, 11, 14, 17, 20, 23, 26, 6, 9, 12, 15, 18, 21, 24, 2, 27, 1, 4, 7, 10, 13, 16, 19, 22, 25, 3, 28]
        insert_top_to_bottom(deck)
        self.assertEqual(deck,expected)
        
class testget_card_at_top_index(unittest.TestCase):
    def test_basic(self):
        deck = [23, 26, 28, 9, 12, 15, 18, 21, 24, 2, 27, 1, 4, 7, 10, 13, 16, 19, 22, 25, 3, 5, 8, 11, 14, 17, 20, 6]
        result = get_card_at_top_index(deck)
        self.assertEqual(result,11)
    def test_joker2head(self):
        deck = [28, 26, 23, 9, 12, 15, 18, 21, 24, 2, 27, 1, 4, 7, 10, 13, 16, 19, 22, 25, 3, 5, 8, 11, 14, 17, 20, 6]
        result = get_card_at_top_index(deck)
        self.assertEqual(result,6)
    
if __name__ == '__main__':
    unittest.main(exit=False) 
    