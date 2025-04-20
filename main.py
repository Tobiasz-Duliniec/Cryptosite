from flask import Flask, flash, render_template, request, send_from_directory
from string import ascii_letters, ascii_lowercase, ascii_uppercase
import hashlib


app = Flask(__name__)

app.secret_key = hashlib.sha256().digest()

class KeyIterator:
    def __init__(self, key):
        self.index = -1
        self.key = ""
        for letter in key:
            if letter in ascii_letters:
                self.key += letter
        if(self.key == ""):
            raise ValueError("Key doesn't contain any letters from the Latin alphabet!")
        
    def __iter__(self):
        return self
    
    def __next__(self):
        self.index += 1
        return self.key[self.index]

def checkKey(key:str):
    for letter in key:
        if letter not in ascii_letters:
            return False
    return True

@app.route('/style.css')
def send_styles():
    return send_from_directory('static', 'style.css')

def CeasarCipher(message:str, rotation:int) -> str:
    def get_letter_no(letter:str):
        for index, let in enumerate(ascii_lowercase):
            if(let == letter):
                return index
        for index, let in enumerate(ascii_uppercase):
            if(let == letter):
                return index

    alphabet = ascii_letters * 2
    if(rotation > 26):
        rotation %= 26
    elif(rotation < -26):
        rotation %= -26
    encryptedMessage = ""
    for letter in message:
        if(letter not in ascii_letters):
            encryptedMessage += letter
            continue
        if(letter.islower()):
            newLetter = (ascii_lowercase * 2)[get_letter_no(letter) + rotation]
        else:
            newLetter = (ascii_uppercase * 2)[get_letter_no(letter) + rotation]
        encryptedMessage += newLetter
    return encryptedMessage

@app.route('/Ceasar', methods = ['GET', 'POST'])
def CeasarCipherPage():
    if(request.method == 'POST'):
        message = request.form.get('message', None)
        shift = request.form.get('shift', None)
        action = request.form.get('action', 'encrypt')
        if message is None or shift is None:
            flash('Invalid shift value!', 'error')
            return render_template('ceasarcipher.html')
        else:
            try:
                shift = int(shift)
            except ValueError:
                flash('Invalid shift value!', 'error')
                return render_template('ceasarcipher.html')
            if(action == 'decrypt'):
                result = CeasarCipher(message, -1 * shift)
            else:
                 result = CeasarCipher(message, shift)
        return render_template('ceasarcipher.html', result = result, message = message, shift = shift)
    return render_template('ceasarcipher.html')

def VigenereCipher(message:str, key:str, action:str):
    if(checkKey(key)):
        while(len(key) < len(message)):
            key += key
        keyGenerator = KeyIterator(key)
        encryptedMessage = ""
        for letter in message:
            if letter not in ascii_letters:
                encryptedMessage += letter
                continue
            else:
                shift = ord(next(keyGenerator).lower()) - 97
                if(action == 'decrypt'):
                    encryptedMessage += CeasarCipher(letter, -1 * shift)
                else:
                    encryptedMessage += CeasarCipher(letter, shift)
        return encryptedMessage
    else:
        flash("Key doesn't containt any values from the Latin alphabet!", 'error')
        print("Zwracam None")
        return None

@app.route('/Vigenere', methods = ['GET', 'POST'])
def VigenereCipherPage():
    if(request.method == 'POST'):
        message = request.form.get('message', None)
        key = request.form.get('key', None)
        action = request.form.get('action', 'encrypt')
        if message is None or key is None:
            flash('Invalid message and/or key values!', 'error')
            return render_template('vigenerecipher.html')
        result = VigenereCipher(message, key, action)
        return render_template('vigenerecipher.html', result = result, message = message, key = key)
    return render_template('vigenerecipher.html')

@app.route('/')
def index():
    return render_template('index.html')

if(__name__ == '__main__'):
    app.run()