# This is what a comment looks like
fruits = ['apples', 'oranges', 'pears', 'bananas', 'item8']  # Added item8
for fruit in fruits:
    print(fruit + ' for sale')

fruitPrices = {'apples': 2.00, 'oranges': 1.50, 'pears': 1.75, 'item8': 2.50}  # Added item8
for fruit, price in fruitPrices.items():
    if price < 2.00:
        print('%s cost %f a pound' % (fruit, price))
    else:
        print(fruit + ' are too expensive!')