import enchant
import argparse
import sys
import os
import multiprocessing as mp
import random


def arguments():
    # Currently known letters
    def_voc = ','.join(['a', 'i', 'o', 'e', 'ei'])
    def_consomns = ','.join(['m', 'p', 'r', 'l', 's', 'n', 'g', 't', 'd'])

    # Parse inputs
    parser = argparse.ArgumentParser(
            description='List of German words with given letters')

    parser.add_argument('-s',
                        '--size',
                        help='Size of words [default: 3]',
                        default='3',
                        required=False)
    parser.add_argument('-o',
                        '--output',
                        help='Output file [default: \'\'/stdout]',
                        default='',
                        required=False)
    parser.add_argument('-t',
                        '--top-next',
                        help='Top letter for the next [default: 5]',
                        default='5',
                        required=False)
    parser.add_argument('-n',
                        '--get-next',
                        help='Calculate the number of words available for '
                             'each possible next letter [default: false]',
                        action='store_true')
    parser.add_argument('--vocals',
                        help='List of comma-separated vocals '
                             '[default: %s]' % (def_voc),
                        default=def_voc,
                        required=False)
    parser.add_argument('--consomns',
                        help='List of comma-separated consomns '
                             '[default: %s]' % (def_consomns),
                        default=def_consomns, required=False)
    parser.add_argument('--no-check-dict',
                        help='Check if the resulting words are in the German'
                             'dictionary [default: true]',
                        action='store_false')
    parser.add_argument('--random',
                        help='Display the output in random order [default: '
                             'false]',
                        action='store_true')

    options = parser.parse_args()

    # Parameters container
    params = {}

    if options.size.isdigit():
        params['size'] = int(options.size)
    else:
        sys.stderr.write('Error: size format wrong: '+options.size)
        sys.exit(1)

    if options.top_next.isdigit():
        params['top'] = int(options.top_next)
    else:
        sys.stderr.write('Error: top format wrong: '+options.top_next)
        sys.exit(1)

    if '' == options.output:
        params['out'] = ''
    else:
        if os.path.isdir(os.path.dirname(options.output)) \
           or '' == os.path.dirname(options.output):
            params['out'] = options.output
        else:
            sys.stderr.write('Error for output file: '+options.output)
            sys.exit(1)

    params['vocals'] = options.vocals.split(',')
    params['consomns'] = options.consomns.split(',')

    params['chk_dict'] = options.no_check_dict

    params['out_rnd'] = options.random

    params['next'] = options.get_next

    return params


################################

def init(vocals, consomns):
    return vocals+consomns


################################

def extend(vocals, consomns):
    ext = []

    for v in vocals:
        for c in consomns:
            ext += [c+v]

    return ext


################################

def print_array(array, out='', rnd=False):

    if rnd:
        random.shuffle(array)

    if '' == out:
        for e in array:
            print(e, end='\t')
    else:
        with open(out, 'wt') as f:
            for e in array:
                f.write(e+'\n')
            f.close()
    print('')


################################

def add_layer(blocks, size):
    if 1 >= size:
        return blocks

    out = set()
    for b in blocks:
        for e in add_layer(blocks, size-1):
            out.add(b+e)
    return out


def generate_words(blocks, size):
    out = set()
    bset = set(blocks)

    for s in range(size):
        if s == 0:
            out = set(bset)
        else:
            tm = set(out)
            for b in bset:
                for n in tm:
                    out.add(n+b)

    return out


################################

def prune(words, chk=False):

    if chk:
        d = enchant.Dict('de_DE')
        return (sorted(set(filter(lambda w: d.check(w) or d.check(w.title()),
                words))))

    return (sorted(words))


################################

def get_words(parameters, p=False):

    print('.', end=' ', flush=True)
    blocks = init(parameters['vocals'], parameters['consomns'])
    blocks += extend(parameters['vocals'], parameters['consomns'])

    w = generate_words(blocks, parameters['size'])

    dw = prune(w, chk=parameters['chk_dict'])
    if p:
        print(str(len(dw))+' German words:')
        print_array(dw, out=parameters['out'], rnd=parameters['out_rnd'])
    else:
        return len(dw)


################################

def pool_wrap_get_words(parameters, letter, p=False):
    params = parameters.copy()
    params['consomns'] += [letter]
    return get_words(params)


################################

def next_letter(parameters):

    allelements = set(list('abcdefghijklmnopqrstuvwxyzäöü')+['ei', 'ai', 'eu',
                      'au', 'ch', 'sch', 'sp', 'st'])
    currentelements = set(parameters['vocals']+parameters['consomns'])
    remaining = allelements-currentelements

    pool = mp.Pool(mp.cpu_count())

    possible = {}
    results = [(e, pool.apply(
            pool_wrap_get_words,
            args=(parameters, e)
        )) for e in remaining]

    for r in results:
        (l, c) = r
        possible[l] = c

    print('\nNext letter to add: ')
    n = 0
    for r in [k+': '+str(v) for k, v in sorted(possible.items(),
                                               key=lambda item: item[1],
                                               reverse=True)]:
        print(r)
        n += 1
        if n >= parameters['top']:
            break


################################

def main():
    parameters = arguments()

    get_words(parameters, p=True)

    if parameters['next']:
        next_letter(parameters)


if __name__ == '__main__':
    main()
