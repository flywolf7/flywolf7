import string


def encrypt_caesar(word, shift):
    abc = string.ascii_lowercase + string.ascii_uppercase

    ciphertext = ''
    for i in range(len(word)):
        char = word[i]

        if char not in abc:
            ciphertext += char
        elif char in abc[:26]:
            index = (ord(char) - ord('a') + shift) % 26
            ciphertext += chr(ord('a') + index)
        elif char in abc[26:]:
            index = (ord(char) - ord('A') + shift) % 26
            ciphertext += chr(ord('A') + index)

    return ciphertext


def decrypt_caesar(word, shift):
    abc = string.ascii_lowercase + string.ascii_uppercase

    plaintext = ""
    for i in range(len(word)):
        char = word[i]

        if char not in abc:
            plaintext += char
        elif char in abc[:26]:
            index = (ord(char) - ord('a') - shift) % 26
            plaintext += chr(ord('a') + index)
        elif char in abc[26:]:
            index = (ord(char) - ord('A') - shift) % 26
            plaintext += chr(ord('A') + index)

    return plaintext
