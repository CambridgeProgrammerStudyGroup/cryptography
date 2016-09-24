#include <string.h>
#include <stdio.h>

#include "../common.h"

static const double english_fingerprint[256];

void normalised_freq(
  const bytes in,
  const int len,
  double frequencies[256]
);

double score(
  const bytes buffer,
  const int len,
  double fingerprint[256]
);

void print_frequencies(double freq[256]);
