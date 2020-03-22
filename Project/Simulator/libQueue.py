# hashcode2020

class LibQueue:
    """This is a linked list to simulate a queue for library sign-up.
    It is iterable"""
    def __init__(self, head=None):
        self.head = head
        self.tail = head
        self.current = head
    
    def insert(self, library):
        if not self.head:
            self.head = library
            self.tail = library
        else:
            library.previous = self.tail
            self.tail.next = library
            self.tail = library
    
    def removeFromTop(self):
        assert self.head, 'Queue is empty!'
        temp = self.head
        self.head = temp.next
        temp = None
        if self.head:
            self.head.previous = None
        else:
            self.tail = None
    
    def isEmpty(self):
        return not self.head

    def __iter__(self):
        return self

    def __next__(self):
        if not self.current:
            raise StopIteration
        else:
            item = self.current
            self.current = self.current.next
            return item
