from faker import Faker

fake = Faker(seed=42)
for _ in range(5):
    print(fake.email())
    print(fake.password())
"""
adam31@example.com
%(6BD_!oy!
chelsea56@example.org
MM9M70$bW(
monica94@example.com
j1DzHDQR^X
qwilliams@example.com
@GuWFq%s^5
stephenriggs@example.net
%D3TzSnWRD
"""
