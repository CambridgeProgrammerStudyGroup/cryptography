#include "common.h"

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


typedef ERROR (ENCRYPT_FN)(
  const unsigned char* plaintext,
  const int plaintext_length,
  OUT unsigned char* ciphertext,
  const int ciphertext_limit,
  OUT int* encrypted_bytes
);

typedef ERROR (DECRYPT_FN)(
  const unsigned char* ciphertext,
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

Cipher CipherInit(
  Mode mode,
  Primitive cipher,
  Padding padding_mode,
  const unsigned char* key,
  const unsigned char* iv
);

const unsigned char* error_string(ERROR);

void log_error(ERROR);
