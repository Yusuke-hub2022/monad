import unittest
from monad import Maybe, Just, Nothing, Either, Left, Right, IO

class TestMaybe(unittest.TestCase):
    def test_create_just(self):
        j = Maybe.just('a')
        self.assertEqual(type(j), Just)

    def test_create_nothing(self):
        n = Maybe.nothing()
        self.assertEqual(type(n), Nothing)

    def test_justOrNothing(self):
        j = Maybe.justOrNothing('a')
        self.assertEqual(type(j), Just)
        n = Maybe.justOrNothing(None)
        self.assertEqual(type(n), Nothing)

    def test_of(self):
        j = Maybe.of('a')
        self.assertEqual(type(j), Just)

    def test_isJust(self):
        j = Maybe.of('a')
        self.assertTrue(j.isJust())

    def test_isNothing(self):
        n = Nothing()
        self.assertTrue(n.isNothing())

class TestJust(unittest.TestCase):
    def test_getValue(self):
        j = Just('a')
        self.assertEqual(j.getValue(), 'a')

    def test_map(self):
        result = Just('a').map(str.upper)
        self.assertEqual(type(result), Just)

    def test_getOrElse(self):
        j = Just('a')
        self.assertEqual(j.getOrElse('_'), 'a')

    def test_filter(self):
        def len1(s):
            return len(s) == 1

        def len10(s):
            return len(s) == 10

        j = Just('a')

        result1 = j.filter(len1) 
        self.assertEqual(type(result1), Just)

        result2 = j.filter(len10) 
        self.assertEqual(type(result2), Nothing)

    def test_chain(self):
        j = Just('a')
        self.assertEqual(j.chain(str.upper), 'A')

    def test___str__(self):
        j = Just('a')
        expected = 'Maybe.Just(a)'
        self.assertEqual(str(j), expected)

class TestNothing(unittest.TestCase):
    def test_map(self):
        n = Nothing()
        self.assertEqual(type(n.map('_')), Nothing)

    def test_getValue(self):
        n = Nothing()
        with self.assertRaises(TypeError):
            n.getValue()

    def test_getOrElse(self):
        n = Nothing()
        self.assertEqual(n.getOrElse('default value'), 'default value')

    def test_filter(self):
        n = Nothing()
        self.assertEqual(n.filter('_'), n)

    def test_chain(self):
        n = Nothing()
        self.assertEqual(n.chain('_'), n)

    def test___str__(self):
        n = Nothing()
        self.assertEqual(str(n), 'Maybe.Nothing')

class TestEither(unittest.TestCase):
    def test_left(self):
        l = Either.left('a')
        self.assertEqual(type(l), Left)

    def test_right(self):
        r = Either.right('a')
        self.assertEqual(type(r), Right)

    def test_of(self):
        r = Either.of('a')
        self.assertEqual(type(r), Right)

    def test_leftOrRight(self):
        result1 = Either.leftOrRight('a')
        self.assertEqual(type(result1), Right)
        result2 = Either.leftOrRight(None)
        self.assertEqual(type(result2), Left)

    def test_getValue(self):
        e = Either('a')
        self.assertEqual(e.getValue(), 'a')

class TestLeft(unittest.TestCase):
    def test_map(self):
        l = Left(None)
        self.assertEqual(l.map('_'), l)

    def test_getValue(self):
        l = Left(None)
        with self.assertRaises(TypeError):
            l.getValue()

    def test_getOrElse(self):
        l = Left(None)
        self.assertEqual(l.getOrElse('other'), 'other')

    def test_orElse(self):
        l = Left('left')
        self.assertEqual(l.orElse(str.upper), 'LEFT')

    def test_chain(self):
        l = Left('left')
        self.assertEqual(l.chain('_'), l)

    def test_getOrElseRaise(self):
        l = Left('left')
        with self.assertRaises(Exception):
            e = l.getOrLeseRaise('Exception raised')
            self.assertEqual(e.message, 'Exception raised')

    def test_filter(self):
        l = Left('left')
        self.assertEqual(l.filter('_'), l)

    def test___str__(self):
        l = Left('this is left')
        self.assertEqual(str(l), 'Either.Left(this is left)')

class TestRight(unittest.TestCase):
    def test_map(self):
        r = Right('a')
        result = r.map(str.upper)
        self.assertEqual(type(result), Right)
        self.assertEqual(result.value, 'A')

    def test_getValue(self):
        r = Right('a')
        self.assertEqual(r.getValue(), 'a')

    def test_getOrElse(self):
        r = Right('a')
        self.assertEqual(r.getOrElse('_'), 'a')

    def test_orElse(self):
        r = Right('a')
        self.assertEqual(r.orElse('_'), r)

    def test_chain(self):
        r = Right('a')
        self.assertEqual(r.chain(str.upper), 'A')

    def test_getOrElseRaise(self):
        r = Right('a')
        self.assertEqual(r.getOrElseRaise('_'), 'a')

    def test_filter(self):
        r = Right('a')

        result1 = r.filter(str.upper)
        self.assertEqual(type(result1), Right)
        self.assertEqual(result1.value, 'A')

        result2 = r.filter(lambda _: None)
        self.assertEqual(type(result2), Left)
        self.assertEqual(result2.value, None)

    def test___str__(self):
        r = Right('a')
        self.assertEqual(str(r), 'Either.Right(a)')

class TestIO(unittest.TestCase):
    def test_of(self):
        io = IO.of('a')
        self.assertEqual(type(io), IO)
        self.assertEqual(io.effect(), 'a')

    def test_makeFrom(self):
        io = IO.makeFrom(lambda : 'a')
        self.assertEqual(io.effect(), 'a')

    def test_init(self):
        io = IO(lambda : 'a')
        self.assertEqual(io.effect(), 'a')

        with self.assertRaises(TypeError):
            io = IO('a')

    def test_map(self):
        io = IO(lambda : 'a')
        result = io.map(str.upper)
        self.assertEqual(result.effect(), 'A')

    def test_chain(self):
        io = IO(lambda : 'a')
        self.assertEqual(io.chain(str.upper), 'A')

    def test_run(self):
        io = IO(lambda : 'a')
        self.assertEqual(io.run(), 'a')


if __name__ == '__main__':
    unittest.main()
