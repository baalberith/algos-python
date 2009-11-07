from leftleaningrbtree import RBNode, RBTree
from leftleaningrbtree import RED, BLACK, _is_red

class Interval:
  def __init__(self, low, high):
    self.low = low
    self.high = high
    
def _are_overlap(int1, int2):
  return int1.low <= int2.high and int2.low <= int1.high
  
def _are_equal(int1, int2):
  return int1.low == int2.low and int1.high == int2.high

class INode(RBNode):
  def __init__(self, key, value):
    RBNode.__init__(self, key, value)
    self.max_high = value.high
    
class ITree(RBTree):
  def __init__(self):
    RBTree.__init__(self)    
    
  def _search(self, curr, interval):
    if curr == None:
      return None
    else:
      if _are_overlap(curr.value, interval):
        return curr
      elif curr.left != None and curr.left.max_high >= interval.low:
        return self._search(curr.left, interval)
      else:
        return self._search(curr.right, interval)   
        
  def _insert(self, curr, key, interval):
    if curr == None:
      return INode(key, interval)
    else:
      if _are_equal(curr.value, interval):
        pass
      elif key < curr.key:
        curr.left = self._insert(curr.left, key, interval)
      else:
        curr.right = self._insert(curr.right, key, interval)
      if _is_red(curr.right) and not _is_red(curr.left):
        curr = self._rotate_left(curr)
      if _is_red(curr.left) and _is_red(curr.left.left):
        curr = self._rotate_right(curr)
      if _is_red(curr.left) and _is_red(curr.right):
        self._flip_color(curr)
      self._max_high(curr)
      return curr   
      
  def _max_high(self, curr):
    left_max_high = curr.left.max_high if curr.left != None else None
    right_max_high = curr.right.max_high if curr.right != None else None
    curr.max_high = max(curr.value.high, left_max_high, right_max_high)
      
  def _rotate_left(self, curr):
    right = curr.right
    curr.right = right.left
    right.left = curr
    right.color = curr.color
    curr.color = RED
    self._max_high(curr)
    self._max_high(right)
    return right
    
  def _rotate_right(self, curr):
    left = curr.left
    curr.left = left.right
    left.right = curr    
    left.color = curr.color
    curr.color = RED
    self._max_high(curr)
    self._max_high(left)
    return left       
    
if __name__ == '__main__':
  def test(tests = 10, num = 256, ran = 1000000):
    from random import randint, shuffle
    depth = []
    
    for t in range(tests):
      array = []
      for i in range(num):
        tmp1 = randint(1, ran)
        tmp2 = randint(1, ran)
        if tmp2 > tmp1:
          tmp1, tmp2 = tmp2, tmp1
        array.append((tmp1, Interval(tmp1, tmp2)))
      
      tree = ITree()
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

      
    print 'depth:', (sum(depth) / tests), 'min:', min(depth), 'max:', max(depth)
      
  test()            