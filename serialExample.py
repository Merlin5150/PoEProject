import serial

# create an instance of the Serial class, called arduino
# set the port to COM4, the baudrate to 9600, and, optionally,
# the timeout to 1 second
#
# The timeout makes sure that if you try to read data when there
# is no data, it stops trying to read after 1 second of waiting.
# otherwise your program could end up in a forever-loop
arduino = serial.Serial(port = '/dev/ttyACM0', baudrate = 9600, timeout = 1)

# if you want to read one line use this:
string = arduino.readline()
print string


# if you want to read some number of characters, n, then use this:
n = 10
string = arduino.read(n)
print string


# if you want to read a specific number of characters though, you
# should check the Serial.in_waiting variable/field.  it lets you know
# how many characters are ready to be read from the serial port
num_bytes = arduino.in_waiting

# then you can ensure that you don't try to read more characters than
# are available
if num_bytes >= 10:
    string = arduino.read(10)

# or you can just read the whole damn buffer into a string
# remember, in_waiting is a variable/field not a method or function
string = arduino.read(arduino.in_waiting)
print string

# if you know your data is formatted like this for example:
# 1 2 3 4 5 6 7 8
# 9 10 11 12 13 14 15 16
# (ie 8 numbers per line, delimited by spaces)
# Then you can write a little function that will handle converting
# the string to a list

def parseString(string):
    """Parses strings read from the serial port."""

    # make a list of substrings, delimited by the newline character
    # each item in the list should be a string with 8 space-delimited numbers
    # like this:
    # ['1 2 3 4 5 6 7 8', '9 10 11 12 13 14 15 16', '']
    # because the original string looks something like this:
    # '1 2 3 4 5 6 7 8\n9 10 11 12 13 14 15 16\n'
    stringlist = string.split('\n')

    # make sure you catch a hanging null string on the end!  if the string
    # ended with a '\n' then python will split the string at the last
    # character

    # python considers empty strings to be 'false' so this if-statement works well
    if not stringlist[-1]:
        stringlist.pop(-1)

    # split each sublist by the space character
    # looks like this: [ ['1','2','3', ...],['9', '10', ...]]
    returnList = [line.split() for line in stringlist]   

    # make the damn strings into numbers already!
    for index, sublist in enumerate(returnList):
        # DO IT
        returnList[n] = [int(number) for number in sublist]

    return returnList


data = parseString(string)
# there's other stuff but this gets the job done.
# the functions for reading you see above have 'write' counterparts
# examples:
arduino.write('Hello ')
# there is no writeline() function.  just use write with a '\n' at the end
arduino.write('World!\n')

# You can see how many characters are in the output buffer with out_waiting
# just like you can with in_waiting
bytes_written = arduino.out_waiting
print 'Number of bytes the arduino has yet to read:', bytes_written
print 'If it''s zero then it read ''Hello World\\n'' just like we want!'
print 'If it''s non-zero then the arduino is not reading from serial.'

################# IMPORTANT ###################
# Make sure you close the serial port when you're done!
# this can cause a lot of headaches if you forget it.
#
# Sometimes you open the serial port in your script but the script fails
# halfway through.  YOUR PORT IS STILL OPEN CLOSE IT IN THE TERMINAL IF THIS HAPPENS!!!!!!

arduino.close()