#!/usr/bin/env python3
"""Encrypt/decrypt repo secrets with a passphrase (scrypt N=2^20 + AES-256-CBC via openssl).
Passphrase is read from env GROKBOT_HOME_PASSPHRASE (never pass it on the command line).
  encrypt text:   secret-crypt.py enc     <plain_in> <enc_out>
  decrypt text:   secret-crypt.py dec     <enc_in>   <plain_out>
  encrypt binary: secret-crypt.py enc-bin <plain_in> <enc_out>
  decrypt binary: secret-crypt.py dec-bin <enc_in>   <plain_out>
File format: b"GBH1" + 16-byte salt + AES-256-CBC ciphertext (key/iv = scrypt(pass, salt)[:32]/[32:48]).
enc/dec are for text secrets (Composio keys): decrypt rejects non-ASCII-printable output.
enc-bin/dec-bin are for binary blobs (e.g. finance.tgz): decrypt skips the printable check.
Never prints key material: on any failure only a short generic message is shown.
Note: scrypt needs ~1 GiB RAM and a few seconds per call.
"""
import hashlib, os, subprocess, sys

def die(msg, code=1):
    sys.stderr.write("secret-crypt: " + msg + "\n"); sys.exit(code)

if len(sys.argv) != 4 or sys.argv[1] not in ("enc", "dec", "enc-bin", "dec-bin"):
    die("usage: secret-crypt.py enc|dec|enc-bin|dec-bin <in> <out>", 2)
mode, src, dst = sys.argv[1:4]
pw = os.environ.get("GROKBOT_HOME_PASSPHRASE", "")
if not pw:
    die("GROKBOT_HOME_PASSPHRASE is not set (ask the user via a masked secret-request)", 2)
pw = pw.encode()

def derive(salt):
    k = hashlib.scrypt(pw, salt=salt, n=2**20, r=8, p=1, maxmem=2**31-1, dklen=48)
    return k[:32].hex(), k[32:].hex()

def openssl(args, data):
    # key/iv go on openssl's argv (visible only to this box user); errors are swallowed so they never reach logs
    r = subprocess.run(["openssl", "enc", "-aes-256-cbc", *args], input=data, capture_output=True)
    return r.stdout if r.returncode == 0 else None

def write_private(path, data):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        os.fchmod(fd, 0o600); os.write(fd, data)
    finally:
        os.close(fd)

if mode in ("enc", "enc-bin"):
    plain = open(src, "rb").read()
    if not plain.strip():
        die("refusing to encrypt an empty file")
    salt = os.urandom(16); key, iv = derive(salt)
    ct = openssl(["-K", key, "-iv", iv], plain)
    if ct is None:
        die("encryption failed")
    open(dst, "wb").write(b"GBH1" + salt + ct)
else:
    data = open(src, "rb").read()
    if data[:4] != b"GBH1" or len(data) < 36:
        die("not a GBH1-encrypted file: " + src)
    key, iv = derive(data[4:20])
    pt = openssl(["-d", "-K", key, "-iv", iv], data[20:])
    if pt is None or not pt.strip():
        die("decryption failed (wrong passphrase or corrupted file); nothing written")
    # text mode: reject non-printable (wrong passphrase may still yield garbage that passes padding)
    if mode == "dec":
        if any(b < 0x20 and b not in (9, 10, 13) for b in pt) or any(b > 0x7e for b in pt):
            die("decryption failed (wrong passphrase or corrupted file); nothing written")
    write_private(dst, pt)
