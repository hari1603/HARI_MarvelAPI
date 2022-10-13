import argparse


class Person:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Provide the api key, hash")
        parser.add_argument('api_key', type=str, help='provide the api_key')
        parser.add_argument('hash', type=str, help='provide the hash')

        args = parser.parse_args()
        self.api_key = getattr(args, "api_key")
        self.hash = getattr(args, "hash")
    
    def fn(self, nameStartsWith):
        print(self.api_key)
        print(self.hash)
        print(nameStartsWith)

p1 = Person()
p1.fn('a')

print(p1.api_key)
print(p1.hash)
