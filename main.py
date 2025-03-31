from flask import Flask, render_template, send_from_directory


app = Flask(__name__)


@app.route('/style.css')
def send_styles():
    return send_from_directory('static', 'style.css')

def CeasarCipher(message:str, rotation:int) -> str:
    encryptedMessage = ""
    for letter in message:
        if(letter not in 'abcdefghijklmnopqrstwxyzABCDEFGHIJKLMNOPQRSTWXYZ'):
            encryptedMessage += letter
            continue
        newLetter = ord(letter) + rotation
        if((newLetter not in range(97, 123)) and (newLetter not in range(65, 91))):
            newLetter -= 26
        encryptedMessage += chr(newLetter)
    return encryptedMessage

@app.route('/')
def index():
    return render_template('index.html')

if(__name__ == '__main__'):
    app.run()