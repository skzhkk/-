import argparse
from fractions import Fraction
import random
import re

def getNumber(maxNum):
    # 随机生成整数或分数
    tag = random.randint(0, 1)
    num = ''
    maxNum = int(maxNum)
    # tag为0生成正整数（0-最大值之间)
    if tag == 0:
        num = str(random.randint(0, maxNum))

    # tag为1生成分数
    elif tag == 1:
        # 生成分母（1-最大值之间)
        denominator = random.randint(1, maxNum)
        # 分子（0-分母倍的最大值之间)
        molecule = random.randint(0, denominator * maxNum)

        if molecule == 0:
            num = 0

        if molecule > denominator:
            mixed_fraction = int(molecule / denominator)
            molecule -= mixed_fraction * denominator
            if molecule != 0:
                num = str(mixed_fraction) + "'" + str(molecule) + '/' + str(denominator)
            else:
                num = str(mixed_fraction)
        else:
            num = str(molecule) + '/' + str(denominator)
    return num

def getOperator(count):
    operator = []
    for i in range(count):
        operator_count = random.randint(0, 3)
        operation = ['+', '-', '*', '/']
        operator.append(operation[operator_count])
    return operator


def getNoBracketFormula(parameter_list, operator_list):
    top = parameter_list[0]
    formula_list = []
    formula_list.append(top)
    for index in range(len(operator_list)):
        formula_list.append(operator_list[index])
        formula_list.append(parameter_list[index + 1])
    return " ".join(str(i) for i in formula_list)


def getBracketFormula(parameter_list, operator_list):
    formula_list = []
    leftBracket_index = random.randint(0, len(operator_list) - 1)
    rightBracket_index = random.randint(leftBracket_index + 1, len(parameter_list) - 1)
    # 当左括号在最左边
    # tag == 1 生成式子的括号在头尾，无需加,要去掉
    if leftBracket_index == 0 and rightBracket_index == len(parameter_list) - 1:
        tag = 1
        first_str = parameter_list[0]
    elif leftBracket_index == 0:
        tag = 0
        first_str = '(' + parameter_list[0]
    else:
        first_str = parameter_list[0]
        tag = 0
    formula_list.append(first_str)

    for index in range(len(operator_list)):
        formula_list.append(operator_list[index])
        if index + 1 == leftBracket_index:
            formula_list.append('(')

        formula_list.append(parameter_list[index + 1])
        if index + 1 == rightBracket_index:
            if tag == 0:
                formula_list.append(')')

    return " ".join(str(i) for i in formula_list)


def getrandomFormula(maxNum):
    # 随机得到运算符个数
    operator_count = random.randint(1, 3)
    # 随机得到运算符数组
    operator_list = getOperator(operator_count)
    brackets = random.randint(0, 1)
    parameter_list = []
    #根据生成的运算符数量确定参数的数量
    for i in range(operator_count + 1):
        parameter_list.append(str(getNumber(maxNum)))

    if brackets == 0:
        return getNoBracketFormula(parameter_list, operator_list)
    elif brackets == 1:
        return getBracketFormula(parameter_list, operator_list)

def mixed_to_improper(mixed_fraction):
    whole_number, fraction_part = mixed_fraction.split("'")
    numerator, denominator = map(int, fraction_part.split('/'))
    improper_fraction = whole_number * denominator + numerator
    return improper_fraction, denominator

def replace_mixed_numbers(input_string):
    pattern = r'(\d+\'\d+/\d+)'  # 匹配带分数的正则表达式模式
    matches = re.findall(pattern, input_string)  # 查找所有匹配的带分数

    for match in matches:
        whole, numerator, denominator = map(int, re.split("[/'']", match))  # 将带分数拆分成整数部分、分子和分母
        improper_fraction = whole * denominator + numerator  # 将带分数转换为假分数
        replacement = f"({improper_fraction}/{denominator})"  # 构建替换字符串
        input_string = input_string.replace(match, replacement)  # 替换带分数

    return input_string

def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    stack = []
    postfix = []

    i = 0
    while i < len(expression):
        char = expression[i]
        if char.isalnum():
            # 读取连续的数字
            num = char
            while i + 1 < len(expression) and expression[i + 1].isalnum():
                num += expression[i + 1]
                i += 1
            postfix.append(num)
        elif char in precedence:
            postfix.append(' ')
            while stack and precedence.get(stack[-1], 0) >= precedence.get(char, 0):
                postfix.append(stack.pop())
                postfix.append(' ')
            stack.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                postfix.append(' ')
                postfix.append(stack.pop())
            stack.pop()
        i += 1

    while stack:
        postfix.append(' ')
        postfix.append(stack.pop())

    return ''.join(postfix)

def evaluate_postfix(postfix_expression):
    stack = []
    elements = postfix_expression.split()

    for char in elements:
        if char.isalnum():
            stack.append(Fraction(char))
        else:
            operand2 = stack.pop()
            operand1 = stack.pop()
            if char == '+':
                stack.append(operand1 + operand2)
            elif char == '-':
                stack.append(operand1 - operand2)
            elif char == '*':
                stack.append(operand1 * operand2)
            elif char == '/':
                stack.append(Fraction(operand1, operand2))

    return stack.pop()

def evaluate_expression(expr):
    """计算表达式的值"""
    expr = replace_mixed_numbers(expr)
    postfix = infix_to_postfix(expr)
    return evaluate_postfix(postfix)


def generate_exercises(num,range):
    """生成题目并保存到文件"""
    exercises = set()
    while len(exercises) < num:
        expr = getrandomFormula(range)
        if expr not in exercises:
            exercises.add(expr)

    with open('Exercises.txt', 'w') as ex_file, open('Answers.txt', 'w') as ans_file:
        for expr in exercises:
            print(expr)
            answer = evaluate_expression(expr)
            ex_file.write(f"{expr} =\n")
            ans_file.write(f"{answer}\n")


def grade_exercises(exercise_file, answer_file):
    """判定答案的正确性并统计结果"""
    with open(exercise_file, 'r') as ex_file, open(answer_file, 'r') as ans_file:
        exercises = ex_file.readlines()
        answers = ans_file.readlines()

    correct = []
    wrong = []

    for i, (exercise, answer) in enumerate(zip(exercises, answers)):
        exercise = exercise.strip()
        correct_answer = evaluate_expression(exercise[:-2])  # 去掉最后的" ="
        if str(correct_answer) == answer.strip():
            correct.append(i + 1)
        else:
            wrong.append(i + 1)

    with open('Grade.txt', 'w') as grade_file:
        grade_file.write(f"Correct: {len(correct)} ({', '.join(map(str, correct))})\n")
        grade_file.write(f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate arithmetic exercises or grade them.')
    parser.add_argument('-n', type=int, help='Number of exercises to generate')
    parser.add_argument('-r', type=int, help='Range of numbers for exercises')
    parser.add_argument('-e', type=str, help='Exercise file to grade')
    parser.add_argument('-a', type=str, help='Answer file to grade')

    args = parser.parse_args()

    if args.n and args.r:
        generate_exercises(args.n,args.r)
    elif args.e and args.a:
        grade_exercises(args.e, args.a)
    else:
        parser.print_help()