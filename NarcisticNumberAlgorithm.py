# Python 3.5
# Narcistic Numbers Finder Algorithm

from datetime import datetime
from decimal import Decimal
import decimal

def find_armstrong_numbers(number_of_digits):
    """
    Find narcistic numbers from given number of digits
    @param number_of_digits 
    """
    pows = [idx ** number_of_digits for idx in range(10)]
    low_value = 10**(number_of_digits - 1) 
    max_value = 10**number_of_digits - 1
    
    digi_count = [0,0,0,0,0,0,0,0,0,0]

    def search(d, todo, total):

        powd = pows[d]
        d1 = d-1
        powd1 = pows[d1]
        L = total + powd1 * todo # largest possible taking no d's
        dL = powd - powd1  # the change to L when i goes up 1

        for idx in range(todo + 1):
            if idx:
                total += powd
                todo -= 1
                L += dL
                digi_count[d] += 1

            if total > max_value:
                break
            if L < low_value:
                continue
            if total < low_value or L > max_value:
                yield from search(d1, todo, total)
                continue

            t1 = total.as_tuple().digits
            t2 = L.as_tuple().digits

            # Every possible continuation has sum between total and
            # L, and has a full-width sum.  So if total and L have
            # some identical leading digits, a solution must include
            # all such leading digits.  Count them.
            c = [0] * 10
            for a, b in zip(t1, t2):
                if a == b:
                    c[a] += 1
                else:
                    break
            else:  # the tuples are identical
                # assert d == 1 or todo == 0
                # assert total == L
                # This is the only sum we can get - no point to
                # recursing.  It's a solution iff each digit has been
                # picked exactly as many times as it appears in the
                # sum.
                # If todo is 0, we've picked all the digits.
                # Else todo > 0, and d must be 1:  all remaining
                # digits must be 0.
                digi_count[0] += todo
                # assert sum(c) == sum(digitcount) == width
                if digi_count == c:
                    yield total
                digi_count[0] -= todo
                continue
            # The tuples aren't identical, but may have leading digits
            # in common.  If, e.g., "9892" is a common prefix, then to
            # get a solution we must pick at least one 8, at least two
            # 9s, and at least one 2.
            if any(digi_count[j] < c[j] for j in range(d, 10)):
                continue

            newtodo, newtotal = todo, total
            added = []
            for j in range(d):
                need = c[j] - digi_count[j]

                if need:
                    newtodo -= need
                    added.append((j, need))
            if newtodo < 0:
                continue
            for j, need in added:
                newtotal += pows[j] * need
                digi_count[j] += need
            yield from search(d1, newtodo, newtotal)
            for j, need in added:
                digi_count[j] -= need
        digi_count[d] -= idx

    yield from search(9, number_of_digits, Decimal(0))

# Start Time
start_time = datetime.now()
# Starting number of digits
number_of_digits = 0
# Sum of find Narcistic numbers
total_numbers = 0

while True:
	number_of_digits += 1
	print("Number of digits:", number_of_digits)

	#Finds and prints numbers that have number_of_digits
	for number in find_armstrong_numbers(number_of_digits):
		print(number)
		total_numbers += 1
	end_time = datetime.now()
	print("Total numbers Found:", total_numbers, " Total time:" , end_time - start_time, "\n")

