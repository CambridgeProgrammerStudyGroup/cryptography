
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
  corpus_len = read_to_buffer("../data/COLLECTED_ENGLISH_CORPUS.txt", &buffer);
  normalised_freq(buffer, corpus_len, fingerprint);
  printf("Read %li corpus bytes.\n", corpus_len);
  free(buffer);
  // print_frequencies(english_fingerprint);
  return corpus_len;
}

char* mkKey(char c, const int len){
  char* key = malloc(len);
  memset(key,c,len);
  return key;
}

char best_xor_key(
  const bytes ciphertext,
  int length,
  double fingerprint[256],
  OUT double* out_score
){
  double best_score = -100.0;
  char best_candidate = '\0';

  char* key = malloc(length);
  bytes maybe_plaintext = calloc(length,1);
  for (int n = 0; n < 256; n++){
    memset(key,n,length);
    xor(ciphertext, key, length, maybe_plaintext);
    double this_score = score(maybe_plaintext, length, fingerprint);
    if(this_score>best_score){
      best_score = this_score;
      best_candidate = (char) n;
    }
  }
  *out_score = best_score;
  free(key);
  free(maybe_plaintext);
  return best_candidate;
}


typedef struct Node {
  struct Node* next;
  bytes item;
  long item_length;
  double score;
  char keyChar;
} Node;

Node* splitLinesFromHexIntoBytes(char* buffer, long len){
  const char *delim = "\r\n";
  char *token = strtok(buffer, delim);
  Node* head = NULL;
  Node* current = NULL;

  while(token != NULL) {
      int limit = 256;
      int length = 0;
      bytes ciphertext = calloc(limit, 1);
      fromHex((const bytes) token, strlen(token), ciphertext, limit, &length);
      // printf("found token: %s\n", token);
      Node* new_node = malloc(sizeof(Node));
      new_node->item = ciphertext;
      new_node->next = NULL;
      new_node->keyChar = '\0';
      new_node->score = -1000.0;
      new_node->item_length = length;
      if(current != NULL){
        current->next = new_node;
        current = new_node;
      }else{
        head = new_node;
        // printf("Head's at: %p\n", head);
        current = new_node;
      }
      token = strtok(NULL, delim);
  }
  return head;
}

const static int BUFSIZE = 256;
int main(int argc, char** args){
  printf("=== Challenge-4: Detect Single Character XOR ===\n");
  int challenge_status = SUCCESS;
  ERROR status = OK;

  /* Get the fingerprint for english */
  double english_fingerprint[256] = {0.0};
  long corpus_len = get_english_fingerprint(english_fingerprint);

  /* Read in the exrcise file into a buffer */
  unsigned char* buffer = NULL;
  long input_len = 0;
  input_len = read_to_buffer("../data/challenge-4.txt", &buffer);

  if(buffer == NULL){
    fprintf(stderr, "[FATAL]: Could not read data file!");
    exit(1);
  }

  Node* all_candidates = splitLinesFromHexIntoBytes(buffer, input_len);

  Node* best_node = all_candidates;

  Node* current = all_candidates;
  while(current){
    current->keyChar = best_xor_key(
      current->item,
      current->item_length,
      english_fingerprint,
      &(current->score)
    );

    if(current->score > best_node->score){
      best_node = current;
    }
    current = current->next;
  }



  char* key = mkKey(best_node->keyChar, best_node->item_length);

  char* plaintext = calloc(BUFSIZE, 1);
  xor(best_node->item, key, best_node->item_length, plaintext);

  printf("[%f] with key '0x%02x' <<%s>> original:", best_node->score, best_node->keyChar, plaintext);
  print_hex_c(best_node->item, best_node->item_length);
  printf("\n");

  free(plaintext);
  free(buffer);
  free(key);

  current = all_candidates;
  while(current){
    Node* next = current->next;
    free(current->item);
    free (current);
    current = next;
  }


  /* Get raw ciphertext */
  // int limit = 256;
  // int length = 0;
  // bytes ciphertext = calloc(limit, 1);
  // if( OK != (status = fromHex((const bytes) ciphertext_h, strlen(ciphertext_h), ciphertext, limit, &length))){
  //   log_error(status); exit(1);
  // };

  /* Get best score */
  // double best_score = -10.0;
  // char best_candidate = '\0';
  // for (int n = 0; n < 256; n++){
  //   char* key = malloc(length);
  //   memset(key,n,length);
  //
  //   bytes maybe_plaintext = calloc(limit,1);
  //   xor(ciphertext, key, length, maybe_plaintext);
  //   // printf("0x%02x: %s\n", n, maybe_plaintext);
  //   double this_score = score(maybe_plaintext, length, english_fingerprint);
  //   if(this_score>best_score){
  //     best_score = this_score;
  //     best_candidate = (char) n;
  //   }
  //   free(key);
  //   free(maybe_plaintext);
  // }

  /* Print the best solution out */
  // bytes plaintext = calloc(limit,1);
  // char* key = malloc(length);
  // memset(key,best_candidate,length);
  // xor(ciphertext, key, length, plaintext);
  // printf("Best score was %f with '0x%02x'/'%c': \"%s\"\n", best_score, best_candidate, best_candidate, plaintext);


  return challenge_status;
}
