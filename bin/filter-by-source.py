#!/usr/bin/env python

'''Select a paper at random.'''

import argparse
import bibtexparser
import re
import sys

import util

STRING_PAT = re.compile(r'@string{(.+?)\s*=\s*"(.+?)"}')
TUE_WANTED = {'esec-fse', 'fse', 'icse', 'icsme', 'msr', 'saner'}


def main():
    options = get_options()
    wanted = set(options.source) if options.source else TUE_WANTED
    entries = util.get_entries(options.strings, options.input)
    sources = get_sources(options.strings, wanted)
    entries = [e for e in entries if keep(e, sources)]
    keys = [e['ID'] for e in entries]
    for k in keys:
        print(k)


def get_sources(strings, sources):
    result = set()
    with open(strings, 'r') as reader:
        for line in reader:
            match = STRING_PAT.search(line)
            if match:
                key = match.group(1)
                name = match.group(2)
                if key in sources:
                    result.add(name)
    return result


def keep(entry, sources):
    for key in ('booktitle', 'journal'):
        if (key in entry) and (entry[key] in sources):
            return True
    return False


def get_options():
    '''Turn arguments into configuration object.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='specify input file')
    parser.add_argument('--random', action='store_true', help='select a single random entry')
    parser.add_argument('--strings', help='string definitions file (optional)')
    parser.add_argument('--source', nargs='+', help='specify the source')
    return parser.parse_args()


if __name__ == '__main__':
    main()
