import sys
import os
import unittest
import random
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from colors import Colors
from match import Match
from status import Status
from master_mind import play, guess, select_colors, Colors

EXACT = Match.EXACT
PARTIAL = Match.PARTIAL
NO_MATCH = Match.NO_MATCH

WON = Status.WON
IN_PROGRESS = Status.IN_PROGRESS
LOST = Status.LOST

class MasterMindTests(unittest.TestCase):

    def test_canary(self):
        self.assertTrue(True)

    def test_guess_with_all_colors_match_in_position(self):
        selected_colors = [Colors.RED, Colors.ORANGE, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE]
        user_provided_colors = selected_colors
        
        response = guess(selected_colors, user_provided_colors)

        self.assertEqual(response[EXACT], 6)
    
    def test_guess_all_colors_mismatch(self):
        selected_colors = [Colors.RED, Colors.ORANGE, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE]
        user_provided_colors = [Colors.PINK, Colors.PURPLE, Colors.BROWN, Colors.MAGENTA, Colors.PINK, Colors.PURPLE]
        
        response = guess(selected_colors, user_provided_colors)

        self.assertEqual(response[NO_MATCH], 6)

    def test_guess_all_colors_match_out_of_position(self):
        selected_colors = [Colors.RED, Colors.ORANGE, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE]
        user_provided_colors = [Colors.ORANGE, Colors.RED, Colors.GREEN, Colors.YELLOW, Colors.BLUE, Colors.CYAN]
        
        response = guess(selected_colors, user_provided_colors)

        self.assertEqual(response[PARTIAL], 6)

    def test_guess_first_four_colors_match_in_position(self):
        selected_colors = [Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.RED, Colors.ORANGE]
        user_provided_colors = [Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.PINK, Colors.PURPLE]

        response = guess(selected_colors, user_provided_colors)
        
        self.assertEqual(response, {EXACT: 4, PARTIAL: 0, NO_MATCH: 2})
    
    def test_guess_last_four_colors_match_in_position(self):
        selected_colors = [Colors.RED, Colors.ORANGE, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE]
        user_provided_colors = [Colors.PINK, Colors.PURPLE, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE]
        
        response = guess(selected_colors, user_provided_colors)

        self.assertEqual(response, {EXACT: 4, PARTIAL: 0, NO_MATCH: 2})

    def test_guess_first_three_in_position_last_three_out_of_position(self):
        selected_colors = [Colors.RED, Colors.ORANGE, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE]
        user_provided_colors = [Colors.RED, Colors.ORANGE, Colors.YELLOW, Colors.BLUE, Colors.GREEN, Colors.CYAN]
        
        response = guess(selected_colors, user_provided_colors)

        self.assertEqual(response, {EXACT: 3, PARTIAL: 3, NO_MATCH: 0})
    
    def test_guess_first_and_third_mismatch_second_in_position(self):
        selected_colors = [Colors.RED, Colors.ORANGE, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE]
        user_provided_colors = [Colors.PINK, Colors.ORANGE, Colors.BROWN, Colors.BLUE, Colors.GREEN, Colors.CYAN]
        
        response = guess(selected_colors, user_provided_colors)

        self.assertEqual(response, {EXACT: 1, PARTIAL: 3, NO_MATCH: 2})

    def test_guess_with_first_color_repeated_five_times(self):
        selected_colors = [Colors.RED, Colors.ORANGE, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE]
        user_provided_colors = [Colors.RED] * 5 + [Colors.BLUE]
        
        response = guess(selected_colors, user_provided_colors)

        self.assertEqual(response, {EXACT: 2, PARTIAL: 0, NO_MATCH: 4})

    def test_guess_with_last_color_repeated(self):
        selected_colors = [Colors.RED, Colors.ORANGE, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE]
        user_provided_colors = [Colors.BLUE] * 6
        
        response = guess(selected_colors, user_provided_colors)

        self.assertEqual(response, {EXACT: 1, PARTIAL: 0, NO_MATCH: 5})

    def test_guess_with_first_color_repeated_from_position_two_to_six(self):
        selected_colors = [Colors.RED, Colors.ORANGE, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE]
        user_provided_colors = [Colors.ORANGE] + [Colors.RED] * 5
        
        response = guess(selected_colors, user_provided_colors)

        self.assertEqual(response, {EXACT: 0, PARTIAL: 2, NO_MATCH: 4})

    def test_guess_with_first_color_repeated_from_position_two_to_six_first_position_no_match(self):
        selected_colors = [Colors.RED, Colors.ORANGE, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE]
        user_provided_colors = [Colors.PINK] + [Colors.RED] * 5
        
        response = guess(selected_colors, user_provided_colors)

        self.assertEqual(response, {EXACT: 0, PARTIAL: 1, NO_MATCH: 5})

    def test_play_with__first_attempt_exact_match(self):
        selected_colors = [Colors.RED, Colors.ORANGE, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE]
        user_provided_colors = selected_colors

        response, attempts, status = play(selected_colors, user_provided_colors, 1)

        self.assertEqual(response, {EXACT: 6, PARTIAL: 0, NO_MATCH: 0})
        self.assertEqual(attempts, 2) 
        self.assertEqual(status, WON) 

    def test_play_with_first_attempt_no_match(self):
        selected_colors = [Colors.RED, Colors.ORANGE, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE]
        user_provided_colors = [Colors.PINK, Colors.PURPLE, Colors.BROWN, Colors.MAGENTA, Colors.PINK, Colors.PURPLE]

        response, attempts, status = play(selected_colors, user_provided_colors, 1)

        self.assertEqual(response, {EXACT: 0, PARTIAL: 0, NO_MATCH: 6})
        self.assertEqual(attempts, 2) 
        self.assertEqual(status, IN_PROGRESS)

    def test_play_with_first_attempt_some_exact_some_non_exact_match(self):
        selected_colors = [Colors.RED, Colors.ORANGE, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE]
        user_provided_colors = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.ORANGE, Colors.CYAN, Colors.BLUE]

        response, attempts, status = play(selected_colors, user_provided_colors, 1)
        
        self.assertEqual(response, {EXACT: 3, PARTIAL: 3, NO_MATCH: 0})
        self.assertEqual(attempts, 2)
        self.assertEqual(status, IN_PROGRESS)

    def test_play_with_second_attempt_exact_match(self):
        selected_colors = [Colors.RED, Colors.ORANGE, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE]
        user_provided_colors = selected_colors

        response, attempts, status = play(selected_colors, user_provided_colors, 2)
        
        self.assertEqual(response, {EXACT: 6, PARTIAL: 0, NO_MATCH: 0})
        self.assertEqual(attempts, 3) 
        self.assertEqual(status, WON)

    def test_play_with_second_attempt_no_match(self):
        selected_colors = [Colors.RED, Colors.ORANGE, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE]
        user_provided_colors = [Colors.PINK, Colors.PURPLE, Colors.BROWN, Colors.MAGENTA, Colors.PINK, Colors.PURPLE]

        response, attempts, status = play(selected_colors, user_provided_colors, 2)
        
        self.assertEqual(response, {EXACT: 0, PARTIAL: 0, NO_MATCH: 6})
        self.assertEqual(attempts, 3)
        self.assertEqual(status, IN_PROGRESS)

    def test_play_with_twentieth_attempt_exact_match(self):
        selected_colors = [Colors.RED, Colors.ORANGE, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE]
        user_provided_colors = selected_colors

        response, attempts, status = play(selected_colors, user_provided_colors, 20)
        
        self.assertEqual(response, {EXACT: 6, PARTIAL: 0, NO_MATCH: 0})
        self.assertEqual(attempts, 21) 
        self.assertEqual(status, WON)

    def test_play_with_twentieth_attempt_no_match(self):
        selected_colors = [Colors.RED, Colors.ORANGE, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE]
        user_provided_colors = [Colors.PINK, Colors.PURPLE, Colors.BROWN, Colors.MAGENTA, Colors.PINK, Colors.PURPLE]

        response, attempts, status = play(selected_colors, user_provided_colors, 20)
        
        self.assertEqual(response, {EXACT: 0, PARTIAL: 0, NO_MATCH: 6})
        self.assertEqual(attempts, 21) 
        self.assertEqual(status, LOST)

    def test_play_with_twentyone_attempt_exact_match(self):
        selected_colors = [Colors.RED, Colors.ORANGE, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE]
        user_provided_colors = selected_colors

        self.assertRaises(ValueError, play, selected_colors, user_provided_colors, 21)

    def test_play_with_twentyone_attempt_no_match(self):
        selected_colors = [Colors.RED, Colors.ORANGE, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE]
        user_provided_colors = [Colors.PINK, Colors.PURPLE, Colors.BROWN, Colors.MAGENTA, Colors.PINK, Colors.PURPLE]

        self.assertRaises(ValueError, play, selected_colors, user_provided_colors, 21)

    def test_randomized_selected_colors_given(self):
        selected_colors = select_colors(seed=42)

        self.assertEqual(len(selected_colors), 6)  
        self.assertTrue(set(selected_colors).issubset(Colors))  

    def test_randomized_selected_colors_different_when_called_twice(self):
        selection_1 = select_colors(seed=42)
        selection_2 = select_colors(seed=43)
        
        self.assertNotEqual(selection_1, selection_2) 

if __name__ == '__main__':
    unittest.main()
