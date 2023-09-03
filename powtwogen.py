def powtwogen(max):
    n = 0
    while n < max:
        yield 2**n
        n += 1

for x in powtwogen(4):
    print x