import base64
from utils import *

if __name__ == "__main__":
    with open("../data/7.txt") as fp:
        ct = base64.b64decode(fp.read())
        print( AES_ECB_decrypt("YELLOW SUBMARINE", ct))
