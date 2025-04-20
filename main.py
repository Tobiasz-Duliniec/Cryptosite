from flask import Flask, flash, render_template, request, send_from_directory
from string import ascii_lowercase

app = Flask(__name__)

class KeyIterator:
    def __init__(self, key):
        self.index = -1
        self.key = ''
        for letter in key:
            if letter in ascii_lowercase:
                self.key += letter
        
    def __iter__(self):
        return self
    
    def __next__(self):
        self.index += 1
        return self.key[self.index]

@app.route('/style.css')
def send_styles():
    return send_from_directory('static', 'style.css')

def CeasarCipher(message:str, rotation:int) -> str:
    def get_alphabet_no(letter:str):
        for index, let in enumerate(alphabet):
            if(let == letter):
                return index
        
    alphabet = ascii_lowercase * 2
    if(rotation > 26):
        rotation %= 26
    elif(rotation < -26):
        rotation %= -26
    encryptedMessage = ""
    for letter in message:
        if(letter not in alphabet):
            encryptedMessage += letter
            continue
        if(rotation > 0):
            newLetter = alphabet[get_alphabet_no(letter) + rotation]
        else:
            newLetter = alphabet[26 + get_alphabet_no(letter) + rotation]
        encryptedMessage += newLetter
    return encryptedMessage

@app.route('/Cesar', methods = ['GET', 'POST'])
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
        return render_template('ceasarcipher.html', result = result)
    return render_template('ceasarcipher.html')

def VigenereCipher(message:str, key:str, action:str) -> str:
    while(len(key) < len(message)):
        key += key
    keyGenerator = KeyIterator(key)
    encryptedMessage = ""
    for letter in message:
        if letter not in ascii_lowercase:
            encryptedMessage += letter
            continue
        else:
            shift = ord(next(keyGenerator).lower()) - 97
            if(action == 'decrypt'):
                encryptedMessage += CeasarCipher(letter, -1 * shift)
            else:
                encryptedMessage += CeasarCipher(letter, shift)
    return encryptedMessage

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
        return render_template('vigenerecipher.html', result = result)
    return render_template('vigenerecipher.html')

def OneTimePad():
    message = "abc"
    key = KeyIterator("dtgr")
    message = ''
    for x in 'abc':
        print(ord(x) ^ ord(next(key)))
    print(message)

@app.route('/')
def index():
    return render_template('index.html')

if(__name__ == '__main__'):
    app.run()