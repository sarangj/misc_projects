from __future__ import absolute_import
import sqlite3
import TrueSkill as ts
from flask import Flask, request, g, render_template
from app.elo import *

app = Flask(__name__)
app.config.from_object('config')

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET', 'POST'])
def elo_view():
    if request.method == 'POST':
        sport = request.form['sport']
        game_type = request.form['game_type']
        conn = connect_db()
        c = conn.cursor()
        c.execute('select * from atx_games where sport = (?)', (sport,))
        res = c.fetchall()
        players_dict = {player: ts.Rating(mu=mu, sigma=sigma, tau=tau) for
                        player, mu, sigma, tau in res}
        if game_type == '1v1':
            game = Game_1v1(request.form['winner'], request.form['loser'])
        elif game_type == '2v2':
            game = Game_2v2(request.form['winner1'], request.form['winner2'],
                            request.form['loser1'], request.form['loser2'])
        elif game_type == '1v1v1':
            game = Game_1v1v1(request.form['first'], request.form['second'],
                              request.form['third'])
        elif game_type == '1v1v1v1':
            game = Game_1v1v1v1(request.form['first'], request.form['second'],
                                request.form['third'], request.form['fourth'])
        game.verify_players(players_dict)
        game.play_game()

        c.execute('insert or replace into atx_games (sport, name, mu, sigma, tau)
                   values (?,?,?,?,?)', [sport, name, mu, sigma, tau])


        return render_template('elo.html')
    else:
        return render_template('elo.html')

if __name__ == '__main__':
    app.run()
