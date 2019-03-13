class Enum:
    dic = {}
    def __init__(self, *args):
        for i in range(0, len(args)):
            self.dic[args[i]] = i

    def __getitem__(self, item):
        return self.dic[item]

    def __getattr__(self, item):
        return self.dic[item]
