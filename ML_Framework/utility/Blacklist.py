from sys import setrecursionlimit
import re
import pickle
import pandas as pd

setrecursionlimit(10000)

DATASET_PATH = "ML_Framework/Dataset/"
CSVS_PATH = DATASET_PATH + "csvs/"
MODELS_PATH = DATASET_PATH + "models/"

class TrieNode(object):
    def __init__(self, char=None):
        self.char = char
        self.children = []
        self.terminal = False


class Blacklist:
    def __init__(self):
        self.root = TrieNode()
    
    # add new url in TRIE
    def add_url(self, url):
        node = self.root
        for char in url:
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
    def find_url(self, url):
        if not self.root.children:
            return False

        node = self.root
        for char in url:
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
    def create_blacklist(self, path_to_csv =  CSVS_PATH + 'filtered_malicious.csv'):
        blacklisted_urls = pd.read_csv(path_to_csv)['url']
        for url in blacklisted_urls:
            # remove protocol
            blacklist.add_url(re.sub(r'^http(s*)://', '', url))
        pickle.dump(blacklist, open(MODELS_PATH + 'blacklist.pkl', 'wb'))
        

# Actual blacklist
try:
    blacklist = pickle.load(open( MODELS_PATH + 'blacklist.pkl', 'rb'))
except:
    print('No blacklist found, creating new.')
    try:
        blacklist = Blacklist()
        blacklist.create_blacklist(CSVS_PATH + 'filtered_malicious.csv')
        print('Blacklist dumpled as blacklist.pkl')
    except Exception as error:
        print(error)
        print('Cannot create new blacklist.')
