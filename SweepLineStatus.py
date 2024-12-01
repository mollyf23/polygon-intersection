class SweepLineStatusNode:
    def __init__(self, segment):
        self.segment = segment
        self.left = None  
        self.right = None  
        self.parent = None

class SweepLineStatus:
    def __init__(self):
        self.root = None

    def insert(self, segment):
        new_node = SweepLineStatusNode(segment)

        if self.root is None:
            self.root = new_node
            return

        # Find the correct position for the new node
        current = self.root
        parent = None
        while current:
            parent = current
            if self.comparator(segment, current.segment) < 0:
                current = current.left
            else:
                current = current.right

        # Insert the new node as a child
        if self.comparator(segment, parent.segment) < 0:
            parent.left = new_node  # Below neighbor
        else:
            parent.right = new_node  # Above neighbor
        new_node.parent = parent

    def delete(self, segment):
        node = self.find_node(self.root, segment)
        if not node:
            return  # Node not found

        # Perform standard BST deletion
        self.root = self.delete_node(self.root, node)

    def find_node(self, root, segment):
        if root is None or root.segment == segment:
            return root
        if self.comparator(segment, root.segment) < 0:
            return self.find_node(root.left, segment)
        else:
            return self.find_node(root.right, segment)

    def delete_node(self, root, node):
        if root is None:
            return root
        if self.comparator(node.segment, root.segment) < 0:
            root.left = self.delete_node(root.left, node)
        elif self.comparator(node.segment, root.segment) > 0:
            root.right = self.delete_node(root.right, node)
        else:
            # Node to be deleted found
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            # Node with two children: Get the inorder successor
            successor = self.min_value_node(root.right)
            root.segment = successor.segment
            root.right = self.delete_node(root.right, successor)
        return root

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
                while parent and self.comparator(segment, parent.segment) > 0:
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
                while parent and self.comparator(segment, parent.segment) > 0:
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
