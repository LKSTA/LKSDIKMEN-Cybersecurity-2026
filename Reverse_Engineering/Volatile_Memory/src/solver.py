#!/usr/bin/env python3
"""
Solver untuk challenge binary dengan self-decrypting code
Binary menggunakan XOR 0xAA untuk menyembunyikan logika verifikasi flag
"""

import sys
import re
from pathlib import Path

def get_section_info(binary_path):
    """Parse ELF header untuk mendapatkan info section .data"""
    with open(binary_path, 'rb') as f:
        data = f.read()
    
    # ELF header parsing sederhana
    if data[:4] != b'\x7fELF':
        raise ValueError("Bukan file ELF valid")
    
    is_64bit = data[4] == 2
    if not is_64bit:
        raise ValueError("Hanya support ELF 64-bit")
    
    # Section header offset dan info
    e_shoff = int.from_bytes(data[0x28:0x30], 'little')
    e_shentsize = int.from_bytes(data[0x3a:0x3c], 'little')
    e_shnum = int.from_bytes(data[0x3c:0x3e], 'little')
    e_shstrndx = int.from_bytes(data[0x3e:0x40], 'little')
    
    # String table section
    shstr_offset = e_shoff + e_shstrndx * e_shentsize
    shstr_sh_offset = int.from_bytes(data[shstr_offset+0x18:shstr_offset+0x20], 'little')
    
    # Cari section .data
    for i in range(e_shnum):
        sh_offset = e_shoff + i * e_shentsize
        sh_name_idx = int.from_bytes(data[sh_offset:sh_offset+4], 'little')
        
        # Baca nama section
        name_end = data.find(b'\x00', shstr_sh_offset + sh_name_idx)
        name = data[shstr_sh_offset + sh_name_idx:name_end].decode('ascii')
        
        if name == '.data':
            sh_addr = int.from_bytes(data[sh_offset+0x10:sh_offset+0x18], 'little')
            sh_offset_file = int.from_bytes(data[sh_offset+0x18:sh_offset+0x20], 'little')
            sh_size = int.from_bytes(data[sh_offset+0x20:sh_offset+0x28], 'little')
            return {
                'vaddr': sh_addr,
                'offset': sh_offset_file,
                'size': sh_size
            }
    
    raise ValueError("Section .data tidak ditemukan")

def find_encrypted_code_params(binary_path):
    """Cari parameter encrypted code dari disassembly main()"""
    with open(binary_path, 'rb') as f:
        data = f.read()
    
    # Pattern untuk mencari: movq $size, -0x10(%rbp) dan mov $addr, %esi (memcpy source)
    # Kita cari pattern XOR key juga: xor $0xNN, %edx
    
    # Cari XOR key - pattern: 83 f2 XX (xor $XX, %edx)
    xor_pattern = re.compile(rb'\x83\xf2(.)', re.DOTALL)
    xor_match = xor_pattern.search(data)
    xor_key = xor_match.group(1)[0] if xor_match else 0xAA
    
    # Cari size - pattern: 48 c7 45 f0 XX XX 00 00 (movq $size, -0x10(%rbp))
    size_pattern = re.compile(rb'\x48\xc7\x45\xf0(....)' , re.DOTALL)
    size_match = size_pattern.search(data)
    size = int.from_bytes(size_match.group(1), 'little') if size_match else 0x21f
    
    # Cari source address untuk memcpy - pattern: be XX XX XX XX (mov $addr, %esi)
    # Biasanya setelah mov -0x10(%rbp), %rdx
    memcpy_pattern = re.compile(rb'\xbe(....)\x48\x89\xc7\xe8', re.DOTALL)
    memcpy_match = memcpy_pattern.search(data)
    src_addr = int.from_bytes(memcpy_match.group(1), 'little') if memcpy_match else 0x403060
    
    return {
        'src_addr': src_addr,
        'size': size,
        'xor_key': xor_key
    }

def decrypt_shellcode(binary_path):
    """Dekripsi shellcode dari binary"""
    with open(binary_path, 'rb') as f:
        binary_data = f.read()
    
    # Dapatkan info
    section_info = get_section_info(binary_path)
    params = find_encrypted_code_params(binary_path)
    
    # Hitung file offset dari virtual address
    file_offset = section_info['offset'] + (params['src_addr'] - section_info['vaddr'])
    
    # Ekstrak dan dekripsi
    encrypted = binary_data[file_offset:file_offset + params['size']]
    decrypted = bytes([b ^ params['xor_key'] for b in encrypted])
    
    return decrypted, params

def extract_flag_from_shellcode(shellcode):
    """Ekstrak flag dari shellcode dengan parsing instruksi CMP"""
    flag_chars = []
    i = 0
    
    while i < len(shellcode) - 2:
        # Pattern: 3c XX (cmp $XX, %al)
        if shellcode[i] == 0x3c:
            char_val = shellcode[i + 1]
            # Skip jika bukan printable ASCII
            if 0x20 <= char_val <= 0x7e:
                flag_chars.append(chr(char_val))
            i += 2
        # Pattern: 84 c0 (test %al, %al) - null terminator check
        elif shellcode[i:i+2] == b'\x84\xc0':
            break
        else:
            i += 1
    
    return ''.join(flag_chars)

def solve(binary_path):
    """Main solver function"""
    print(f"[*] Analyzing: {binary_path}")
    
    # Dekripsi shellcode
    shellcode, params = decrypt_shellcode(binary_path)
    print(f"[+] Found encrypted code at 0x{params['src_addr']:x}")
    print(f"[+] Size: {params['size']} bytes")
    print(f"[+] XOR key: 0x{params['xor_key']:02x}")
    
    # Ekstrak flag
    flag = extract_flag_from_shellcode(shellcode)
    print(f"\n[✓] FLAG: {flag}")
    
    return flag

if __name__ == "__main__":
    binary = sys.argv[1] if len(sys.argv) > 1 else "chall"
    
    if not Path(binary).exists():
        print(f"[-] File tidak ditemukan: {binary}")
        sys.exit(1)
    
    solve(binary)
