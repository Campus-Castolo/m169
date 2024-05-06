from flask import Flask, render_template
from pymodules.inserter import inserter_bp
from pymodules.fetcher import fetcher_bp

app = Flask(__name__)
app.register_blueprint(fetcher_bp)
app.register_blueprint(inserter_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5500, host="0.0.0.0")
