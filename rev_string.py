def rev_string(str):
    length = len(str)
    for i in range(length - 1, -1 , -1):
        yield str[i]


for i in rev_string("hello"):
    print i