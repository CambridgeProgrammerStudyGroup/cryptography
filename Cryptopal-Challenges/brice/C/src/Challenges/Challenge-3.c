#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "../cryptolib/api.h"
#include "../cryptolib/errors.h"
#include "../../test/common.h"
#include "../cryptolib/tools/frequencies.h"

long get_english_fingerprint(double fingerprint[256]){
  unsigned char* buffer = NULL;
  long corpus_len = 0;
  corpus_len = read_to_buffer("./data/COLLECTED_ENGLISH_CORPUS.txt", &buffer);
  normalised_freq(buffer, corpus_len, fingerprint);
  printf("Read %li corpus bytes.\n", corpus_len);
  free(buffer);
  // print_frequencies(english_fingerprint);
  return corpus_len;
}

int main(int argc, char** args){
  printf("=== Challenge-3: Break one byte XOR cipher ===\n");
  int challenge_status = SUCCESS;
  ERROR status = OK;
  char* ciphertext_h = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736";
  printf("Ciphertext: %s\n", ciphertext_h);

  /* Get the fingerprint for english */
  double english_fingerprint[256] = {0.0};
  long corpus_len = get_english_fingerprint(english_fingerprint);

  /* Get raw ciphertext */
  int limit = 256;
  int length = 0;
  bytes ciphertext = calloc(limit, 1);
  if( OK != (status = fromHex((const bytes) ciphertext_h, strlen(ciphertext_h), ciphertext, limit, &length))){
    log_error(status); exit(1);
  };

  /* Get best score */
  double best_score = -10.0;
  char best_candidate = '\0';
  for (int n = 0; n < 256; n++){
    char* key = malloc(length);
    memset(key,n,length);

    bytes maybe_plaintext = calloc(limit,1);
    xor(ciphertext, key, length, maybe_plaintext);
    // printf("0x%02x: %s\n", n, maybe_plaintext);
    double this_score = score(maybe_plaintext, length, english_fingerprint);
    if(this_score>best_score){
      best_score = this_score;
      best_candidate = (char) n;
    }
    free(key);
    free(maybe_plaintext);
  }

  /* Print the best solution out */
  bytes plaintext = calloc(limit,1);
  char* key = malloc(length);
  memset(key,best_candidate,length);
  xor(ciphertext, key, length, plaintext);
  printf("Best score was %f with '0x%02x'/'%c': \"%s\"\n", best_score, best_candidate, best_candidate, plaintext);

  free(ciphertext);
  free(plaintext);
  free(key);
  return challenge_status;
}
