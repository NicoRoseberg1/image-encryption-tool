from PIL import Image
import numpy as np
import os
import random
from datetime import datetime

class ImageEncryptor:
    def __init__(self):
        self.supported_formats = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']
        
    def load_image(self, image_path):
        try:
            img = Image.open(image_path)
            # Convert to RGB if not already
            if img.mode != 'RGB':
                img = img.convert('RGB')
            return np.array(img)
        except Exception as e:
            print(f"Error loading image: {e}")
            return None
    
    def save_image(self, image_array, output_path):
        try:
            # Ensure values are in valid range
            img_array = np.clip(image_array, 0, 255).astype(np.uint8)
            img = Image.fromarray(img_array)
            img.save(output_path)
            print(f"Image saved to: {output_path}")
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False
    
    def encrypt_xor(self, image_array, key):
        key = key % 256  # Ensure key is in byte range
        encrypted = np.bitwise_xor(image_array, key)
        return encrypted
    
    def decrypt_xor(self, encrypted_array, key):
        # XOR is symmetric
        return self.encrypt_xor(encrypted_array, key)
    
    def encrypt_math(self, image_array, shift_value):
        shift = shift_value % 256
        encrypted = (image_array.astype(np.int16) + shift) % 256
        return encrypted.astype(np.uint8)
    
    def decrypt_math(self, encrypted_array, shift_value):
        shift = shift_value % 256
        decrypted = (encrypted_array.astype(np.int16) - shift) % 256
        return decrypted.astype(np.uint8)
    
    def encrypt_scramble(self, image_array, seed=None):
        if seed is None:
            seed = random.randint(0, 1000000)
        
        random.seed(seed)
        height, width, channels = image_array.shape
        flat = image_array.flatten()
        indices = list(range(len(flat)))
        random.shuffle(indices)
        
        scrambled = flat[indices].reshape(image_array.shape)
        return scrambled, seed
    
    def decrypt_scramble(self, scrambled_array, seed):
        random.seed(seed)
        height, width, channels = scrambled_array.shape
        flat = scrambled_array.flatten()
        indices = list(range(len(flat)))
        
        # Get the shuffled order
        shuffled_indices = indices.copy()
        random.shuffle(shuffled_indices)
        
        # Reverse the shuffle
        reverse_indices = [0] * len(shuffled_indices)
        for i, idx in enumerate(shuffled_indices):
            reverse_indices[idx] = i
        
        decrypted = flat[reverse_indices].reshape(scrambled_array.shape)
        return decrypted
    
    def encrypt_combined(self, image_array, key, shift, seed=None):
        # Step 1: XOR encryption
        result = self.encrypt_xor(image_array, key)
        
        # Step 2: Mathematical operation
        result = self.encrypt_math(result, shift)
        
        # Step 3: Pixel scrambling
        result, scramble_seed = self.encrypt_scramble(result, seed)
        
        # Store all keys for decryption
        keys = {
            'xor_key': key,
            'shift_value': shift,
            'scramble_seed': scramble_seed
        }
        
        return result, keys
    
    def decrypt_combined(self, encrypted_array, keys):
        # Reverse order of encryption
        # Step 3 reverse: Unscramble
        result = self.decrypt_scramble(encrypted_array, keys['scramble_seed'])
        
        # Step 2 reverse: Mathematical operation
        result = self.decrypt_math(result, keys['shift_value'])
        
        # Step 1 reverse: XOR
        result = self.decrypt_xor(result, keys['xor_key'])
        
        return result


