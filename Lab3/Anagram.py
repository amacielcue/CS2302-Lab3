#CS2302 Lab3-B
#By: Alejandra Maciel
#Last Modified: Nov-4-2018
#Instructor: Diego Aguirre
#TA: Manoj  Pravaka  Saha
#The purpose of this lab was to create a program that would read a file with all the valid english words, which would be
#use to find valid anagrams for specific words. The program would ask the user what kind of tree they would want to use
#to store the english words, then the program would create the tree. It would read a file with the list of specific
#words to analyze and will get all the possible anagrams for each and return the one with the most anagrams.

########################################################################################################################
# AVL Tree: Node class
class AVLNode:
    #Constructor
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None
        self.height = 0
    #Method to get the balance value of the node
    def get_balance(self):
        left_height = -1
        if self.left is not None:
            left_height = self.left.height

        right_height = -1
        if self.right is not None:
            right_height = self.right.height

        return left_height - right_height

    #Method to get the height value of the node
    def update_height(self):
        left_height = -1
        if self.left is not None:
            left_height = self.left.height

        right_height = -1
        if self.right is not None:
            right_height = self.right.height

        self.height = max(left_height, right_height) + 1

    #Method to set the child value of the node
    def set_child(self, which_child, child):
        if which_child != "left" and which_child != "right":
            return False

        if which_child == "left":
            self.left = child
        else:
            self.right = child

        if child is not None:
            child.parent = self

        self.update_height()
        return True

    #Method to replace the child of the node
    def replace_child(self, current_child, new_child):
        if self.left is current_child:
            return self.set_child("left", new_child)
        elif self.right is current_child:
            return self.set_child("right", new_child)

        return False




########################################################################################################################


AVL Tree: Tree class
class AVLTree:
    #Constructor
    def __init__(self):
        self.root = None

    #Method to do a left rotation on the tree
    def rotate_left(self, node):
        right_left_child = node.right.left

        if node.parent is not None:
            node.parent.replace_child(node, node.right)
        else:
            self.root = node.right
            self.root.parent = None

        node.right.set_child('left', node)
        node.set_child('right', right_left_child)

        return node.parent

    #Method to do a right rotation on the tree
    def rotate_right(self, node):
        left_right_child = node.left.right

        if node.parent is not None:
            node.parent.replace_child(node, node.left)
        else:
            self.root = node.left
            self.root.parent = None

        node.left.set_child('right', node)
        node.set_child('left', left_right_child)

        return node.parent

    #Method to rebalance the tree
    def rebalance(self, node):
        node.update_height()

        if node.get_balance() == -2:
            if node.right.get_balance() == 1:
                self.rotate_right(node.right)
            return self.rotate_left(node)

        elif node.get_balance() == 2:
            if node.left.get_balance() == -1:
                self.rotate_left(node.left)
            return self.rotate_right(node)

        return node

    #Method to insert a new node to the tree
    def insert(self, node):
        if self.root is None:
            self.root = node
            node.parent = None

        else:
            current_node = self.root
            while current_node is not None:
                if node.key < current_node.key:
                    if current_node.left is None:
                        current_node.left = node
                        node.parent = current_node
                        current_node = None
                    else:
                        current_node = current_node.left
                else:
                    if current_node.right is None:
                        current_node.right = node
                        node.parent = current_node
                        current_node = None
                    else:
                        current_node = current_node.right

            node = node.parent
            while node is not None:
                self.rebalance(node)
                node = node.parent





