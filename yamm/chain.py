import random


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

    def step(self, state):
        try:
            s = self[state]
            return tuple(random.choices(tuple(s.keys()), tuple(s.values())))
        except KeyError:
            return None

    def walk(self, start):
        def walk_generator(current_state):
            while current_state:
                yield current_state
                current_state = self.step(current_state)
        return walk_generator(start)

    def walk_until(self, start, max_steps):
        generator = self.walk(start)
        return tuple(next(generator) for i in range(max_steps))
