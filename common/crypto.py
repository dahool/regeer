"""Copyright (c) 2009, Sergio Gabriel Teves
All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from random import randrange
import base64
from Crypto.Cipher import Blowfish
from django.conf import settings

class BCipher:
    def __init__(self, pwd=None):
        if not pwd:
            pwd = getattr(settings, 'SECRET_KEY')
        self.__cipher = Blowfish.new(pwd)
    def encrypt(self, text):
        ciphertext = self.__cipher.encrypt(self.__pad_file(text))
        return base64.b64encode(ciphertext)
    def decrypt(self, b64text):
        try:
            ciphertext = base64.b64decode(b64text)
        except TypeError:
            # text is not encrypted
            return b64text
        cleartext = self.__depad_file(self.__cipher.decrypt(ciphertext))
        return cleartext
    # Blowfish cipher needs 8 byte blocks to work with
    def __pad_file(self, text):
        pad_bytes = 8 - (len(text) % 8)
        # try to deal with unicode strings
        asc_text = str(text)
        for i in range(pad_bytes - 1):
            asc_text += chr(randrange(0, 256))
        # final padding byte; % by 8 to get the number of padding bytes
        bflag = randrange(6, 248); bflag -= bflag % 8 - pad_bytes
        asc_text += chr(bflag)
        return asc_text
    def __depad_file(self, text):
        pad_bytes = ord(text[-1]) % 8
        if not pad_bytes: pad_bytes = 8
        return text[:-pad_bytes]

if __name__ == '__main__':
    print "INIT TEST"
    key = '%8%z7z3&*8*3t^h@j!!z953js5!3h^g%+1m9xcr17e!%dqb+2w'
    text = "este es un TEXTO que hay que encriptar"
    print "ENCRYPT: %s" % text
    bc = BCipher(key)
    crypt = bc.encrypt(text)
    print "RESULT: %s" % crypt
    res = bc.decrypt(crypt)
    print "DESCRYPTED: %s" % res
    if res == text:
        print "Success"
    else:
        print "Fail"