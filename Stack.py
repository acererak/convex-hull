from seq import seq, empty, seqWith

class StackEmptyError(Exception):
    pass

class Stack:

    def __init__(self):
        self.contents = empty

    def push(self,x):
        self.contents = seqWith(x,self.contents)

    def pop(self):
        if self.contents:
            t = self.top
            self.contents = self.contents.tail
            return t
        else:
            raise StackEmptyError

    @property
    def top(self):
        if self.contents:
            return self.contents.head
        else:
            raise StackEmptyError

    def isEmpty(self):
        return self.contents.isEmpty()

    def __repr__(self):
        if self.isEmpty():
            return ']'
        else:
            s = '(' + str(self.top) + ')'
            xs = self.contents.tail
            while not xs.isEmpty():
                s = s + ' ' + str(xs.head)
                xs = xs.tail
            s = s + ']'
            return s

    __str__ = __repr__
