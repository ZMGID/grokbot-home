#!/usr/bin/env python3
"""Encrypt/decrypt repo secrets with a passphrase (scrypt N=2^20 + AES-256-CBC via openssl).
Passphrase is read from env GROKBOT_HOME_PASSPHRASE (never pass it on the command line).
  encrypt: secret-crypt.py enc <plain_in> <enc_out>
  decrypt: secret-crypt.py dec <enc_in> <plain_out>
"""
import hashlib, os, subprocess, sys
mode, src, dst = sys.argv[1:4]
pw = os.environ["GROKBOT_HOME_PASSPHRASE"].encode()
def derive(salt):
    k = hashlib.scrypt(pw, salt=salt, n=2**20, r=8, p=1, maxmem=2**31-1, dklen=48)
    return k[:32].hex(), k[32:].hex()
if mode == "enc":
    salt = os.urandom(16); key, iv = derive(salt)
    ct = subprocess.run(["openssl","enc","-aes-256-cbc","-K",key,"-iv",iv,"-in",src], check=True, capture_output=True).stdout
    open(dst,"wb").write(b"GBH1" + salt + ct)
elif mode == "dec":
    data = open(src,"rb").read(); assert data[:4] == b"GBH1", "bad format"
    key, iv = derive(data[4:20])
    pt = subprocess.run(["openssl","enc","-d","-aes-256-cbc","-K",key,"-iv",iv], input=data[20:], check=True, capture_output=True).stdout
    fd = os.open(dst, os.O_WRONLY|os.O_CREAT|os.O_TRUNC, 0o600); os.write(fd, pt); os.close(fd)
else:
    sys.exit("mode must be enc or dec")
