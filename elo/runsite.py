from __future__ import absolute_import
import sqlite3
import trueskill as ts
from flask import Flask, request, g, render_template, redirect, url_for
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

@app.route('/add_a_game', methods=['GET'])
def render_game_form(game, game_type):
    if game_type == '1v1':   
        field_list = ['winner', 'loser']
    elif game_type == '2v2':
        field_list = ['winner1', 'winner2', 'loser1', 'loser2']
    elif game_type == '1v1v1':
        field_list = ['first', 'second', 'third']
    elif game_type == '1v1v1v1':
        field_list = ['first', 'second', 'third', 'fourth']
    return redirect(url_for('add_game', field_list=field_list))

@app.route('/', methods = ['GET', 'POST'])
def main_page():
    if request.method == 'GET':
        return render_template('home_page.html')
    game = request.form['game']
    game_type = request.form['game_type']
    if game_type == '':
        return redirect(url_for('leaderboard_view', game=game))
    return redirect(url_for('add_entry', game=game, game_type=game_type))

@app.route('/add_a_game', methods=['POST'])
def add_entry(game, game_type):
    if request.method == 'POST':
        sport = request.form['game']
        game_type = request.form['game_type']
        conn = connect_db()
        c = conn.cursor()
        c.execute('select * from ratings where sport = (?)', (sport,))
        res = c.fetchall()
        all_results = {result[0] + '_' + result[1]:
                        ts.Rating(mu=result[2], sigma=result[3]) for result in res}

        if game_type == '1v1':
            game = Game_1v1(request.form['winner1'], request.form['winner2'], sport)
        elif game_type == '2v2':
            game = Game_2v2(request.form['winner1'], request.form['winner2'],
                            request.form['loser1'], request.form['loser2'], sport)
        elif game_type == '1v1v1':
            game = Game_1v1v1(request.form['winner1'], request.form['winner2'],
                              request.form['loser1'], sport)
        elif game_type == '1v1v1v1':
            game = Game_1v1v1v1(request.form['winner1'], request.form['winner2'],
                                request.form['loser1'], request.form['loser2'], sport)

        all_results = game.play_game(all_results)

        # write new results all back into the table
        for key, rating in all_results.items():
            c.execute('insert into ratings values (?,?,?,?)', (
                      key.split('_')[0], key.split('_')[1], rating.mu, rating.sigma))
        conn.commit()
        conn.close()

        return redirect(url_for('main_page'))
    else:
        return render_gameform(game, game_type)

@app.route('/leaderboard', methods=['GET'])
def leaderboard_view(game, game_type):
    conn = connect_db()
    c = conn.cursor()
    c.execute('select * from ratings where game = {game}'.format(game=game))
    res = c.fetchall()
    scores = {result[0] + '_' + result[1]:
              ts.Rating(mu=result[2], sigma=result[3]) for result in res}
    leaderboard = Leaderboard(scores)
    rankings = leaderboard.sort_leaderboard()
    conn.close()
    return render_template('leaderboard.html', rankings=rankings)

if __name__ == '__main__':
    app.run(debug=True)
