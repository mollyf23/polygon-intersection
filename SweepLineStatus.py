class SweepLineStatusNode:
    def __init__(self, segment):
        self.segment = segment
        self.left = None
        self.right = None
        self.parent = None
        self.height = 1  # Height of the node for balancing

class SweepLineStatus:
    def __init__(self):
        self.root = None

    # get the height of a node
    def get_height(self, node):
        return node.height if node else 0

    # get the balance of a node
    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    # Perform a right rotation
    def rotate_right(self, node):
        left_child = node.left
        left_right_subtree = left_child.right

        # Perform rotation
        left_child.right = node
        node.left = left_right_subtree

        # Update heights
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        left_child.height = 1 + max(self.get_height(left_child.left), self.get_height(left_child.right))

        # Update parent pointers
        left_child.parent = node.parent
        if left_right_subtree:
            left_right_subtree.parent = node
        node.parent = left_child

        return left_child

    # Perform a left rotation
    def rotate_left(self, node):
        right_child = node.right
        right_left_subtree = right_child.left

        # Perform rotation
        right_child.left = node
        node.right = right_left_subtree

        # Update heights
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        right_child.height = 1 + max(self.get_height(right_child.left), self.get_height(right_child.right))

        # Update parent pointers
        right_child.parent = node.parent
        if right_left_subtree:
            right_left_subtree.parent = node
        node.parent = right_child

        return right_child

    # Insert a segment into the AVL tree
    def insert(self, segment):
        self.root = self.insert_node(self.root, segment)
    
    # Delete a segment from the AVL tree
    def delete(self, segment):
        self.root = self.delete_node(self.root, segment)

    def insert_node(self, node, segment):
        if not node:
            return SweepLineStatusNode(segment)

        if self.comparator(segment, node.segment) < 0:
            node.left = self.insert_node(node.left, segment)
            node.left.parent = node
        else:
            node.right = self.insert_node(node.right, segment)
            node.right.parent = node

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        balance = self.get_balance(node)

        if balance > 1:
            if self.comparator(segment, node.left.segment) < 0: 
                return self.rotate_right(node)
            else: 
                node.left = self.rotate_left(node.left)
                return self.rotate_right(node)

        if balance < -1:
            if self.comparator(segment, node.right.segment) > 0: 
                return self.rotate_left(node)
            else:  
                node.right = self.rotate_right(node.right)
                return self.rotate_left(node)

        return node
    
    def find_node(self, root, segment):
        if root is None or root.segment == segment:
            return root
        if self.comparator(segment, root.segment) < 0:
            return self.find_node(root.left, segment)
        else:
            return self.find_node(root.right, segment)

    def delete_node(self, node, segment):
        if node is None:
            return node

        if self.comparator(segment, node.segment) < 0:
            node.left = self.delete_node(node.left, segment)
        elif self.comparator(segment, node.segment) > 0:
            node.right = self.delete_node(node.right, segment)
        else:
            # Node to be deleted found
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            # Node with two children: Get the inorder successor
            successor = self.min_value_node(node.right)
            node.segment = successor.segment
            node.right = self.delete_node(node.right, successor.segment)

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        balance = self.get_balance(node)

        if balance > 1:
            if self.get_balance(node.left) >= 0:
                return self.rotate_right(node)
            else:  # Left-right case
                node.left = self.rotate_left(node.left)
                return self.rotate_right(node)

        if balance < -1:
            if self.get_balance(node.right) <= 0:  
                return self.rotate_left(node)
            else:  # Right-left case
                node.right = self.rotate_right(node.right)
                return self.rotate_left(node)

        return node
    
    def min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def above(self, segment):
        node = self.find_node(self.root, segment)
        if node:
            if node.right: 
                current = node.right
                while current.left:
                    current = current.left
                return current.segment
            else: 
                parent = node.parent
                while parent and self.comparator(segment, parent.segment) >= 0:
                    parent = parent.parent
                if (parent): return parent.segment
        return None

    def below(self, segment):
        node = self.find_node(self.root, segment)
        if node:
            if node.left: 
                current = node.left
                while current.right:
                    current = current.right
                return current.segment
            else: 
                parent = node.parent
                while parent and self.comparator(segment, parent.segment) <= 0:
                    parent = parent.parent
                if (parent): return parent.segment
        return None
    
    def comparator(self,segment1, segment2):
        # y-coordinates of left endpoints
        if segment1.leftEndPoint().y() < segment2.leftEndPoint().y():
         return -1
        elif segment1.leftEndPoint().y() > segment2.leftEndPoint().y():
           return 1
        else:
            # x-coordinates of left endpoints
            if segment1.leftEndPoint().x() < segment2.leftEndPoint().x():
                return -1
            elif segment1.leftEndPoint().x() > segment2.leftEndPoint().x():
                return 1
            else:
                # y-coordinates of right endpoints
                if segment1.rightEndPoint().y() < segment2.rightEndPoint().y():
                    return -1
                elif segment1.rightEndPoint().y() > segment2.rightEndPoint().y():
                    return 1
                else:
                    # x-coordinates of right endpoints
                    if segment1.rightEndPoint().x() < segment2.rightEndPoint().x():
                        return -1
                    elif segment1.rightEndPoint().x() > segment2.rightEndPoint().x():
                        return 1
                    else:
                        return 0
