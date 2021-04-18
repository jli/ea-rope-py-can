class Rope:
  def __init__(self, text):
    self.text = text
    self.size = len(text)
    self.left = None
    self.right = None

  # prints contents including showing the hierarchy
  # it's not required for this function to work, it's just there to help with debugging
  #
  # e.g. if the  root node has ABC, the left node has DEF, and the right node has GHI,
  # the output will look like:
  # -DEF
  # ABC
  # -GHI
  def to_string_debug(self, indentLevel = 0):
    leftText = self.left.to_string_debug(indentLevel + 1) if self.left else ''
    rightText = self.right.to_string_debug(indentLevel + 1) if self.right else ''
    return leftText + ('-'*indentLevel) + self.text + '\n' + rightText

  # just prints the stored text
  def to_string(self):
    leftText =  self.left.to_string() if self.left else  ''
    rightText = self.right.to_string() if self.right else  ''
    return leftText + self.text + rightText

  # How long the text stored is in all of the children combined
  # This is the same as this.to_string().length
  def total_size(self):
    leftText =  self.left.total_size() if self.left else  0
    rightText = self.right.total_size() if self.right else  0
    return leftText + self.size + rightText

  # how deep the tree is (I.e. the maximum depth of children)
  def depth(self):
    return 1 + max(self.left_depth(), self.right_depth())

  # Whether the rope is balanced, i.e. whether any subtrees have branches
  # which differ by more than one in depth.
  def is_balanced(self):
    leftBalanced =  self.left.is_balanced() if self.left else True
    rightBalanced = self.right.is_balanced() if self.right else True

    return leftBalanced and rightBalanced and abs(self.left_depth() - self.right_depth()) < 2

  def left_depth(self):
    if (not self.left):
      return 0
    return self.left.depth()

  def right_depth(self):
    if (not self.right):
      return 0
    return self.right.depth()

  # Helper method which converts the rope into an associative array
  #
  # Only used for debugging, this has no functional purpose
  def to_dictionary(self):
    mapVersion = {
      'text': self.text
    }
    if (self.right):
      mapVersion['right'] = self.right.to_dictionary()
    if (self.left):
      mapVersion['left'] = self.left.to_dictionary()
    return mapVersion

def create_rope_from_map(map):
  rope = Rope(map['text'])
  if 'left' in map:
    rope.left = create_rope_from_map(map['left'])
  if 'right' in map:
    rope.right = create_rope_from_map(map['right'])
  return rope

def prepend(rope, text):
  if (rope.left):
    prepend(rope.left, text)
  else:
    rope.left = Rope(text)

  return rope

def append(rope, text):
  if (rope.right):
    append(rope.right, text)
  else:
    rope.right = Rope(text)

  return rope

# This is an internal API. You can implement it however you want.
# (E.g. you can choose to mutate the input rope or not)
def split_at(rope, position):
  # TODO
  return [newLeft, right]

def delete_range(rope, start, end):
  # TODO
  return rope

def insert(rope, text, location):
  # TODO
  return rope

def rebalance(rope):
  # TODO
  return rope

'''
 Rotates a tree: used for rebalancing.

 Turns:
    b
  /  \
  a   c

  Into:
     c
    /
   b
  /
a
'''
def rotate_left(rope):
  newParent = rope.right
  newLeft = rope
  newLeft.right = newParent.left
  newParent.left = newLeft
  return newParent

'''
/*
 Rotates a tree: used for rebalancing.

 Turns:
    b
  /  \
  a   c

  Into:
     a
      \
       b
        \
         c
'''
def rotate_right(rope):
  newParent = rope.left
  newRight = rope
  newRight.left = newParent.right
  newParent.right = newRight
  return newParent
