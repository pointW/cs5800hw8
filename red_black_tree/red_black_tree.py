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
        self.insert_fixup(z)

    def insert_fixup(self, z):
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
    tree.insert(r4)
    tree.insert(r5)
    tree.insert(r7)
    tree.insert(r8)
    tree.insert(r11)
    tree.insert(r14)







test_insert()
