from nonparentbstree import BSNode, BSTree
RED, BLACK = True, False

def _is_red(node):
  return node != None and node.color == RED  

class RBNode(BSNode):
  def __init__(self, key, value):
    BSNode.__init__(self, key, value)
    self.color = RED
    
class RBTree(BSTree):
  def __init__(self):
    BSTree.__init__(self)
    
  def _insert(self, curr, key, value):
    if curr == None:
      return RBNode(key, value)
    else:
      if key == curr.key:
        curr.value = value
      elif key < curr.key:
        curr.left = self._insert(curr.left, key, value)
      else:
        curr.right = self._insert(curr.right, key, value)
      if _is_red(curr.right) and not _is_red(curr.left):
        curr = self._rotate_left(curr)
      if _is_red(curr.left) and _is_red(curr.left.left):
        curr = self._rotate_right(curr)
      if _is_red(curr.left) and _is_red(curr.right):
        self._flip_color(curr)
      return curr
      
  def __setitem__(self, key, value):
    self.root = self._insert(self.root, key, value)
    self.root.color = BLACK
    
  def _delete(self, curr, key):
    if key < curr.key:
      if not _is_red(curr.left) and not _is_red(curr.left.left):
        curr = self._move_red_left(curr)
      curr.left = self._delete(curr.left, key)
    else:
      if _is_red(curr.left):
        curr = self._rotate_right(curr)
      if key == curr.key and curr.right == None:
        return None
      if not _is_red(curr.right) and not _is_red(curr.right.left):
        curr = self._move_red_right(curr)
      if key == curr.key:
        minimum = self._min(curr.right)
        curr.key, curr.value = minimum.key, minimum.value
        curr.right = self._delete_min(curr.right)
      else:
        curr.right = self._delete(curr.right, key)
    return self._delete_fixup(curr)

  def __delitem__(self, key):
    if key in self:
      self.root = self._delete(self.root, key)
      if self.root != None:
        self.root.color = BLACK
    else:
      raise KeyError
    
  def _flip_color(self, curr):
    curr.color = not curr.color
    curr.left.color = not curr.left.color
    curr.right.color = not curr.right.color   
  
  def _rotate_left(self, curr):
    right = curr.right
    curr.right = right.left
    right.left = curr
    right.color = curr.color
    curr.color = RED
    return right
    
  def _rotate_right(self, curr):
    left = curr.left
    curr.left = left.right
    left.right = curr    
    left.color = curr.color
    curr.color = RED
    return left 
    
  def _move_red_right(self, node):
    self._flip_color(node)
    if _is_red(node.left.left):
      node = self._rotate_right(node)
      self._flip_color(node)
    return node
      
  def _move_red_left(self, node):
    self._flip_color(node)
    if _is_red(node.right.left):
      node.right = self._rotate_right(node.right)
      node = self._rotate_left(node)
      self._flip_color(node)   
    return node      
      
  def _delete_fixup(self, node):
    if _is_red(node.right):
      node = self._rotate_left(node)
    if _is_red(node.left) and _is_red(node.left.left):
      node = self._rotate_right(node)
    if _is_red(node.left) and _is_red(node.right): 
      self._flip_color(node)
    return node
    
  def _delete_max(self, curr):
    if _is_red(curr.left):
      curr = self._rotate_right(curr)
    if curr.right == None:
      return None
    if not _is_red(curr.right) and not _is_red(curr.right.left):
      curr = self._move_red_right(curr)
    curr.left = self._delete_max(curr.left)
    return self._delete_fixup(curr)
    
  def _delete_min(self, curr):
    if curr.left == None:
      return None
    if not _is_red(curr.left) and not _is_red(curr.left.left):
      curr = self._move_red_left(curr)
    curr.left = self._delete_min(curr.left)
    return self._delete_fixup(curr)
    
if __name__ == '__main__':
  def test(tests = 10, num = 256, ran = 1000000):
    from random import randint, shuffle
    depth = []
    
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
      depth.append(tree.depth())
      
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
      
    print 'depth:', (sum(depth) / tests), 'min:', min(depth), 'max:', max(depth)
      
  test()        