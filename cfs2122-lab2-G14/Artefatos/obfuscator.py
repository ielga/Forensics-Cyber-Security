# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 2.7.17 (default, Sep 30 2020, 13:38:04) 
# [GCC 7.5.0]
# Warning: this version of Python has problems handling the Python 3 "byte" type in constants properly.

# Embedded file name: obfuscator.py
# Compiled at: 2021-10-16 15:34:12
# Size of source mod 2**32: 295 bytes
import hashlib, sys
with open('seeds.txt', 'r') as (f):
    lines = f.readlines()
with open('seeds.txt', 'w') as (f):
    for line in lines[1:]:
        f.write(line)
    else:
        f.write(lines[0])

pw = hashlib.sha256(str(lines[0] + str(sys.argv[1])).encode('utf-8'))
print(pw.hexdigest())