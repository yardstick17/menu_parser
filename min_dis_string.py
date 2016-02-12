import sys
import string 

DICTIONARY = "moderator_dish_names.txt";

# Keep some interesting statistics
NodeCount = 0
WordCount = 0
tr = string.maketrans(string.whitespace, ' '*len(string.whitespace))

class TrieNode:
    def __init__(self):
        self.word = None
        self.children = {}

        global NodeCount
        NodeCount += 1

    def insert( self, word ):
        node = self
        for letter in word:
            if letter not in node.children: 
                node.children[letter] = TrieNode()

            node = node.children[letter]

        node.word = word

trie = TrieNode()
with open('moderator_dish_names.txt' , 'rt') as f:
    for line in f:
        #print line
        line = line[:-1]
        #line = line.translate(tr).replace(' ', '')
        trie.insert(line.lower())
        WordCount += 1


print "Read %d words into %d nodes" % (WordCount, NodeCount)
def min_distance_dish(word , maxCost):

    l = search(word , maxCost)
    l.sort(key=lambda x: x[1])
    try:
        print 'found this ' , l
        return l[0][0]
    except:
        return word

# The search function returns a list of all words that are less than the given
# maximum distance from the target word
def search( word, maxCost ):

    # build first row
    currentRow = range( len(word) + 1 )

    results = []

    # recursively search each branch of the trie
    for letter in trie.children:
        searchRecursive( trie.children[letter], letter, word, currentRow, 
            results, maxCost )

    return results

# This recursive helper is used by the search function above. It assumes that
# the previousRow has been filled in already.
def searchRecursive( node, letter, word, previousRow, results, maxCost ):

    columns = len( word ) + 1
    currentRow = [ previousRow[0] + 1 ]

    # Build one row for the letter, with a column for each letter in the target
    # word, plus one for the empty string at column 0
    for column in xrange( 1, columns ):

        insertCost = currentRow[column - 1] + 1
        deleteCost = previousRow[column] + 1

        if word[column - 1] != letter:
            replaceCost = previousRow[ column - 1 ] + 1
        else:                
            replaceCost = previousRow[ column - 1 ]

        currentRow.append( min( insertCost, deleteCost, replaceCost ) )

    # if the last entry in the row indicates the optimal cost is less than the
    # maximum cost, and there is a word in this trie node, then add it.
    if currentRow[-1] <= maxCost and node.word != None:
        results.append( (node.word, currentRow[-1] ) )

    # if any entries in the row are less than the maximum cost, then 
    # recursively search each branch of the trie
    if min( currentRow ) <= maxCost:
        for letter in node.children:
            searchRecursive( node.children[letter], letter, word, currentRow, 
                results, maxCost )
'''
while 1:

    y = raw_input('TARGET:\n')
    start = time.time()

    TARGET = y 
    MAX_COST = int(2)
    results = min_distance_dish( TARGET.lower(), MAX_COST )

    end = time.time()
    print 'results are : '
    print results
#    for result in results: print result        

    print "Search took %g s" % (end - start)
'''
