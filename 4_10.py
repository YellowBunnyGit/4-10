from copy import copy
from sys import argv
from fractions import Fraction
import fractions

class Expression:
    def __init__(self, value, string=None):
        self.value = Fraction(value)
        if string is None:
            if value >= 0:
                self.string = str(value)
            else:
                self.string = '(' + str(value) + ')'
        else:
            self.string = string
    
    def __repr__(self):
        return self.string
    
    def __add__(self, other):
        value = self.value + other.value
        string = self.string + '+' + other.string
        return Expression(value, string)
    
    def __iadd__(self, other):
        self.value += other.value
        self.string += '+' + other.string
        return self
    
    def __sub__(self, other):
        value = self.value - other.value
        string = self.string + '-' + other.string
        return Expression(value, string)
    
    def __isub__(self, other):
        self.value -= other.value
        self.string += '-' + other.string
        return self
    
    def __mul__(self, other):
        value = self.value * other.value
        string = self.string + '*' + other.string
        return Expression(value, string)
    
    def __imul__(self, other):
        self.value *= other.value
        self.string += '*' + other.string
        return self
    
    def __truediv__(self, other):
        value = self.value / other.value
        string = self.string + '/' + other.string
        return Expression(value, string)
    
    def __itruediv__(self, other):
        self.value /= other.value
        self.string += '/' + other.string
        return self

def powerset(s):
    l = len(s)
    for i in range(1 << l):
        yield [s[j] for j in range(l) if (i & (1 << j))]


def outerAdd(result, numbers):
    assert len(numbers) != 0
    posPartitions = [x for x in powerset(numbers) if 0 < len(x)]
    for posPartition in posPartitions:
        negPartition = list(set(numbers) - set(posPartition))
        sum = copy(posPartition[0])
        for x in posPartition[1::]:
            sum += x
        for x in negPartition:
            sum -= x
        if sum.value == result:
            print(sum, '=', sum.value)
        """if sum.value.is_integer() and abs(sum.value) < 100:
            print(sum, '=', sum.value)"""

def outerMult(result, sum, numbers, products = []):
    subsets = [x for x in powerset(numbers) if len(x) != (1 if sum is None else 0)]
    for subset in subsets:
        remaining = list(set(numbers) - set(subset))
        if sum is not None:
            subset.append(sum)
        posPartitions = [[]]
        if len(subset) != 0:
            posPartitions = [x for x in powerset(subset) if 0 < len(x)]
        for posPartition in posPartitions:
            product = None
            try:
                if len(posPartition) > 0:
                    negPartition = list(set(subset) - set(posPartition))
                    product = copy(posPartition[0])
                    for x in posPartition[1::]:
                        product *= x
                    for x in negPartition:
                        product /= x
            except ZeroDivisionError:
                continue
            newProducts = copy(products)
            if product is not None:
                newProducts.append(product)
                if len(remaining) > 1:
                    outerMult(result, None, remaining, newProducts)
            outerAdd(result, newProducts + remaining)

def innerAdd(result, numbers, products):
    length = len(numbers)
    proLength = len(products)
    subsets = [x for x in powerset(numbers) if len(x) + len(products) != 1 and length - len(x) >= 1]
    for subset in subsets:
        remaining = list(set(numbers) - set(subset))
        subset += products
        posPartitions = [[]]
        if len(subset) != 0:
            posPartitions = [x for x in powerset(subset) if 0 < len(x)]
        for posPartition in posPartitions:
            sum = None
            if len(posPartition) > 0:
                negPartition = list(set(subset) - set(posPartition))
                sum = copy(posPartition[0])
                for x in posPartition[1::]:
                    sum += x
                for x in negPartition:
                    sum -= x
                sum.string = '(' + sum.string + ')'
            outerMult(result, sum, remaining)

def innerMult(result, numbers, products = []):
    length = len(numbers)
    subsets = [x for x in powerset(numbers) if len(x) != 1 and length - len(x) >= 2]
    for subset in subsets:
        remaining = list(set(numbers) - set(subset))
        posPartitions = [[]]
        if len(subset) != 0:
            posPartitions = [x for x in powerset(subset) if 0 < len(x)]
        for posPartition in posPartitions:
            product = None
            try:
                if len(posPartition) > 0:
                    negPartition = list(set(subset) - set(posPartition))
                    product = copy(posPartition[0])
                    for x in posPartition[1::]:
                        product *= x
                    for x in negPartition:
                        product /= x
            except ZeroDivisionError:
                continue
            newProducts = copy(products)
            if product is not None:
                newProducts.append(product)
                if len(remaining) > 2:
                    innerMult(result, remaining, newProducts)
            innerAdd(result, remaining, newProducts)
    

def main():
    result = Fraction(argv[1]) / Fraction(argv[2])
    numbers = argv[3::]
    numbers = [Expression(int(x)) for x in numbers]
    innerMult(result, numbers)

if __name__ == '__main__':
    main()
