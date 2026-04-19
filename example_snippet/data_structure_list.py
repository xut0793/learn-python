numbers = [1, 2, 3]
numbers.append(4)
print(numbers)  # Output: [1, 2, 3, 4]

numbers.extend([5, 6])
print(numbers)  # Output: [1, 2, 3, 4, 5, 6]

numbers.insert(0, 0)
print(numbers)  # Output: [0, 1, 2, 3, 4, 5, 6]

numbers.remove(3)
print(numbers)  # Output: [0, 1, 2, 4, 5, 6]

numbers.pop()
print(numbers)  # Output: [0, 1, 2, 4, 5]

numbers.reverse()
print(numbers)  # Output: [5, 4, 2, 1, 0]

numbers.sort()
print(numbers)  # Output: [0, 1, 2, 4, 5]

numbers.clear()
print(numbers)  # Output: []

fruits = ['apple', 'banana', 'cherry']
print(fruits[0])  # Output: 'apple'
print(fruits.index('banana'))  # Output: 1
print('cherry' in fruits)  # Output: True


nums = [4, 2, 5, 4, 1]
sorted_numbers = sorted(nums)
print(sorted_numbers)  # Output: [1, 2, 4, 4, 5]

sort_reversed_numbers = sorted(nums, reverse=True)
print(sort_reversed_numbers)  # Output: [5, 4, 4, 2, 1]

reversed_numbers = list(reversed(nums))
print(reversed_numbers)  # Output: [1, 4, 5, 4, 2]

for i in reversed(nums):
    print(i)  # Output: 1, 4, 5, 2, 4 (in reverse order)


for i in range(1, 6):
    print(i)  # Output: 1, 2, 3, 4, 5

zip_numbers = zip([1, 2, 3], ['a', 'b', 'c'])
print(list(zip_numbers))  # Output: [(1, 'a'), (2, 'b'), (3, 'c')]
for i in zip_numbers:
    print(i)  # Output: (1, 'a'), (2, 'b'), (3, 'c')

squares = map(lambda x: x**2, [1, 2, 3])
print(list(squares))  # Output: [1, 4, 9]

filtered_numbers = filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5])
print(list(filtered_numbers))  # Output: [2, 4]

# 统计相关函数
numbers = [1, 2, 3, 4, 5]
print(len(numbers))  # Output: 5
print(sum(numbers))  # Output: 15
print(min(numbers))  # Output: 1
print(max(numbers))  # Output: 5

parts = numbers[1:3]
print(parts)  # Output: [2, 3]

chars = ["a", "b", "a", "d"]
print(chars.count("a"))  # Output: 2