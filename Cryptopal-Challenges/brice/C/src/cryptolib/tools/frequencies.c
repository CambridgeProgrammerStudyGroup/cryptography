#include <stdio.h>
#include <math.h>

#include "../common.h"
#include "frequencies.h"



void normalised_freq(const bytes in, const int len, double frequencies[256]){
  int total = 0;
  for(int i = 0; i < len; i++){
    frequencies[in[i]] += 1;
    total++;
  }
  for(int j = 0; j < 256; j++){
    frequencies[j]/=total;
  }
}

void print_frequencies(double freq[256]){
  char* bar = "================================";
  double barlen = (double) strlen(bar);
  for(int i = 'a'; i<='z'; i++){
    char c = (32<=i && i <= 126)?i:' ';
    printf("[%c]%.*s\n",c,(int)floor(freq[i]*barlen*10.0), bar);
  }

}

double score(const bytes buffer, const int len, double fingerprint[256]){
  /* Use sum of squares as score.
   * Make negative to have best score be maximum.
   */
  double freqs[256] = {0};
  normalised_freq(buffer, len, freqs);
  double sum = 0;
  for(int i=0; i<256; i++){
    double difference = fingerprint[i] - freqs[i];
    sum+= difference*difference;
  }
  return -sum;
}
