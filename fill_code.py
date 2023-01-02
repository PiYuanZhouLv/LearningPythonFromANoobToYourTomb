# Hello world
print('Hello world~')

# IPO simple
name = input('Your name please:')
print(f"Hello {name}!")

# if-else statement
num = int(input('A number:'))
if num >= 5:
    print('It is bigger than or equal to 5.')
else:
    print('It is smaller than 5.')

# := mark (higher than 3.8)
if content := input('Input something or not'):
    print('You inputted:', content)
else:
    print("You didn't input anything")

# match-case statement (higher than 3.10)
l = eval(input('Input a list:'))
match l:
    case [1, 2, 3]:
        print('It is [1, 2, 3].')
    case [_, _]:
        print('It just has 2 item.')
    case [1, *_, 1]:
        print('The first and the last one are 1.')
    case [1, i, *_] if i != 1:
        print('The first is 1 but the second is not 1.')
    case _:
        print("I just can't understand what you have inputted.")

# for-in statement
for name in ['Tom', 'Alice', 'Bob', 'John']:
    print('Hello', name)

# while statement
time = 7
while time <= 21:
    print(f"It is {time} o'clock now.")
    time += 1

# The Zen of Python
import this

# Another hello-world
import __hello__

# try-except statement
import traceback
try:
    1/0
except ZeroDivisionError as err:
    traceback.print_last()
else:
    print('It is infinite.')

# Interesting float
print(float('inf'), hash(float('inf')))
print(f'0 * -1 = {0 * -1}')
print(f'but 0.0 * -1 = {0.0 * -1}')
print(float('nan'))

# compute pi
import math
def pi(n=1, s=0):
    s += (-1)**(n+1) * (1/(2*n-1))
    if s == math.pi:
        print('pi is', s)
        return
    pi(n+1, s)
pi()

# prime list
def is_prime(num):
    if num == 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True
i = 1
while i <= 1000:
    print(i if is_prime(i) else 'x', end='\t' if i % 10 != 0 else '\n')
    i += 1

# tkinter
import tkinter
root = tkinter.Tk()

tkinter.Label(root, textvariable=(tv:=tkinter.StringVar(value='Your name here:'))).pack()
tkinter.Entry(root, textvariable=(nv:=tkinter.StringVar(value='Python'))).pack()
tkinter.Button(root, text='OK',
               command=lambda *args: tv.set(f'Hello {tmp}' if (tmp:=nv.get())!='' else 'Nothing Inputted')).pack()
tkinter.mainloop()
