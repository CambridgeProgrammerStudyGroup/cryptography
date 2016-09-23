#ifndef CRYPTOLIB_API_INCLUDED
#define CRYPTOLIB_API_INCLUDED

#include "common.h"
#include "errors.h"

typedef ERROR (ENCRYPT_FN)(
  const bytes plaintext,
  const int plaintext_length,
  OUT unsigned char* ciphertext,
  const int ciphertext_limit,
  OUT int* encrypted_bytes
);

typedef ERROR (DECRYPT_FN)(
  const bytes ciphertext,
  const int ciphertext_length,
  OUT unsigned char* plaintext,
  const int plaintext_limit,
  OUT int* decrypted_bytes
);

typedef struct {
  unsigned char* key;
  unsigned char* iv;
  ENCRYPT_FN* encrypt;
  DECRYPT_FN* decrypt;
} Cipher;

/*
 * Crypto primitives
 */
Primitive RIJNDAEL_128_128(void);

/*
 * Block cipher modes of operation
 */
Mode MODE_ECB(void);
Mode MODE_CBC(void);

/*
 * Available ciphers
 */
Cipher AES_128_128(void);

/*
 * Available padding modes
 */
Padding PKCS7(void);

Cipher CipherInit(
  Mode mode,
  Primitive cipher,
  Padding padding_mode,
  bytes key,
  bytes iv
);

ERROR toBase64(
  const bytes raw,
  const int raw_length,
  OUT unsigned char* base64,
  const int base64_limit,
  OUT int* out_length
);
ERROR fromBase64(
  const unsigned char* base64,
  const int base64_length,
  OUT bytes raw,
  const int raw_limit,
  OUT int* out_length
);

ERROR toHex(
  const bytes raw,
  const int raw_length,
  OUT unsigned char* hex,
  const int hex_limit,
  OUT int* out_length
);

ERROR fromHex(
  const unsigned char* hex,
  const int hex_length,
  OUT bytes raw,
  const int raw_limit,
  OUT int* out_length
);

ERROR xor(
  const bytes A,
  const bytes B,
  const int len,
  OUT bytes out
);

#endif
