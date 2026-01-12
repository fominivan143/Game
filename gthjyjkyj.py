from random import choices, sample, shuffle, random, randrange, randint, uniform


a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
print(round(uniform(0.12, 0.81), 2))
print(randrange(0, 100, 12)) #100 не включено, 0 включено
print(randint(1, 6)) #6 включено, 1 включено, шага нет
print(choices(a, k=5))
print(sample(a, 10))
shuffle(a)
print(a)
print(round(random(), 2))