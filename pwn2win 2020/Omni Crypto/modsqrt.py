def sqrt_power_of_2_mod(a, n):
    assert a % 8 == 1

    res = []
    for x in [1, 3]:
        for k in range(3, n):
            i = ((x*x - a) // pow(2, k)) % 2
            x = x + i * pow(2, k-1)

        res.append(x)
        res.append(2**n - x)
    return res

