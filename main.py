from flask import Flask, flash, render_template, request, send_from_directory
from string import ascii_letters, ascii_lowercase, ascii_uppercase
import hashlib


app = Flask(__name__)

app.secret_key = hashlib.sha256().digest()

class KeyIterator:
    def __init__(self, key):
        self.index = -1
        self.key = key
        
    def __iter__(self):
        return self
    
    def __next__(self):
        self.index += 1
        return self.key[self.index]

def checkKey(key:str) -> bool:
    checked_key = ""
    for letter in key:
        if letter not in ascii_letters:
            continue
        checked_key += letter
    return checked_key != ""

@app.route('/style.css')
def send_styles():
    return send_from_directory('static', 'style.css')

@app.route('/skrypt.js')
def send_js():
    return send_from_directory('static', 'skrypt.js')

@app.route('/favicon.ico')
def send_favicon():
    return send_from_directory('static', 'favicon.ico')

def BaconsCipher(message:str, action:str):
    letter_to_code = {
        'a': 'aaaaa',
        'b': 'aaaab',
        'c': 'aaaba',
        'd': 'aaabb',
        'e': 'aabaa',
        'f': 'aabab',
        'g': 'aabba',
        'h': 'aabbb',
        'i': 'abaaa',
        'j': 'abaab',
        'k': 'ababa',
        'l': 'ababb',
        'm': 'abbaa',
        'n': 'abbab',
        'o': 'abbba',
        'p': 'abbbb',
        'q': 'baaaa',
        'r': 'baaab',
        's': 'baaba',
        't': 'baabb',
        'u': 'babaa',
        'v': 'babab',
        'w': 'babba',
        'x': 'babbb',
        'y': 'bbaaa',
        'z': 'bbaab'
        }

    code_to_key = {code:letter for letter, code in letter_to_code.items()}

    def encrypt(message:str):
        encrypted = ''
        for letter in message:
            letter = letter.lower()
            if letter in letter_to_code:
                encrypted += letter_to_code[letter] + ' '
        return encrypted[:-1]

    def decrypt(cipher:str):
        cipher = cipher.split(' ')
        decrypted = ''
        for code in cipher:
            if code in code_to_key:
                decrypted += code_to_key[code]
        return decrypted
    
    return decrypt(message) if(action == 'decrypt') else encrypt(message)

@app.route('/Bacon', methods = ['GET', 'POST'])
def BaconsCipherPage():
    if(request.method == 'POST'):
        message = request.form.get('message', None)
        action = request.form.get('action', 'encrypt')
        if message is None or message == "":
            flash('Invalid messahe/key value!', 'error')
            return render_template('baconscipher.html')
        return render_template('baconscipher.html', message = message, action = action, result = BaconsCipher(message, action))
    return render_template('baconscipher.html')

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
        if message is None or message == "" or shift is None or shift == "":
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
        return render_template('ceasarcipher.html', result = result, message = message, shift = shift, action = action)
    return render_template('ceasarcipher.html')

def VigenereCipher(message:str, key:str, action:str):
    #if(checkKey(key)):
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

@app.route('/Vigenere', methods = ['GET', 'POST'])
def VigenereCipherPage():
    if(request.method == 'POST'):
        message = request.form.get('message', None)
        key = request.form.get('key', None)
        action = request.form.get('action', 'encrypt')
        if message is None or message == "" or key is None or key == "":
            flash('Invalid message and/or key values!', 'error')
            return render_template('vigenerecipher.html')
        result = VigenereCipher(message, key, action)
        return render_template('vigenerecipher.html', result = result, message = message, key = key, action = action)
    return render_template('vigenerecipher.html')

@app.route('/')
def index():
    return render_template('index.html')

if(__name__ == '__main__'):
    app.run()