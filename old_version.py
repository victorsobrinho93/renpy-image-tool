from itertools import zip_longest, chain

lista = ["Hey there bud"]
suffixo = ['nome_slow', 'nome_notSoSlow', 'nome_fast', 'nome_not_so_fast']
result = []

for item in suffixo:
    if isinstance(item, int):
        print(item)

for item in zip_longest(lista, suffixo):
    if isinstance(item, str):
        print(item)