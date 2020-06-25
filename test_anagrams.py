import anagrams

import os
import re
import sys


def test_init():
    assert 'ab' == anagrams.init('a', 'b')
    assert ['a', 'b'] == anagrams.init(['a'], ['b'])


def test_extend():
    assert [] == anagrams.extend([], [])
    assert set(['ba', 'ca']) == set(anagrams.extend(['a'], ['b', 'c']))


def test_print_array(capsys):
    # Default printing
    anagrams.print_array(['a'])
    out, err = capsys.readouterr()
    assert out == 'a\t\n'

    # Random printing
    anagrams.print_array(['a', 'b', 'c', 'd'])
    out, err = capsys.readouterr()
    assert set(['a', 'b', 'c', 'd', '\n']) == set(out.split('\t'))
    # For the random printing, we can only check if everything is still here
    anagrams.print_array(['a', 'b', 'c', 'd'], rnd=True)
    out, err = capsys.readouterr()
    assert set(['a', 'b', 'c', 'd', '\n']) == set(out.split('\t'))

    # Writing to a file
    anagrams.print_array(['a'], out='tmp_test_print_array.dat')
    with open('tmp_test_print_array.dat', 'rt') as f:
        content = f.readlines()
        assert ['a\n'] == content
        f.close()
        os.remove('tmp_test_print_array.dat')


def test_add_layer():
    blocks = ['a', 'b', 'c']
    assert blocks == anagrams.add_layer(blocks, 0)
    assert blocks == anagrams.add_layer(blocks, 1)

    res2 = set()
    for b1 in blocks:
        for b2 in blocks:
            res2.add(b1+b2)
    assert res2 == anagrams.add_layer(blocks, 2)

    res3 = set()
    for b1 in blocks:
        for b2 in res2:
            res3.add(b1+b2)
    assert res3 == anagrams.add_layer(blocks, 3)


def test_generate_words():
    res = set()
    blocks = ['a', 'b', 'c']

    assert res == anagrams.generate_words(blocks, 0)

    assert set(blocks) == anagrams.generate_words(blocks, 1)

    res2 = set(blocks)
    for b1 in blocks:
        for b2 in blocks:
            res2.add(b1+b2)
    assert set(res2) == anagrams.generate_words(blocks, 2)


def test_prune():
    words = ['der', 'die', 'das', 'drt']

    assert sorted(words) == anagrams.prune(words, chk=False)
    assert sorted(['der', 'die', 'das']) == anagrams.prune(words, chk=True)


def test_get_words(capsys):
    parameters = {
            'vocals': ['a'],
            'consomns': ['b'],
            'size': 1,
            'chk_dict': False,
            'out': '',
            'out_rnd': False,
    }

    assert 3 == anagrams.get_words(parameters, p=False)

    anagrams.get_words(parameters, p=True)
    out, err = capsys.readouterr()
    assert '. . 3 German words:\na\tb\tba\t\n' == out

    parameters['consomns'] = []
    assert 3 == anagrams.pool_wrap_get_words(parameters, 'b', p=False)


def test_next_letter(capsys):
    parameters = {
            'vocals': ['a'],
            'consomns': ['b'],
            'size': 1,
            'chk_dict': False,
            'out': '',
            'out_rnd': False,
            'top': 5,
    }

    anagrams.next_letter(parameters)
    out, err = capsys.readouterr()
    assert re.match(
        '\nNext letter to add: (\n\w+: \d){5}',
        out
    ) is not None


def test_arguments_defaults(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['anagrams'])
    arguments = anagrams.arguments()
    assert arguments['size'] == 3
    assert arguments['out'] == ''
    assert arguments['top'] == 5
    assert arguments['next'] is False
    assert arguments['chk_dict'] is True
    assert arguments['out_rnd'] is False
    assert arguments['vocals'] == ['a', 'i', 'o', 'e', 'ei']
    assert arguments['consomns'] == [
            'm', 'p', 'r', 'l', 's', 'n', 'g', 't', 'd'
            ]


def test_arguments(monkeypatch):
    monkeypatch.setattr(sys, 'argv', [
        'anagrams',
        '-s', '1',
        '-o', 'foo.dat',
        '-t', '4',
        '-n',
        '--vocals', 'a,e',
        '--consomns', 'b,c',
        '--no-check-dict',
        '--random'
        ])
    arguments = anagrams.arguments()
    assert arguments['size'] == 1
    assert arguments['out'] == 'foo.dat'
    assert arguments['top'] == 4
    assert arguments['next'] is True
    assert arguments['chk_dict'] is False
    assert arguments['out_rnd'] is True
    assert arguments['vocals'] == ['a', 'e']
    assert arguments['consomns'] == ['b', 'c']
