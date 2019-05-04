class MinHeap:
  def __init__(self):
    self.heap_list = [None]
    self.count = 0

  # HEAP HELPER METHODS
  # DO NOT CHANGE!
  def parent_idx(self, idx):
    return idx // 2

  def left_child_idx(self, idx):
    return idx * 2

  def right_child_idx(self, idx):
    return idx * 2 + 1
  
  def get_smaller_child_idx(self, idx):
    if self.right_child_idx(idx) > self.count:
      print("There is only a left child")
      return self.left_child_idx(idx)
    left_child = self.heap_list[self.left_child_idx(idx)]
    right_child = self.heap_list[self.right_child_idx(idx)]
    if (left_child < right_child):
      print("Left child is smaller")
      return self.left_child_idx(idx)
    print("Right child is smaller")
    return self.right_child_idx(idx)


  # END OF HEAP HELPER METHODS
  
  def retrieve_min(self):
    if self.count == 0:
      print("No items in heap")
      return None
    
    min = self.heap_list[1]
    print("Removing: {0} from {1}".format(min, self.heap_list))
    self.heap_list[1] = self.heap_list[self.count]
    self.count -= 1
    self.heap_list.pop()
    print("Last element moved to first: {0}".format(self.heap_list))    
    self.heapify_down()
    return min

  def add(self, element):
    self.count += 1
    print("Adding: {0} to {1}".format(element, self.heap_list))
    self.heap_list.append(element)
    self.heapify_up()

  # define .get_smaller_child_idx() below...
    
  def heapify_up(self):
    # start at the last element of the list
    # while there's a parent element available:
        # if the parent element is greater:
          # swap the elements
        # set the target element index to be the parent's index
    idx = self.count
    while self.parent_idx(idx) > 0:
      if self.heap_list[self.parent_idx(idx)] > self.heap_list[idx]:
        tmp = self.heap_list[self.parent_idx(idx)]
        print("swapping {0} with {1}".format(tmp, self.heap_list[idx]))
        self.heap_list[self.parent_idx(idx)] = self.heap_list[idx]
        self.heap_list[idx] = tmp
      idx = self.parent_idx(idx)
    print("HEAP RESTORED! {0}".format(self.heap_list))
    print("")
      
  def heapify_down(self):
    print("Heapifying down! {incomplete}")
    idx = 1 
