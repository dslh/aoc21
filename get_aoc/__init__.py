import requests
from os.path import isfile, dirname, join

INPUT_URL = 'https://adventofcode.com/2021/day/%d/input'

def session_token():
    return open(join(dirname(__file__), '../.session'), 'r').read().strip()

# Use this to get the entire input as a single string.
# Caches the data on disk after first download.
def get_input(day):
    filename = join(dirname(__file__), '../input/%d.txt' % day)
    if isfile(filename):
        return open(filename, 'r').read().rstrip()

    headers = { 'cookie': 'session=%s' % session_token() }
    contents = requests.get(INPUT_URL % day, headers=headers).text.rstrip()
    open(filename, 'w').write(contents)
    return contents

# Use this to get the input as a list of strings, one per line
def get_input_lines(day):
    return get_input(day).rsplit('\n')

# Use this to read each line of input as an integer number
def get_input_integers(day):
    return [int(line) for line in get_input_lines(day)]
