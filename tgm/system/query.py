"""

"""

from operator import and_, or_


class Query(object):
    """ """
    optimizations = {
        and_: set.intersection,
        or_: set.union,

    }

    def __init__(self, operation, *arguments):
        self.operation = operation
        self.args = arguments

    def get_candidates(self, test):
        if self.operation == "and":
            pass


    def get_unoptimizable(self):
        pass
