Cryptography
============

This repository is for all the work done on Cryptography as part of the [Cambridge Programmer's Study Group](http://www.meetup.com/Cambridge-Programmers-Study-Group/).

## Classical cryptography

 - [US Army Field Manual 34-40-2: Basic Cryptanalysis](http://www.umich.edu/~umich/fm-34-40-2/)
 - [Classical Cryptography (Wikipedia)](https://en.wikipedia.org/wiki/Classical_cipher)
 - [Cryptanalysis of ADFGVX cipher](http://link.springer.com/chapter/10.1007%2F3-540-39568-7_26#page-1)
 - [Practical Cryptography](http://practicalcryptography.com/)

## Modern Cryptography

 - [Block ciphers modes of operation](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation)
 - The [notes in the Libtomcrypt library](https://github.com/libtom/libtomcrypt/tree/develop/notes) contain test vectors, and many practical implementation guidelines. The Libtomcrypt code also seems to be beginner friendly.
 - [Clear explanation of the Padding Oracle Attack with examples](http://robertheaton.com/2013/07/29/padding-oracle-attack/)
 - [Set of modern crypto challenges](http://cryptopals.com/)
 - [Thorough speed test of common crypto libraries](https://panthema.net/2008/0714-cryptography-speedtest-comparison/) Note well, this excludes the more recent [NaCl](https://nacl.cr.yp.to/) and [NSS](https://developer.mozilla.org/en-US/docs/Mozilla/Projects/NSS).

## Command Line help

### Strings and Hexadecimal

Using `xxd` to convert a string to Hexadecimal. Note how we use `echo`'s `-n` option to not print a newline at the end.

```bash
 ➤ echo -n "Hello" | xxd -p
 48656c6c6f
```

Converting hex back to string (which will not include a newline):

```bash
 ➤ echo -n "48656c6c6f" | xxd -p -r
 Hello
 ```

### Strings and base 64

Same idea, but for base 64:

```bash
➤ echo -n "Hello" | base64
SGVsbG8=
➤ echo -n "SGVsbG8=" | base64 --decode
Hello
```

### Using OPENSSL to test your code on the command line

Let's set up our key and plaintext

```bash
➤ PLAINTEXT="YELLOWFIN TUNAS." # Exactly 16 characters (128 bits)
➤ KEY="YELLOW SUBMARINE" # Exactly 16 characters (128 bits)
➤ HEX_KEY=$(echo $KEY | xxd -p)
```

Then we can encrypt and decrypt using openssl. We'll need to tell openssl to **not add a salt and to not pad our plaintext** using the `-nopad` and `-nosalt` option. We'll use `-aes-128-ecb` as a simple test.

```bash
➤ CIPHERTEXT=$(echo -n ${PLAINTEXT} | openssl enc -aes-128-ecb -nopad -nosalt -K ${HEX_KEY} )
➤ echo -n ${CIPHERTEXT} | openssl enc -d -aes-128-ecb -nopad -nosalt -K ${HEX_KEY}
YELLOWFIN TUNAS.
```

Using a file is just as easy:

```bash
➤  base64 --decode < secret-lyrics.txt | openssl enc -d -aes-128-ecb -nopad -nosalt -K $(echo -n "YELLOW SUBMARINE" | xxd -p)
I'm back and I'm ringin' the bell
[...many more lines...]
Play that funky music
```
