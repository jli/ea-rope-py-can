from typing import Any, Dict, List, Optional


class Rope:
  def __init__(self, text: str):
    self.text: str = text
    self.size: int = len(text)
    self.left: Optional[Rope] = None
    self.right: Optional[Rope] = None

  # prints contents including showing the hierarchy
  # it's not required for this function to work, it's just there to help with debugging
  #
  # e.g. if the  root node has ABC, the left node has DEF, and the right node has GHI,
  # the output will look like:
  # -DEF
  # ABC
  # -GHI
  def to_string_debug(self, indentLevel: int = 0) -> str:
    leftText = self.left.to_string_debug(indentLevel + 1) if self.left else ''
    rightText = self.right.to_string_debug(indentLevel + 1) if self.right else ''
    return leftText + ('-'*indentLevel) + self.text + '\n' + rightText

  # just prints the stored text
  def to_string(self) -> str:
    leftText =  self.left.to_string() if self.left else  ''
    rightText = self.right.to_string() if self.right else  ''
    return leftText + self.text + rightText

  # How long the text stored is in all of the children combined
  # This is the same as this.to_string().length
  def total_size(self) -> int:
    leftText =  self.left.total_size() if self.left else  0
    rightText = self.right.total_size() if self.right else  0
    return leftText + self.size + rightText

  # how deep the tree is (I.e. the maximum depth of children)
  def depth(self) -> int:
    return 1 + max(self.left_depth(), self.right_depth())

  # Whether the rope is balanced, i.e. whether any subtrees have branches
  # which differ by more than one in depth.
  def is_balanced(self) -> bool:
    leftBalanced =  self.left.is_balanced() if self.left else True
    rightBalanced = self.right.is_balanced() if self.right else True

    return leftBalanced and rightBalanced and abs(self.left_depth() - self.right_depth()) < 2

  def left_depth(self) -> int:
    if (not self.left):
      return 0
    return self.left.depth()

  def right_depth(self) -> int:
    if (not self.right):
      return 0
    return self.right.depth()

  # Helper method which converts the rope into an associative array
  #
  # Only used for debugging, this has no functional purpose
  def to_dictionary(self) -> Dict[str, Any]:
    mapVersion: Dict[str, Any] = {
      'text': self.text
    }
    if (self.right):
      mapVersion['right'] = self.right.to_dictionary()
    if (self.left):
      mapVersion['left'] = self.left.to_dictionary()
    return mapVersion

def create_rope_from_map(map: Dict[str, Any]) -> Rope:
  rope = Rope(map['text'])
  if 'left' in map:
    rope.left = create_rope_from_map(map['left'])
  if 'right' in map:
    rope.right = create_rope_from_map(map['right'])
  return rope

def prepend(rope: Rope, text: str) -> Rope:
  if (rope.left):
    prepend(rope.left, text)
  else:
    rope.left = Rope(text)

  return rope

def append(rope: Rope, text: str) -> Rope:
  if (rope.right):
    append(rope.right, text)
  else:
    rope.right = Rope(text)

  return rope

# This is an internal API. You can implement it however you want.
# (E.g. you can choose to mutate the input rope or not)
def split_at(rope: Rope, position: int) -> List:
  # TODO
  return [] # [newLeft, right]

def delete_range(rope: Rope, start: int, end: int) -> Rope:
  # TODO
  return rope

def insert(rope: Rope, text: str, location: int) -> Rope:
  # TODO
  return rope

def rebalance(rope: Rope) -> Rope:
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
def rotate_left(rope: Rope) -> Rope:
  assert rope.right is not None
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
def rotate_right(rope: Rope) -> Rope:
  assert rope.left is not None
  newParent = rope.left
  newRight = rope
  newRight.left = newParent.right
  newParent.right = newRight
  return newParent
