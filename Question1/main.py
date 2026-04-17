import os

def main():

    base_dir = os.path.dirname(os.path.abspath(__file__))

    def generate_maps(shift1, shift2):
        encrypt_map = {}

        # lowercase a-m
        for i in range(13):                          
            enc_char = chr((i + shift1 * shift2) % 13 + 97)
            encrypt_map[chr(97 + i)] = enc_char
    
        # lowercase n-z
        for i in range(13):
            enc_char = chr((i - (shift1 + shift2)) % 13 + 110)
            encrypt_map[chr(110 + i)] = enc_char

        # uppercase A-M
        for i in range(13):
            enc_char = chr((i - shift1) % 13 + 65)
            encrypt_map[chr(65 + i)] = enc_char

        # uppercase N-Z
        for i in range(13):                          
            enc_char = chr((i + shift2 ** 2) % 13 + 78)
            encrypt_map[chr(78 + i)] = enc_char

        decrypt_map = {v: k for k, v in encrypt_map.items()}
        return encrypt_map, decrypt_map

    def encrypt(text, shift1, shift2):
        enc_map, _ = generate_maps(shift1, shift2)
        return "".join(enc_map.get(ch, ch) for ch in text)

    def decrypt(text, shift1, shift2):
        _, dec_map = generate_maps(shift1, shift2)
        return "".join(dec_map.get(ch, ch) for ch in text)

    def verify():
        with open(os.path.join(base_dir, "raw_text.txt"), "r") as f:
            original = f.read()
        with open(os.path.join(base_dir, "decrypted_text.txt"), "r") as f:
            recovered = f.read()
        if original == recovered:
            print("Verification successful: decrypted text matches the original.")
        else:
            print("Verification failed: texts do not match.")

    # create raw_text.txt if it doesn't exist
    if not os.path.exists(os.path.join(base_dir, "raw_text.txt")):
        with open(os.path.join(base_dir, "raw_text.txt"), "w") as f:
            f.write("Hello World! This is a Test File: A-M, N-Z, a-m, n-z. 12345\n"
                    "Special chars: @#$%\n")

    try:
        s1 = int(input("Enter Shift 1: "))
        s2 = int(input("Enter Shift 2: "))
    except ValueError:
        print("Invalid input — integers required.")
        return

    # read
    with open(os.path.join(base_dir, "raw_text.txt"), "r") as f:
        raw = f.read()

    # encrypt
    cipher = encrypt(raw, s1, s2)
    with open(os.path.join(base_dir, "encrypted_text.txt"), "w") as f:
        f.write(cipher)

    # decrypt
    recovered = decrypt(cipher, s1, s2)
    with open(os.path.join(base_dir, "decrypted_text.txt"), "w") as f:
        f.write(recovered)

    # verify
    verify()


if __name__ == "__main__":
    main()