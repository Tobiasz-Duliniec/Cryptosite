from flask import Flask, render_template


app = Flask(__name__)


def CeasarCipher(message:str, rotation:int) -> str:
    encryptedMessage = ""
    for letter in message:
        encryptedMessage += chr(ord(letter) + rotation)
    return encryptedMessage

@app.route('/')
def index():
    return render_template('index.html')

if(__name__ == '__main__'):
    app.run()