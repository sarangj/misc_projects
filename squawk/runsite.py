from __future__ import absolute_import
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
        abort, render_template, flash
from app.squawk import Squawk

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
def squawk_view():
    try:
        last_candidate
    except NameError:
        last_candidate = ''  # will cache this value so I don't recompute vocab every time
    if request.method == 'POST':
        candidate = str(request.form['Candidate'])
        image = 'static/%s.jpg' % candidate.lower()
        conn = connect_db()
        c = conn.cursor()
        c.execute('select speech from words where candidate = (?)', (candidate,))
        r = c.fetchone()
        squawker = Squawk(candidate, r[0])
        if candidate != last_candidate:
            doc = squawker.generate_vocab()
            starts, trigram_transitions = squawker.generate_word_order(doc)
        try:
            sentence = squawker.generate_using_trigrams(starts, trigram_transitions)
            last_candidate = candidate
            return render_template('candidate.html', sentence=sentence, image=image)
        except IndexError:
            error = 'Oops. Chief Squawk says try again.'
            last_candidate = candidate
            return render_template('candidate.html', error=error)
    else:
        return render_template('candidate.html')

if __name__ == '__main__':
    app.run()
