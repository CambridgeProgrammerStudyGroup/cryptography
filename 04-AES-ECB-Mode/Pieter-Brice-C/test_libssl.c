// #include <stdio.h>
#include <string.h>
#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>

/*
 * Implement CBC mode
 *
 * CBC mode is a block cipher mode that allows us to encrypt
 * irregularly-sized messages, despite the fact that a block
 * cipher natively only transforms individual blocks.
 *
 * In CBC mode, each ciphertext block is added to the next
 * plaintext block before the next call to the cipher core.
 *
 * The first plaintext block, which has no associated previous
 * ciphertext block, is added to a "fake 0th ciphertext block"
 * called the initialization vector, or IV.
 *
 * Implement CBC mode by hand by taking the ECB function you
 * wrote earlier, making it encrypt instead of decrypt (verify
 * this by decrypting whatever you encrypt to test), and using
 * your XOR function from the previous exercise to combine them.
 *
 * The file here is intelligible (somewhat) when CBC decrypted
 * against "YELLOW SUBMARINE" with an IV of all ASCII 0
 * (\x00\x00\x00 &c)
 */

static const int BLOCK_SIZE = 16;
static const int NO_PADDING = 0;

void handleErrors(void){
  ERR_print_errors_fp(stderr);
  abort();
}

int encrypt_block(const unsigned char* plaintext, const unsigned char* key, unsigned char* ciphertext){
  EVP_CIPHER_CTX *ctx;
  int outlen, tmplen;

  // Create and initialise the context
  if(!(ctx = EVP_CIPHER_CTX_new())){
    handleErrors();
  }

  // Initialises context with cipher
   if(1 != EVP_EncryptInit_ex(ctx, EVP_aes_128_ecb(), NULL, key, NULL)){
     handleErrors();
   }

   // Don't PCKS5 pad
   EVP_CIPHER_CTX_set_padding(ctx, NO_PADDING);

   // Encrypt plaintext
   if(1 != EVP_EncryptUpdate(ctx, ciphertext, &outlen , plaintext, BLOCK_SIZE)){
     handleErrors();
   }

   // Finalise the encryption.
   if(1 != EVP_EncryptFinal_ex(ctx, ciphertext + outlen, &tmplen)){
     handleErrors();
   }

   // Clean up
   EVP_CIPHER_CTX_free(ctx);

   return outlen;
}

int decrypt_block(const unsigned char* ciphertext, const unsigned char* key, unsigned char* plaintext){
  EVP_CIPHER_CTX *ctx;
  int outlen, tmplen;

  // Create and initialise the context
  if(!(ctx = EVP_CIPHER_CTX_new())){
    handleErrors();
  }

  // Initialises context with cipher
   if(1 != EVP_DecryptInit_ex(ctx, EVP_aes_128_ecb(), NULL, key, NULL)){
     handleErrors();
   }

   // Don't PCKS5 pad
   EVP_CIPHER_CTX_set_padding(ctx, NO_PADDING);

   // Encrypt plaintext
   if(1 != EVP_DecryptUpdate(ctx, plaintext, &outlen , ciphertext, BLOCK_SIZE)){
     handleErrors();
   }

   // Finalise the encryption.
   if(1 != EVP_DecryptFinal_ex(ctx, plaintext + outlen, &tmplen)){
     handleErrors();
   }

   // Clean up
   EVP_CIPHER_CTX_free(ctx);

   return outlen;
}

void print_hex(const unsigned char *s){
  while(*s)
    printf("%02x ", (unsigned int) *s++);
}

void decrypt_ecb(
  const unsigned char* ciphertext,
  const unsigned char* key,
  const int len,
  unsigned char* plaintext
){
  for( int offset = 0; offset < len; offset+=BLOCK_SIZE){
    decrypt_block(ciphertext+offset, key, plaintext+offset);
  }
}
// ➤ echo -n "TO BE OR NOT TO " | openssl enc -e -aes-128-ecb -nosalt -nopad -K "59454c4c4f57205355424d4152494e45"| xxd
// 0000000: f1f3 5e74 1d4b 2bbb f82e 7f7c d1a2 b60f  ..^t.K+....|....

void test_basic(){
  unsigned char original[] = "TO BE OR NOT TO ";
  unsigned char key[]   = "YELLOW SUBMARINE";

  unsigned char ciphertext[64];
  unsigned char plaintext[64];
  memset(ciphertext, 0, 64);
  memset(plaintext, 0, 64);

  printf("ORIGINAL: >%s<\n", original);
  printf("ORIGINAL: ");print_hex(original);printf("\n");
  encrypt_block(original, key, ciphertext);
  decrypt_block(ciphertext, key, plaintext);
  printf("CIPHERTEXT: ");print_hex(ciphertext);printf("\n");
  printf("PLAINTEXT: ");print_hex(plaintext);printf("\n");
  printf("PLAINTEXT: >%s<\n", plaintext);
}

long read_to_buffer(const char* filename, unsigned char** buffer){
  long length;
  FILE * f = fopen (filename, "rb");

  if (f){
    fseek (f, 0, SEEK_END);
    length = ftell (f);
    fseek (f, 0, SEEK_SET);
    *buffer = malloc (length);
    if (*buffer)
    {
      fread (*buffer, 1, length, f);
    }
    fclose (f);
  }
  return length;
}

int main (int argc, char** agrv){
  // test_basic();
  unsigned char * buffer = NULL;
  long length = read_to_buffer("aes-test.dat", &buffer);
  unsigned char* plaintext = calloc(length, sizeof(unsigned char));

  if (buffer){
    decrypt_ecb(buffer, (unsigned char *)"YELLOW SUBMARINE", length, plaintext);
    printf("PLAINTEXT: >%s<\n", plaintext);
    free(buffer);
  }
  free(plaintext);

  return 0;
}
