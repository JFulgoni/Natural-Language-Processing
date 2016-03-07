class Transition(object):
    """
    This class defines a set of transitions which are applied to a
    configuration to get the next configuration.
    """
    # Define set of transitions
    LEFT_ARC = 'LEFTARC'
    RIGHT_ARC = 'RIGHTARC'
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'

    def __init__(self):
        raise ValueError('Do not construct this object!')

    @staticmethod
    def left_arc(conf, relation):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
        idx_wi = conf.stack[-1]
        idx_wj = conf.buffer[0] # we can't use pop like below

	# Can't operate if idx_wi = 0
	if idx_wi == 0:
		return -1

	# For this, we only operate if the does not have a head
        has_head  = False
        for arc in conf.arcs:
            if arc[2] == idx_wi: # if the child of arc equals wi
                has_head = True
        if has_head:
            return -1

        # wj is dependent on wi
	idx_wi = conf.stack.pop(-1) # remove from the stack
        conf.arcs.append((idx_wj, relation, idx_wi))


        # raise NotImplementedError('Please implement left_arc!')
        # return -1

    @staticmethod
    def right_arc(conf, relation):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
        if not conf.buffer or not conf.stack:
            return -1

        # You get this one for free! Use it as an example.

        idx_wi = conf.stack[-1]
        idx_wj = conf.buffer.pop(0)

        conf.stack.append(idx_wj)
        conf.arcs.append((idx_wi, relation, idx_wj))

    @staticmethod
    def reduce(conf):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """

        idx_wi = conf.stack[-1]
	reduce_me = False
	# for this, reduce should only operate if the arc has a head
        for arc in conf.arcs:
            if arc[2] == idx_wi:
                reduce_me = True

	if reduce_me:
		conf.stack.pop(-1)
	else:
		return -1
        #raise NotImplementedError('Please implement reduce!')
        #return -1

    @staticmethod
    def shift(conf):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
        if not conf.buffer or not conf.stack:
            return -1
	# get word from buffer
        idx_wi = conf.buffer.pop(0)
        # and push it onto the stack!
        conf.stack.append(idx_wi)

        #raise NotImplementedError('Please implement shift!')
        #return -1
