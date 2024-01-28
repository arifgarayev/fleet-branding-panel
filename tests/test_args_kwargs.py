def myFunc(*args, **kwargs):
    print(*args)
    print("----------")
    print(kwargs)


myFunc(1, 2, 3, 4, 5, ar=12, ga=21)
