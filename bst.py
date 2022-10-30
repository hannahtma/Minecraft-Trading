""" Binary Search Tree ADT.
    Defines a Binary Search Tree with linked nodes.
    Each node contains a key and item as well as references to the children.
"""

from __future__ import annotations

__author__ = 'Brendon Taylor, modified by Alexey Ignatiev, further modified by Jackson Goerner'
__docformat__ = 'reStructuredText'

from typing import TypeVar, Generic
from linked_stack import LinkedStack
from node import TreeNode
import sys


# generic types
K = TypeVar('K')
I = TypeVar('I')
T = TypeVar('T')


class BSTInOrderIterator:
    """ 
    In-order iterator for the binary search tree.
    Performs stack-based BST traversal.
    """

    def __init__(self, root: TreeNode[K, I]) -> None:
        """ 
        Iterator initialiser. 
        
        Complexity: O(1)
        """

        self.stack = LinkedStack()
        self.current = root

    def __iter__(self) -> BSTInOrderIterator:
        """ 
        Standard __iter__() method for initialisers. Returns itself. 
        
        Complexity: O(1)
        """
        return self

    def __next__(self) -> K:
        """ 
        The main body of the iterator.
        Returns keys of the BST one by one respecting the in-order.

        Complexity: O(1)
        """

        while self.current:
            self.stack.push(self.current)
            self.current = self.current.left

        if self.stack.is_empty():
            raise StopIteration

        result = self.stack.pop()
        self.current = result.right

        return result.key


