class SeqEmptyError(Exception):
    pass

class SeqIndexError(IndexError):
    pass

class seq:

    def __str__(self):
        return '<' + self.asText() + '>'

    __repr__ = __str__

class empty(seq):

    def __init__(self):
        pass

    def isEmpty(self):
        return True

    def __bool__(self):
        return False

    def __eq__(self,other):
        if other:
            return False
        else:
            return True
        
    @property
    def head(self):
        raise SeqEmptyError

    @property
    def tail(self):
        raise SeqEmptyError

    def __getitem__(self,_):
        raise SeqIndexError

    def __add__(self,other):
        return other

    def __mul__(self,n):
        return self

    def __len__(self):
        return 0

    def __contains__(self,_):
        return False

    def reverseOf(self):
        return empty

    def map(self,_):
        return empty

    def filter(self,_):
        return empty

    def foldLeft(self,op,sofar):
        return sofar
        
    def foldRight(self,op,base):
        return base
                           
    def asText(self):
        return ''
    
class seqWith(seq):

    def __init__(self, h, t):
        self.head = h
        self.tail = t

    def __bool__(self):
        return True

    def __eq__(self,other):
        if other:
            return self.head == other.head \
               and self.tail == other.tail 
        else:
            return False

    def __getitem__(self,i):
        if i >= len(self):
            raise SeqIndexError
        elif i == 0:
            return self.head
        else:
            return self.tail[i-1]

    def __add__(self,other):
        return seqWith(self.head,self.tail + other)

    def __mul__(self,n):
        if n == 0:
            return empty
        else:
            return self + (self * (n-1))

    def __len__(self):
        return 1 + len(self.tail)

    def __contains__(self,x):
        return x == self.head or (x in self.tail)

    def reverseOf(self):
        rev = empty
        for x in self:
            rev = seqWith(x,rev)
        return rev

    def map(self,f):
        return seqWith(f(self.head),self.tail.map(f))

    def filter(self,p):
        otail = self.tail.filter(p)
        if p(self.head):
            return seqWith(self.head,otail)
        else:
            return otail

    def foldLeft(self,op,sofar):
        return self.tail.foldLeft(op,op(sofar,self.head))
        
    def foldRight(self,op,base):
        return op(self.head,self.tail.foldLeft(op,base))
                           
    def isEmpty(self):
        return False
    
    def asText(self):
        if self.tail:
            return str(self.head) + ', ' + self.tail.asText()
        else:
            return str(self.head)

empty = empty()

def seq(*tuple):
    xs = empty
    for x in reversed(tuple):
        xs = seqWith(x,xs)
    return xs



