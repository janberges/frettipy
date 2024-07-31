#!/usr/bin/env python3

w = 80
h = 36

nobr = {'end': ''}

for i in range(h)[::-1]:
    y = (-1.5 * (h - i) + 1.5 * i) / h
    for j in range(w):
        x = (-2.1 * (w - j) + 0.9 * j) / w
        c = x + 1j * y

        z = 0.0
        for n in range(16):
            z = z * z + c
            if abs(z) > 6:
                print('%x' % n,
                    **nobr) # print number of iterations as hexadecimal number
                break
        else:
            print(' ', **nobr)
    print(flush=True)
