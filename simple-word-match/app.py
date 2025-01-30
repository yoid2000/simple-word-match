from flask import Flask, render_template, request
from word_manager import WordManager

app = Flask(__name__)
wm = WordManager(num_words=10)

@app.route('/')
def home():
    x = request.args.get('x')
    y = request.args.get('y')
    english_words, german_words = wm.get_words(english_index=int(x) if x is not None else None, german_index=int(y) if y is not None else None)
    return render_template('index.html', english_words=english_words, german_words=german_words)

if __name__ == "__main__":
    app.run(debug=True)