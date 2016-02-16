
class Sandra:
    def __init__(self):
        self.name       = 'Sandra'
        self.full_name  = 'Sandra I. Morales.'
        self.email       = 'ismorvil@hotmail.com'
        self.months     = ['Jan']
        self.perct      = 1.25/100


class Alan:
    def __init__(self):
        self.name       = 'Alan'
        self.full_name  = 'Alan Garcia V.'
        self.email       = 'gagvillegas@hotmail.com'
        self.perct      = 1.25/100
        self.months     = ['Jan']


if __name__ == "__main__":
    alan = Alan()
    print Alan().full_name, alan.email
