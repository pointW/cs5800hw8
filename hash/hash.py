import urllib
import string
import sys


MAX_HASH = 10000


def hash_function(string):
    h = 0
    for c in string:
        h = 101 * h + ord(c)
    return h % MAX_HASH


class Node:
    def __init__(self, key, value, nxt=None):
        self.key = key
        self.value = value
        self.nxt = nxt

    def delete(self, key):
        if self.nxt is None:
            return
        elif self.nxt.key == key:
            self.nxt = self.nxt.nxt
        else:
            self.nxt.delete(key)

    def find(self, key):
        if self.key == key:
            return self.value
        elif self.nxt is None:
            return None
        else:
            return self.nxt.find(key)

    def increase(self, key):
        if self.key == key:
            self.value += 1
        elif self.nxt is None:
            return
        else:
            self.nxt.increase(key)

    def list_all_keys(self):
        if self.nxt is None:
            return [self.key]
        else:
            return [self.key] + self.nxt.list_all_keys()


class HashTable:
    def __init__(self):
        self._list = [None] * MAX_HASH

    def delete(self, key):
        h = hash_function(key)
        head = self._list[h]
        if head is None:
            return
        elif head.key == key:
            self._list[h] = head.nxt
        else:
            head.delete(key)

    def find(self, key):
        h = hash_function(key)
        head = self._list[h]
        if head is None:
            return None
        return self._list[h].find(key)

    def increase(self, key):
        h = hash_function(key)
        head = self._list[h]
        if head is None:
            return
        head.increase(key)

    def insert(self, key, value):
        if self.find(key) is not None:
            raise KeyError(key)
        h = hash_function(key)
        head = self._list[h]
        new_head = Node(key, value, head)
        self._list[h] = new_head

    def list_all_keys(self):
        keys = reduce(lambda x, y: x + y.list_all_keys() if y is not None else x,
                      self._list,
                      [])
        # print keys
        return keys

    def print_all_pairs(self):
        for key in self.list_all_keys():
            print key, self.find(key)


def test():
    link = 'http://www.ccs.neu.edu/home/vip/teach/Algorithms//7_hash_RBtree_simpleDS/hw_hash_RBtree/alice_in_wonderland.txt'
    f = urllib.urlopen(link)
    text = f.read()
    strings = text.split()
    strings = filter(lambda x: x is not '', map(lambda x: x.translate(None, string.punctuation).lower(), strings))
    hash_table = HashTable()
    for s in strings:
        if hash_table.find(s) is not None:
            hash_table.increase(s)
        else:
            hash_table.insert(s, 1)

    orig_stdout = sys.stdout
    f = open('output.txt', 'w')
    sys.stdout = f

    hash_table.print_all_pairs()

    sys.stdout = orig_stdout
    f.close()


# hash_table = HashTable()
# hash_table.insert('abc', 1)
# hash_table.insert('aaa', 1)
# hash_table.increase('abc')
# print hash_table.find('abc')
# hash_table.delete('aaa')
# hash_table.list_all_keys()

test()