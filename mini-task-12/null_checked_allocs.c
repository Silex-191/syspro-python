#include <stdio.h>
#include <stdlib.h>

/*--------------------------------------------------------*/
/*     Allocation and reallocation with null checkers     */
/*     The size is specified in bytes                     */
/*--------------------------------------------------------*/


void* nc_malloc(size_t size) {
  void* result = malloc(size);
  if (result == NULL) {
    printf("OUT OF MEMORY!\n");
    exit(1);
  }
  return result;
}

void* nc_calloc(size_t number_of_blocks, size_t size_of_block) {
  void* result = calloc(number_of_blocks, size_of_block);
  if (result == NULL) {
    printf("OUT OF MEMORY!\n");
    exit(1);
  }
  return result;
}

void* nc_realloc(void* ptr, size_t new_size) {
  void* result = realloc(ptr, new_size);
  if (result == NULL) {
    printf("OUT OF MEMORY!\n");
    exit(1);
  }
  return result;
}
