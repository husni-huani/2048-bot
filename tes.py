def count_set_bits(n): 
    count = 0
    while (n): 
        count += n & 1
        n >>= 1
    return count 

bit = 250

print(bin(bit)[2:], count_set_bits(bit))

