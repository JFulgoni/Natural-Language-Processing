#import nltk
import A
from nltk.align import AlignedSent
from nltk.align import IBMModel1
from collections import defaultdict
import time

class BerkeleyAligner():

    def __init__(self, align_sents, num_iter):
        self.t, self.q = self.train(align_sents, num_iter)

    # TODO: Computes the alignments for align_sent, using this model's parameters. Return
    #       an AlignedSent object, with the sentence pair and the alignments computed.
    def align(self, align_sent):
        this_alignment = []
        en_len = len(align_sent.words)
        ger_len = len(align_sent.mots)

        for j, en_word in enumerate(align_sent.words):
            p = self.t[en_word][None] * self.q[0][j + 1][en_len][ger_len]
            max_prob = (p, None)
            for i, ger_word in enumerate(align_sent.mots):
                this_p = self.t[en_word][ger_word] * self.q[i + 1][j + 1][en_len][ger_len]
                this_prob = (this_p, i)
                max_prob = max(max_prob, this_prob)

            if max_prob[1] is not None:
                this_alignment.append((j, max_prob[1]))

        return AlignedSent(align_sent.words, align_sent.mots, this_alignment)

    # TODO: Implement the EM algorithm. num_iters is the number of iterations. Returns the
    # translation and distortion parameters as a tuple.
    def train(self, aligned_sents, num_iters):
        t = {}
        q = {}

        # John's edit starts here
        # initialization step of EM
        # might have to change this to the IBMModel1 init method
        # instead of this function
        ibm1 = IBMModel1(aligned_sents, 10)
        t_eg = ibm1.probabilities
        t_ge = ibm1.probabilities
        t_eg_copy = t_eg.copy()

        align_eg = self.initEM(aligned_sents, 'Forwards') # go forwards for the first set


        align_ge = self.initEM(aligned_sents, 'Backwards')
        align_eg_copy = align_eg.copy()

        # make vocabulary sets for each language
        ger_vocab = set()
        en_vocab = set()
        for sent in aligned_sents:
            en_vocab.update(sent.words)
            ger_vocab.update(sent.mots)
        en_vocab.add(None)
        ger_vocab.add(None)

        derp = True
        derp2 = True
        derp3 = True

        # begin EM Iterations
        for n in range (0, num_iters):
            print 'Iter: ' + str(n + 1) + ' of 10'
            count_eg = defaultdict(lambda: defaultdict(lambda: 0.0)) # counts going forward
            count_ge = defaultdict(lambda: defaultdict(lambda: 0.0)) # counts going backward
            total_g = defaultdict(lambda: 0.0)
            total_e = defaultdict(lambda: 0.0)

            # denominators for the equation
            total_enorm = defaultdict(lambda: 0.0)
            total_gnorm = defaultdict(lambda: 0.0)

            count_align_eg = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0))))
            total_align_eg = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
            count_align_ge = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0))))
            total_align_ge = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

            for sent in aligned_sents:
                german = [None] + sent.mots
                english = [None] + sent.words
                ger_len = len(german) - 1
                en_len = len(english) - 1

                # this whole thing uses the equation on page 13 of collins
                # get sum for the denominator
                # this uses dictionaries total_enorm and total_gnorm
                # forwards
                for j in range (1, en_len + 1):
                    en_word = english[j]
                    for i in range (0, ger_len + 1): # supposed to be 0 or 1?
                        # if derp3:
                        #     print 'Derp3'
                        #     print german[i]
                        #     derp3 = False
                        ger_word = german[i]
                        add_en = t_eg[en_word][ger_word] * align_eg[i][j][en_len][ger_len]
                        total_enorm[en_word] = total_enorm[en_word] + add_en
                # backwards
                for j in range (1, ger_len + 1):
                    ger_word = german[j]
                    for i in range (0, en_len + 1): # supposed to be 0 or 1?
                        en_word = english[i]
                        add_ger = t_ge[ger_word][en_word] * align_ge[i][j][ger_len][en_len]
                        total_gnorm[ger_word] = total_gnorm[ger_word] + add_ger

                # compute counts using delta
                # uses count_eg, total_g, count_align_eg, total_align_eg
                # forwards
                for j in range (1, en_len + 1):
                    en_word = english[j]
                    for i in range (0, ger_len + 1): # supposed to be 0 or 1?
                        ger_word = german[i]
                        add_en = t_eg[en_word][ger_word] * align_eg[i][j][en_len][ger_len]
                        # if derp:
                        #     print 'Derp'
                        #     print ger_word
                        #     print t_eg[en_word][ger_word]
                        #     print align_eg[i][j][en_len][ger_len]
                        #     derp = False

                        en_delta = add_en / total_enorm[en_word]
                        #now that we have delta, add it to all of our variables from above
                        count_eg[en_word][ger_word] = count_eg[en_word][ger_word] + en_delta
                        total_g[ger_word] = total_g[ger_word] + en_delta

                        count_align_eg[i][j][en_len][ger_len] = count_align_eg[j][i][en_len][ger_len] + en_delta
                        total_align_eg[j][en_len][ger_len] = total_align_eg[j][en_len][ger_len] + en_delta
                # backwards
                for j in range (1, ger_len + 1):
                    ger_word = german[j]
                    # if derp:
                    #     print ger_word
                    #     derp = False
                    for i in range (0, en_len + 1): # supposed to be 0 or 1?
                        en_word = english[i]
                        add_ger = t_ge[ger_word][en_word] * align_ge[i][j][ger_len][en_len]
                        # if add_ger == 0:
                        #     print 'add en sucks'
                        #     print en_word
                        #     print ger_word
                        #     print t_ge[ger_word][en_word]
                        #     print align_ge[i][j][ger_len][en_len]
                        ger_delta = add_ger / total_gnorm[ger_word]

                        #now that we have delta, add it to all of our variables from above
                        count_ge[ger_word][en_word] = count_ge[ger_word][en_word] + ger_delta
                        total_e[en_word] = total_e[en_word] + ger_delta

                        count_align_ge[i][j][ger_len][en_len] = count_align_ge[i][j][ger_len][en_len] + ger_delta
                        total_align_ge[j][ger_len][en_len] = total_align_ge[j][ger_len][en_len] + ger_delta
                # now done with for sent in aligned sent

            # copied form IBM2 Pydoc
            # Smoothing the counts for alignments
            for alignSent in aligned_sents:
                en_set = alignSent.words
                fr_set = [None] + alignSent.mots
                l_f = len(fr_set) - 1
                l_e = len(en_set)

                laplace = 1.0
                for i in range(0, l_f+1):
                    for j in range(1, l_e+1):
                        value = count_align_eg[i][j][l_e][l_f]
                        if 0 < value < laplace:
                            laplace = value

                laplace *= 0.5
                for i in range(0, l_f+1):
                    for j in range(1, l_e+1):
                        count_align_eg[i][j][l_e][l_f] += laplace

                initial_value = laplace * l_e
                for j in range(1, l_e+1):
                    total_align_eg[j][l_e][l_f] += initial_value

            for alignSent in aligned_sents:
                en_set = alignSent.mots
                fr_set = [None] + alignSent.words
                l_f = len(fr_set) - 1
                l_e = len(en_set)

                laplace = 1.0
                for i in range(0, l_f+1):
                    for j in range(1, l_e+1):
                        value = count_align_ge[i][j][l_e][l_f]
                        if 0 < value < laplace:
                            laplace = value

                laplace *= 0.5
                for i in range(0, l_f+1):
                    for j in range(1, l_e+1):
                        count_align_ge[i][j][l_e][l_f] += laplace

                initial_value = laplace * l_e
                for j in range(1, l_e+1):
                    total_align_ge[j][l_e][l_f] += initial_value

            # # Now we average the distortion and translation
            # # might be able to put this in the above loop
            # for sent in aligned_sents:
            #     german = [None] + sent.mots
            #     english = [None] + sent.words
            #     ger_len = len(german) - 1
            #     en_len = len(english) - 1
            #
            #     # averaging the two values for forward and backward q (distortion)
            #     # this can be done inside of the big loop for each sent
            #     for j in range (1, ger_len + 1):
            #         for i in range (0, en_len + 1):
            #             en_val = count_align_eg[i][j][en_len][ger_len]
            #             ger_val = count_align_ge[j][i][ger_len][en_len]
            #             avg_val = (en_val + ger_val) / float(2)
            #             # now set the value to each
            #             count_align_eg[i][j][en_len][ger_len] = avg_val
            #             count_align_ge[j][i][ger_len][en_len] = avg_val
            #
            # # averaging the values for t (translation)
            # for en_word in count_eg:
            #     for ger_word in count_ge:
            #         en_count = count_eg[en_word][ger_word]
            #         ger_count = count_ge[ger_word][en_word]
            #         avg_count = (en_count + ger_count) / float(2)
            #         # now set the value to each
            #         count_eg[en_word][ger_word] = avg_count
            #         count_ge[ger_word][en_word] = avg_count

            # now we can find the next round of translation and distortion probabilities
            t_eg_new = defaultdict(lambda: defaultdict(lambda: 0.0)) # counts going forwards
            align_eg_new = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0))))

            t_ge_new = defaultdict(lambda: defaultdict(lambda: 0.0)) # counts going backwards
            align_ge_new = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0))))

            # Estimating lexical translation probabilities
            for en_word in en_vocab:
                for ger_word in ger_vocab:
                    # if derp2:
                    #     print 'Derp2'
                    #     print ger_word
                    #     derp2 = False
                    try:
                        t_eg_new[en_word][ger_word] = count_eg[en_word][ger_word] / total_g[ger_word]
                        t_ge_new[ger_word][en_word] = count_ge[ger_word][en_word] / total_e[en_word]
                    except:
                        print 'Except triggered:'
                        print ger_word
                        print en_word
                        exit(1)

            # Estimating new alignment probabilities
            for sent in aligned_sents:
                german = [None] + sent.mots
                english = [None] + sent.words
                ger_len = len(german) - 1
                en_len = len(english) - 1
                # forwards
                for j in range (1, en_len + 1):
                    for i in range (0, ger_len + 1): # supposed to be 0 or 1?
                        align_eg_new[i][j][en_len][ger_len] = count_align_eg[i][j][en_len][ger_len] / total_align_eg[j][en_len][ger_len]
                # backwards
                for j in range (1, ger_len + 1):
                    for i in range (0, en_len + 1): # supposed to be 0 or 1?
                        align_ge_new[i][j][ger_len][en_len] = count_align_ge[i][j][ger_len][en_len] / total_align_ge[j][ger_len][en_len]

            # set values so it loops properly
            t_eg = t_eg_new.copy()
            t_ge = t_ge_new.copy()
            align_eg = align_eg_new.copy()
            align_ge = align_ge_new.copy()


        # Now we average the distortion and translation
        for sent in aligned_sents:
            german = [None] + sent.mots
            english = [None] + sent.words
            ger_len = len(german) - 1
            en_len = len(english) - 1

            # averaging the two values for forward and backward q (distortion)
            # this can be done inside of the big loop for each sent
            for j in range (1, ger_len + 1):
                for i in range (0, en_len + 1):
                    en_val = align_eg[i][j][en_len][ger_len]
                    ger_val = align_ge[j][i][ger_len][en_len]
                    avg_val = (en_val + ger_val) / float(2)
                    # now set the value to each
                    align_eg[i][j][en_len][ger_len] = avg_val

        # averaging the values for t (translation)
        for en_word in t_eg:
            for ger_word in t_ge:
                en_count = t_eg[en_word][ger_word]
                ger_count = t_ge[ger_word][en_word]
                avg_count = (en_count + ger_count) / float(2)
                # now set the value to each
                t_eg[en_word][ger_word] = avg_count

        # return provided by the professor
        t = t_eg.copy()
        q = align_eg_copy.copy() # using a copy of the initialized q improves the results
        # which means align_eg as it iterates hurts the accuracy
        return (t,q)


    # initialization step of EM algorithm
    def initEM(self, aligned_sents, forwards):
        # set up t and q using default dict
        # nevermind
        q = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0))))
        #t = defaultdict(lambda: defaultdict(lambda: 0.0))

        # now we have to initialize q in a similar fashion
        # q is (1/L+1) for the whole set, not per word
        # I also don't want to make q a four dimensional dictionary
        for sent in aligned_sents:
            if forwards == 'Forwards':
                english = sent.words
                german = [None] + sent.mots
            else:
                english = sent.mots
                german = [None] + sent.words

            en_len = len(english)
            ger_len = len(german) - 1
            init_val = 1 / float(ger_len + 1)
            for i in range(0, ger_len + 1): # want it to be inclusive
                for j in range (1, en_len + 1): # want it to be inclusive
                    #q[(i, j, en_len, ger_len)] = init_val
                    q[i][j][en_len][ger_len] = init_val
        return q



def main(aligned_sents):
    t0 = time.time()
    print 'Starting Berkeley Aligner'
    ba = BerkeleyAligner(aligned_sents, 10)
    A.save_model_output(aligned_sents, ba, "ba.txt")
    avg_aer = A.compute_avg_aer(aligned_sents, ba, 50)

    print ('Berkeley Aligner')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))
    t1 = time.time()
    print 'Total B Time: ' + str(t1 - t0)
