import registry
class Cat:  # noqa: WPS306
    legs = 4


class Bird:  # noqa: WPS306
    legs = 2


# BEGIN (write your solution here)
registry.add(Cat)
registry.add(Bird)
# END
