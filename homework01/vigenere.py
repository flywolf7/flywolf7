import caesar


def encrypt_vigenere(word, key_word):
    if len(word) > len(key_word):  # Увеличение длины ключа
        for i in range(len(word)):
            key_word += key_word[i]
    key_word = key_word.upper()

    ciphertext = ""
    for i in range(len(word)):
        char = word[i]
        shift = ord(key_word[i]) - ord("A")
        ciphertext += caesar.encrypt_caesar(char, shift)

    return ciphertext


def decrypt_vigenere(word, key_word):
    if len(word) > len(key_word):  # Увеличение длины ключа
        for i in range(len(word)):
            key_word += key_word[i]
    key_word = key_word.upper()

    plaintext = ""
    for i in range(len(word)):
        char = word[i]
        shift = ord(key_word[i]) - ord("A")
        plaintext += caesar.decrypt_caesar(char, shift)

    return plaintext

