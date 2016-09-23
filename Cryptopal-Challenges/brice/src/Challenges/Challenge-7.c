#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include "../utils.h"
#include "../cryptolib/api.h"

int main(){
  ERROR status = OK;

  /* For example: */
  Cipher AES_ECB = CipherInit(
    MODE_ECB(),
    RIJNDAEL_128_128(),
    PKCS7(),
    (const bytes) "YELLOW SUBMARINE",
    (const bytes) "I AM AN INIT VEC"
  );


  bytes original = (bytes)"My big secret";
  int original_length = strlen((char *)original);

  int ciphertext_limit = 64;
  unsigned char ciphertext[ciphertext_limit];
  int encrypted_bytes = 0;

  if(OK != (status = AES_ECB.encrypt(original, original_length, ciphertext, ciphertext_limit, &encrypted_bytes))){
    log_error(status);
    exit(1);
  };

  int plaintext_limit = 64;
  unsigned char plaintext[plaintext_limit];
  int decrypted_bytes = 0;

  if(OK != (status = AES_ECB.decrypt(ciphertext, encrypted_bytes, plaintext, plaintext_limit, &decrypted_bytes))){
    log_error(status);
    exit(1);
  };

  printf("ORIGINAL: ");print_hex(original);printf("\n");
  printf("CIPHERTEXT: ");print_hex(ciphertext);printf("\n");
  printf("PLAINTEXT: ");print_hex(plaintext);printf("\n");
}
