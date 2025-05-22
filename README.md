# **Image Encryption & Digital Signature Project**  

This project provides **two distinct methods** for secure image encryption and digital signing:  
1. **OpenSSL Command-Line Approach** (manual, step-by-step)  
2. **Automated Python Script** (VS Code, runs all operations)  

Both methods implement:  
✅ **AES-128 Encryption** (ECB, CBC, CFB, OFB modes)  
✅ **RSA-2048 Digital Signatures** (SHA-1 hashing)  
✅ **Key & IV Generation**  
✅ **Signature Verification**  

---

## **📌 Approach 1: OpenSSL (Terminal Commands)**  
### **Step-by-Step Execution**  
**1️⃣ Convert Image to BMP (for consistent encryption)**
```bash
convert input.png input.bmp  # Requires ImageMagick
```

**2️⃣ AES-128 Encryption (4 Modes)**
```bash
# Generate a random 128-bit key & IV
openssl rand -hex 16 > aes_key.txt
openssl rand -hex 16 > aes_iv.txt

# Encrypt in different modes
openssl enc -aes-128-ecb -in input.bmp -out encrypted_ECB.bmp -K $(cat aes_key.txt)
openssl enc -aes-128-cbc -in input.bmp -out encrypted_CBC.bmp -K $(cat aes_key.txt) -iv $(cat aes_iv.txt)
openssl enc -aes-128-cfb -in input.bmp -out encrypted_CFB.bmp -K $(cat aes_key.txt) -iv $(cat aes_iv.txt)
openssl enc -aes-128-ofb -in input.bmp -out encrypted_OFB.bmp -K $(cat aes_key.txt) -iv $(cat aes_iv.txt)
```

**3️⃣ RSA Key Generation & Signing**
```bash
# Generate RSA-2048 keys
openssl genpkey -algorithm RSA -out private.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -pubout -in private.pem -out public.pem

# Sign CBC-encrypted image
openssl dgst -sha1 -sign private.pem -out signature.bin encrypted_CBC.bmp

# Verify signature
openssl dgst -sha1 -verify public.pem -signature signature.bin encrypted_CBC.bmp
```

---

## **📌 Approach 2: Python Script (VS Code Automation)**  
### **Single Script Execution**  
**1️⃣ Run `main.py` in VS Code**  
```python
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
import matplotlib.pyplot as plt
import os

# Converts PNG → BMP, encrypts in 4 modes, signs, and verifies
# Outputs saved in `/outputs/`
```

**2️⃣ What It Does Automatically**  
✔ Converts `input.png` → `input.bmp`  
✔ Generates **AES-128 keys & IVs**  
✔ Encrypts in **ECB, CBC, CFB, OFB**  
✔ Saves encrypted images in `/outputs/`  
✔ Generates **RSA-2048 keys**  
✔ Signs CBC-encrypted image  
✔ Verifies signature  
✔ Shows **side-by-side comparison** (original vs encrypted)  

**3️⃣ Example Output Structure**  
```
outputs/
├── encrypted_ECB.bmp
├── encrypted_CBC.bmp
├── encrypted_CFB.bmp
├── encrypted_OFB.bmp
├── aes_key.txt
├── aes_iv.txt
├── private.pem
├── public.pem
└── signature.bin
```

---

## **🔍 Key Differences**  
| Feature | OpenSSL (Manual) | Python Script (Auto) |
|---------|----------------|----------------|
| **Execution** | Terminal commands | VS Code script |
| **Steps** | Manual (copy-paste) | Fully automated |
| **Outputs** | Must organize files | Auto-saved in `/outputs/` |
| **Visualization** | None | Side-by-side image comparison |
| **Flexibility** | More control | Less manual tweaking |

---

## **🚀 Which Should You Use?**  
- **For learning/testing** → **OpenSSL commands** (see how crypto works step-by-step)  
- **For batch processing** → **Python script** (faster, automated, better for multiple files)  

---

## **📜 License**  
MIT License - Free for academic & personal use.  

---

### **🔗 References**  
- [OpenSSL Docs](https://www.openssl.org/docs/)  
- [PyCryptodome Docs](https://pycryptodome.readthedocs.io/)  

---

This version:  
✔ Clearly separates **two approaches**  
✔ Shows **terminal vs script tradeoffs**  
✔ Includes **ready-to-run commands**  
✔ Maintains **professional formatting**  

Would you like me to add **NIST randomness testing** instructions for both methods? 🚀
