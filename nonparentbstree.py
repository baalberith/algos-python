class BSNode:    
  def __init__(self, key, value):    
    self.key = key  
    self.value = value  
    self.left = None
    self.right = None  
    
  def __str__(self):
    return str(self.value)
    
  def tuple(self):
    return (self.key, self.value)     
    
  def __repr__(self):
    return repr(self.tuple())  
    
class BSTree:
  def __init__(self):
    self.root = None

  def _search(self, curr, key):
    if curr == None:
      return None
    else:
      if key == curr.key:
        return curr
      elif key < curr.key:
        return self._search(curr.left, key)
      else:
        return self._search(curr.right, key)
        
  def __getitem__(self, key):
    found = self._search(self.root, key)
    if found != None:
      return found.value
    else:
      raise KeyError
    
  def _insert(self, curr, key, value):
    if curr == None:
      return BSNode(key, value)
    else:
      if key == curr.key:
        curr.value = value
      elif key < curr.key:
        curr.left = self._insert(curr.left, key, value)
      else:
        curr.right = self._insert(curr.right, key, value)
      return curr
      
  def __setitem__(self, key, value):
    self.root = self._insert(self.root, key, value)
    
  def _delete(self, curr, key):
    if key < curr.key:
      curr.left = self._delete(curr.left, key)
    else:
      if key == curr.key:
        if curr.right == None:
          return curr.left
        else:
          minimum = self._min(curr.right)
          curr.key, curr.value = minimum.key, minimum.value
          curr.right = self._delete_min(curr.right)
      else:
        curr.right = self._delete(curr.right, key)
    return curr

  def __delitem__(self, key):
    if key in self:
      self.root = self._delete(self.root, key)
    else:
      raise KeyError
    
  def _delete_min(self, curr):
    if curr.left == None:
      return curr.right
    curr.left = self._delete_min(curr.left)
    return curr
    
  def _delete_max(self, curr):
    if curr.right == None:
      return curr.left
    curr.right = self._delete_max(curr.right)
    return curr    
    
  def _min(self, curr):
    if curr.left == None:
      return curr
    else:
      return self._min(curr.left)

  def _max(self, curr):
    if curr.right == None:
      return curr
    else:
      return self._max(curr.right)
    
  def __contains__(self, key):
    found = self._search(self.root, key) 
    return found != None  
    
  def _order(self, curr, items):
    if curr != None:
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
    if curr == None:
      return 0
    else:
      return self._size(curr.left) + 1 + self._size(curr.right)
      
  def __len__(self):
    return self._size(self.root)   
    
  def min(self):
    if self.root != None:
      return self._min(self.root).value
    
  def max(self): 
    if self.root != None:
      return self._max(self.root).value
      
  def _depth(self, curr):
    if curr == None:
      return -1
    else:
      return 1 + max(self._depth(curr.left), self._depth(curr.right))
      
  def depth(self):
    return self._depth(self.root)     
      
  def _print(self, curr, mode = 'in', descr = 'T', level = 0):
    if curr != None:
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
  def test(tests = 10, num = 256, ran = 1000000):
    from random import randint, shuffle
    depth = []
    
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