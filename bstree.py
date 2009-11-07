class BSNode:    
  def __init__(self, key, value, parent = None, left = None, right = None):    
    self.key = key  
    self.value = value  
    self.parent = parent
    self.left = left 
    self.right = right  
    
  def __str__(self):
    return str(self.value)
    
  def tuple(self):
    return (self.key, self.value)     
    
  def __repr__(self):
    return repr(self.tuple())   
    
class BSTree:
  def __init__(self):
    self.null = None
    self.root = self.null

  def _search(self, key):
    prev = self.null
    curr = self.root
    while curr != self.null:
      prev = curr
      if key == curr.key:
        break
      elif key < curr.key:
        curr = curr.left
      else:
        curr = curr.right
    return prev
    
  def __getitem__(self, key):
    found = self._search(key)
    if found != self.null and found.key == key:
      return found.value
    else:
      raise KeyError, 'Key %s not found!' % key
    
  def _insert(self, curr, key, value):
    node = BSNode(key, value, curr, self.null, self.null)
    if curr == self.null:
      self.root = node
    elif node.key < curr.key:
      curr.left = node
    else:
      curr.right = node
    
  def __setitem__(self, key, value):
    found = self._search(key)
    if found != self.null and found.key == key:
      found.value = value
    else:
      self._insert(found, key, value)  
      
  def _delete(self, node):
    if node.left == self.null or node.right == self.null:
      curr = node
    else:
      curr = self._predecessor(node)
      # curr = self._successor(node)
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
      
  def __delitem__(self, key):
    found = self._search(key)
    if found != self.null and found.key == key:
      self._delete(found)
    else:
      raise KeyError, 'Key %s not found!' % key      
    
  def _min(self, curr):
    while curr.left != self.null:
      curr = curr.left
    return curr

  def _max(self, curr):
    while curr.right != self.null:
      curr = curr.right
    return curr    
    
  def _successor(self, node):
    if node.right != self.null:
      return self._min(node.right)
    else:
      parent = node.parent
      while parent != self.null and node is parent.right:
        node = parent
        parent = parent.parent
      return parent
      
  def _predecessor(self, node):
    if node.left != self.null:
      return self._max(node.left)
    else:
      parent = node.parent
      while parent != self.null and node is parent.left:
        node = parent
        parent = parent.parent
      return parent    
    
  def __contains__(self, key):
    found = self._search(key)
    return found != self.null and found.key == key    
    
  def _order(self, curr, items):
    if curr != self.null:
      self._order(curr.left, items)
      items.append(curr)
      self._order(curr.right, items) 
        
  def tree(self):
    items = []
    self._order(self.root, items)
    return items 
        
  def list(self):
    return [node.tuple() for node in self.tree()]   
    
  def dict(self):   
    return dict(self.list())    
    
  def __repr__(self):
    return repr(self.dict())
    
  def values(self):
    return [v for (k, v) in self.list()]      
    
  def __str__(self):
    return str(self.values())
    
  def keys(self):
    return [k for (k, v) in self.list()]    
      
  def __iter__(self):
    for key in self.keys():
      yield key
    
  def _size(self, curr):
    if curr == self.null:
      return 0
    else:
      return self._size(curr.left) + 1 + self._size(curr.right)
      
  def __len__(self):
    return self._size(self.root)   
    
  def min(self):
    if self.root != self.null:
      return self._min(self.root).value
    
  def max(self): 
    if self.root != self.null:
      return self._max(self.root).value
      
  def _depth(self, curr):
    if curr == self.null:
      return -1
    else:
      return 1 + max(self._depth(curr.left), self._depth(curr.right))
      
  def depth(self):
    return self._depth(self.root)     
      
  def _print(self, curr, mode = 'in', descr = 'T', level = 0):
    if curr != self.null:
      tmp = '%s %s: %s' % (' ' * 8 * level, descr, curr)
      if mode == 'pre':
        print tmp
      self._print(curr.left, mode, 'L', level + 1)
      if mode == 'in': 
        print tmp
      self._print(curr.right, mode, 'R', level + 1) 
      if mode == 'post':
        print tmp
        
  def puts(self, mode = 'in'):
    self._print(self.root, mode)
    
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
      
      tree = BSTree()
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