class BinarySearchTree(Generic[K, I]):
    """ Basic binary search tree. """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """

        self.root = None
        self.length = 0

    def is_empty(self) -> bool:
        """
            Checks to see if the bst is empty
            :complexity: O(1)
        """
        return self.root is None

    def __len__(self) -> int:
        """ 
        Returns the number of nodes in the tree. 
        
        Complexity: O(1)
        """

        return self.length

    def __contains__(self, key: K) -> bool:
        """
            Checks to see if the key is in the BST
            :complexity: see __getitem__(self, key: K) -> (K, I)

        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __iter__(self) -> BSTInOrderIterator:
        """ 
        Create an in-order iterator. 
        
        Complexity: O(1)
        """
        return BSTInOrderIterator(self.root)

    def __getitem__(self, key: K) -> I:
        """
            Attempts to get an item in the tree, it uses the Key to attempt to find it
            :complexity best: O(CompK) finds the item in the root of the tree
            :complexity worst: O(CompK * D) item is not found, where D is the depth of the tree
            CompK is the complexity of comparing the keys
        """
        return self.get_tree_node_by_key(key).item

    def get_tree_node_by_key(self, key: K) -> TreeNode:
        """
        Returns the node by the key

        Complexity: see get_tree_node_by_key_aux(self, current: TreeNode, key: K) -> TreeNode
        """
        return self.get_tree_node_by_key_aux(self.root, key)

    def get_tree_node_by_key_aux(self, current: TreeNode, key: K) -> TreeNode:
        """
        Returns the node by the key

        :complexity best: O(CompK) returns the item at the root.
        :complexity worst: O(CompK * D) returns at the bottom of the tree
        where D is the depth of the tree
        CompK is the complexity of comparing the keys
        """
        if current is None:  # base case: empty
            raise KeyError('Key not found: {0}'.format(key))
        elif key == current.key:  # base case: found
            return current
        elif key < current.key:
            return self.get_tree_node_by_key_aux(current.left, key)
        else:  # key > current.key
            return self.get_tree_node_by_key_aux(current.right, key)

    def __setitem__(self, key: K, item: I) -> None:
        """
        Sets the item at a key in terms of root

        Complexity: see insert_aux(self, current: TreeNode, key: K, item: I) -> TreeNode
        """
        self.root = self.insert_aux(self.root, key, item)

    def insert_aux(self, current: TreeNode, key: K, item: I) -> TreeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert it

            :complexity best: O(CompK) inserts the item at the root.
            :complexity worst: O(CompK * D) inserting at the bottom of the tree
            where D is the depth of the tree
            CompK is the complexity of comparing the keys
        """
        if current is None:  # base case: at the leaf
            current = TreeNode(key, item)
            self.length += 1
        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
        else:  # key == current.key
            raise ValueError('Inserting duplicate item')
        return current

    def __delitem__(self, key: K) -> None:
        """
        Deletes the item at a certain key in relation to the root

        Complexity: see delete_aux(self, current: TreeNode, key: K) -> TreeNode
        """
        self.root = self.delete_aux(self.root, key)

    def delete_aux(self, current: TreeNode, key: K) -> TreeNode:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete.
            
            :complexity best: O(CompK) deletes the item at the root.
            :complexity worst: O(CompK * D) deletes at the bottom of the tree
            where D is the depth of the tree
            CompK is the complexity of comparing the keys
        """

        if current is None:  # key not found
            raise ValueError('Deleting non-existent item')
        elif key < current.key:
            current.left  = self.delete_aux(current.left, key)
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
        else:  # we found our key => do actual deletion
            if self.is_leaf(current):
                self.length -= 1
                return None
            elif current.left is None:
                self.length -= 1
                return current.right
            elif current.right is None:
                self.length -= 1
                return current.left

            # general case => find a successor
            succ = self.get_successor(current)
            current.key  = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)

        return current

    def get_successor(self, current: TreeNode) -> TreeNode:
        """
            Get successor of the current node.
            It should be a node in the subtree rooted at current having the smallest key among all the
            larger keys.
            If no such node exists, then none should be returned.

            Best Complexity: O(1), where there is no successor
            Worst Complexity: O(D), where there is a successor
            where D is the depth of the right subtree
        """
        # if the current does not have a right node, there is no successor
        if current.right == None:
            current = None
        else:
            # if there is a right node, moves the current to the right
            current = current.right
            while current.left != None:
                # checks all the way to the left to find the smallest value in the right subtree
                current = current.left

        return current

    def get_minimal(self, current: TreeNode) -> TreeNode:
        """
            Get a node having the smallest key in the current sub-tree.

            Best Complexity: O(1), where current is the smallest key node
            Worst Complexity: O(D), where current is the root of the tree
            where D is the depth of the tree
        """
        # if the current does not have a left node, it is the smallest in the subtree
        while current.left != None:
            current = current.left

        return current

    def get_maximal(self, current: TreeNode) -> TreeNode:
        """
        Get a node having the highest key in the current sub-tree.

        Best Complexity: O(1), where current is the largest key node
        Worst Complexity: O(D), where current is the root of the tree
        where D is the depth of the tree
        """
        # checks all the way to the right to find the largest value in the subtree
        while current.right != None:
            current = current.right

        return current

    def is_leaf(self, current: TreeNode) -> bool:
        """ 
        Simple check whether or not the node is a leaf. 
        
        Complexity: O(1)
        """

        return current.left is None and current.right is None

    def draw(self, to=sys.stdout):
        """ 
        Draw the tree in the terminal. 
        
        Complexity: see draw_aux(self, current: TreeNode, prefix='', final='', to=sys.stdout) -> K
        """

        # get the nodes of the graph to draw recursively
        self.draw_aux(self.root, prefix='', final='', to=to)

    def draw_aux(self, current: TreeNode, prefix='', final='', to=sys.stdout) -> K:
        """ 
        Draw a node and then its children. 
        
        Best Complexity: O(1), where current is None
        Worst Complexity: O(n), where current is not None
        where n is the depth of the left leaf node
        """
        if current is not None:
            real_prefix = prefix[:-2] + final
            print('{0}{1}'.format(real_prefix, str(current.key)), file=to)

            if current.left or current.right:
                self.draw_aux(current.left,  prefix=prefix + '\u2551 ', final='\u255f\u2500', to=to)
                self.draw_aux(current.right, prefix=prefix + '  ', final='\u2559\u2500', to=to)
        else:
            real_prefix = prefix[:-2] + final
            print('{0}'.format(real_prefix), file=to)
