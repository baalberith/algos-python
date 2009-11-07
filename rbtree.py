from bstree import BSNode, BSTree

class RBNode(BSNode):
  def __init__(self, key, value, parent = None, left = None, right = None, color = 'red'):
    BSNode.__init__(self, key, value, parent, left, right)
    self.color = color
    
class RBTree(BSTree):
  def __init__(self):
    self.null = RBNode(None, None, color = 'black')
    self.null.left = self.null.right = self.null
    self.null.parent = self.null
    self.root = self.null
    
  def _ins(self, node):
    while node != self.root and node.parent.color == 'red':
      if node.parent is node.parent.parent.left:
        uncle = node.parent.parent.right
        if uncle.color == 'red':
          node.parent.color = 'black'
          uncle.color = 'black'
          node.parent.parent.color = 'red'
          node = node.parent.parent
        else:
          if node is node.parent.right:
            node = node.parent
            self._rotate_left(node)
          node.parent.color = 'black'
          node.parent.parent.color = 'red'
          self._rotate_right(node.parent.parent)
      else:
        uncle = node.parent.parent.left
        if uncle.color == 'red':
          node.parent.color = 'black'
          uncle.color = 'black'
          node.parent.parent.color = 'red'
          node = node.parent.parent
        else:
          if node is node.parent.left:
            node = node.parent
            self._rotate_right(node)
          node.parent.color = 'black'
          node.parent.parent.color = 'red'
          self._rotate_left(node.parent.parent)
    self.root.color = 'black'
    
  def _insert(self, curr, key, value):
    node = RBNode(key, value, curr, self.null, self.null)
    if curr == self.null:
      self.root = node
    elif node.key < curr.key:
      curr.left = node
    else:
      curr.right = node
    self._ins(node)
    
  def _del(self, node):
    while node != self.root and node.color == 'black':
      if node is node.parent.left:
        sibling = node.parent.right
        if sibling.color == 'red':
          sibling.color = 'black'
          node.parent.color = 'red'
          self._rotate_left(node.parent)
          sibling = node.parent.right
        if sibling.left.color == 'black' and sibling.right.color == 'black':
          sibling.color = 'red'
          node = node.parent
        else:
          if sibling.right.color == 'black':
            sibling.left.color = 'black'
            sibling.color = 'red'
            self._rotate_right(sibling)
            sibling = node.parent.right
          sibling.color = node.parent.color
          node.parent.color = 'black'
          sibling.right.color = 'black'
          self._rotate_left(node.parent)
          node = self.root
      else:
        sibling = node.parent.left
        if sibling.color == 'red':
          sibling.color = 'black'
          node.parent.color = 'red'
          self._rotate_right(node.parent)
          sibling = node.parent.left
        if sibling.left.color == 'black' and sibling.right.color == 'black':
          sibling.color = 'red'
          node = node.parent
        else:
          if sibling.left.color == 'black':
            sibling.right.color = 'black'
            sibling.color = 'red'
            self._rotate_left(sibling)
            sibling = node.parent.left
          sibling.color = node.parent.color
          node.parent.color = 'black'
          sibling.left.color = 'black'
          self._rotate_right(node.parent)
          node = self.root
    node.color = 'black'
      
  def _delete(self, node):
    if node.left == self.null or node.right == self.null:
      curr = node
    else:
      curr = self._successor(node)
    if curr.left != self.null:
      child = curr.left
    else:
      child = curr.right
    child.parent = curr.parent
    if curr.parent == self.null:
      self.root = child
    elif curr is curr.parent.left:
      curr.parent.left = child
    else:
      curr.parent.right = child
    if node != curr:
      node.key, node.value = curr.key, curr.value
    if curr.color == 'black':
      self._del(child)
      
  def _rotate_left(self, node):
    right = node.right
    node.right = right.left
    if right.left != self.null:
      right.left.parent = node
    right.parent = node.parent
    if node.parent == self.null:
      self.root = right
    elif node is node.parent.left:
      node.parent.left = right
    else:
      node.parent.right = right
    right.left = node
    node.parent = right
    
  def _rotate_right(self, node):
    left = node.left
    node.left = left.right
    if left.right != self.null:
      left.right.parent = node
    left.parent = node.parent
    if node.parent == self.null:
      self.root = left
    elif node is node.parent.left:
      node.parent.left = left
    else:
      node.parent.right = left
    left.right = node
    node.parent = left   
    
if __name__ == '__main__':
  def test(tests = 10, num = 100, ran = 10000):
    from random import randint, shuffle
    depth = 0
    
    for t in range(tests):
      array = []
      for i in range(num):
        tmp = randint(1, ran)
        array.append((tmp, str(tmp)))
      dictionary = dict(array)
      
      tree = RBTree()
      for (k, v) in array:
        tree[k] = v
        #print tree[k],
      array = []
      for key in tree:
        array.append((key, tree[key]))
        #print key,
      depth += tree.depth()
      
      #tree.puts()
      #print tree.tree()
      #print tree.list()
      #print tree.dict()
      #print repr(tree)
      #print str(tree)
      #print tree.values()
      #print tree.keys() 
      #print 'size:', len(tree),
      #print 'depth:', tree.depth()
      #print 'min:', tree.min(),
      #print 'max:', tree.max()
      
      assert tree.list() == array
      assert tree.dict() == dictionary
      assert len(tree) == len(array)
      assert tree.min() == min(array)[1] 
      assert tree.max() == max(array)[1]
      
      keys = tree.keys()
      result = keys[:]
      shuffle(keys)
      for key in keys:
        assert key in tree
        del tree[key]
        result.remove(key)
        assert tree.keys() == result
      assert tree.keys() == []  
      
    print 'depth:', (depth / tests)
      
  test()