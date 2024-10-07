#!/usr/bin/python3
import argparse

# unittest modulis naudojamas atskirų programos funkcijų testavimui
import unittest

from converter import HEX_REGEX, convert, validate_regex


class TestConvert(unittest.TestCase):
    """Testavimo klasė, kuri sukuriama pagal
    unittest modulio reikalavimus. Šioje klasėje
    yra testuojama konvertavimo funckija, kad
    užtikrintume, jog ji veikia kaip numatyta.
    """

    def test_round_numbers(self):
        """Tikrinama, ar išvedami teisingi skaičiai
        su sveikaisiais šešioliktainiais skaičiais.
        """
        self.assertEqual(convert("1A3F"), "1101000111111")
        self.assertEqual(convert("ff00ff"), "111111110000000011111111")
        self.assertEqual(convert("abcDEF"), "101010111100110111101111")
        self.assertEqual(convert("B12"), "101100010010")
        self.assertEqual(convert("DEADbeef"), "11011110101011011011111011101111")

    def test_decimal_numbers(self):
        """Tikrinama, ar išvedami teisingi skaičiai
        su trupmeniniais šešioliktainiais skaičiais.
        """
        self.assertEqual(convert("1A.3F"), "11010.00111111")
        self.assertEqual(convert("abc.DEF"), "101010111100.110111101111")
        self.assertEqual(convert("0f.1a2"), "1111.00011010001")
        self.assertEqual(convert("1.0"), "1.0")
        self.assertEqual(convert("0.1234"), "0.00010010001101")


class TestValidateRegex(unittest.TestCase):
    """Testavimo klasė, kuri sukuriama pagal
    unittest modulio reikavimus. Šioje klasėje
    yra testuojama įvesties tikrinimo funkcija,
    kad užtikrintume, jog ji leidžia tik taisiklingus
    įvesties skaičius.
    """

    def test_valid_input(self):
        """Tikrinama, ar leidžiama įvesti
        taisiklingus šešioliktainius skaičius.
        """
        validate_hex = validate_regex(HEX_REGEX)
        valid_hex = [
            "1A3F",
            "ff00ff",
            "abcDEF",
            "0B12",
            "DEADbeef",
            "1A.3F",
            "abc.DEF",
            "0f.1a2",
            "1.0",
            "0.1234",
        ]
        for test_hex in valid_hex:
            self.assertEqual(validate_hex(test_hex), test_hex)

    def test_invalid_input(self):
        """Tikrinama, ar grąžinamas klaidos
        pranešimas su netaisiklingais
        šešioliktainiais skaičiais.
        """
        validate_hex = validate_regex(HEX_REGEX)
        invalid_hex = [
            "1G3F",  # Neleistinas simbolis "G"
            "123H",  # Neleistinas simbolis "H"
            "12 34",  # Neleistinas tarpo simbolis
            "-ABCDEF",  # Neleistinas simbolis "-",
            "xyz123",  # Neleistini simboliai "x", "y", "z"
            "1a3..f",  # Neleistinas dvigubas taškas
            "12.34.56",  # Neleistinas daugiau nei vienas taškas
            "-12.34",  # Neleistinas simbolis "-",
            "ab.cg12",  # Neleistinas simbolis "g"
            "123.",  # Neleistinas taškas be trupmeninės dalies
            "abc,",  # Neleistinas kablelis be trupmeninės dalies
        ]
        for test_hex in invalid_hex:
            with self.assertRaises(argparse.ArgumentTypeError):
                validate_hex(test_hex)

    def test_empty_input(self):
        """Tikrinama, ar grąžinamas klaidos
        pranešimas su tuščia įvestimi.
        """
        validate_hex = validate_regex(HEX_REGEX)
        with self.assertRaises(argparse.ArgumentTypeError):
            validate_hex("")


# Pradedame funkcijų testavimą, jeigu šis failas buvo paleistas tiesiogiai
if __name__ == "__main__":
    unittest.main()
