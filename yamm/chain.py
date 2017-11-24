class Chain(dict):
    """
    Representation of a markov chain as a dictionary.
    The keys are state-tuples and the values are dictionaries.
    In these dictionaries the keys are single states and the values are weights
    to reach this state.
    Example:
    {("hello",): {"hello": 0.5, "markov": 0.5},
    ("markov",): {"hello": 2, "markov": 3}}
    """

    @classmethod
    def from_data(cls, data, order=1):
        raise NotImplementedError

    @classmethod
    def from_matrix(cls, matrix):
        raise NotImplementedError

    def step(self, start):
        raise NotImplementedError

    def walk(self, start):
        raise NotImplementedError

    def walk_until(self, start, max_steps):
        raise NotImplementedError
