#include <stdio.h>
#include <stdlib.h>

// #include "utils.h"

void print_hex(const unsigned char *s){
  while(*s)
    printf("%02x", (unsigned int) *s++);
}

void print_hex_c(const unsigned char *s, int len){
  for(int i = 0; i <len; i++){
    printf("%02x", (unsigned int) s[i]);
  }
}

long read_to_buffer(const char* filename, unsigned char** buffer){
  long length = 0;
  FILE * f = fopen (filename, "rb");

  if (f == NULL){
    fprintf(stderr, "[FATAL]: File '%s' could not be opened.\n", filename);
    exit(1);
  }

  fseek (f, 0, SEEK_END);
  length = ftell (f);

  if(length < 0){
    fprintf(stderr, "[FATAL]: Could not read length of '%s'.\n", filename);
  }

  fseek (f, 0, SEEK_SET);
  *buffer = malloc (length+1);

  if (*buffer == NULL){
    fprintf(stderr, "[FATAL]: Failed to allocate memory while reading file.");
    fclose(f);
    exit(1);
  }

  fread (*buffer, 1, length, f);
  fclose (f);

  return length;
}
