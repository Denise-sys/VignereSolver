from english_quadgrams import quadgram_score
import random

specialchars = ['!', ' ', '.', ',']
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def group_info():
    """
    Prints group info
    :return: list[tuple]
    """
    return [("0996954", "Denise van Roon", "Dinf1"), ("0980696", "Stelios Stigter", "Dinf2")]

def encrypt_vigenere(plaintext, key):
    """
    :param plaintext:
    :param key:
    :return:
    """
    result = ''
    loop = True
    plaintext = list(plaintext)
    key = list(key)
    index = 0
    while loop:
        character = key[index]
        indexCharacter = alphabet.index(character)
        plaintextCharacter = plaintext.pop(0)

        if set(plaintextCharacter).issubset(set(alphabet)) or set(plaintextCharacter.lower()).issubset(set(alphabet)):
            if plaintextCharacter.isupper():
                indexPlaintextCharacter = alphabet.index(plaintextCharacter.lower())

                sum = indexPlaintextCharacter + indexCharacter
                if sum > 26:
                    sum = sum - 26
                newCharacter = alphabet[sum]
                newCharacter = newCharacter.upper()
            else:
                indexPlaintextCharacter = alphabet.index(plaintextCharacter)

                sum = indexPlaintextCharacter + indexCharacter
                if sum > 26:
                    sum = sum - 26

                newCharacter = alphabet[sum]
            index = index + 1
            if index >= len(key):
                index = 0
        else:
            newCharacter = plaintextCharacter
        result = result + newCharacter
        if len(plaintext) == 0:
            loop = False
    return str(result)

def decrypt_vigenere(ciphertext, key):
    """
    :param ciphertext:
    :param key:
    :return:
    """
    result = ''
    loop = True
    ciphertext = list(ciphertext)
    key = list(key)
    index = 0
    while loop:
        character = key[index]
        indexCharacter = alphabet.index(character)
        ciphertextCharacter = ciphertext.pop(0)

        if set(ciphertextCharacter).issubset(set(alphabet)) or set(ciphertextCharacter.lower()).issubset(set(alphabet)):
            if ciphertextCharacter.isupper():
                indexciphertextCharacter = alphabet.index(ciphertextCharacter.lower())

                sum = indexciphertextCharacter - indexCharacter
                if sum < 0:
                    sum = sum + 26
                newCharacter = alphabet[sum]
                newCharacter = newCharacter.upper()
            else:
                indexciphertextCharacter = alphabet.index(ciphertextCharacter)

                sum = indexciphertextCharacter - indexCharacter
                if sum < 0:
                    sum = sum + 26
                newCharacter = alphabet[sum]
            index = index + 1
            if index >= len(key):
                index = 0
        else:
            newCharacter = ciphertextCharacter
        result = result + newCharacter
        if len(ciphertext) == 0:
            loop = False
    return str(result)

def quadgram_fitness(text):
    """
    :param text:
    :return:
    """
    result = 0
    text = text.replace(" ", "").lower()
    loop = True
    while loop:
        substring = text[:4]
        text = text[1:]

        if substring in quadgram_score:
            result = result + quadgram_score.get(substring)
        else:
            result = result + 23

        if len(list(text)) < 4:
            loop = False
    return result

def newKey(key, keylen):
    randomNumber = random.randint(0, keylen - 1)
    randomlist = list(key)
    randomlist[randomNumber] = random.choice(alphabet)
    key = "".join(c for c in randomlist)
    return key

def solve_vigenere(ciphertext, keylen):
    minimum = ('', '', 999)
    keys = []
    maxSteps = 1000 * (keylen ** 2)
    survivalRate = 0.01
    i = 1
    key = ''.join(random.choice(alphabet) for i in range(keylen))
    bestkeysofar = ()
    while i <= maxSteps:
        decrypted = decrypt_vigenere(ciphertext, key)
        quadgram_fit = quadgram_fitness(decrypted)
        if quadgram_fit < minimum[2]:
            minimum = (decrypted, key, quadgram_fit)
            bestkeysofar = (decrypted, key)
            key = newKey(key, keylen)
        elif random.uniform(0, 1) <= survivalRate:
            bestkeysofar = (decrypted, key)
            key = newKey(key, keylen)
        i = i + 1
    return (bestkeysofar[0], bestkeysofar[1])
