from ecdsa import SECP256k1
import hashlib
import secrets

G = SECP256k1.generator
n = SECP256k1.order

d = secrets.randbelow(50000) + 1
k = secrets.randbelow(n - 1) + 1

Q = d * G
R = k * G
S = d * R

key = hashlib.sha256(S.x().to_bytes(32, 'big')).digest()[:16]

flag = b"LKS{8c916260eeffe2d0e60b688eb1226337}"
ciphertext = bytes([p ^ key[i % 16] for i, p in enumerate(flag)])

print(f"Qx = {hex(Q.x())[2:]}")
print(f"Qy = {hex(Q.y())[2:]}")
print(f"Rx = {hex(R.x())[2:].zfill(64)}")
print(f"Ry = {hex(R.y())[2:].zfill(64)}")
print(f"Ciphertext = {ciphertext.hex()}")
