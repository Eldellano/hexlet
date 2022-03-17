from functions import get_function

take = get_function()

assert take([], 2) == []
assert take([1, 2, 3]) == [1]
assert take([1, 2, 3], 2) == [1, 2]
assert take([4, 3], 9) == [4, 3]
