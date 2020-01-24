
# Note: This Queue class is sub-optimal. Why?
class Queue():
    def __init__(self):
        self.ssize=0
        self.head=None
        self.tail=None

    def enqueue(self, data):
        if self.ssize>0:
            self.tail.next=LinkedPair(data)
            self.tail=self.tail.next
        else:
            temp=LinkedPair(data)
            self.tail=temp
            self.head=temp
        self.ssize+=1

    def dequeue(self):
        if not self.head:
            return None
        else:
            self.ssize-=1
            temp=self.head.data
            self.head=self.head.next
            return temp

    def size(self):
        return self.ssize

class LinkedPair:
    def __init__(self, data, next=None):
        self.data=data
        self.next=next

    def __repr__(self):
        return f'{self.data}'

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

