
# -------------------
# Maybe

class Maybe:
    # static method

    def just(a):
        return Just(a)

    def nothing():
        return Nothing()

    def justOrNothing(a, pred=lambda x: x):
        if pred(a):
            return Maybe.just(a)
        return Maybe.nothing()

    def of(a):
        return Maybe.just(a)

    # instance method

    def isJust(self):
        return type(self) == Just

    def isNothing(self):
        return type(self) == Nothing

class Just(Maybe):
    def __init__(self, value):
        self.value = value

    def getValue(self):
        return self.value

    def map(self, fn):
        return Maybe.justOrNothing(fn(self.value))

    def getOrElse(self, _):
        return self.value

    def filter(self, pred):
        if pred(self.value):
            return self
        return Maybe.nothing()

    def chain(self, fn):
        return fn(self.value)

    def __str__(self):
        return 'Maybe.Just({})'.format(self.value)

class Nothing(Maybe):
    def map(self, _):
        return self

    def getValue(self):
        raise TypeError('Nothing object has no value')

    def getOrElse(self, other):
        return other

    def filter(self, _):
        return self

    def chain(self, _):
        return self

    def __str__(self):
        return 'Maybe.Nothing'

# -------------------
# Either

class Either:

    # static method

    def left(a):
        return Left(a)

    def right(a):
        return Right(a)

    def of (a):
        return Either.right(a)

    def leftOrRight(a, pred=lambda x: x):
        if pred(a):
            return Either.right(a)
        return Either.left(a)

    # instance method

    def __init__(self, value):
        self.value = value

    def getValue(self):
        return self.value

    def isLeft(self):
        return type(self) == Left

    def isRight(self):
        return type(self) == Right

class Left(Either):
    def map(self, _):
        return self

    def getValue(self):
        raise TypeError('can not get the value of a Left')

    def getOrElse(self, other):
        return other

    def orElse(self, fn):
        return fn(self.value)

    def chain(self, _):
        return self

    def getOrElseRaise(self, message):
        raise Error(message)

    def filter(self, _):
        return self

    def __str__(self):
        return 'Either.Left({})'.format(self.value)

class Right(Either):
    def map(self, fn):
        return Either.of(fn(self.value))

    def getValue(self):
        return self.value

    def getOrElse(self, _):
        return self.value

    def orElse(self, _):
        return self

    def chain(self, fn):
        return fn(self.value)

    def getOrElseRaise(self, _):
        return self.value

    def filter(self, pred):
        return Either.leftOrRight(pred(self.value))

    def __str__(self):
        return 'Either.Right({})'.format(self.value)

# -------------------
# IO

class IO:

    # static method

    def of(a):
        return IO(lambda : a)

    def makeFrom(fn):
        return IO(fn)

    # instance method

    def __init__(self, effect):
        if not callable(effect):
            raise TypeError('{} is not callable'.format(effect))
        self.effect = effect

    def run(self):
        return self.effect()

    def map(self, fn):
        this = self
        return IO(lambda : fn(this.effect()))

    def chain(self, fn):
        return fn(self.effect())

