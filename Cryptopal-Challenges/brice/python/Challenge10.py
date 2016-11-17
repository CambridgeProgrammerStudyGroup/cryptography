import utils
import base64

if __name__ == "__main__":
    IV = bytearray([0]*16)
    KEY = "YELLOW SUBMARINE"
    with open("../data/10.txt") as fp:
        CIPHERTEXT = base64.b64decode(fp.read())

    PLAINTEXT = utils.AES_CBC_decrypt(KEY, CIPHERTEXT, IV)
    ENCRYPTED = utils.AES_CBC_encrypt(KEY, PLAINTEXT, IV)

    assert CIPHERTEXT == ENCRYPTED

    print( PLAINTEXT[:200]+"..." )
