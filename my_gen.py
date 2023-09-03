def my_gen():
    n = 1 
    yield n

    n += 1 
    yield n

    n += 1 
    yield n

for item in my_gen():
    print item