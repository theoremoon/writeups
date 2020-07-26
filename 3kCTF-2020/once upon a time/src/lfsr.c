/*
    Modified version of Matthew Darnell code
*/
#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
#include <lfsr.h>


void setup_lfsr(struct lfsr *l, int *num_bits, int *taps)
{
  BIT bit = ZERO;
  l->num_bits = *num_bits;
  l->contents = (BYTE*)malloc(*num_bits * sizeof(BYTE));
  memset(l->contents, bit, *num_bits * sizeof(BYTE));
  bit = ONE;
  memset(l->contents + *num_bits - 1, bit, sizeof(BYTE));

  int i;
  l->taps = (int*)malloc(*num_bits * sizeof(BYTE));
  memset(l->taps, 0, *num_bits * sizeof(BYTE));
  for(i=0; i<*num_bits; i++){
    if(taps[i] == 1){
        l->taps[i] = 1;
    }
  }
}

void init_with_key(struct lfsr *lf_arr[], int num_lfsrs, BYTE *b)
{
  int i,j;
  BYTE *temp_key = b;
  for(i=0; i<num_lfsrs; i++){
    struct lfsr *l = lf_arr[i];
    for(j=0; j<l->num_bits; j++){
      if(j == l->num_bits - 4){
        l->contents[j] = 1;
      }
      else{
        l->contents[j] = *temp_key;
        temp_key++;
      }
    }
  }
}

void print_lfsr(struct lfsr *l)
{
  int i, count = l->num_bits;
  printf("|");
  for (i=0; i<count; i++){
    printf("%d|", l->contents[i]);
  }
  printf("\n");
  for (i=count; i>0; i--){
    if(l->taps[i-1] == 1){
    printf("%d| ", i);
    }
    else{
      printf(" ");
    }
  }
  printf("\n");
}


BIT shift_lfsr(struct lfsr *l)
{
  int i;
  BYTE xor[l->num_bits];
  memset(xor, 0, l->num_bits * sizeof(BYTE));

  int index, count_taps = 0;

  for(i = l->num_bits; i > 0; i--){    //Get Tap Values into xor array
    index = l->num_bits - (i-1);
    if(l->taps[index - 1] == 1){
      //printf("Adding Tap at index: [%d] value(%d), count_taps now %d\n", index, l->contents[l->num_bits - index], count_taps + 1);
      xor[count_taps] = l->contents[l->num_bits - index];
      count_taps++;
    }
  }
  for(i=l->num_bits; i > 0; i--){      //Shift values 1 to the right
    l->contents[i] = l->contents[i-1];
  }
  //print_lfsr(l);
  int dNewBit = xor[0];
  for(i=1; i<count_taps; i++){
    //printf("%d ^ %d = %d\n", dNewBit, xor[i],   dNewBit ^ xor[i]);
    dNewBit ^= xor[i];
  }
  BIT new_bit = dNewBit == 1 ? ONE : ZERO;

  l->contents[0] = new_bit;

  //printf("\n\n");
  return new_bit;
}


void get_next_byte(struct lfsr *l, BIT b[8])
{
  int i;
  for(i=0; i<8; i++){
    b[i] = shift_lfsr(l);
    //print_lfsr(l);
    //printf("%d", b[i]);
  }
  //printf("\n");
}
