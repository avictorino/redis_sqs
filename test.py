


def count(n=1):
    if n > 3:
        return
    print(n)

    count(n+1)

count()