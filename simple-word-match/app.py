from flask import Flask, render_template, request
from word_manager import WordManager

app = Flask(__name__)
wm = WordManager(num_words=10)

@app.route('/')
def home():
    x = request.args.get('x')
    y = request.args.get('y')
    click_type = request.args.get('clickType')

    # Extract and print the port information
    host = request.host
    if ':' in host:
        hostname, port = host.split(':')
    else:
        hostname = host
        port = '8100'  # Default port for HTTP if not specified
    
    print(f"Hostname: {hostname}")
    print(f"Port: {port}")
    wm.set_port(port)
    
    print(f"x: {x}, y: {y}, clickType: {click_type}")
    english_words, german_words = wm.get_words(english_index=int(x) if x is not None else None, german_index=int(y) if y is not None else None, click_type=click_type)
    print(english_words)
    print(german_words)
    return render_template('index.html', english_words=english_words, german_words=german_words)

if __name__ == "__main__":
    app.run(debug=True)