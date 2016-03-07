from nltk.compat import python_2_unicode_compatible

printed = False

@python_2_unicode_compatible
class FeatureExtractor(object):
    @staticmethod
    def _check_informative(feat, underscore_is_informative=False):
        """
        Check whether a feature is informative
        """

        if feat is None:
            return False

        if feat == '':
            return False

        if not underscore_is_informative and feat == '_':
            return False

        return True

    @staticmethod
    def find_left_right_dependencies(idx, arcs):
        left_most = 1000000
        right_most = -1
        dep_left_most = ''
        dep_right_most = ''
        for (wi, r, wj) in arcs:
            if wi == idx:
                if (wj > wi) and (wj > right_most):
                    right_most = wj
                    dep_right_most = r
                if (wj < wi) and (wj < left_most):
                    left_most = wj
                    dep_left_most = r
        return dep_left_most, dep_right_most

    # this is the given method
    # I'm going to leave this untouched until I can figure out a better option
    @staticmethod
    def extract_features(tokens, buffer, stack, arcs):
        """
        This function returns a list of string features for the classifier

        :param tokens: nodes in the dependency graph
        :param stack: partially processed words
        :param buffer: remaining input words
        :param arcs: partially built dependency tree

        :return: list(str)
        """

        """
        Think of some of your own features here! Some standard features are
        described in Table 3.2 on page 31 of Dependency Parsing by Kubler,
        McDonald, and Nivre

        [http://books.google.com/books/about/Dependency_Parsing.html?id=k3iiup7HB9UC]
        """

        result = []


        global printed
        if not printed:
            #print("This is not a very good feature extractor!")
            printed = True

        '''
        Features that exist in dependencygraph.py, called by trasitionparser.py
                'word': word, -> given
                'lemma': '_', -> added
                'ctag': tag, -> added (0 and 1)
                'tag': tag, -> added
                'feats': '_', -> given
                'rel': '_',
                'deps': defaultdict(),
                'head': '_',
                'address': index + 1,
        '''

        # an example set of features:
        if stack:
            stack_idx0 = stack[-1]
            token = tokens[stack_idx0]
            if FeatureExtractor._check_informative(token['word'], True):
                result.append('STK_0_FORM_' + token['word'])

            # John's edit starts here
            # add the lemma for stack 0
            if FeatureExtractor._check_informative(token['lemma'], True):
                result.append('STK_0_LEMMA_' + token['lemma'])
            else: # add an underscore if we can't find it
                result.append('STK_0_LEMMA_' + '_')

            # add the tag for stack 0
            if FeatureExtractor._check_informative(token['tag'], True):
                result.append('STK_0_TAG_' + token['tag'])

            # add the ctag for stack 0
            if FeatureExtractor._check_informative(token['ctag'], True):
                result.append('STK_0_CTAG_' + token['ctag'])

            # want to try and get the ctag for second item in the stack
            if len(stack) > 1:
                stack_idx1 = stack[-2]
                token1 = tokens[stack_idx1]
                if FeatureExtractor._check_informative(token1['ctag'], True):
                    result.append('STK_1_CTAG_' + token1['ctag'])


                # from the chart, the stack doesn't have a good form to use
                # that's why I don't write it out

            # John's edit ends here
            if 'feats' in token and FeatureExtractor._check_informative(token['feats']):
                feats = token['feats'].split("|")
                for feat in feats:
                    result.append('STK_0_FEATS_' + feat)

            # Left most, right most dependency of stack[0]
            dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(stack_idx0, arcs)

            if FeatureExtractor._check_informative(dep_left_most):
                result.append('STK_0_LDEP_' + dep_left_most)
            if FeatureExtractor._check_informative(dep_right_most):
                result.append('STK_0_RDEP_' + dep_right_most)

        if buffer:
            buffer_idx0 = buffer[0]
            token = tokens[buffer_idx0]
            if FeatureExtractor._check_informative(token['word'], True):
                result.append('BUF_0_FORM_' + token['word'])

            # John's Edit starts here
            # add lemma for buffer 0
            if FeatureExtractor._check_informative(token['lemma'], True):
                result.append('BUF_0_LEMMA_' + token['lemma'])
            else: # add an underscore if we can't find it
                result.append('BUF_0_LEMMA_' + '_')

            # add tag for buffer 0
            if FeatureExtractor._check_informative(token['tag'], True):
                result.append('BUF_0_TAG_' + token['tag'])

            # add the ctag for buffer 0
            if FeatureExtractor._check_informative(token['ctag'], True):
                result.append('BUF_0_CTAG_' + token['ctag'])

            # want to try and get the ctag for second item in the buffer now
            if len(buffer) > 1:
                buffer_idx1 = buffer[1]
                token1 = tokens[buffer_idx1]

                # add ctag for buffer 1
                if FeatureExtractor._check_informative(token1['ctag'], True):
                    result.append('BUF_1_CTAG_' + token1['ctag'])

                # We've past the acceptable mark!

                # add term for buffer 1
                if FeatureExtractor._check_informative(token1['word'], True):
                    result.append('BUF_1_FORM_' + token1['word'])


            # if len(buffer) > 2:
            #     buffer_idx2 = buffer[2]
            #     token2 = tokens[buffer_idx2]
            #
            #     # add ctag for buffer2

            # John's Edit ends here
            if 'feats' in token and FeatureExtractor._check_informative(token['feats']):
                feats = token['feats'].split("|")
                for feat in feats:
                    result.append('BUF_0_FEATS_' + feat)

            dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(buffer_idx0, arcs)

            if FeatureExtractor._check_informative(dep_left_most):
                result.append('BUF_0_LDEP_' + dep_left_most)
            if FeatureExtractor._check_informative(dep_right_most):
                result.append('BUF_0_RDEP_' + dep_right_most)

        return result
