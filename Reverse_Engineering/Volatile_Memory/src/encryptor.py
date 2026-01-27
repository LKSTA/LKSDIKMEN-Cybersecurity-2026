key = 0xAA

with open("payload.bin", "rb") as f:
    content = f.read()

print("{")
for byte in content:
    encrypted_byte = byte ^ key
    print(f"0x{encrypted_byte:02x}, ", end="")
print("\n}")