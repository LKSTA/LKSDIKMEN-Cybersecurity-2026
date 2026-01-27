### Proses Build Challenge

Langkah-langkah yang digunakan untuk menyusun challenge ini:

1.  **Kompilasi Payload:**
    ```bash
    gcc -c -fPIC -fno-stack-protector payload.c -o payload.o
    ```
2.  **Ekstraksi Binary:**
    ```bash
    objcopy -O binary --only-section=.text payload.o payload.bin
    ```
3.  **Enkripsi:**
    Menjalankan `encryptor.py` untuk mengenkripsi shellcode.
4.  **Injeksi:**
    Menyalin output enkripsi ke dalam array `encrypted_code[]` pada `chall.c`.
5.  **Final Build:**
    ```bash
    gcc chall.c -o chall
    ```
