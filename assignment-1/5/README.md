# Assignment 1 number 5, Affine Cipher

## What we know
- C1 = 0xB7 (integer: 183), P1 = 0xFF (integer: 255)
- C2 = 0x32 (integer: 50), P2 = 0xD8 (integer: 216)
- Diketahui dari potongan kode yang digunakan untuk affine cipher, nilai n (ukuran alfabet) yang digunakan adalah 256 (hexadecimal).
Sehingga nilai m yang memungkinkan adalah semua angka ganjil antara 1 dan 256 (256 merupakan hasil dari pangkat dengan
base 2 yaitu 2^8 , sehingga semua bilangan genap bukan merupakan koprima dari 256).
- Nilai b yang mungkin adalah 0 sampai 255 karena nilai n adalah 256, sehingga nilai b diatas 255 akan menghasilkan nilai
terulang.
- Dari pasangan ciphertext dan plaintext yang diketahui, dapat digunakan 2 buah persamaan:
  - 183 = 255m + b (mod 256)
  - 50 = 216m + b (mod 256)

  Kita kurangkan persamaan pertama dengan persamaan kedua, mendapatkan: 133 = 39m (mod 256)

  Menghasilkan m = 115, sehingga nilai b = 42 (didapat menggunakan kode)

## Kode yang digunakan
- [Kode](./code/m_and_b_searcher.py) yang digunakan untuk mencari nilai x (invers dari m), m, dan b
- [Kode](./code/image_restore.py) yang digunakan untuk mendapatkan hasil gambar yang dienkrip

## Hasil Dekripsi
![Decrypted Image](./code/decrypted.jpeg)

## Waktu yang digunakan untuk kriptanalisis
Waktu yang digunakan untuk mencari nilai m dan b melalui *looping* yaitu 128 + 256 (128 merupakan jumlah kunci m yang mungkin
dan 256 adalah jumla h nilai b yang mungkin), sehingga waktu yang dibutuhkan adalah konstan.

## Pendekatan dengan metode lain

### Brute Force dan Exhaustive Key Attack
- Nilai n (ukuran alfabet) yang digunakan adalah 256, sehingga nilai yang b yang memungkinkan adalah 0-255 (di luar hal tersebut),
hasil modulo akan terulang
- Karena nilai m merupakan bilangan yang koprima dengan nilai n, maka nilai m pasti di antara 1 dan 256
- Dari kedua poin di atas, dapat digunakan kode *looping* untuk mengetahui nilai m dan b berdasarkan *known plain text* yang diketahui
di awal

Dari hasil kode yang digunakan, waktu yang digunakan untuk mencari nilai m dan b adalah 256 * 256 (karena *constraint*
banyak alfabet diketahui), sehingga waktu yang dibutuhkan untuk mendapatkannya adalah konstan. Jika nilai n tidak diketahui,
nilai Big O adalah (n * n) atau n^2.

Perbandingan dengan kriptanalisis yang dilakukan sebelumnya

### Kode yang digunakan
- [Kode](./code/brute_force.py) yang digunakan untuk *brute force key* yang digunakan
