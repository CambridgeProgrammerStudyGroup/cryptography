
#define OUT /**/

typedef enum {
  OK,
  IV_PROVIDED_IN_ERROR,
  LIMIT_TOO_SMALL,
  UNKNOWN_FATAL
} ERROR;

typedef ERROR (ENCRYPT_BLOCK)(
  const unsigned char* key,
  const unsigned char* plainblock,
  OUT unsigned char* cipherblock
);

typedef ERROR (DECRYPT_BLOCK)(
  const unsigned char* key,
  const unsigned char* cipherblock,
  OUT unsigned char* plainblock
);

typedef ERROR (PAD_FN)(
  const int block_size,
  const int text_length, /*The length of the text to be padded*/
  unsigned char* text, /* Pointer to the text buffer, which should be allocated as a multiple of block_size */
  const int text_limit
);

typedef ERROR (DEPAD_FN)(
  const int block_size,
  unsigned char* text, /* Pointer to the text buffer, We're going to 'depad' by overwriting the padding with '\0' */
  const int text_limit
);

typedef struct {
  int block_size;
  int key_size;
  ENCRYPT_BLOCK* encrypt;
  DECRYPT_BLOCK* decrypt;
} Primitive;

typedef struct {
  PAD_FN* pad;
  DEPAD_FN* depad;
} Padding;

typedef ERROR (MODE_ENCRYPT)(
  const Primitive* cipher,
  const Padding* padding,
  const unsigned char* key,
  const unsigned char* iv,
  const unsigned char* plaintext,
  const int plaintext_length,
  OUT unsigned char* ciphertext,
  const int ciphertext_limit
);

typedef ERROR (MODE_DECRYPT)(
  const Primitive* cipher,
  const Padding* padding,
  const unsigned char* key,
  const unsigned char* iv,
  const unsigned char* ciphertext,
  const int ciphertext_length,
  OUT unsigned char* plaintext,
  const int plaintext_limit
);

typedef struct {
  MODE_ENCRYPT* encrypt;
  MODE_DECRYPT* decrypt;
} Mode;
