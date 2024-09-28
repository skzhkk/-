import argparse
from fractions import Fraction
import random
import re


import random

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
            num = '0'

        if molecule > denominator:
            mixed_fraction = int(molecule / denominator)
            molecule -= mixed_fraction * denominator
            if molecule != 0:
                num = str(mixed_fraction) + "'" + str(molecule) + '/' + str(denominator)  # 带分数形式
            else:
                num = str(mixed_fraction)  # 整数形式
        else:
            num = str(molecule) + '/' + str(denominator)  # 分数形式
    return num

import random

def getOperator(count):
    # 生成指定数量的运算符列表
    operator = []
    for i in range(count):
        # 随机生成0到3之间的整数，用于选择运算符
        operator_count = random.randint(0, 3)
        operation = ['+', '-', '*', '/']
        operator.append(operation[operator_count])
    return operator


def getNoBracketFormula(parameter_list, operator_list):
    # 从参数列表中取出第一个参数作为初始值
    top = parameter_list[0]
    formula_list = []
    formula_list.append(top)

    # 将参数和运算符交替添加到公式列表中
    for index in range(len(operator_list)):
        formula_list.append(operator_list[index])
        formula_list.append(parameter_list[index + 1])

    # 将公式列表中的元素转换为字符串并用空格连接起来 形成算式
    return " ".join(str(i) for i in formula_list)


def getBracketFormula(parameter_list, operator_list):
    formula_list = []
    # 随机生成左右括号的位置
    leftBracket_index = random.randint(0, len(operator_list) - 1)
    rightBracket_index = random.randint(leftBracket_index + 1, len(parameter_list) - 1)

    # 处理左括号在最左边的情况
    if leftBracket_index == 0 and rightBracket_index == len(parameter_list) - 1:
        tag = 1  # 生成式子的括号在头尾，无需加逗号
        first_str = parameter_list[0]
    elif leftBracket_index == 0:
        tag = 0
        first_str = '(' + parameter_list[0]
    else:
        first_str = parameter_list[0]
        tag = 0
    formula_list.append(first_str)

    # 将参数和运算符按照括号位置添加到公式列表中
    for index in range(len(operator_list)):
        formula_list.append(operator_list[index])
        if index + 1 == leftBracket_index:
            formula_list.append('(')

        formula_list.append(parameter_list[index + 1])
        if index + 1 == rightBracket_index:
            if tag == 0:
                formula_list.append(')')

    # 将公式列表中的元素转换为字符串并用空格连接起来 形成算式
    return " ".join(str(i) for i in formula_list)


def getrandomFormula(maxNum):
    # 随机得到运算符个数
    operator_count = random.randint(1, 3)
    # 随机得到运算符数组
    operator_list = getOperator(operator_count)
    brackets = random.randint(0, 1)
    parameter_list = []

    # 根据生成的运算符数量确定参数的数量
    for i in range(operator_count + 1):
        parameter_list.append(str(getNumber(maxNum)))

    # 根据随机生成的括号情况调用不同的函数生成公式
    if brackets == 0:
        return getNoBracketFormula(parameter_list, operator_list)
    elif brackets == 1:
        return getBracketFormula(parameter_list, operator_list)


def replace_mixed_numbers(input_string):
    # 将算式中的带分数替换为假分数
    pattern = r'(\d+\'\d+/\d+)'  # 匹配带分数的正则表达式模式
    matches = re.findall(pattern, input_string)  # 查找所有匹配的带分数

    for match in matches:
        whole, numerator, denominator = map(int, re.split("[/']", match))  # 将带分数拆分成整数部分、分子和分母
        improper_fraction = whole * denominator + numerator  # 将带分数转换为假分数
        replacement = f"({improper_fraction}/{denominator})"  # 构建替换字符串
        input_string = input_string.replace(match, replacement)  # 替换带分数

    return input_string


def infix_to_postfix(expression):
    # 中缀表达式转换为后缀表达式
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    stack = []
    postfix = []

    i = 0
    while i < len(expression):
        char = expression[i]
        if char.isalnum():
            # 如果是数字，读取连续的数字字符
            num = char
            while i + 1 < len(expression) and expression[i + 1].isalnum():
                num += expression[i + 1]
                i += 1
            postfix.append(num)
        elif char in precedence:
            # 如果是运算符
            postfix.append(' ')
            while stack and precedence.get(stack[-1], 0) >= precedence.get(char, 0):
                postfix.append(stack.pop())
                postfix.append(' ')
            stack.append(char)
        elif char == '(':
            # 如果是左括号，直接入栈
            stack.append(char)
        elif char == ')':
            # 如果是右括号，将栈顶元素弹出直到遇到左括号
            while stack and stack[-1] != '(':
                postfix.append(' ')
                postfix.append(stack.pop())
            stack.pop()
        i += 1

    # 将栈中剩余的运算符弹出并添加到后缀表达式中
    while stack:
        postfix.append(' ')
        postfix.append(stack.pop())

    return ''.join(postfix)


