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

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>

#include "utils.h"
#include "common.h"


static const int NO_PADDING = 0;
static const int BLOCK_SIZE = 16;

void handleErrors(void){
  ERR_print_errors_fp(stderr);
  abort();
}

void aes_encrypt_block(const unsigned char* plaintext, const unsigned char* key, unsigned char* ciphertext){
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
}

void aes_decrypt_block(const unsigned char* ciphertext, const unsigned char* key, unsigned char* plaintext){
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

}


void test_basic_block_encryption(){
  unsigned char original[] = "TO BE OR NOT TO ";
  unsigned char key[]   = "YELLOW SUBMARINE";

  unsigned char ciphertext[64];
  unsigned char plaintext[64];
  memset(ciphertext, 0, 64);
  memset(plaintext, 0, 64);

  printf("ORIGINAL: >%s<\n", original);
  printf("ORIGINAL: ");print_hex(original);printf("\n");
  aes_encrypt_block(original, key, ciphertext);
  aes_decrypt_block(ciphertext, key, plaintext);
  printf("CIPHERTEXT: ");print_hex(ciphertext);printf("\n");
  printf("PLAINTEXT: ");print_hex(plaintext);printf("\n");
  printf("PLAINTEXT: >%s<\n", plaintext);
}


void decrypt_ecb(
  const unsigned char* ciphertext,
  const unsigned char* key,
  const int len,
  unsigned char* plaintext
){
  for( int offset = 0; offset < len; offset+=BLOCK_SIZE){
    aes_decrypt_block(ciphertext+offset, key, plaintext+offset);
  }
}


int main (int argc, char** agrv){
  // test_basic_block_encryption();
  unsigned char * ciphertext = NULL;
  long length = read_to_buffer("aes-test.dat", &ciphertext);

  if (!ciphertext){
    printf("No ciphertext found!\n");
    return 1;
  }

  unsigned char* plaintext = calloc(length, sizeof(unsigned char)+BLOCK_SIZE+BLOCK_SIZE);

  if(!plaintext){
    printf("Calloc returned null for some reason o_O?\n");
    free(ciphertext);
    return 1;
  }

  decrypt_ecb(ciphertext, (unsigned char *)"YELLOW SUBMARINE", length, plaintext);
  printf(">>%s\n", plaintext);

  free(plaintext);
  free(ciphertext);
  return 0;
}
