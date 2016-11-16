import utils
import base64

if __name__ == "__main__":
    IV = bytearray([0]*16)
    KEY = "YELLOW SUBMARINE"
    with open("../data/10.txt") as fp:
        CIPHERTEXT = base64.b64decode(fp.read())

    PLAINTEXT = utils.CBC_AES_decrypt(CIPHERTEXT, KEY, IV)
    ENCRYPTED = utils.CBC_AES_encrypt(PLAINTEXT, KEY, IV)

    assert CIPHERTEXT == ENCRYPTED

    print( PLAINTEXT[:200]+"..." )
