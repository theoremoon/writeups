/*
    Modified version of Matthew Darnell code
*/
#include <adder.h>
void half_add(BIT one, BIT two, BIT *carry, BIT *sum)
{
    *carry = one & two;
    *sum   = one ^ two;
}

void full_add(BIT one, BIT two, BIT carry_in, BIT *carry_out, BIT *sum)
{
    BIT temp_carry, temp_carry_two;
    half_add(one, two, &temp_carry, sum);
    temp_carry_two = *sum & carry_in;
    *sum ^= carry_in;
    *carry_out = temp_carry | temp_carry_two;
}

void sum_bytes(BIT *one, BIT *two, BIT carry_in, BIT *sum, BIT *carry_out)
{
    *carry_out=  carry_in;
    int i;
    for(i=7; i>=0; i--){
        full_add(one[i], two[i], *carry_out, carry_out, &(sum[i]));
    }
}
