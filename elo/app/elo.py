import TrueSkill as ts

ts.setup(mu=100.0, sigma=33.333, beta=16.667, tau=0.33333, draw_probability=0)

class Game(object):

    def __init__(self, game_type, players):
        self.game_type = game_type
        self.players = players


class Game_1v1(Game):

    def __init__(self, winner, loser):
        Game.__init__(self, '1v1', players)
        self.winner = winner
        self.loser = loser

    def verify_players(self, players):
        for player in [self.winner, self.loser]:
            if player not in self.players.keys():
                self.players[player] = ts.Rating()
        return

    def play_game(self):
        self.verify_players(self.players)
        self.players[winner], self.players[loser] = ts.rate_1vs1(winner, loser)
        return


class Game_2v2(Game):

    def __init__(self, winner1, winner2, loser1, loser2):
        Game.__init__(self, '2v2', players)
        self.winner1 = winner1
        self.winner2 = winner2
        self.loser1 = loser1
        self.loser2 = loser2

    def verify_players(self, players):
        for player in [self.winner1, self.winner2, self.loser1, self.loser2]:
            if player not in self.players.keys():
                self.players[player] = ts.Rating()
        return

    def play_game(self):
        self.verify_players(self.players)
        rating_groups = [(self.players[winner1], self.players[winner2)],
                         (self.players[loser1], self.players[loser2])]
        [(self.players[winner1], self.players[winner2]),
         (self.players[loser1], self.players[loser2])] = ts.rate(rating_groups)
        return


class Game_1v1v1(Game):

    def __init__(self, first, second, third):
        Game.__init__(self, '1v1v1', players)
        self.first = first
        self.second = second
        self.third = third

    def verify_players(self, players):
        for player in [self.first, self.second, self.third]:
            if player not in self.players.keys():
                self.players[player] = ts.Rating()
        return

    def play_game(self):
        self.verify_players(self.players)
        rating_groups = [(self.players[first],), (self.players[second],), (self.players[third],)]
        [(self.players[first],), (self.players[second],), (self.players[third],)] = ts.rate(rating_groups)
        return


class Game_1v1v1v1(Game):

    def __init__(self, first, second, third, fourth):
        Game.__init__(self, '1v1v1v1', players)
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth

    def verify_players(self, players):
        for player in [self.first, self.second, self.third, self.fourth]:
            if player not in self.players.keys():
                self.players[player] = ts.Rating()

    def play_game(self):
        self.verify_players(self.players)
        rating_groups = [(self.players[first],), (self.players[second],),
                         (self.players[third],), (self.players[fourth],)]
        return


class Leaderboard(object):

    def __init__(self, players):
        self.players = players

    def sort_leaderboard(self):
        sorted_ratings = sorted(self.players.values(), key=ts.expose, reverse=True)
        lookup = {val: key for key, val in self.players.items()}
        return [(lookup[rating], rating.mu)] for rating in sorted_ratings]

