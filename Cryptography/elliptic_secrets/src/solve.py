from ecdsa import SECP256k1, ellipticcurve
import hashlib

G = SECP256k1.generator
curve = SECP256k1.curve

Qx = 0x1f2c2edcd5643a05db1f60e55dddac62cfbbb843656320ee357b51e928a95c51
Qy = 0x7cf71fcd4bccc2d0f2932223f3af08ff9d1897829c0cde918161a9c15e6baf03
Rx = 0x36ca9a8f731680f8e669f14e69fa7b6079cafdbeb94ed3d8a91cea90cf528474
Ry = 0xea2e627b5fdecafdf6c9bc3974b17029a1480eac2d06c8a71cf88bbe4c193de5
ciphertext = bytes.fromhex("a7a794cd149820fbccdab12bd4ce62428edea38649cd29a8ccd0bf7ed39a3616dddff48151")

for d in range(1, 50001):
    Q = d * G
    if Q.x() == Qx and Q.y() == Qy:
        break

R = ellipticcurve.Point(curve, Rx, Ry)
S = d * R
key = hashlib.sha256(S.x().to_bytes(32, 'big')).digest()[:16]
flag = bytes([c ^ key[i % 16] for i, c in enumerate(ciphertext)])

print(f"d = {d}")
print(f"Flag: {flag.decode()}")
