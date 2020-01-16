import collections as coll
import itertools as it
import random as rand


class Chain(dict):
    """
    Representation of a markov chain as a dictionary.
    The keys are state-tuples and the values are dictionaries.
    In these dictionaries the keys are single states and the values are weights
    to reach this state. None is a marker for an end.
    Example:
    {("hello",): {"hello": 0.5, "markov": 0.5},
    ("markov",): {"hello": 2, "markov": 3, None : 4}}
    """

    # properties
    @property
    def order(self):
        return len(tuple(self.keys())[0])

    # input data
    def vary_weight(self, state, aim, value=1):
        if state not in self:
            self[state] = coll.Counter()
        if aim not in self[state]:
            self[state][aim] = 0
        self[state][aim] += value
        if self[state][aim] <= 0:
            self[state].pop(aim)
            if not self[state]:
                self.pop(state)

    @classmethod
    def from_data(cls, data, order=1):
        chain = cls()
        nested = (it.islice(data, i, None) for i in range(order + 1))
        for n in zip(*nested):
            state = n[:-1]
            aim = n[-1]
            chain.vary_weight(state, aim)
        last = tuple(data[-i] for i in range(1, order + 1))
        chain.vary_weight(last, None)
        return chain

    def merge(self, chain):
        result = self.__class__()
        for s in self:
            if s in chain:
                result[s] = coll.Counter(self[s]) + coll.Counter(chain[s])
            else:
                result[s] = coll.Counter(self[s])
        for s in chain:
            if s not in self:
                result[s] = coll.Counter(chain[s])
        return result

    # normal random markov output
    def step(self, state):
        try:
            s = self[state]
        except KeyError:
            return None
        return rand.choices(tuple(s.keys()), tuple(s.values()), k=1)[0]

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

    # deterministic output
    @classmethod
    def distribute(cls, dic):
        def distribute_generator():
            pairs = []
            # make weights which are evenly spaced
            for key in dic:
                step = 1.0 / (dic[key] + 1)
                pairs += [(key, step * i) for i in range(1, dic[key] + 1)]
            pairs_sorted = sorted(pairs, key=lambda x: x[1])
            for x in it.cycle(pairs_sorted):
                yield x[0]

        return distribute_generator()

    def make_deterministic_map(self):
        self.__deterministic_map = {}
        for key in self:
            self.__deterministic_map[key] = self.distribute(self[key])

    def deterministic_step(self, state):
        try:
            s = self.__deterministic_map[state]
        except KeyError:
            return None
        return next(s)

    def walk_deterministic(self, start):
        def walk_generator(current_state):
            for element in current_state:
                yield element
            res = self.deterministic_step(current_state)
            while True:
                yield res
                if res is None:
                    current_state = start
                else:
                    current_state = current_state[1:] + (res,)
                res = self.deterministic_step(current_state)

        return walk_generator(start)

    def walk_deterministic_until(self, start, max_steps):
        generator = self.walk_deterministic(start)
        return tuple(next(generator) for i in range(max_steps))
