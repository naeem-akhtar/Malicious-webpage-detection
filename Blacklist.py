from sys import setrecursionlimit
import re
import pickle
import pandas as pd

setrecursionlimit(5000)

class TrieNode(object):
    def __init__(self, char=None):
        self.char = char
        self.children = []
        self.terminal = False


class Blacklist:
    def __init__(self):
        self.root = TrieNode()
    
    # add new url in TRIE
    def add_domains(self, domains):
        node = self.root
        for char in domains:
            found_in_child = False
            # Search for the character in the children of the current `node`
            for child in node.children:
                if child.char == char:
                    # And point the node to the child that contains this char
                    node = child
                    found_in_child = True
                    break
            # We did not find it so add a new chlid
            if not found_in_child:
                new_node = TrieNode(char)
                node.children.append(new_node)
                # And then point node to the new child
                node = new_node
        # Everything finished. Mark it as the end of a word.
        node.terminal = True

    # query -> find if url exist
    def find_domains(self, domains):
        if not self.root.children:
            return False

        node = self.root
        for char in domains:
            char_not_found = True
            # Search through all the children of the present `node`
            for child in node.children:
                if child.char == char:
                    # We found the char existing in the child.
                    char_not_found = False
                    # Assign node as the child containing the char and break
                    node = child
                    break
            # Return False anyway when we did not find a char.
            if char_not_found:
                return False
        # Return True if only is is end of an existing url otherwise, False 
        return node.terminal

    # A trie will be created for faster queries and space optimization
    def create_blacklist(self, path_to_csv = './Dataset/filtered_malicious.csv'):
        blacklisted_urls = pd.read_csv(path_to_csv)['url']
        
        for url in blacklisted_urls:
            # extract domain from url and add it to trie
            blacklist.add_domains(re.match(r'^[^/]*', re.sub(r'^http(s*)://', '', url)).group(0))



# Actual blacklist
try:
    blacklist = pickle.load(open('./Dataset/blacklist.pkl', 'rb'))
except:
    print('No blacklist found, creating new.')
    try:
        blacklist = Blacklist()
        blacklist.create_blacklist('./Dataset/filtered_malicious.csv')
        pickle.dump(blacklist, open('./Dataset/blacklist.pkl', 'wb'))
        print('Blacklist dumpled as blacklist.pkl')
    except Exception as error:
        print(error)
        print('Cannot create new blacklist.')
        blacklist = TrieNode()
