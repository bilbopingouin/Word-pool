import scipy.special
import enchant
import argparse
import sys
import os
import multiprocessing as mp

def arguments():
    global vocals, consomns

    def_voc = ','.join(['a','i','o','e','ei'])
    def_consomns = ','.join(['m','p','r','l','s','n','g'])

    parser = argparse.ArgumentParser(description='List of German words with given letters')

    parser.add_argument('-s','--size',help='Size of words [default: 3]',default='3',required=False)
    parser.add_argument('-o','--output',help='Output file [default: \'\'/stdout]',default='',required=False)
    parser.add_argument('-t','--top-next',help='Top letter for the next [default: 5]',default='5',required=False)
    parser.add_argument('-n','--get-next',help='Calculate the number of words available for each possible next letter [default: false]',action='store_true')
    parser.add_argument('-v','--vocals',help='List of comma-separated vocals [default: %s]' % (def_voc),default=def_voc,required=False)
    parser.add_argument('-c','--consomns',help='List of comma-separated consomns [default: %s]' % (def_consomns),default=def_consomns,required=False)

    try:
        options = parser.parse_args()
    except:
        sys.exit(0)

    if options.size.isdigit():
        size = int(options.size)
    else:
        print('Error: size format wrong: '+options.size)
        sys.exit(1)

    if options.top_next.isdigit():
        top = int(options.top_next)
    else:
        print('Error: top format wrong: '+options.top_next)

    if '' == options.output:
        out=''
    else:
        if os.path.isdir(os.path.dirname(options.output)) or '' == os.path.dirname(options.output):
            out=options.output
        else:
            print('Error for output file: '+options.output)
            sys.exit(1)

    vocals   = options.vocals.split(',')
    consomns = options.consomns.split(',')
        
    return (size,top,out,options.get_next)


################################

def init(vocals,consomns):
    return vocals+consomns

################################

def extend(vocals, consomns):
    ext=[]

    for v in vocals:
        for c in consomns:
            ext += [c+v]

    return ext

################################

def print_array(array,out=''):
    if '' == out:
        for e in array:
            print(e, end='\t')
    else:
        with open(out,'wt') as f:
            for e in array:
                f.write(e+'\n')
            f.close()
    print('')

################################

def add_layer(blocks,size):
    if 1>=size:
        return blocks
    else:
        out = set()
        for b in blocks:
            for e in add_layer(blocks,size-1):
                out.add(b+e)
        return out

def generate_words(blocks, size):
    out = set()
    bset = set(blocks)

    for s in range(size):
        if s==0:
            out = set(bset)
        else:
            tm=set(out)
            for b in bset:
                for n in tm:
                    out.add(n+b)

    return out

################################

def prune(words):
    d = enchant.Dict('de_DE')

    return (sorted(set(filter(lambda w: d.check(w) or d.check(w.title()), words))))

################################

def get_words(vocals,consomns,size,out='',p=False):
    print('.', end=' ',flush=True)
    blocks = init(vocals,consomns)
    blocks += extend(vocals,consomns)

    w = generate_words(blocks,size)

    dw = prune(w)
    if p:
        print(str(len(dw))+' German words:')
        print_array(dw,out=out)
    else:
        return len(dw)

################################

def next_letter(top,size):
    global vocals, consomns

    allelements = set(list('abcdefghijklmnopqrstuvwxyzäöü')+['ei','ai','eu','au','ch','sch','sp','st'])
    currentelements = set(vocals+consomns)
    remaining = allelements-currentelements

    pool = mp.Pool(mp.cpu_count())
    #print(mp.cpu_count())

    possible = {}
    #for e in remaining:
    #    print('.',end=' ',flush=True)
    #    possible[e] = get_words(vocals,consomns+[e],size,p=False)
    #p=False
    results = [(e,pool.apply(get_words, args=(vocals,consomns+[e],size))) for e in remaining]
    #print(results)

    for r in results:
        (l,c) = r
        possible[l] = c

    print('\nNext letter to add: ')
    n=0
    for r in [k+': '+str(v) for k,v in sorted(possible.items(), key=lambda item: item[1], reverse=True)]:
        print(r)
        n+=1
        if n>=top:
            break;


################################

if __name__ == '__main__':
    global vocals,consomns

    (size,top,out,gnext) = arguments()

    #vocals = ['a','i','o','e','ei']
    #consomns = ['m','p','r','l','s','n','g']

    get_words(vocals,consomns,size,out=out,p=True)

    if gnext:
        next_letter(top,size)

