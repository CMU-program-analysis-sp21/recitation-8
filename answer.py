chars = {'c2': 108,
         'c3': 118,
         'c4': 101,
         'c5': 100,
         'c6': 105,
         'c0': 115,
         'c1': 111,
         'c7': 116}

print([chr(v) for _, v in sorted(chars.items())])
