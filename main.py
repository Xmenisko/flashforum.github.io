from website import create_app
from flask import Flask

app = Flask('app')

if __name__ == '__main__':
    app.run(debug=True)
    
app.run(host="0.0.0.0", port=8080)