def main():
    encryptor = ImageEncryptor()
    
    print("=" * 60)
    print("        IMAGE ENCRYPTION TOOL")
    print("        Pixel Manipulation Based")
    print("=" * 60)
    
    while True:
        print("\nSelect an option:")
        print("1. Encrypt image (XOR)")
        print("2. Decrypt image (XOR)")
        print("3. Encrypt image (Mathematical)")
        print("4. Decrypt image (Mathematical)")
        print("5. Encrypt image (Pixel Scrambling)")
        print("6. Decrypt image (Pixel Scrambling)")
        print("7. Encrypt image (Combined method)")
        print("8. Decrypt image (Combined method)")
        print("9. Exit")
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == '9':
            print("Thank you for using the Image Encryption Tool!")
            break
        
        if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
            # Get input file path
            input_path = input("Enter input image path: ").strip()
            
            if not os.path.exists(input_path):
                print("Error: File not found!")
                continue
                
            # Load image
            print("Loading image...")
            image_array = encryptor.load_image(input_path)
            if image_array is None:
                continue
            
            # Generate output path
            base, ext = os.path.splitext(input_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if choice in ['1', '3', '5', '7']:  # Encryption
                output_path = f"{base}_encrypted_{timestamp}{ext}"
                
                if choice == '1':  # XOR
                    try:
                        key = int(input("Enter encryption key (0-255): ").strip())
                        key = key % 256
                        print("Encrypting...")
                        result = encryptor.encrypt_xor(image_array, key)
                        print(f"Encryption key: {key} (remember this for decryption)")
                    except ValueError:
                        print("Invalid key! Using default key 42")
                        key = 42
                        result = encryptor.encrypt_xor(image_array, key)
                
                elif choice == '3':  # Mathematical
                    try:
                        shift = int(input("Enter shift value (0-255): ").strip())
                        shift = shift % 256
                        print("Encrypting...")
                        result = encryptor.encrypt_math(image_array, shift)
                        print(f"Shift value: {shift} (remember this for decryption)")
                    except ValueError:
                        print("Invalid shift! Using default shift 50")
                        shift = 50
                        result = encryptor.encrypt_math(image_array, shift)
                
                elif choice == '5':  # Scrambling
                    seed_input = input("Enter seed (optional, press Enter for random): ").strip()
                    seed = int(seed_input) if seed_input else None
                    print("Encrypting...")
                    result, seed = encryptor.encrypt_scramble(image_array, seed)
                    print(f"Scramble seed: {seed} (remember this for decryption)")
                
                elif choice == '7':  # Combined
                    try:
                        key = int(input("Enter XOR key (0-255): ").strip()) % 256
                        shift = int(input("Enter shift value (0-255): ").strip()) % 256
                        seed_input = input("Enter scramble seed (optional, press Enter for random): ").strip()
                        seed = int(seed_input) if seed_input else None
                        print("Encrypting with combined method...")
                        result, keys = encryptor.encrypt_combined(image_array, key, shift, seed)
                        print("\n=== ENCRYPTION KEYS (SAVE THESE) ===")
                        print(f"XOR Key: {keys['xor_key']}")
                        print(f"Shift Value: {keys['shift_value']}")
                        print(f"Scramble Seed: {keys['scramble_seed']}")
                        print("=====================================")
                    except ValueError:
                        print("Invalid input! Using default values.")
                        result, keys = encryptor.encrypt_combined(image_array, 42, 50, None)
                        print("\n=== ENCRYPTION KEYS (SAVE THESE) ===")
                        print(f"XOR Key: {keys['xor_key']}")
                        print(f"Shift Value: {keys['shift_value']}")
                        print(f"Scramble Seed: {keys['scramble_seed']}")
                        print("=====================================")
                
                # Save encrypted image
                encryptor.save_image(result, output_path)
                print("Encryption completed successfully!")
            
            else:  # Decryption
                output_path = f"{base}_decrypted_{timestamp}{ext}"
                
                if choice == '2':  # XOR Decrypt
                    try:
                        key = int(input("Enter the encryption key used: ").strip())
                        key = key % 256
                        print("Decrypting...")
                        result = encryptor.decrypt_xor(image_array, key)
                    except ValueError:
                        print("Invalid key! Using default key 42")
                        key = 42
                        result = encryptor.decrypt_xor(image_array, key)
                
                elif choice == '4':  # Mathematical Decrypt
                    try:
                        shift = int(input("Enter the shift value used: ").strip())
                        shift = shift % 256
                        print("Decrypting...")
                        result = encryptor.decrypt_math(image_array, shift)
                    except ValueError:
                        print("Invalid shift! Using default shift 50")
                        shift = 50
                        result = encryptor.decrypt_math(image_array, shift)
                
                elif choice == '6':  # Scrambling Decrypt
                    try:
                        seed = int(input("Enter the scramble seed used: ").strip())
                        print("Decrypting...")
                        result = encryptor.decrypt_scramble(image_array, seed)
                    except ValueError:
                        print("Invalid seed! Cannot decrypt without correct seed.")
                        continue
                
                elif choice == '8':  # Combined Decrypt
                    try:
                        key = int(input("Enter XOR key used: ").strip()) % 256
                        shift = int(input("Enter shift value used: ").strip()) % 256
                        seed = int(input("Enter scramble seed used: ").strip())
                        keys = {
                            'xor_key': key,
                            'shift_value': shift,
                            'scramble_seed': seed
                        }
                        print("Decrypting with combined method...")
                        result = encryptor.decrypt_combined(image_array, keys)
                    except ValueError:
                        print("Invalid input! Cannot decrypt without correct keys.")
                        continue
                
                # Save decrypted image
                encryptor.save_image(result, output_path)
                print("Decryption completed successfully!")
        
        else:
            print("Invalid choice! Please select 1-9.")


if __name__ == "__main__":
    # Check if PIL is installed
    try:
        import PIL
    except ImportError:
        print("Error: Pillow library is required.")
        print("Install it using: pip install Pillow")
        exit(1)
    
    try:
        import numpy as np
    except ImportError:
        print("Error: NumPy library is required.")
        print("Install it using: pip install numpy")
        exit(1)
    
    main()