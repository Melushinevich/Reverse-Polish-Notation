import unittest
from calculator import Calculator


class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = Calculator()

    def test_basic_addition(self):
        result = self.calc.calculate("2+3")
        self.assertEqual(result, 5.0)

    def test_basic_subtraction(self):
        result = self.calc.calculate("10-4")
        self.assertEqual(result, 6.0)

    def test_basic_multiplication(self):
        result = self.calc.calculate("6*7")
        self.assertEqual(result, 42.0)

    def test_basic_division(self):
        result = self.calc.calculate("15/3")
        self.assertEqual(result, 5.0)

    def test_multiple_operations(self):
        result = self.calc.calculate("2+3*4")
        self.assertEqual(result, 14.0)

    def test_parentheses(self):
        result = self.calc.calculate("(2+3)*4")
        self.assertEqual(result, 20.0)

    def test_nested_parentheses(self):
        result = self.calc.calculate("2*(3+(4-2))")
        self.assertEqual(result, 10.0)

    def test_unary_minus(self):
        result = self.calc.calculate("-5+3")
        self.assertEqual(result, -2.0)

    def test_unary_minus_with_parentheses(self):
        result = self.calc.calculate("-(3+2)")
        self.assertEqual(result, -5.0)

    def test_double_unary_minus(self):
        result = self.calc.calculate("--5")
        self.assertEqual(result, 5.0)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.calculate("10/0")

    def test_complex_expression(self):
        result = self.calc.calculate("18+18-2*(13+6-3/5)-64")
        self.assertAlmostEqual(result, -64.8, places=10)

    def test_floating_point(self):
        result = self.calc.calculate("3.5+2.5")
        self.assertEqual(result, 6.0)

    def test_negative_numbers(self):
        result = self.calc.calculate("-3*4")
        self.assertEqual(result, -12.0)

    def test_expression_with_spaces(self):
        result = self.calc.calculate(" 2 + 3 * 4 ")
        self.assertEqual(result, 14.0)

    def test_empty_expression(self):
        with self.assertRaises(ValueError):
            self.calc.calculate("")

    def test_non_string_input(self):
        with self.assertRaises(ValueError):
            self.calc.calculate(123)

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            self.calc.calculate("2^3")

    def test_missing_operand(self):
        with self.assertRaises(ValueError):
            self.calc.calculate("2+")

    def test_extra_operand(self):
        with self.assertRaises(ValueError):
            self.calc.calculate("2 3+4")

    def test_variables(self):
        variables = {'x': 5, 'y': 3}
        result = self.calc.calculate("x*y+2", variables)
        self.assertEqual(result, 17.0)

    def test_undefined_variable(self):
        with self.assertRaises(ValueError):
            self.calc.calculate("x+2")

    def test_variable_with_expression(self):
        variables = {'a': 10, 'b': 2}
        result = self.calc.calculate("(a+b)*3", variables)
        self.assertEqual(result, 36.0)

    def test_unary_minus_with_multiplication(self):
        result = self.calc.calculate("-2*-3")
        self.assertEqual(result, 6.0)

    def test_complex_with_unary(self):
        result = self.calc.calculate("-(-2+3)*4")
        self.assertEqual(result, -4.0)

    def test_operator_precedence(self):
        result = self.calc.calculate("2+3*4-6/2")
        self.assertEqual(result, 11.0)

    def test_parentheses_precedence(self):
        result = self.calc.calculate("(2+3)*(4-1)")
        self.assertEqual(result, 15.0)

    def test_division_result_type(self):
        result = self.calc.calculate("5/2")
        self.assertEqual(result, 2.5)
        self.assertIsInstance(result, float)

    def test_large_numbers(self):
        result = self.calc.calculate("1000000*1000000")
        self.assertEqual(result, 1000000000000.0)

    def test_decimal_precision(self):
        result = self.calc.calculate("1/3")
        self.assertAlmostEqual(result, 0.3333333333333333, places=15)

    def test_multiple_parentheses(self):
        result = self.calc.calculate("(1+2)*(3+4)*(5+6)")
        self.assertEqual(result, 231.0)

    def test_chain_operations(self):
        result = self.calc.calculate("1+2+3+4+5")
        self.assertEqual(result, 15.0)

    def test_recalculate_same_instance(self):
        self.calc.calculate("2+3")
        result = self.calc.calculate("5*6")
        self.assertEqual(result, 30.0)

    def test_calculate_without_expression(self):
        self.calc.start_calculator("2+3")
        result = self.calc.calculate()
        self.assertEqual(result, 5.0)


class TestCalculatorEdgeCases(unittest.TestCase):

    def setUp(self):
        self.calc = Calculator()

    def test_single_number(self):
        result = self.calc.calculate("42")
        self.assertEqual(result, 42.0)

    def test_single_negative_number(self):
        result = self.calc.calculate("-42")
        self.assertEqual(result, -42.0)

    def test_decimal_numbers(self):
        with self.assertRaises(ValueError):
            self.calc.calculate("3.14.15")

    def test_leading_zeros(self):
        result = self.calc.calculate("002+003")
        self.assertEqual(result, 5.0)

    def test_trailing_operator(self):
        with self.assertRaises(ValueError):
            self.calc.calculate("2+3+")

    def test_leading_operator(self):
        with self.assertRaises(ValueError):
            self.calc.calculate("+2+3")

    def test_empty_parentheses(self):
        with self.assertRaises(ValueError):
            self.calc.calculate("()")

    def test_unmatched_parentheses(self):
        with self.assertRaises(ValueError):
            self.calc.calculate("(2+3")

    def test_variable_with_undefined_variable(self):
        with self.assertRaises(ValueError):
            self.calc.calculate("x+y", {'x': 5})

    def test_whitespace_only(self):
        with self.assertRaises(ValueError):
            self.calc.calculate("   ")


def run_all_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestCalculatorEdgeCases))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == "__main__":
    run_all_tests()