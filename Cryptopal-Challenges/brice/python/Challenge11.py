import random
from utils import *

ciphers = [AES_CBC_encrypt, AES_ECB_encrypt]

def encryption_oracle(mode=None):
    KEY = randstr(16)
    IV = randstr(16)
    prefix = randstr(random.randint(5,10))
    suffix = randstr(random.randint(5,10))
    if not mode:
        encrypt = random.choice(ciphers)
    else:
        encrypt = mode
    def encryptor(plaintext):
        return encrypt(KEY, pkcs7_pad(prefix+plaintext+suffix), IV)
    return encryptor

def predict_mode(oracle):
    chosen_plaintext = "A"*100
    ciphertext = oracle(chosen_plaintext)
    rbs = repeated_blocks(ciphertext, 16)
    if rbs > 4:
        return AES_ECB_encrypt
    else:
        return AES_CBC_encrypt

if __name__ == "__main__":
    modes = [random.choice(ciphers) for i in range(100)]
    tries = [encryption_oracle(mode) for mode in modes]
    predictions = [predict_mode(encryptor) for encryptor in tries]
    print("We can detect the correct mode {:.0%} of the time.".format(accuracy(predictions, modes)))
