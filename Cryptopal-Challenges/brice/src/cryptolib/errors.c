#include <stdlib.h>
#include <stdio.h>

#include "api.h"
#include "errors.h"

typedef struct {
  ERROR error;
  char* message;
} ErrorMessage;

static ErrorMessage Errors[] = {
  {OK, "Everything OK"},
  {OPENSSL_ERROR, "Caught openssl exception"},
  {IV_PROVIDED_IN_ERROR, "IV was provided for a block cipher mode that doesn't need it."},
  {LIMIT_TOO_SMALL, "Size limit of output buffer was too small. Try again with a bigger buffer."},
  {UNKNOWN_FATAL, "Fatal unknown error occured."},
  {OK, NULL}

};

const unsigned char* error_string(ERROR status){
  for(int i = 0; Errors[i].message != NULL; i++){
    if(status == Errors[i].error){
      return (const unsigned char*) Errors[i].message;
    }
  }
  return (const unsigned char*) "Unknown error status.";
}
void log_error(ERROR status){
  fprintf(stderr, "[CRYPTOLIB/ERROR]: %s\n", error_string(status));
};
