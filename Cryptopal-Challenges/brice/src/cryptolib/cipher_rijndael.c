#include <string.h>

#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>

#include "common.h"
#include "api.h"

static const int NO_PADDING = 0;
static const int BLOCK_SIZE = 16;

void handleErrors(void){
  ERR_print_errors_fp(stderr);
  abort();
}

ERROR aes_encrypt_block(const bytes plaintext, const bytes key, OUT bytes ciphertext){
  EVP_CIPHER_CTX *ctx;
  int outlen, tmplen;

  // Create and initialise the context
  if(!(ctx = EVP_CIPHER_CTX_new())){
    handleErrors(); return OPENSSL_ERROR;
  }

  // Initialises context with cipher
   if(1 != EVP_EncryptInit_ex(ctx, EVP_aes_128_ecb(), NULL, key, NULL)){
     handleErrors(); return OPENSSL_ERROR;
   }

   // Don't PCKS5 pad
   EVP_CIPHER_CTX_set_padding(ctx, NO_PADDING);

   // Encrypt plaintext
   if(1 != EVP_EncryptUpdate(ctx, ciphertext, &outlen , plaintext, BLOCK_SIZE)){
     handleErrors(); return OPENSSL_ERROR;
   }

   // Finalise the encryption.
   if(1 != EVP_EncryptFinal_ex(ctx, ciphertext + outlen, &tmplen)){
     handleErrors(); return OPENSSL_ERROR;
   }

   // Clean up
   EVP_CIPHER_CTX_free(ctx);
   return OK;
}

ERROR aes_decrypt_block(const bytes ciphertext, const bytes key, OUT bytes plaintext){
  EVP_CIPHER_CTX *ctx;
  int outlen, tmplen;

  // Create and initialise the context
  if(!(ctx = EVP_CIPHER_CTX_new())){
    handleErrors(); return OPENSSL_ERROR;
  }

  // Initialises context with cipher
   if(1 != EVP_DecryptInit_ex(ctx, EVP_aes_128_ecb(), NULL, key, NULL)){
     handleErrors(); return OPENSSL_ERROR;
   }

   // Don't PCKS5 pad
   EVP_CIPHER_CTX_set_padding(ctx, NO_PADDING);

   // Encrypt plaintext
   if(1 != EVP_DecryptUpdate(ctx, plaintext, &outlen , ciphertext, BLOCK_SIZE)){
     handleErrors(); return OPENSSL_ERROR;
   }

   // Finalise the encryption.
   if(1 != EVP_DecryptFinal_ex(ctx, plaintext + outlen, &tmplen)){
     handleErrors(); return OPENSSL_ERROR;
   }

   // Clean up
   EVP_CIPHER_CTX_free(ctx);
   return OK;

}


static const Primitive rijndael_128_128 = {
  128,
  128,
  &aes_encrypt_block,
  &aes_decrypt_block
};

Primitive RIJNDAEL_128_128(void){ return rijndael_128_128; }
