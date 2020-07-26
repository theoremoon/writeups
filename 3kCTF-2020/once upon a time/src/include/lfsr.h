/*
    Modified version of Matthew Darnell code
*/
#ifndef LFSR_H_
#define LFSR_H_
#include <bits.h>
struct lfsr {
  int num_bits;
  BYTE *contents;
  int *taps;
};
void print_lfsr(struct lfsr*);
void setup_lfsr(struct lfsr*, int*, int*);
void init_with_key(struct lfsr* lf_arr[], int, BYTE*);
BIT shift_lfsr(struct lfsr*);
void get_next_byte(struct lfsr*, BIT b[8]);
#endif
