from pwn import xor

with open("out.txt", "rb") as f:
    enc = f.read()

L = len(enc)
seal_a = int(str(L)[0])
seal_b = int(str(L)[-1])

s = seal_a + seal_b
p = seal_a * seal_b

a2 = enc[:L//3]
b2 = enc[L//3:2*L//3]
c2 = enc[2*L//3:]
c1 = xor(c2, p)
b1 = xor(b2, a2, cut="max")
a1 = xor(a2, c1, cut="max")
c0 = xor(c1, b1, cut="max")
b0 = xor(b1, a1, cut="max")
a0 = xor(a1, s)

flag = a0 + b0 + c0

flag = flag.rstrip(b"\x00")

print("FLAG:", flag.decode())
