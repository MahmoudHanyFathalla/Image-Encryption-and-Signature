# Image-Encryption-and-Signature
This project demonstrates image encryption using AES-128 in different modes (ECB, CBC, CFB, OFB), RSA digital signature creation and verification, and randomness analysis using NIST tests.

## Project Overview
This project demonstrates image encryption using AES-128 in different modes (ECB, CBC, CFB, OFB), RSA digital signature creation and verification, and randomness analysis using NIST tests.

## Requirements
- OpenSSL (for encryption and signature operations)
- Image viewer (to inspect encrypted images)
- Python (for NIST test suite)
- NIST Statistical Test Suite (for randomness analysis)

## Files Included
1. `profile.jpg` - Original image file
2. `profile_ecb.jpg` - ECB encrypted image
3. `profile_cbc.jpg` - CBC encrypted image
4. `profile_cfb.jpg` - CFB encrypted image
5. `profile_ofb.jpg` - OFB encrypted image
6. `private_key.pem` - RSA private key
7. `public_key.pem` - RSA public key
8. `signature.bin` - Digital signature file
9. `report.pdf` - Detailed project report

## How to Run

### Task 1: Image Encryption
1. Generate a 128-bit AES key:
   ```bash
   openssl rand -hex 16
   ```

2. Encrypt the image in different modes:
   ```bash
   # ECB Mode
   openssl enc -aes-128-ecb -in profile.jpg -out profile_ecb.jpg -K [your_key]
   
   # CBC Mode
   openssl enc -aes-128-cbc -in profile.jpg -out profile_cbc.jpg -K [your_key] -iv 00000000000000000000000000000000
   
   # CFB Mode
   openssl enc -aes-128-cfb -in profile.jpg -out profile_cfb.jpg -K [your_key] -iv 00000000000000000000000000000000
   
   # OFB Mode
   openssl enc -aes-128-ofb -in profile.jpg -out profile_ofb.jpg -K [your_key] -iv 00000000000000000000000000000000
   ```

### Task 2: Digital Signature
1. Generate RSA keys:
   ```bash
   openssl genrsa -out private_key.pem 2048
   openssl rsa -in private_key.pem -pubout -out public_key.pem
   ```

2. Create SHA1 hash of encrypted image:
   ```bash
   openssl dgst -sha1 -hex profile_cbc.jpg
   ```

3. Create signature:
   ```bash
   openssl dgst -sha1 -sign private_key.pem -out signature.bin profile_cbc.jpg
   ```

4. Verify signature:
   ```bash
   openssl dgst -sha1 -verify public_key.pem -signature signature.bin profile_cbc.jpg
   ```

### Bonus: NIST Randomness Tests
1. Run tests on original image:
   ```bash
   python nist_tests.py original_image.bin
   ```

2. Run tests on encrypted images:
   ```bash
   python nist_tests.py encrypted_ecb.bin
   python nist_tests.py encrypted_cbc.bin
   python nist_tests.py encrypted_cfb.bin
   python nist_tests.py encrypted_ofb.bin
   ```

## Results Interpretation
- View encrypted images to observe visual differences between modes
- Check signature verification output ("Verified OK" indicates success)
- Compare NIST test p-values (values > 0.01 generally indicate randomness)

## Notes
- Replace `[your_key]` with your actual 128-bit AES key
- The IV used in this example is all zeros - in production use a random IV
- See the detailed report for analysis and observations
