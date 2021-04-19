from typing import Any, Dict, List, Optional, Tuple


class Rope:
  def __init__(self, text: str):
    self.text: str = text
    # TODO: use property setter for text to set size to enforce consistency.
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
def split_at(rope: Rope, position: int) -> None:
  """Splits rope text at position, moving left and right pieces into child
  ropes and clearing rope's own text."""
  # print(f"split_at({position=}) top")
  left_bit = rope.text[:position]
  right_bit = rope.text[position:]
  # print(f"split_at({position=}). {left_bit=} {right_bit=}")
  if rope.left:
    append(rope.left, left_bit)
  else:
    rope.left = Rope(left_bit)
  if rope.right:
    prepend(rope.right, right_bit)
  else:
    rope.right = Rope(right_bit)

  rope.text = ''
  rope.size = 0

def delete_range(rope: Rope, start: int, end: int) -> Rope:
  left_size = 0 if rope.left is None else rope.left.total_size()
  right_size = 0 if rope.right is None else rope.right.total_size()
  mid_range_end = left_size + rope.size
  # print(f"DR top. {start=}, {end=}, rope:\n", rope.to_string_debug(), sep='')
  # print(f"DR top. {left_size=}, {mid_range_end=}, {right_size=}")

  if rope.left and intersects((start, end), (0, left_size)):
    # print(f"intersects left.. ({rope.left.to_string()})")
    rope.left = delete_range(rope.left, start, end)
    # print(f"..intersects left. new: {rope.left.to_string()}")

  if intersects((start, end), (left_size, mid_range_end)):
    # print(f"rope.text[:{start - left_size}] + rope.text[{end - left_size}:]")
    # Note: max sets lower bound of 0 to avoid wrapping around
    rope.text = rope.text[:max(start - left_size, 0)] + rope.text[end - left_size:]
    # print(f"intersects mid. new {rope.text=}")
    rope.size = len(rope.text)

  if rope.right and intersects((start, end), (mid_range_end, mid_range_end + right_size)):
    # print(f"intersects right.. ({rope.right.to_string()})")
    rope.right = delete_range(rope.right, start - mid_range_end, end - mid_range_end)
    # print(f"..intersects right. new: {rope.right.to_string()}")

  return rope

def intersects(r1: Tuple[int, int], r2: Tuple[int, int]) -> bool:
  # r1 ends before r2 begins, or r2 ends before r1 begins
  if r1[1] < r2[0] or r2[1] < r1[0]:
    return False
  return True

def insert(rope: Rope, text: str, location: int) -> Rope:
  left_size = 0 if rope.left is None else rope.left.total_size()
  mid_range_end = left_size + rope.size
  # print(f"I top. {location=}, rope:\n", rope.to_string_debug(), sep='')
  # print(f"I top. {left_size=}, {mid_range_end=}")

  if location <= left_size:
    if rope.left:
      insert(rope.left, text, location)
    else:
      rope.left = Rope(text)
  elif left_size < location < mid_range_end:
    mid_location = location - left_size
    split_at(rope, mid_location)
    rope.text = text
    rope.size = len(text)
  else:
    if rope.right:
      right_location = location - mid_range_end
      insert(rope.right, text, right_location)
    else:
      rope.right = Rope(text)
  return rope

def rebalance(rope: Rope) -> Rope:
  if rope.is_balanced():
    return rope

  # TODO: this happens to pass existing tests, but i'm not confident this is
  # fully general.
  while rope.left_depth() - rope.right_depth() > 1:
    assert rope.left is not None
    if rope.left.right_depth() > rope.left.left_depth():
      rope.left = rotate_left(rope.left)
    rope = rotate_right(rope)
  while rope.right_depth() - rope.left_depth() > 1:
    assert rope.right is not None
    if rope.right.left_depth() > rope.right.right_depth():
      rope.right = rotate_right(rope.right)
    rope = rotate_left(rope)

  if rope.left:
    rebalance(rope.left)
  if rope.right:
    rebalance(rope.right)

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
