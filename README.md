# Image Encryption Tool

A Python-based image encryption tool using pixel manipulation techniques including XOR encryption, mathematical operations, and pixel scrambling.

## Features

-  **XOR Encryption**: Simple bitwise XOR operation with a key
-  **Mathematical Encryption**: Add/subtract shift values to pixels
-  **Pixel Scrambling**: Shuffle pixel positions using a seed
-  **Combined Method**: Multi-layer encryption for stronger security
-  **Multiple Format Support**: PNG, JPG, JPEG, BMP, TIFF

## Installation

```bash
# Clone the repository
git clone https://github.com/NicoRoseberg1/image-encryption-tool.git

# Navigate to project directory
cd image-encryption-tool

# Install dependencies
pip install -r requirements.txt
python image_encryptor.py

Example
Encrypt an image:
1. Select encryption method
2. Enter image path
3. Provide encryption key
4. Image will be saved as encrypted_version.jpg
Decrypt an image:
1. Select decryption method
2. Enter encrypted image path
3. Provide the same key used for encryption
4. Image will be restored
XOR Encryption
Each pixel value is XORed with a key. XOR is symmetric, so the same operation decrypts.

Mathematical Encryption
Adds a shift value to each pixel (modulo 256). Decryption subtracts the shift.

Pixel Scrambling
Flattens the image, shuffles pixel positions using a random seed, and reshapes.

Combined Method
Applies XOR, then mathematical shift, then scrambling for multi-layer security.
Requirements
Python 3.6+

Pillow

NumPy

License
MIT License

Contributing
Pull requests are welcome. For major changes, please open an issue first.

Author
Your Name - NicoRoseberg1
