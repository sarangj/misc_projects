import trueskill as ts

class Game_1v1(object):

    def __init__(self, winner, loser, sport):
        self.winner = winner
        self.loser = loser
        self.sport = sport
        self.winnerkey = self.winner + '_' + self.sport
        self.loserkey = self.loser + '_' + self.sport
        ts.setup(mu=100.0, sigma=33.333, beta=16.667, tau=0.33333, draw_probability=0)

    def verify_players(self, players):
        for player in [self.winnerkey, self.loserkey]:
            if player not in players.keys():
                players[player] = ts.Rating()
        return players

    def play_game(self, players):
        self.verify_players(players)
        players[self.winnerkey], players[self.loserkey] = ts.rate_1vs1(players[self.winnerkey],
                                                                       players[self.loserkey])
        return players


class Game_2v2(object):

    def __init__(self, winner1, winner2, loser1, loser2, sport):
        self.winner1 = winner1
        self.winner2 = winner2
        self.loser1 = loser1
        self.loser2 = loser2
        self.sport = sport
        self.winner1key = self.winner1 + '_' + self.sport
        self.winner2key = self.winner2 + '_' + self.sport
        self.loser1key = self.loser1 + '_' + self.sport
        self.loser2key = self.loser2 + '_' + self.sport
        ts.setup(mu=100.0, sigma=33.333, beta=16.667, tau=0.33333, draw_probability=0)

    def verify_players(self, players):
        for player in [self.winner1key, self.winner2key, self.loser1key, self.loser2key]:
            if player not in players.keys():
                players[player] = ts.Rating()
        return players

    def play_game(self, players):
        self.verify_players(players)
        rating_groups = [(players[self.winner1key], players[self.winner2key]),
                         (players[self.loser1key], players[self.loser2key])]
        [(players[self.winner1key], players[self.winner2key]),
         (players[self.loser1key], players[self.loser2key])] = ts.rate(rating_groups)
        return players


class Game_1v1v1(object):

    def __init__(self, first, second, third, sport):
        self.first = first
        self.second = second
        self.third = third
        self.sport = sport
        self.firstkey = self.first + '_' + self.sport
        self.secondkey = self.second + '_' + self.sport
        self.thirdkey = self.third + '_' + self.sport
        ts.setup(mu=100.0, sigma=33.333, beta=16.667, tau=0.33333, draw_probability=0)

    def verify_players(self, players):
        for player in [self.firstkey, self.secondkey, self.thirdkey]:
            if player not in players.keys():
                players[player] = ts.Rating()
        return players

    def play_game(self, players):
        self.verify_players(players)
        rating_groups = [(players[self.firstkey],), (players[self.secondkey],),
                         (players[self.thirdkey],)]
        [(players[self.firstkey],), (players[self.secondkey],),
         (players[self.thirdkey],)] = ts.rate(rating_groups)
        return players


class Game_1v1v1v1(object):

    def __init__(self, first, second, third, fourth, sport):
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth
        self.sport = sport
        self.firstkey = self.first + '_' + self.sport
        self.secondkey = self.second + '_' + self.sport
        self.thirdkey = self.third + '_' + self.sport
        self.fourthkey = self.fourth + '_' + self.sport
        ts.setup(mu=100.0, sigma=33.333, beta=16.667, tau=0.33333, draw_probability=0)

    def verify_players(self, players):
        for player in [self.firstkey, self.secondkey, self.thirdkey, self.fourthkey]:
            if player not in players.keys():
                players[player] = ts.Rating()
        return players

    def play_game(self, players):
        self.verify_players(players)
        rating_groups = [(players[self.firstkey],), (players[self.secondkey],),
                         (players[self.thirdkey],), (players[self.fourthkey],)]
        [(players[self.firstkey],), (players[self.secondkey],),
         (players[self.thirdkey],), (players[self.fourthkey],)] = ts.rate(rating_groups)
        return players


class Leaderboard(object):

    def __init__(self, scores):
        self.scores = scores

    def sort_leaderboard(self):
        sorted_ratings = sorted(self.scores.values(), key=ts.expose, reverse=True)
        lookup = {val: key for key, val in self.scores.items()}
        return [(lookup[rating].split('@')[0], "%.2f" % rating.mu) for rating in sorted_ratings]

