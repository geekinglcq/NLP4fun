# -*- coding: utf-8 -*- 
# Utilities for processing text file.


from collections import Counter

def seek_non_ascii_char(s):
    """
    s is a byte of string possibly containing non-ascii characters.
    The function will return a Counter of non-ascii characters
    """
    chr_counter = Counter()
    for c in s:
        if ord(c) > 127:
            chr_counter.update([c])
    return chr_counter


    