########################################################################################################################
#Red-Black Tree: Node class
class RBNode:
    #Constructor
    def __init__(self, key, parent, is_red=False, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent

        if is_red:
            self.color = "red"
        else:
            self.color = "black"

    #Method to see if both children of the node are black
    def are_both_children_black(self):
        if self.left != None and self.left.is_red():
            return False
        if self.right != None and self.right.is_red():
            return False
        return True

    #Method to count nodes after itself
    def count(self):
        count = 1
        if self.left != None:
            count = count + self.left.count()
        if self.right != None:
            count = count + self.right.count()
        return count

    #Method to find the node's grandparent
    def get_grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

    #Method to find the node's parent
    def get_parent(self):
        node = self.left
        while node.right is not None:
            node = node.right
        return node

    #Method to find the node's sibling
    def get_sibling(self):
        if self.parent is not None:
            if self is self.parent.left:
                return self.parent.right
            return self.parent.left
        return None

    #Method to find the node's uncle
    def get_uncle(self):
        grandparent = self.get_grandparent()
        if grandparent is None:
            return None
        if grandparent.left is self.parent:
            return grandparent.right
        return grandparent.left

    #Method to see if the node is black
    def is_black(self):
        return self.color == "black"

    #Method to see if the node is red
    def is_red(self):
        return self.color == "red"

    #Method to replace the node's child
    def replace_child(self, current_child, new_child):
        if self.left is current_child:
            return self.set_child("left", new_child)
        elif self.right is current_child:
            return self.set_child("right", new_child)
        return False

    #Method to set the node's child
    def set_child(self, which_child, child):
        if which_child != "left" and which_child != "right":
            return False

        if which_child == "left":
            self.left = child
        else:
            self.right = child

        if child != None:
            child.parent = self

        return True

########################################################################################################################

#Red-Black Tree: Tree class
class RBTree:
    #Constructor
    def __init__(self):
        self.root = None

    #Method to insert a new key as node to the tree
    def insert(self, key):
        new_node = RBNode(key, None, True, None, None)
        self.insert_node(new_node)

    #Method to insert a new node to the tree
    def insert_node(self, node):
        if self.root is None:
            self.root = node
        else:
            current_node = self.root
            while current_node is not None:
                if node.key < current_node.key:
                    if current_node.left is None:
                        current_node.set_child("left", node)
                        break
                    else:
                        current_node = current_node.left
                else:
                    if current_node.right is None:
                        current_node.set_child("right", node)
                        break
                    else:
                        current_node = current_node.right

        node.color = "red"
        self.insertion_balance(node)

    #Method to insert a node keeping the tree balanced
    def insertion_balance(self, node):
        if node.parent is None:
            node.color = "black"
            return

        if node.parent.is_black():
            return

        parent = node.parent
        grandparent = node.get_grandparent()
        uncle = node.get_uncle()

        if uncle is not None and uncle.is_red():
            parent.color = uncle.color = "black"
            grandparent.color = "red"
            self.insertion_balance(grandparent)
            return

        if node is parent.right and parent is grandparent.left:
            self.rotate_left(parent)
            node = parent
            parent = node.parent

        elif node is parent.left and parent is grandparent.right:
            self.rotate_right(parent)
            node = parent
            parent = node.parent

        parent.color = "black"
        grandparent.color = "red"

        if node is parent.left:
            self.rotate_right(grandparent)
        else:
            self.rotate_left(grandparent)

    #Method to do a left rotation
    def rotate_left(self, node):
        right_left_child = node.right.left
        if node.parent != None:
            node.parent.replace_child(node, node.right)
        else:
            self.root = node.right
            self.root.parent = None
        node.right.set_child("left", node)
        node.set_child("right", right_left_child)

    #Method to do a right rotation
    def rotate_right(self, node):
        left_right_child = node.left.right
        if node.parent != None:
            node.parent.replace_child(node, node.left)
        else:
            self.root = node.left
            self.root.parent = None
        node.left.set_child("right", node)
        node.set_child("left", left_right_child)



########################################################################################################################

# Method to read the english dictionary file, create the desired tree and call the other methods.
def read_file(fileName, fileName2):
    #Read File
    f = open(fileName, 'r')
    line = f.readline()
    #Ask the user
    user_tree = input("What kind of tree would you like to use? 1. AVL Tree or 2. Red-Black Tree (Please enter a number)")

    #If the user's input is 1 then notify them their choice (AVL) and create the chosen tree with the file's information
    if user_tree == "1" :
        print("Your choice was AVL")
        tree = AVLTree()
        #While there are information lines on the file keep inserting nodes to the tree
        while line:
            # print(line)
            avl_node = AVLNode(line)
            tree.insert(avl_node)
            line = f.readline()
        read_words(tree, fileName2)

    #If the user's input is 2 then notify them their choice (RBT) and create the chosen tree with the file's information
    elif user_tree == "2":
        print("Your choice was R-B")
        tree = RBTree()
        #While there are information lines on the file keep inserting nodes to the tree
        while line:
            # print(line)
            tree.insert(line)
            line = f.readline()
        read_words(tree, fileName2)
    #Else notify them their choice does not exist and ask for a different input.
    else:
        print("That is not an option, please re-enter your choice.")
        read_file(fileName, fileName2)


# Method to read the words file to analyze and find the word with more anagrams.
def read_words(eng_words, fileName):
    #Read File
    f = open(fileName, 'r')
    line = f.readline()
    # while line:
    #     print_anagrams(eng_words,line)
    #     line = f.readline()
    max = 0
    max_anagram = ""
    # While there are information lines on the file keep comparing the number of anagrams each word has.
    while line:
        #If the word has more anagrams than the stored max, then set max_anagram to the new word
        if max < count_anagrams(eng_words,line) :
            max = count_anagrams(eng_words,line)
            max_anagram = line
        line = f.readline()
    print("The word with the most anagrams is " + max_anagram + " with " + str(max) + " anagrams.")

    return max_anagram

# #Method to print all the valid anagrams of a word
# def print_anagrams(t, word, prefix = ""):
#     if len(word) <= 1:
#         str = prefix + word
#
#         current_node = t.root
#         while current_node is not None:
#             if current_node.key == str:
#                 print(prefix + word)
#             elif current_node.key < key:
#                 current_node = current_node.right
#             else:
#                 current_node = current_node.left
#
#     else:
#         for i in range(len(word)):
#             cur = word[i: i + 1]
#             before = word[0: i]
#             after = word[i+1:]
#
#             if cur not in before:
#                 print_anagrams(before + after, prefix + cur)


#Method to return the number of anagrams a word has
def count_anagrams(t, word, prefix = ""):
    count = 0
    #If the length of the word is smaller or equal to 1 than set the str to the prefix and the word, and search for the
    #anagram in the tree.
    if len(word) <= 1:
        str = prefix + word

        current_node = t.root
        while current_node is not None:
            #If the anagram is found than increase counter
            if current_node.key == str:
                count += 1
            #Else check on the next available child
            elif current_node.key < key:
                current_node = current_node.right
            else:
                current_node = current_node.left
    #ELse change the order of the word's letters
    else:
        for i in range(len(word)):
            cur = word[i: i + 1]
            before = word[0: i]
            after = word[i+1:]

            if cur not in before:
                count_anagrams(before + after, prefix + cur)
    return count




#Method call
read_file("word", "example")
