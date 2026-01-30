#!/bin/bash

PDF_NAME="BANK_FLAG.pdf"
IMG_NAME="disk.img"
MOUNT_DIR="/mnt/disk_img"
HEADER_SIZE=1024
EOF_SIZE=32
IMG_SIZE_MB=10
if [ ! -f "$PDF_NAME" ]; then
  echo "[!] File $PDF_NAME tidak ditemukan!"
  exit 1
fi
echo "[*] Memecah file PDF menjadi 3 bagian..."
PDF_SIZE=$(stat -c%s "$PDF_NAME")
CHUNK_START=$HEADER_SIZE
CHUNK_SIZE=$(($PDF_SIZE - $HEADER_SIZE - $EOF_SIZE))
dd if="$PDF_NAME" of=header.bin bs=1 count=$HEADER_SIZE status=none
dd if="$PDF_NAME" of=chunk.bin  bs=1 skip=$CHUNK_START count=$CHUNK_SIZE status=none
dd if="$PDF_NAME" of=eof.bin    bs=1 skip=$(($PDF_SIZE - $EOF_SIZE)) status=none
echo "[+] Fragmen (asli) dibuat:"
ls -lh header.bin chunk.bin eof.bin
echo "[*] Membuat image FAT32 sebesar $IMG_SIZE_MB MB..."
dd if=/dev/zero of="$IMG_NAME" bs=1M count=$IMG_SIZE_MB status=none
mkfs.vfat "$IMG_NAME" > /dev/null
sudo mkdir -p "$MOUNT_DIR"
sudo mount -o loop "$IMG_NAME" "$MOUNT_DIR"
echo "[*] Membuat struktur folder ala Windows..."
sudo mkdir -p "$MOUNT_DIR/PerfLogs"
sudo mkdir -p "$MOUNT_DIR/Program Files/Common Files"
sudo mkdir -p "$MOUNT_DIR/Program Files (x86)/Common Files"
sudo mkdir -p "$MOUNT_DIR/ProgramData/Microsoft/Windows"
sudo mkdir -p "$MOUNT_DIR/\$RECYCLE.BIN/S-1-5-21-1000-1000-1000-1000"
sudo mkdir -p "$MOUNT_DIR/System Volume Information"
sudo mkdir -p "$MOUNT_DIR/Windows/System32"
sudo mkdir -p "$MOUNT_DIR/Windows/SysWOW64"
sudo mkdir -p "$MOUNT_DIR/Windows/Temp"
sudo mkdir -p "$MOUNT_DIR/Windows/Logs"
sudo mkdir -p "$MOUNT_DIR/Windows/SoftwareDistribution/Download"
sudo mkdir -p "$MOUNT_DIR/Users/Default/Desktop"
sudo mkdir -p "$MOUNT_DIR/Users/Public/Desktop"
sudo mkdir -p "$MOUNT_DIR/Users/Public/Documents"
sudo mkdir -p "$MOUNT_DIR/Users/Public/Downloads"
sudo mkdir -p "$MOUNT_DIR/Users/LKS/Desktop"
sudo mkdir -p "$MOUNT_DIR/Users/LKS/Documents"
sudo mkdir -p "$MOUNT_DIR/Users/LKS/Downloads"
sudo mkdir -p "$MOUNT_DIR/Users/LKS/Pictures"
sudo mkdir -p "$MOUNT_DIR/Users/LKS/AppData/Local/Temp"
sudo mkdir -p "$MOUNT_DIR/Users/LKS/AppData/Roaming/Microsoft/Windows/Recent"
echo "[*] Menyalin fragmen ke Users/LKS/Documents (tanpa ganti nama)..."
sudo cp header.bin "$MOUNT_DIR/Users/LKS/Documents/header.bin"
sudo cp chunk.bin  "$MOUNT_DIR/Users/LKS/Documents/chunk.bin"
sudo cp eof.bin    "$MOUNT_DIR/Users/LKS/Documents/eof.bin"
sync
sudo umount "$MOUNT_DIR"
echo "[✓] Selesai. Image siap: $IMG_NAME"
