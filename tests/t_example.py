from unittest import TestCase

# -> For all inspection disabling modifier see (https://gist.github.com/pylover/7870c235867cf22817ac5b096defb768)
# noinspection PyUnresolvedReferences
class ExampleTest(TestCase):
    def test_print_hi(self):
        print("Hi, this test was sucessful!")
        self.assertTrue(True)
