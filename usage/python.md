# Python

Python is a wonderful and powerful programming language that's easy to use (easy to read **and** write) and with Raspberry Pi lets you connect your project to the real world.

Python syntax is very clean, with an emphasis on readability and uses standard English keywords.

Hello world in Python:

```python
print("Hello world")
```

Simple as that!

Some languages use curly braces `{` and `}` to wrap around lines of code which belong together, and leave it to the writer to indent these lines to appear visually nested. However, Python does not use curly braces but instead requires indentation for nesting. For example a `for` loop in Python:

```python
for i in range(10):
    print("Hello")
```

The indentation is necessary here. A second line indented would be a part of the loop, and a second line not indented would be outside of the loop. For example:

```python
for i in range(2):
    print("A")
    print("B")
```

would print:

```
A
B
A
B
```

whereas:

```python
for i in range(2):
    print("A")
print("B")
```

would print:

```
A
A
B
```

To save a value to a variable, assign it like so:

```python
name = "Bob"
age = 15
```

Note here I did not assign types to these variables, as types are inferred, and can be changed (it's dynamic).

```python
age = 15
age += 1  # increment age by 1
print(age)
```

This time I used comments beside the increment command. Comments are ignored in the program but there for you to leave notes, and are denoted by the hash `#` symbol. Multi-line comments use triple quotes like so:

```python
"""
This is a very simple Python program that prints "Hello".
That's all it does.
"""

print("Hello")
```

Python also has lists (called arrays in some languages) which are collections of data of any type:

```python
numbers = [1, 2, 3]
```

Lists are denoted by the use of square brackets `[]` and each item is separated by a comma.

### Iteration

Some data types are iterable, which means you can loop over the values they contain. For example a list:

```python
numbers = [1, 2, 3]

for number in numbers:
    print(number)
```

This takes each item in the list `numbers` and prints out the item:

```
1
2
3
```

Note I used the word `number` to denote each item. This is merely the word I chose for this - it's recommended you choose descriptive words for variables - using plurals for lists, and singular for each item makes sense. It makes it easier to understand when reading.

Other data types are iterable, for example the string:

```python
dog_name = "BINGO"

for char in dog_name:
    print(char)
```

This loops over each character and prints them out:

```
B
I
N
G
O
```

The integer data type is not iterable and tryng to iterate over it will produce an error:

```python
TypeError: 'int' object is not iterable
```

However you can make an iterable object using the `range` function:

```python
n = 3

for i in range(n):
    print(i)
```

`range(5)` contains the numbers `0`, `1`, `2`, `3` and `4` (five numbers in total). To get the numbers `1` to `5` use `range(1, 6)`.

You can use functions like `len` to find the length of a string or a list:

```python
name = "Jamie"
print(len(name))  # 5

names = ["Bob", "Jane", "James", "Alice"]
print(len(names))  # 4
```

You can use `if` statements for control flow:

```python
name = "Joe"

if len(name) > 3:
    print("Nice name,")
    print(name")
else:
    print("That's a short name,")
    print(name)
```

## Python 2 vs. Python 3

The short version: Python 2 is legacy, Python 3 is the present and future of the language.

Python 2 was released in 2000, and Python 3 was released in 2008. Python 3 is recommended, but some libraries have not yet been ported to Python 3 which is why Python 2 is still present and widely used.

If you are familiar with Python 2 but not Python 3, here is a summary of the basic key differences:

- Print
    - In Python 2, `print` is a statement and did not require brackets, e.g. `print "Hello"`.
    - In Python 3, `print` is a function, so you pass in what you want to print as parameters, e.g. `print("Hello")` or `print("My age is", age)`.
    - Using brackets for `print` in Python 2 works fine, so it's common to see this used for compatability. However printing multiple objects in the same `print` command works differently.
    - In Python 3 this prints each one, space separated, and in Python 2 the collection of items is printed as a tuple, e.g. `("My age is", 15)`
-  Input / Raw input
    -  In Python 2, the function `raw_input` takes input from the user.
    -  In Python 3, the function is called `input`.
- Integer division
    - In Python 2 `/` is used for exact integer division, always returning an integer. This means it returns the value of the number of times one number divides in to another whole, and ignores the remainder, e.g. `1 / 2` returns `0`, `2 / 2` returns `1` and `3 / 2` returns `1`.
    - In Python 3, `/` does precise division, returning a floating point number (decimal) if necessary, e.g. `1 / 2` returns `0.5`.
    - To get precise division in Python 2, convert one or both numbers to a float first, e.g. `1.0 / 2` which returns `0.5`.
    - To get extact integer division in Python 3, use `//`, e.g. `1 // 2` returns `0`.

Python 2.7.6 was released in 2013. The 2.x branch will have no further major releases.

Read more on the differences on the [Python wiki](https://wiki.python.org/moin/Python2orPython3)

## Convention

While indentation is essential in Python, there are other aspects which are syntactically correct but considered bad practise. These are given in a style guide called [PEP 8](http://legacy.python.org/dev/peps/pep-0008/) and include conventions such as always using spaces around operators i.e. `a = 1 + 2` over `a=1+2` and a maximum line length of 79 characters. It also suggests using four spaces per tab (this is configurable in your editor).

The philosophy of Python is summarised in [PEP 20](http://legacy.python.org/dev/peps/pep-0020/) (The Zen of Python) which encourages good Pythonic writing style. For example:

- Beautiful is better than ugly
- Explicit is better than implicit
- Simple is better than complex
- Complex is better than complicated
- Readability counts

## IDLE

The easiest introduction to Python is through IDLE. Double click the IDLE icon on the Desktop (or IDLE3 for Python3) and you're given a REPL (Read-Evaluate-Print-Loop) which is a prompt you can enter Python commands in to. As it's a REPL you even get the output of commands printed to the screen without using `print`. You can use variables if you need to but you can even use it like a calculator. For example:

```python
>>> 1 + 2
3
>>> name = "Sarah"
"Hello " + name
```

IDLE also has syntax highlighting built in and some support for autocompletion. You can look back on the history of the commands you've entered in the REPL with `Alt + P` (previous) and `Alt + N` (next).

### Python files in IDLE

To create a Python file in IDLE, click `File > New File` and you'll be given a blank window. This is an empty file, not a Python prompt. You write a Python file in this window, save it, then run it and you'll see the output in the other window.

For example, in the new window, type:

```python
n = 0

for i in range(1, 101):
    n += i
    
print("The sum of the numbers 1 to 100 is:")
print(n)
```

Then save this file (`File > Save` or `Ctrl + S`) and run (`Run > Run Module` or hit `F5`) and you'll see the output in your original Python window.

## Command Line

The standard built-in Python REPL is accessed by typing `python` in the Terminal. Type `python3` for Python3.

This REPL is a prompt ready for Python commands to be entered. You can use this the same as IDLE, but it does not have syntax highlighting or autocompletion. You can look back on the history of the commands you've entered in the REPL by using the Up/Down keys. Use `Ctrl + D` to exit.

### IPython

An alternative command line Python prompt is IPython. IPython is an interactive Python shell with syntax highlighting, autocompletion, pretty printing, built-in documentation and more. IPython is not installed by default. Install with:

```
sudo apt-get install ipython
```

or for Python 3:

```
sudo apt-get install ipython3
```

Then run with `ipython` or `ipython3` from the command line. It works like the standard `python`, but with more features. Try typing `len?` and hitting `Enter`. You're shown information including the docstring for the `len` function:

```python
Type:       builtin_function_or_method
String Form:<built-in function len>
Namespace:  Python builtin
Docstring:
len(object) -> integer

Return the number of items of a sequence or mapping.
```

Try the following dictionary comprehension:

```python
{i: i ** 3 for i in range(12)}
```

which will pretty print the following:

```python
{1: 1,
 2: 8,
 3: 27,
 4: 64,
 5: 125,
 6: 216,
 7: 343,
 8: 512,
 9: 729,
 10: 1000,
 11: 1331}
```

In `python` this would have printed on one line:

```python
{1: 1, 2: 8, 3: 27, 4: 64, 5: 125, 6: 216, 7: 343, 8: 512, 9: 729, 10: 1000, 11: 1331}
```

You can look back on the history of the commands you've entered in the REPL by using the Up/Down keys like in `python` but it also persists over sessions, so you can exit `ipython` and return (or switch between v2/3) and the history remains. Use `Ctrl + D` to exit.

### Executing Python files

You can write a Python file in a standard editor like Vim, Nano or LeafPad, and run it as a Python script from the command line. Just navigate to the directory the file is saved (use `cd` and `ls` for guidance) and run with `python`, e.g. `python hello.py`.

## Installing Python libraries

### APT

Some Python packages can be found in the Raspbian archives, and can be installed using APT, for example:

```
sudo apt-get update
sudo apt-get install python-picamera
```

This is a preferable method of installing things as it means that the modules you install can be kept up to date easily with the usual `sudo apt-get update` and `sudo apt-get upgrade` commands.

Not all Python packages are available in the Raspbian archives, and those that are can sometimes be out of date. If you can't find a suitable version in the Raspbian archives you can install packages from the [Python Package Index](http://pypi.python.org/) (also known as PyPI). To do so, use the `pip` tool (which is installed with the `python-pip` package in Raspbian:

```
sudo apt-get install python-pip
sudo pip install simplejson
```

Read more on (installing software in Python](https://github.com/raspberrypi/documentation/blob/master/linux/software/python.md)

## GPIO

Using Python on the Raspberry Pi opens up the opportunity to connect to the real world through the Pi's GPIO pins. You'll need to install the RPi GPIO library:

```
sudo apt-get install python-rpi.gpio
```

or 

```
sudo apt-get install python3-rpi.gpio
```

To control the GPIO pins you'll need root access, so run `sudo python`, `sudo ipython` or `sudo idle &`.

In your Python script (or in the REPL), import the GPIO module, set the board mode to that of your preference, set up the pins you want to use and turn them on:

```
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  # set board mode to Broadcom

GPIO.setup(17, GPIO.OUT)  # set up pin 17
GPIO.setup(18, GPIO.OUT)  # set up pin 18

GPIO.output(17, 1)  # turn on pin 17
GPIO.output(18, 1)  # turn on pin 18
```

## Python Documentation

Full documentation for Python is available at [python.org/doc](https://www.python.org/doc/)
