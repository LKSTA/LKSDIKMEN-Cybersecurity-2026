from pwn import xor

with open("flag.txt", "rb") as f:
    noroi = f.read()

while len(noroi) % 3 != 0:
    noroi += b"\x00"

L = len(noroi)
seal_a = int(str(L)[0])
seal_b = int(str(L)[-1])

kokoro   = noroi[:L//3]
chikara  = noroi[L//3:2*L//3]
tamashii = noroi[2*L//3:]

kokoro   = xor(kokoro, seal_a + seal_b)
chikara  = xor(chikara, kokoro, cut="max")
tamashii = xor(tamashii, chikara, cut="max")

kokoro   = xor(kokoro, tamashii, cut="max")
chikara  = xor(chikara, kokoro, cut="max")
tamashii = xor(tamashii, seal_a * seal_b)

with open("out.txt", "wb") as f:
    f.write(kokoro + chikara + tamashii)
