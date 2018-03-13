RED = 'red'
BLACK = 'black'


class Node:
    def __init__(self, value, left=None, right=None, parent=None, color=RED):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
        self.color = color

    def __str__(self):
        return str(self.value) + ', ' + self.color


class RBTree:
    def __init__(self, root=None):
        self.nil = Node('nil', color=BLACK)
        # self.nil.parent = self.nil
        # self.nil.left = self.nil
        # self.nil.right = self.nil
        self.root = root
        if root is None:
            self.root = self.nil
        else:
            self.root.parent = self.nil
            self.root.left = self.nil
            self.root.right = self.nil

    def _left_rotate(self, x):
        if x.right is self.nil:
            return
        # move y.l to x.r
        y = x.right
        x.right = y.left
        if y.left is not self.nil:
            y.left.parent = x
        # move y to x
        y.parent = x.parent
        if x.parent is self.nil:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        # move x to y.l
        y.left = x
        x.parent = y

    def _max(self, x):
        if x.right is self.nil or x is self.nil:
            return x.value
        return self._max(x.right)

    def _min(self, x):
        if x.left is self.nil or x is self.nil:
            return x.value
        return self._min(x.left)

    def _right_rotate(self, y):
        if y.left is self.nil:
            return
        # move x.right to y.l
        x = y.left
        y.left = x.right
        if x.right is not self.nil:
            x.right.parent = y
        # move x to y
        x.parent = y.parent
        if y.parent is self.nil:
            self.root = x
        elif y is y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        # move y to x.r
        x.right = y
        y.parent = x

    def _insert_fixup(self, z):
        if z.parent is self.nil or z.parent.parent is self.nil:
            self.root.color = BLACK
            return
        while z.parent.color == RED:
            if z.parent is z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                elif z is z.parent.right:
                    z = z.parent
                    self._left_rotate(z)
                else:
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                elif z is z.parent.left:
                    z = z.parent
                    self._right_rotate(z)
                else:
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._left_rotate(z.parent.parent)
        self.root.color = BLACK

    def _search(self, x, val):
        if x is self.nil or x.value == val:
            return x
        elif x.value > val:
            return self._search(x.left, val)
        else:
            return self._search(x.right, val)

    def _sort(self, x):
        if x is not self.nil:
            return self._sort(x.left) + [x.value] + self._sort(x.right)
        return []

    def _transplant(self, u, v):
        if u.parent is self.nil:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _delete_fixup(self, x):
        while x is not self.root and x.color == BLACK:
            if x is x.parent.left:
                w = x.parent.right
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self._right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self._left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = BLACK

    def _print(self, x, height=0):
        def color(c):
            if c == RED:
                return 'r'
            return 'b'
        if x is self.nil:
            return
        print '    ' * (height-1) + '+---' * (height > 0) + str(x.value) + color(x.color)
        self._print(x.left, height+1)
        self._print(x.right, height+1)

    def _height(self, x):
        if x is self.nil:
            return 0
        return max(self._height(x.left), self._height(x.right)) + 1

    def insert(self, z):
        y = self.nil
        x = self.root
        while x is not self.nil:
            y = x
            if z.value < x.value:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y is self.nil:
            self.root = z
        elif z.value < y.value:
            y.left = z
        else:
            y.right = z
        z.left = self.nil
        z.right = self.nil
        z.color = RED
        self._insert_fixup(z)

    def max(self):
        return self._max(self.root)

    def min(self):
        return self._min(self.root)

    def search(self, val):
        return self._search(self.root, val)

    def sort(self):
        return self._sort(self.root)

    def successor(self, val):
        node = self.search(val)
        if node is self.nil:
            return None
        if node.right is not self.nil:
            return self._min(node.right)
        y = node.parent
        while y is not self.nil and node is y.right:
            node = y
            y = y.parent
        return y.value

    def predecessor(self, val):
        node = self.search(val)
        if node is self.nil:
            return None
        if node.left is not self.nil:
            return self._max(node.left)
        y = node.parent
        while y is not self.nil and node is y.left:
            node = y
            y = y.parent
        return y.value

    def delete(self, z):
        y = z
        y_original_color = y.color
        if z.left is self.nil:
            x = z.right
            self._transplant(z, z.right)
        elif z.right is self.nil:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._min(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent is z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == BLACK:
            self._delete_fixup(x)

    def print_tree(self):
        self._print(self.root)

    def height(self):
        return self._height(self.root)


def test_rotate():
    y = Node('y')
    r = Node('r', parent=y)
    x = Node('x', parent=y)
    y.left = x
    y.right = r
    a = Node('a', parent=x)
    b = Node('b', parent=x)
    x.left = a
    x.right = b
    tree = RBTree(y)
    tree._right_rotate(y)
    tree._left_rotate(x)
    print 1


def test_insert():
    r1 = Node(1)
    r2 = Node(2)
    r3 = Node(3)
    r4 = Node(4)
    r5 = Node(5)
    r7 = Node(7)
    r8 = Node(8)
    r11 = Node(11)
    r14 = Node(14)
    r15 = Node(15)
    # tree = RBTree(r11)
    # tree.insert(r2)
    # tree.insert(r14)
    # tree.insert(r1)
    # tree.insert(r7)
    # tree.insert(r15)
    # tree.insert(r5)
    # tree.insert(r8)
    # tree.insert(r4)
    tree = RBTree()
    tree.insert(r1)
    tree.insert(r2)
    tree.insert(r3)
    tree.insert(r4)
    tree.insert(r5)
    tree.insert(r7)
    tree.insert(r8)
    tree.insert(r11)
    tree.insert(r14)
    tree.print_tree()
    tree.delete(r1)
    tree.print_tree()
    tree.delete(r2)
    tree.print_tree()
    tree.delete(r4)
    tree.print_tree()
    aaaaa = 1


def main():
    in_command_loop = True
    tree = RBTree()
    while in_command_loop:
        inp = raw_input("> ")
        inp = inp.split()
        try:
            i = inp[0]
            if i == 'insert':
                a = int(inp[1])
                tree.insert(Node(a))
            elif i == 'search':
                a = int(inp[1])
                if tree.search(a) is tree.nil:
                    print 'no such node'
                else:
                    print 'node found'
            elif i == 'sort':
                print tree.sort()
            elif i == 'exit':
                tree.print_tree()
                in_command_loop = False
            elif i == 'delete':
                a = int(inp[1])
                x = tree.search(a)
                if x is tree.nil:
                    print 'no such node'
                else:
                    tree.delete(x)
            elif i == 'successor':
                a = int(inp[1])
                print tree.successor(a)
            elif i == 'predecessor':
                a = int(inp[1])
                print tree.predecessor(a)
            elif i == 'max':
                print tree.max()
            elif i == 'min':
                print tree.min()
            elif i == 'print':
                tree.print_tree()
            else:
                print 'Error'
                print 'valid commands: insert d; search d; sort; delete d; successor d; predecessor d; min; max; ' \
                      'print; exit'
            print 'height:', tree.height()
        except IndexError:
            print 'Error'


main()
