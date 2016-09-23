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
  {BAD_INPUT, "Bad input provided to function."},
  {OPENSSL_ERROR, "Caught openssl exception"},
  {IV_PROVIDED_IN_ERROR, "IV provided while not needed."},
  {LIMIT_TOO_SMALL, "Size limit of output buffer was too small."},
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
