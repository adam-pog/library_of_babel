import json
from flask import Flask, request
from flask_cors import CORS
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from mappings import NUM_TO_CHAR_MAP

app = Flask(__name__)
CORS(app)
KEY = b'\x99\x80\x8d\xdf\x0c\x95P\xb23\xc3\x00).\xdd6\xca'
IV  = b'\x92\xd3L\x18\xa5\x8d%c\xf1T\x82\x02\xd0\x17\xb2\xb4'
BOOK_PAD = 1312000

@app.route('/book', methods=['POST'])
def get_page():
    return {
        "text": split_text(
            generate_text(
                str(request.json['book']),
                int(request.json['page'])
            )
        )
    }


def generate_text(book, page):
    cipher = AES.new(KEY, AES.MODE_CBC, iv=IV)
    pass1 = cipher.encrypt(str(book).encode().ljust(BOOK_PAD))
    cipher = AES.new(KEY, AES.MODE_CBC, iv=IV)
    pass2 = cipher.encrypt(pass1[::-1])

    bytes = [NUM_TO_CHAR_MAP[i] for i in pass2]
    text = ''.join(bytes)

    start = (page-1) * 3200
    end = page * 3200

    return text[start:end]

def split_text(text):
    return [
        text[(i * 80):(i * 80) + 80] for i in range(40)
    ]





# dcipher = AES.new(KEY, AES.MODE_CBC, iv=IV)
# decrypt1 = dcipher.decrypt(pass2)
# dcipher = AES.new(KEY, AES.MODE_CBC, iv=IV)
# decrypt2 = dcipher.decrypt(decrypt1[::-1])



#Recieve book/page
# 1. pad num with 0
# 2. encrypt
# 3. map num to chars

# page - 1 * 410 : page * 410
#
# 1  0:410
# 2  410:820
# 3  820:1230
