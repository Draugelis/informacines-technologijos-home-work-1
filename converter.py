#!/usr/bin/python3

# Užduotis:
# Parašykite programą, kuri įvestą šešioliktainio skaičiaus trumpeninę
# dalį konvertuotų į dvejetainį skaičių.

# argparse modulį naudojame vartotojo įvesčiai komandinėje eilutėje apdoroti
import argparse

# re modulį naudojame regex šablonų tikrinimui
import re

# typing modulis naudojamas duomenų tipų užuominoms (type hints).
# Duomenų tipo užuominos nepagerina programos funkcionalumo, tačiau
# gali pagerinti programuotojo darbo procesą, nes teksto redaktorius
# turi galimybę nustatyti, jog yra naudojami netikėti duomenų tipai.
from typing import Callable

# Regex šablonas naudojamas nustatyti, ar vartotojas
# pateikė taisiklingą šešioliktainį skaičių
HEX_REGEX = r"^[0-9a-fA-F]+[,.][0-9a-fA-F]+$|^[0-9a-fA-F]+$"

# Šešioliktainių skaitmenų ir jų dvejatainių atitikmenų lentelė
HEX_TO_BIN_MAP = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def validate_regex(pattern: str) -> Callable[[str], str]:
    """Patvirtinimo funkcija, kuri naudojama su argparse moduliu.
    Šios funkcijos tikslas yra patvirtinti, jog vartotojas pateikė
    taisinklingą šešioliktainį skaičių, kurio šablonas yra
    apibrėžtas naudojant HEX_REGEX konstanta.

    Args:
        pattern (str): Šablonas, pagal kurį vyksta tikrinimas.

    Returns:
        Callable[[str], str]: Funkcija, kurią naudoja argparse modulis patvirtinti, jog
        įvestis yra taisiklinga.
    """

    def validate(value: str) -> str:
        # Tikrinama, ar įvestis atitinka šabloną
        if not re.match(pattern, value):
            # Jeigu įvestis neatitinka šablono, keliamas (grąžinamas) klaidos pranešimas
            raise argparse.ArgumentTypeError(
                f'Pateiktas skaičius "{value}" neatitinka Regex šablono "{pattern}"'
            )
        # Jeigu įvestis atitinka šablona, grąžinama įvesties vertė
        return value

    return validate


def strip_zeroes(number: str) -> str:
    """Funkcija, kuri pašalina skaičiaus sveikosios
    dalies pirmus nulius bei trupmeninės dalies
    paskutinius nulius.

    Pavyzdžiui:
    0101 -> 101
    0101,1010 -> 101,101
    0000.1000 -> 0.1

    Args:
        number (str): Dvejatainis skaičius, kurios nulius reikia pašalinti.

    Returns:
        str: Gautas dvejatainis „apkarpytas“ skaičius.
    """
    # Nustatome, ar sveikoji bei trupmeninė dalys yra atskirtos
    # kableliu, ar tašku, ar išvis nėra trupmeninės dalies.
    delimiter = "," if "," in number else "." if "." in number else None

    # Jeigu nėra trupmeninės skaičiaus dalies, tai pašaliname
    # nulius iš kairiosios pusės, išskyrus atvejį, kai turime tik nulį.
    if not delimiter:
        number = number.lstrip("0")
        # Kraštutinio atvejo numatymas, kai ištrinami visi
        # skaitmenys (nuliai) tokiu atveju gražiname vieną nulį
        number = number if number else "0"
        return number

    # Atskiriame sveiką ir trupmenines dalis
    whole, decimal = number.split(delimiter)
    # Pašaliname nulius iš kairiosios pusės sveikojoje skaičiaus dalyje
    whole = whole.lstrip("0")
    # Kraštutinio atvejo valdymas, kai pašalinama visa sveikoji dalis
    whole = whole if whole else "0"
    # Pašaliname nulius iš dešionios pusės trupmeninėje skaičiaus dalyje
    decimal = decimal.rstrip("0")
    # Kraštutinio atvejo valdymas, kai pašalinama visa trupmeninė dalis
    # tokiu atveju vis tiek grąžinsime nuli po kablelio (pvz.: 1,0; 2.0; ir t.t.)
    decimal = decimal if decimal else "0"
    # Sujungiame sveikąją bei trupmenines dalis į vieną skaičių
    number = delimiter.join([whole, decimal])

    return number


def convert(number: str) -> str:
    """Funkcija, kuri konvertuoja (angl. convert) trupmeninį šešioliktainį skaičių
    į dvejatainį skaičių. Konvertavimas vyksta naudojantis
    HEX_TO_BIN_MAP lentele.

    Args:
        number (str): Šešioliktainis skaičius, kurį reikia konvertuoti.

    Returns:
        str: Gautas dvejatainis skaičius.
    """
    # Visas raides keičiame didžiosiomis, nes HEX_TO_BIN_MAP
    # lentelė turi atitikmenis didžiosioms raidėms (A-F)
    number = number.upper()

    # Einame pro kiekviena atitikmenį HEX_TO_BIN_MAP
    # lentėje ir keičiame šešioliktainius skaitmenis
    # jų dvejatainiais atitikmenimis
    for hex_digit, bin_digit in HEX_TO_BIN_MAP.items():
        number = number.replace(hex_digit, bin_digit)

    # Ištriname nulius, kuriais prasideda sveikoji skaičiaus
    # dalis, bei nulius, kuriais baigiasi trupmeninė skaičiaus
    # dalis.
    number = strip_zeroes(number)

    return number


def main() -> None:
    """Pagrindinė programos funkcija, kuri paima įvestą skaičių
    iš komandinės eilutės (CLI), pasinaudoja convert funkcija ir
    išveda gautą rezultatą.

    Programa yra paleidžiama naudojant python interpretatorių
    bei būtina pateikti skaičių naudojantis -i arba --input
    argumentais.
    """
    # Sukuriame argparse instanciją, kuri paima programos įvesties
    # argumentus iš komandinės eilutės (CLI).
    parser = argparse.ArgumentParser(
        description="Programa, kuri konvertuoja šešioliktainio skaičiaus trupmeninę dalį į dvejatainį skaičių."
    )
    # Pridedam argumentą, kuris nurodo skaičių, kurį reikės konvertuoti.
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        type=validate_regex(HEX_REGEX),
        help="Šešioliktainis skaičių, kurį konvertuoti į dvejatainę sistemą.",
    )
    # Ištraukiame komandinės eilutės argumentus į args kintamąjį.
    args = parser.parse_args()

    # Konvertuojame pateiktą skaičių į dvejatainę sistemą.
    converted = convert(args.input)

    # Išvedame rezultatą į komandinę eilutę.
    print(
        f"Šešioliktainis skaičius {args.input} konvertuotas į dvejatainę sistemą yra: {converted}"
    )


# Tikriname, ar programa buvo paleista tiesiogiai iš komandinės eilutės.
# Jeigu šis failas būtų pridėtas į kitą programą naudojant import
# ši programa nepradėtų jokių veiksmų apibrėžtų main() funkcijoje.
if __name__ == "__main__":
    main()
