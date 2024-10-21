import random
from colors import Colors
from match import Match
from status import Status
from collections import Counter

TOTAL_COLORS = 6
MAX_ATTEMPTS = 20

def guess(selected_colors, user_provided_colors):
    def match_for_position(position):
        candidate_color = user_provided_colors[position]
        if candidate_color == selected_colors[position]:
            return Match.EXACT
        if candidate_color in user_provided_colors[0:position]:
            return Match.NO_MATCH
        index = selected_colors.index(candidate_color) if candidate_color in selected_colors else -1
        if index > -1 and selected_colors[index] != user_provided_colors[index]:
            return Match.PARTIAL
        return Match.NO_MATCH 
    
    return {**{Match.EXACT: 0, Match.PARTIAL: 0, Match.NO_MATCH: 0}, **Counter(map(match_for_position, range(6)))}

def play(selected_colors, user_provided_colors, number_of_attempts):
    if number_of_attempts > 20:
        raise ValueError()
    
    response = guess(selected_colors, user_provided_colors)

    status = Status.IN_PROGRESS
    if number_of_attempts == MAX_ATTEMPTS:
        status = Status.LOST
    if response[Match.EXACT] == TOTAL_COLORS:
        status = Status.WON
    
    number_of_attempts += 1
    return response, number_of_attempts, status

def select_colors(seed): 
    random.seed(seed)
    return random.sample(list(Colors), TOTAL_COLORS)
