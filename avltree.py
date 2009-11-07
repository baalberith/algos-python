from bstree import BSNode, BSTree

class AVLNode(BSNode):
  def __init__(self, key, value, parent = None, left = None, right = None, depth = 0):
    BSNode.__init__(self, key, value, parent, left, right)
    self.depth = depth
    
  def _depth(self):
    left_depth = self.left.depth if self.left != None else -1
    right_depth = self.right.depth if self.right != None else -1
    return 1 + max(left_depth, right_depth)
    
  def _update_depth(self):
    self.depth = self._depth()
    
  def _balance(self):
    left_depth = self.left.depth if self.left != None else -1
    right_depth = self.right.depth if self.right != None else -1
    return left_depth - right_depth
    
class AVLTree(BSTree):
  def __init__(self):
    BSTree.__init__(self)
    
  def _rebalance(self, node):
    while node != self.null:
      node._update_depth()
      if node._balance() == 2:
        if node.left != self.null and node.left._balance() > 0:
          self._rotate_right(node)
        else:
          self._rotate_left(node.left)
          self._rotate_right(node)
      elif node._balance() == -2:
        if node.right != self.null and node.right._balance() < 0:
          self._rotate_left(node)
        else:
          self._rotate_right(node.right)
          self._rotate_left(node)        
      node = node.parent    
    
  def _insert(self, curr, key, value):
    node = AVLNode(key, value, curr, self.null, self.null)
    if curr == self.null:
      self.root = node
    elif node.key < curr.key:
      curr.left = node
    else:
      curr.right = node
    self._rebalance(node.parent)
      
  def _delete(self, node):
    if node.left == self.null or node.right == self.null:
      curr = node
    else:
      curr = self._successor(node)
    if curr.left != self.null:
      child = curr.left
    else:
      child = curr.right
    if child != self.null:
      child.parent = curr.parent
    if curr.parent == self.null:
      self.root = child
    elif curr is curr.parent.left:
      curr.parent.left = child
    else:
      curr.parent.right = child
    if node != curr:
      node.key, node.value = curr.key, curr.value
    self._rebalance(curr.parent)
      
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
    node._update_depth()
    right._update_depth()
    
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
    node._update_depth()
    left._update_depth()    
     
  def _balance(self, node):
    if node == None:
      return 0
    else:
      return self._depth(node.left) - self._depth(node.right)
    
  def balance(self):
    return self._balance(self.root)
    
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
      
      tree = AVLTree()
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
      #print 'balance:', tree.balance()
      
      assert tree.list() == array
      assert tree.dict() == dictionary
      assert len(tree) == len(array)
      assert tree.min() == min(array)[1] 
      assert tree.max() == max(array)[1]
      assert tree.depth() == tree.root._depth()
      assert tree.balance() == tree.root._balance()
      
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