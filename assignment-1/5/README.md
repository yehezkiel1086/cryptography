# Assignment 1 number 5, Affine Cipher

## What we know
- C1 = 0xB7 (integer: 183), P1 = 0xFF (integer: 255)
- C2 = 0x32 (integer: 50), P2 = 0xD8 (integer: 216)
- Diketahui dari potongan kode yang digunakan untuk affine cipher, nilai n (ukuran alfabet) yang digunakan adalah 256 (hexadecimal).
Sehingga nilai m yang memungkinkan adalah semua angka ganjil antara 1 dan 256.
- Dari pasangan ciphertext dan plaintext yang diketahui, dapat digunakan 2 buah persamaan:
  - 183 = 255m + b (mod 256)
  - 50 = 216m + b (mod 256)

  Kita kurangkan persamaan pertama dengan persamaan kedua, mendapatkan: 133 = 39m (mod 256)

  Menghasilkan m = 115, sehingga nilai b = 42 (didapat menggunakan kode)

## Hasil Dekripsi
![Decrypted Image](./code/decrypted.jpeg)
