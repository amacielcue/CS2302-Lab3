#CS2302 Lab3-B
#By: Alejandra Maciel
#Last Modified: Nov-56-2018
#Instructor: Diego Aguirre
#TA: Manoj  Pravaka  Saha
#The purpose of this lab was to create a program that would read a file with all the valid english words, which would be
#use to find valid anagrams for specific words. The program would ask the user what kind of tree they would want to use
#to store the english words, then the program would create the tree. It would read a file with the list of specific
#words to analyze and will get all the possible anagrams for each and return the one with the most anagrams.

import sys
########################################################################################################################
# AVL Tree: Node class


class AVLNode:


    #Constructor
    def __init__(self, data):
        self.data = data
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

#AVL Tree: Tree class


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
                if node.data < current_node.data:
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

    def search(self, data):
        current_node = self.root
        while current_node is not None:

            if current_node.data == data:
                return True
            elif current_node.data < data:
                current_node = current_node.right
            else:
                current_node = current_node.left
        return False




########################################################################################################################
########################################################################################################################

#Red-Black Tree: Node class


class RBNode:
    #Constructor
    def __init__(self, data, parent, is_red=False, left=None, right=None):
        self.data = data
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


    #Method to insert a new word as node to the tree
    def insert(self, data):
        new_node = RBNode(data, None, True, None, None)
        self.insert_node(new_node)


    #Method to insert a new node to the tree
    def insert_node(self, node):
        if self.root is None:
            self.root = node
        else:
            current_node = self.root
            while current_node is not None:
                if node.data < current_node.data:
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

    def search(self, data):
        current_node = self.root
        while current_node is not None:

            if current_node.data == data:
                return True
            elif current_node.data < data:
                current_node = current_node.right
            else:
                current_node = current_node.left
        return False



########################################################################################################################
########################################################################################################################

#MAIN METHODS

#Method to create an AVL Tree
def AVL_Tree(fileName):
    print("Building...")
    #Read file
    f = open(fileName, 'r')
    line = f.readline()
    avl_tree = AVLTree()

    # While there are information lines on the file keep inserting nodes to the tree
    while line:
        # print(line)
        #Creat new node with the line from the file
        avl_node = AVLNode(line)
        #Insert node into the tree
        avl_tree.insert(avl_node)
        line = f.readline()
    #Return tree
    return avl_tree

#Method to create a Red-Black Tree
def RB_Tree(fileName):
    print("Building...")
    #Read file
    f = open(fileName, 'r')
    line = f.readline()
    rb_tree = RBTree()

    # While there are information lines on the file keep inserting nodes to the tree
    while line:
        # print(line)
        #Insert lines from the file to the tree as nodes
        rb_tree.insert(line)
        line = f.readline()
    #Return tree
    return rb_tree

#Method to get the permutations of any word
def permutations(word):
    perms=[]
    #If the length of the word is 1 then add the word to the list
    if len(word) == 1:
        perms.append(word)
    #Else for the length of the word add to the list the permutations of a fragment of the original wprd and for all the
    #charcaters or strings in the list add the new combination to the list
    else:
        for pos in range(len(word)):
            list = permutations(word[0:pos] + word[pos+1:len(word)])

            for character in list:

                perms.append(word[pos] + character)
    #Return permutations list
    return perms


# Function that prints all valid anagrams from a given word
def print_anagrams(tree, word):
    p = permutations(word)

    for i in range(len(p)):
        if tree.search(p[i]):
            print(p[i])
    return


# Function that returns the number of valid anagrams from a given word
def count_anagrams(tree,word):
    #Get the word's permutations and store in a p variable
    p = permutations(word)
    count = 0
    #For the length of the permutations list if a permutation is in the tree add 1 to the counter
    for i in range(len(p)):
        if tree.search(p[i]):
            count += 1
    #Return counter
    return count

def most_anagrams(fileName, tree):
    f = open(fileName, 'r')
    line = f.readline()
    # while line:
    #     print_anagrams(eng_words,line)
    #     line = f.readline()
    most = 0
    most_anagram = ""
    # While there are information lines on the file keep comparing the number of anagrams each word has.
    while line:
        #If the word has more anagrams than the stored most, then set most_anagram to the new word
        if most < count_anagrams(tree,line) :
            most = count_anagrams(tree,line)
            most_anagram = line
        line = f.readline()

    print("The word with the most anagrams is " + most_anagram + " with " + str(most) + " anagrams.")
    return most_anagram

def main():
    #Print first question and options
    print("-----------------------------------------------------------------------------------------------------------")
    print("Please select the type of tree you would like to use:")
    print("1. AVL Tree")
    print("2. Red-Black Tree")
    print("3. Quit")
    user_tree = input()

    #If user input is 1 proceed to build an AVL Tree
    if user_tree == "1":
        #AVL TREE
        print("You chose an AVL Tree.")
        ut = AVL_Tree("word")
        print("DONE!")
    # Else if user input is 2 proceed to build an R-B Tree
    elif user_tree == "2":
        #RB TREE
        print("You chose a Red-Black Tree.")
        ut = RB_Tree("word")
        print("DONE!")
    #Else if user input is 3 quit program
    elif user_tree == "3":
        sys.exit()
    #Else notify the user their choice is not available and ask to try again
    else:
        print("Your input is not an option. Please try again.")
        main()

    #While the user doesn't quit keep asking for the nexr action
    repeat = True
    while repeat:
        #Ask user for the next action
        print("-----------------------------------------------------------------------------------------------------------")
        print("What would you like to do next?")
        print("1. Get number of anagrams of a word.")
        print("2. Find the word with the most anagrams from a file.")
        print("3. Quit.")
        user_input = input()

        #If user input is 1 then get the number of anagrams a word has
        if user_input == "1":
            # NUM OF ANAGRAMS
            word = input("Please enter a word: ")
            print(count_anagrams(ut, word))
        #Else if the user input is 2 compare the nbumber of anagrams each word on a file have and return the one with
        # the most anagrams
        elif user_input == "2":
            # MOST ANAGRAMS
            file = input("Please enter file name:")
            most_anagrams(file, ut)
        #Else if the user input is 3 quit the program
        elif user_input == "3":
            sys.exit()
        #Else notify the user their choice is not an option and ask to try again.
        else:
            print("Your input is not an option. Please try again.")



#Run the program
main()


# #Method to print all the valid anagrams of a word
# def print_anagrams(t, word, prefix = ""):
#     if len(word) <= 1:
#         str = prefix + word
#
#         included = False
#         current = t.root
#         while current is not None:
#             if current.data.lower() == str.lower():
#                 included = True
#                 current = None
#
#             elif current.data.lower() < str.lower():
#                 current = current.right
#
#             else:
#                 current = current.left
#         if included:
#             print(prefix + word)
#             return 1
#
#     else:
#         for i in range(len(word)):
#             cur = word[i: i + 1]
#             before = word[0: i]
#             after = word[i+1:]
#
#             if cur not in before:
#                 print_anagrams(t, before + after, prefix + cur)

























