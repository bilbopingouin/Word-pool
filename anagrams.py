import scipy.special
import enchant

vocals = ['a','i','o','e']
consomns = ['m','p','r','l','s','n']

################################

def init():
    global vocals, consomns

    return vocals+consomns

################################

def extend():
    global vocals, consomns

    ext=[]

    for v in vocals:
        for c in consomns:
            ext += [c+v]

    return ext

################################

def print_array(array):
    for e in array:
        print(e, end='\t')
    print('')

################################

def add_layer(blocks,size):
    #print('s='+str(size))
    if 1>=size:
        return blocks[:]
    else:
        out = []
        for b in blocks:
            for e in add_layer(blocks,size-1):
                #print('b: '+b+', e: '+e)
                out += [b+e]
        return out[:]

def generate_words(blocks, size):
    out = []

    #print('Starting generating words...')
    #print(out)

    for s in range(size):
        #print('gw'+str(s))
        out += sorted(set(add_layer(blocks,s+1)))
        #print(out)

    #print('Done')
    #print(out)
    return out

################################

def prune(words):
    d = enchant.Dict('de_DE')

    return (sorted(set(filter(lambda w: d.check(w), words))))

# print('\nSyllables:')
# for v in vocals:
#     for c in consomns:
#         print(c+v, end='\t')
# print('')
# 
# print('\nCombination vocal+syllable:')
# for v in vocals:
#     for c in consomns:
#         for v2 in vocals:
#             print(v+c+v2, end='\t')
# print('')
# 
# print('\nCombination syllable+vocal:')
# for v in vocals:
#     for c in consomns:
#         for v2 in vocals:
#             print(c+v+v2, end='\t')
# print('')

################################

if __name__ == '__main__':
    blocks = init()
    blocks += extend()

    #w = generate_words(['a','b'],1)
    #print_array(w)

    #w = generate_words(['a','b'],2)
    #print_array(w)

    #w = generate_words(['a','b'],3)
    #print_array(w)

    #print('blocks:')
    #print_array(blocks)

    w = generate_words(blocks,3)

    #print('words:')
    #print_array(w)

    dw = prune(w)
    print(str(len(dw))+' German words:')
    print_array(dw)
