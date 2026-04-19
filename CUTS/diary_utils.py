# Vigenere cipher utility - for encrypting personal notes
def vigenere_encrypt(text, key):
    result = []
    key = key.lower()
    ki = 0
    for c in text:
        if c.isalpha():
            shift = ord(key[ki % len(key)]) - ord('a')
            if c.isupper():
                result.append(chr((ord(c) - ord('A') + shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(c) - ord('a') + shift) % 26 + ord('a')))
            ki += 1
        else:
            result.append(c)
    return ''.join(result)
