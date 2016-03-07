__author__ = 'johnfulgoni'

import sys
from providedcode.dependencygraph import DependencyGraph
from providedcode.transitionparser import TransitionParser

# DON'T PRINT ANYTHING! OR ELSE IT MESSES THINGS UP

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 2:
        #print sys.argv[1] # just to see

        sentence_list = []
        for sent in sys.stdin: # get the sentences from the englishfile
            sentence = DependencyGraph.from_sentence(sent)
            sentence_list.append(sentence)

        my_model = sys.argv[1]  # should be 'english.model'
        tp = TransitionParser.load(my_model)
        parsed = tp.parse(sentence_list)

        # following the example in test.py
        # but we're not writing it to a file
        for p in parsed:
            print p.to_conll(10).encode('utf-8')
            print '\n'

    else:
        print "Need two arguments"
        exit(1)