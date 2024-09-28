import os
import unittest
from Myapp import *

class TestArithmeticExercises(unittest.TestCase):

    def test_getNumber(self):
        # 测试 getNumber 函数是否返回字符串类型的数字
        maxNum = 10
        num = getNumber(maxNum)
        self.assertTrue(isinstance(num, str))

    def test_getOperator(self):
        # 测试 getOperator 函数是否返回指定数量的运算符列表
        count = 3
        operator_list = getOperator(count)
        self.assertEqual(len(operator_list), count)

    def test_getNoBracketFormula(self):
        # 测试 getNoBracketFormula 函数是否返回字符串类型的算式
        parameter_list = ['2', '3', '4']
        operator_list = ['+', '-']
        formula = getNoBracketFormula(parameter_list, operator_list)
        print(formula)
        self.assertTrue(isinstance(formula, str))

    def test_getBracketFormula(self):
        # 测试 getBracketFormula 函数是否返回字符串类型的带括号算式
        parameter_list = ['2', '3', '4']
        operator_list = ['+', '*']
        formula = getBracketFormula(parameter_list, operator_list)
        self.assertTrue(isinstance(formula, str))

    def test_replace_mixed_numbers(self):
        # 测试 replace_mixed_numbers 函数是否正确替换带分数为假分数
        input_string = "2'1/2 + 3/4"
        result = replace_mixed_numbers(input_string)
        self.assertEqual(result, '(5/2) + 3/4')

    def test_infix_to_postfix(self):
        # 测试 infix_to_postfix 函数是否正确将中缀表达式转换为后缀表达式
        expression = '2 + 3 * 4'
        postfix = infix_to_postfix(expression)
        self.assertEqual(postfix, '2 3 4 * +')

    def test_evaluate_postfix(self):
        # 测试 evaluate_postfix 函数是否返回 Fraction 类型的计算结果
        postfix_expression = '2 3 4 * +'
        result = evaluate_postfix(postfix_expression)
        self.assertTrue(isinstance(result, Fraction))

    def test_improper_to_mixed(self):
        # 测试 improper_to_mixed 函数是否正确将假分数转换为带分数
        improper_fraction = Fraction(7, 2)
        result = improper_to_mixed(improper_fraction)
        self.assertEqual(result, "3'1/2")

    def test_duplicate_check(self):
        # 测试 duplicate_check 函数是否正确检查重复算式
        expr = '2 + 3 * 4'
        exercises = ['3 * 4 + 2', '2 + 3 * 4']
        result = duplicate_check(expr, exercises)
        self.assertTrue(result)

    def test_generate_exercises(self):
        # 测试 generate_exercises 函数是否能够生成题目文件和答案文件
        num = 5
        range = 10
        generate_exercises(num, range)

        # 检查生成的题目文件是否存在
        self.assertTrue(os.path.exists('Exercises.txt'))

        # 检查生成的题目文件中是否有5条记录
        with open('Exercises.txt', 'r') as file:
            exercises = file.readlines()
            self.assertEqual(len(exercises), 5)

    def test_grade_exercises(self):
        # 测试 grade_exercises 函数是否能够正确判定答案并生成正确的成绩文件
        exercise_file = 'Exercises_test.txt'
        answer_file = 'Answers_test.txt'
        grade_exercises(exercise_file, answer_file)

        with open('Grade.txt', 'r') as file:
            content = file.read()
            expected_content = "Correct: 7 (1, 2, 4, 5, 6, 8, 9)\nWrong: 3 (3, 7, 10)"
            self.assertEqual(content.strip(), expected_content)

    def test_evaluate_expression_1(self):
        # 测试计算过程中产生负数的情况，计算结果能否置为 -1
        expr = "3-9+1"
        result = evaluate_expression(expr)
        self.assertEqual(result, "-1")

    def test_evaluate_expression_2(self):
        # 测试存在形如e1÷ e2的子表达式,结果应是真分数
        expr = "7/3"
        result = evaluate_expression(expr)
        self.assertEqual(result, "2'1/3")

    def test_check_identical_formulas(self):
        # 测试 有限次交换+和×左右的算术表达式变换为同一道题目
        formula1 = "2+3*4"
        formula2 = "2+4*3"
        self.assertEqual(check(formula1, formula2), 1)

    def test_check_different_formulas(self):
        # 测试 不同算式是否为不相同
        formula1 = "2+3*4"
        formula2 = "2*3+4"
        self.assertEqual(check(formula1, formula2), 0)

if __name__ == '__main__':
    unittest.main()