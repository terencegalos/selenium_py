def all_even():
    n = 0
    while True:
        yield n + 2
        n += 2



a = all_even()
while True:
    print a.next()