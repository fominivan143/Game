class MinMaxWordFinder:
    def __init__(self):
        self.mini = []
        self.maxi = []
        self.sp = []

    def add_sentence(self, s):
        k = s.strip()
        a = k.replace('    ', '')
        m = a.split(' ')
        for el in m:
            el = el.strip()
            self.sp.append(el)

    def shortest_words(self):
        sp1 = sorted(self.sp, key=lambda x: len(x))
        if sp1 == []:
            return sp1
        t = len(sp1[0])
        for i in range(len(sp1)):
            if len(sp1[i]) == t:
                self.mini.append(sp1[i])
        self.mini.sort()
        return self.mini

    def longest_words(self):
        sp1 = sorted(self.sp, key=lambda x: len(x))
        if sp1 == []:
            return sp1
        d = len(sp1[-1])
        for i in range(len(sp1)):
            if len(sp1[len(sp1) - 1 - i]) == d:
                self.maxi.append(sp1[len(sp1) - 1 - i])
        self.maxi = set(self.maxi)
        self.maxi = list(self.maxi)
        self.maxi.sort()
        return self.maxi


finder = MinMaxWordFinder()
finder.add_sentence('')
print(' '.join(finder.shortest_words()))
print(' '.join(finder.longest_words()))

finder.add_sentence('bb cc    dd')
finder2 = MinMaxWordFinder()
print(' '.join(finder2.shortest_words()))
print(' '.join(finder2.longest_words()))

print(' '.join(finder.shortest_words()))
print(' '.join(finder.longest_words()))

finder2.add_sentence('bbb ccc    ddc')
finder.add_sentence('zzzz')
finder.add_sentence('p q r')

print(' '.join(finder2.shortest_words()))
print(' '.join(finder2.longest_words()))

print(' '.join(finder.shortest_words()))
print(' '.join(finder.longest_words()))

print(' '.join(finder2.shortest_words()))
print(' '.join(finder2.longest_words()))
