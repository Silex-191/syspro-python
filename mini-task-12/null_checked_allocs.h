#ifndef __INCLUDE_GUARD_NULL_CHECKED_ALLOCS_H_SILEX_191__
#define __INCLUDE_GUARD_NULL_CHECKED_ALLOCS_H_SILEX_191__

#include <stdlib.h>

/*--------------------------------------------------------*/
/*     Allocation and reallocation with null checkers     */
/*     The size is specified in bytes                     */
/*--------------------------------------------------------*/


void* nc_malloc(size_t size);

void* nc_calloc(size_t number_of_blocks, size_t size_of_block);

void* nc_realloc(void* ptr, size_t new_size);

#endif /*  __INCLUDE_GUARD_NULL_CHECKED_ALLOCS_H_SILEX_191__  */
