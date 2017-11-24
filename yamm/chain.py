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

    @property
    def order(self):
        return len(tuple(self.keys())[0])

    @classmethod
    def from_data(cls, data, order=1):
        nested = (data[i:] for i in range(order + 1))
        result = {}
        for n in zip(*nested):
            state = n[:-1]
            aim = n[-1]
            if state not in result:
                result[state] = {}
            if aim not in result[state]:
                result[state][aim] = 0
            result[state][aim] += 1
        return cls(result)

    def step(self, state):
        try:
            s = self[state]
            return random.choices(tuple(s.keys()), tuple(s.values()), k=1)[0]
        except KeyError:
            return None

    def walk(self, start):
        def walk_generator(current_state):
            for element in current_state:
                yield element
            res = self.step(current_state)
            while res is not None:
                yield res
                current_state = current_state[1:] + (res,)
                res = self.step(current_state)
        return walk_generator(start)

    def walk_until(self, start, max_steps):
        generator = self.walk(start)
        return tuple(next(generator) for i in range(max_steps))
