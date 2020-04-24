import scipy.special
import enchant


# remaining: u ä ö ü ei ai eu au
# remaining: b c d f g h j k q t v w x y z

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

def print_array(array):
    for e in array:
        print(e, end='\t')
    print('')

################################

def add_layer(blocks,size):
    #print('s='+str(size))
    if 1>=size:
        return blocks
    else:
        out = set()
        for b in blocks:
            for e in add_layer(blocks,size-1):
                #print('b: '+b+', e: '+e)
                out.add(b+e)
        return out

def generate_words(blocks, size):
    out = set()
    bset = set(blocks)

    #print('Starting generating words...')
    #print(out)

    for s in range(size):
        #print('gw'+str(s))
        out = out.union(add_layer(bset,s+1))
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

def get_words(vocals,consomns,p=True):
    blocks = init(vocals,consomns)
    blocks += extend(vocals,consomns)

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
    if p:
        print(str(len(dw))+' German words:')
        print_array(dw)
    else:
        return len(dw)

################################

def next_letter():
    global vocals, consomns

    allelements = set(list('abcdefghijklmnopqrstuvwxyzäöü')+['ei','ai','eu','au','ch','sch','sp','st'])
    currentelements = set(vocals+consomns)
    remaining = allelements-currentelements

    #print(remaining)
    possible = {}
    cnt=1
    for e in remaining:
        #print('With letter '+e+': '+str(get_words(vocals,consomns+[e],p=False)))
        print(str(cnt)+'. '+e+'...')
        possible[e] = get_words(vocals,consomns+[e],p=False)
        cnt+=1

    print('\nNext letter to add: ')
    #print ({k: v for k, v in sorted(possible.items(), key=lambda item: item[1])})
    #for l in sorted_dict:
        #print(l+': '+str(possible[l]))
    for r in [k+': '+str(v) for k,v in sorted(possible.items(), key=lambda item: item[1], reverse=True)]:
        print(r)


################################

if __name__ == '__main__':
    global vocals,consomns

    vocals = ['a','i','o','e']
    consomns = ['m','p','r','l','s','n']

    get_words(vocals,consomns)

    next_letter()

