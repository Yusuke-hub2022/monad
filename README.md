
# Monad
Monad in Python.
It has Maybe, Either and IO.

## Maybe
Consists of Just and Nothing type. Nothing doesn't have any value.
```python
from monad import Maybe, Either, IO

def trimAndUpper(a):
    return (
        Maybe.justOrNothing(a)
        .map(str.strip)
        .map(str.upper)
        .getOrElse(None)
    ) 

# Just
result = trimAndUpper('  aaa  ')
# result -> 'AAA'

# Nothing
result = trimAndUpper([])
# result -> None
```

## Either
Consists of Right and Left type.
Either is like Maybe, but Left can have value.
```python
from monad import Either
import json

def fromJSON(jsonString):
    try:
        data = Either.right(json.loads(jsonString)) # Right
    except Exception as e:
        data = Either.left(e) # Left
    return data

def pickupNumbers(d):
    return [ d['a'], d['b'] ]

def times10(n):
    return n * 10

def plus3(n):
    return n + 3

def calcFromJSON(jsonString):
    return (
        fromJSON(jsonString)
        .map(pickupNumbers)
        .map(sum)
        .map(times10)
        .map(plus3)
        .getOrElse('JSON Error')
    )
    
# Right
result = calcFromJSON('{"a": 10, "b": 5}')
# result -> 153

# Left
result = calcFromJSON('invalid JSON')
# result -> 'JSON Error'
```

## IO
Can delay evaluation.
```python
from monad import IO

def plus10(n):
    return n + 10

def times10(n):
    return n * 10

def plus3(n):
    return n + 3

calc = IO.of(5).map(plus10).map(times10).map(plus3).map(print)
calc.run()
# -> 153
```

