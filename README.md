# Informacinių technologijų namų darbas - Skaičiavimo sistemos

## Užduotis
Parašyti programą, kuri įvestą šešioliktainio skaičiaus trumpeninę dalį konvertuotų į dvejetainį
skaičių. 

## Naudojimas
Programą galima paleisti iš programinės eilutės (CLI) pateikiant šešioliktainį skaičių su `-i` arba `--input` argumentu.

Pagalbos pranešimas:
```sh
$ python converter.py --help
usage: converter.py [-h] -i INPUT

Programa, kuri konvertuoja šešioliktainio skaičiaus trupmeninę dalį į dvejatainį skaičių.

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Šešioliktainis skaičių, kurį konvertuoti į dvejatainę sistemą.
```

Naudojimas:
```sh
$ python converter.py -i SKAIČIUS
```

Pavyzdys:
```sh
$ python converter.py -i 1F,F01
Šešioliktainis skaičius 1F,F01 konvertuotas į dvejatainę sistemą yra: 11111,111100000001
```