def evaluate_postfix(postfix_expression):
    # 计算后缀表达式的值
    stack = []
    elements = postfix_expression.split()

    for char in elements:
        if char.isalnum():
            # 如果是数字，将其转换为分数并入栈
            stack.append(Fraction(char))
        else:
            operand2 = stack.pop()
            operand1 = stack.pop()
            if char == '+':
                stack.append(operand1 + operand2)
            elif char == '-':
                if operand2 > operand1: # 出现减数大于被减数时置为-1
                    return -1
                stack.append(operand1 - operand2)
            elif char == '*':
                stack.append(operand1 * operand2)
            elif char == '/':
                if operand2 == 0:  # 出现除以0的情况置为-1
                    return -1
                if operand1 == 0:  # 分子为0计算结果为0，不返回分数
                    stack.append(0)
                else:
                    stack.append(Fraction(operand1, operand2))

    return stack.pop()


def evaluate_expression(expr):
    # 计算表达式的值
    expr = replace_mixed_numbers(expr)  # 将算式中的带分数替换为假分数
    postfix = infix_to_postfix(expr)  # 中缀表达式转换为后缀表达式
    answer = evaluate_postfix(postfix)
    if answer != 0:  # 0无需变为带分数
        answer = improper_to_mixed(answer)  # 如果是假分数转换为带分数
    return answer


def improper_to_mixed(improper_fraction):
    # 计算带分数的整数部分
    whole = improper_fraction // improper_fraction.denominator
    # 计算带分数的分子
    numerator = improper_fraction.numerator % improper_fraction.denominator
    denominator = improper_fraction.denominator
    if whole != 0:
        if numerator != 0:
            # 如果有整数部分和非零分子，则返回带分数形式
            return f"{whole}'{numerator}/{denominator}"
        else:
            # 如果有整数部分但分子为0，则只返回整数部分
            return f"{whole}"
    else:
        # 如果没有整数部分，则直接返回分数形式
        return f"{numerator}/{denominator}"


def generate_exercises(num,range):
    """生成题目并保存到文件"""
    exercises = set()
    while len(exercises) < num:
        expr = getrandomFormula(range)  # 生成算式
        if expr not in exercises and evaluate_expression(expr) != -1:  # 算式结果为-1说明出现除以0的情况
            exercises.add(expr)

    with open('Exercises.txt', 'w') as ex_file, open('Answers.txt', 'w') as ans_file:
        for expr in exercises:
            print(expr)
            answer = evaluate_expression(expr)
            ex_file.write(f"{expr} =\n")
            ans_file.write(f"{answer}\n")


def grade_exercises(exercise_file, answer_file):
    # 判定答案的正确性并统计结果
    with open(exercise_file, 'r') as ex_file, open(answer_file, 'r') as ans_file:
        exercises = ex_file.readlines()  # 读取习题文件中的所有行
        answers = ans_file.readlines()  # 读取答案文件中的所有行

    correct = []  # 存储正确答案的习题编号
    wrong = []  # 存储错误答案的习题编号

    for i, (exercise, answer) in enumerate(zip(exercises, answers)):
        exercise = exercise.strip()  # 去除习题两端的空白字符
        correct_answer = evaluate_expression(exercise[:-2])  # 去掉最后的" ="
        if str(correct_answer) == answer.strip():  # 检查答案是否正确
            correct.append(i + 1)  # 将正确答案的习题编号加入correct列表
        else:
            wrong.append(i + 1)  # 将错误答案的习题编号加入wrong列表

    with open('Grade.txt', 'w') as grade_file:
        grade_file.write(f"Correct: {len(correct)} ({', '.join(map(str, correct))})\n")  # 将正确答案的数量和编号写入文件
        grade_file.write(f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})\n")  # 将错误答案的数量和编号写入文件


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate arithmetic exercises or grade them.')
    parser.add_argument('-n', type=int, help='Number of exercises to generate')
    parser.add_argument('-r', type=int, help='Range of numbers for exercises')
    parser.add_argument('-e', type=str, help='Exercise file to grade')
    parser.add_argument('-a', type=str, help='Answer file to grade')

    args = parser.parse_args()

    if args.n and args.r:
        generate_exercises(args.n,args.r)  # 生成题目
    elif args.e and args.a:
        grade_exercises(args.e, args.a)  # 判定答案中的对错
    else:
        parser.print_help()