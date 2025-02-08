from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/', methods=['GET', 'POST'])
def plan_15():
    if 'bet_history' not in session:
        session['bet_history'] = []

    if request.method == 'POST':
        capital = float(request.form['capital'])
        odds = float(request.form['odds'])
        outcome = request.form['outcome'].lower()

        stake = round(capital * 0.15)
        bal_after_stake = round(capital - stake, 2)

        if outcome == "win":
            bal_after_stake = round(bal_after_stake + odds * stake, 2)

        bet_history = session['bet_history']
        bet_history.append({
            'capital': round(capital, 2),
            'stake': stake,
            'odds': odds,
            'outcome': outcome.upper(),
            'balance_after_bet': bal_after_stake
        })
        session['bet_history'] = bet_history

        return render_template('index.html', bet_history=bet_history, balance=bal_after_stake)

    return render_template('index.html', bet_history=session['bet_history'], balance=None)

@app.route('/clear', methods=['POST'])
def clear_history():
    session.pop('bet_history', None)
    return redirect(url_for('plan_15'))

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
