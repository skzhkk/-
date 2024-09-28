import re
from fractions import Fraction
def check(formula,formula_past):
#进行算式的查重
    formula_change =processeFormula(formula)
    formula_past_change = processeFormula(formula_past)
    formula=formula_change
    formula_past=formula_past_change
    op1 =[]
    op2 =[]
    #确定两个算式的运算符和顺序
    for i in range(len(formula)):
        if isOperator(formula[i]) == True:
            op1.append(formula[i])
    for i in range(len(formula_past)):
        if isOperator(formula_past[i]) == True:
            op2.append(formula_past[i])
    #查重判断的前提：运算符及运算顺序一样，数字组成一样
    if len(op1) !=len (op2):
        return 0
    for i in range(len(op1)):
        if op1[i] != op2[i]:
            return 0
    for i in range(len(formula)):
        if isOperator(formula[i]) == False:
            if formula[i] in formula_past:
                continue
            else:
                return 0
    count = 0

    for i in range(len(formula)):
        if isOperator(formula[i]) == True:
            count += 1
    # 分为3种查重情况
    if count == 1:
        if (formula[0] == formula_past[0] and formula[1] == formula_past[0]) or (formula[1] == formula_past[0] and formula[0] == formula_past[0]):
            return 1
    elif count == 2:
        check_an1=comp(formula_change,count)
        check_an2=comp(formula_past_change,count)
        str_op = ['*','+']
        #乘法与加法可以交换，即数位可以交换
        if check_an1[2] in  str_op:
            if (check_an1 == check_an2) or (check_an1[0] == check_an2[1] and check_an1[1] == check_an2[0]):
                return 1

        else:
            if check_an1 == check_an2:
                return 1
    else:
        check_an1 = comp(formula_change, count)
        check_an2 = comp(formula_past_change, count)
        str_op = ['*','+']
        #通过devi1，devi2找到分割成子式子的位置
        for i in range(len(check_an1)):
            if check_an1[i] == '#':
                devi1 = i
        for i in range(len(check_an1)):
            if check_an2[i] == '#':
                devi2 = i
        temp1 = []
        temp2 = []
        # 最后一次运算符是乘加
        if check_an1[2] in str_op:
            #如果要交换才能使分割成的新式子两侧结果相同
            if check_an1[1] == check_an2[0] and check_an1[0] == check_an2[1]:
                #调换左右侧，使生成temp存储新的两侧式子并同位置排列
                for i in range(len(check_an1)):
                    if i >= 3 and i < devi1:
                        temp1.append(check_an1[i])
                    elif i > devi1:
                        temp1.append(check_an1[i])

                    if i >= 3 and i < devi2:
                        temp2.append(check_an2[devi2+i-2])
                    elif i > devi2:
                        temp2.append(check_an2[devi2+i-10])
            else:
                #无需调换，原式子分割的左右侧直接存放入temp中
                for i in range(len(check_an1)):
                    if i >= 3 and i < devi1:
                        temp1.append(check_an1[i])
                        temp2.append(check_an2[i])
                    elif i > devi1:
                        temp1.append(check_an1[i])
                        temp2.append(check_an2[i])
            #根据分割点位置不同比较情况也不同
            if devi1 == 6 :
                if (temp1[0] == temp2[0] and temp1[2] == temp2[2]) or (temp1[0] == temp2[2] and temp1[2] == temp2[0]):
                    return 1
            elif devi1 == 4:
                if temp1[0] == temp2[0]:
                    if knowproxy(temp1[2]) < knowproxy(temp1[4]):
                        if temp1[3]==temp2[5]  or temp1[3]==temp2[3]:
                            return 1
                    else:
                        if temp1[1]==temp2[1]  or temp1[1]==temp2[3]:
                            return 1
            else:
                if temp1[5] == temp2[5] :
                    if knowproxy(temp1[1]) < knowproxy(temp1[3]):
                        if temp1[2]==temp1[4]  or temp1[4]==temp1[4]:
                            return 1
                    else:
                        if temp1[0]==temp1[2]  or temp1[0]==temp1[2]:
                            return 1
        else:
            #最后一次运算符不是乘加
            if check_an1[1] == check_an2[1] and check_an1[0] == check_an2[0]:
                if devi1 == devi2:
                    if devi1 == 6:
                        if (temp1[0] == temp2[0] and temp1[2] == temp2[2]) or (
                                temp1[0] == temp2[2] and temp1[2] == temp2[0]):
                            return 1
                    elif devi1 == 4:
                        if temp1[0] == temp2[0] :
                            if knowproxy(temp1[2]) < knowproxy(temp1[4]):
                                if temp1[3] == temp2[3] :
                                    return 1
                            else:
                                if temp1[1] == temp2[1] :
                                    return 1
                    else:
                        if temp1[5] == temp2[5] :
                            if knowproxy(temp1[1]) < knowproxy(temp1[3]):
                                if temp1[4] == temp1[4]:
                                    return 1
                            else:
                                if temp1[0] == temp1[0] :
                                    return 1

    return 0


def isOperator(element):
    #判断是否是运算符
    operators = ['+', '-', '*', '÷']
    if element in operators:
        return True
    else:
        return False

def calculate( num1, num2, op ):
    #计算两数运算结果
    result = 0
    num1 = processeNumber(num1)
    num2 = processeNumber(num2)

    if op == '+':
        result = num1 + num2
    elif op == '-':
        result = num1 - num2
        if result < 0:
            return 'False'
    elif op == '*':
        result = num1 * num2
    elif op == '÷':
        if num2 == 0 or num1 > num2:
            return 'False'
        result = num1 / num2

    return str(result)


def processeNumber( num ):
    #把带分数变假分数
    if '/' not in num:
        return Fraction(int(num))

    elif '\'' in num:
        list_num1 = re.split('([\'\/])', num)
        molecule = int(list_num1[0]) * int(list_num1[4]) + int(list_num1[2])
        return Fraction(molecule, int(list_num1[4]))

    elif '/' in num:
        return Fraction(str(num))

def comp(comp1,count):
    #比较最后一次运算式子是否相同
    count_list=[]
    low =''
    #low存放最后运算符号
    num = 1
    if count >= 2:
        #生成count_list,存放算式中每个运算的先后顺序
        for index in range(len(comp1)):
            if isOperator(comp1[index]) == True:
                if low == '':
                    low = comp1[index]
                    count_list.append('1')
                    count_list.append(comp1[index])
                elif knowproxy(low) >= knowproxy(comp1[index]):
                    for i in range(len(count_list)):
                        if i % 2 == 0:
                            count_list[i] = str(int(count_list[i])+1)
                    count_list.append('1')
                    count_list.append(comp1[index])
                    low = comp1[index]
                else:
                    count_list.append(str(num))
                    count_list.append(comp1[index])
                num += 1
    #devide表示分割成两个新式子的分割位置，分成左侧式子与右侧狮式子
    devide = 0
    new_formula1 = []
    new_formula2 = []
    list_answer = []
    for i in range(len(count_list)):
        if count_list[i] == str(1):
            devide = int((i+2)/2)
    if devide == 2 or devide ==1 or devide ==3:
        for i in range(len(comp1)):
            if i <= devide*2-2:
                new_formula1.append(comp1[i])
            elif i > devide*2-1:
                new_formula2.append(comp1[i])
    #分割成新式子放入new_formula1，new_formula2，表示左侧式子，右侧式子
    if len(new_formula1) > 2:
        #计算运算符左侧式子的值
        answer1 = calculate(new_formula1[0],new_formula1[2],new_formula1[1])
        if len(new_formula1) >= 4:
            if knowproxy(new_formula1[1]) < knowproxy(new_formula1[3]):
                answer1 = calculate(new_formula1[2], new_formula1[4], new_formula1[3])
                answer1 = calculate(answer1, new_formula1[0], new_formula1[1])
            else:
                answer1 = calculate(new_formula1[0], new_formula1[2], new_formula1[1])
                answer1 = calculate(answer1, new_formula1[4], new_formula1[3])
    else:
        answer1 = new_formula1[0]
    # 计算运算符右侧式子的值
    if len(new_formula2) > 2:
        answer2 = calculate(new_formula2[0], new_formula2[2], new_formula2[1])
        if len(new_formula2) >= 4:
            if knowproxy(new_formula2[1]) < knowproxy(new_formula2[3]):
                answer2 = calculate(new_formula2[2], new_formula2[4], new_formula2[3])
                answer2 = calculate(answer2, new_formula2[0], new_formula2[1])
            else:
                answer2 = calculate(new_formula2[0], new_formula2[2], new_formula2[1])
                answer2 = calculate(answer2, new_formula2[4], new_formula2[3])

    else:
        answer2 = new_formula2[0]
    #将左侧式子结果与右侧式子结果放入list_answer，再把分割的两侧放入list_answer
    list_answer.append(answer1)
    list_answer.append(answer2)
    list_answer.append(comp1[devide*2-1])
    if count == 3:
        for i in range(len(new_formula1)):
            list_answer.append(new_formula1[i])
        list_answer.append('#')
        for i in range(len(new_formula2)):
            list_answer.append(new_formula2[i])
    #print(list_answer)

    return list_answer

def knowproxy(low):
    #判断符号的优先级
    low_proxy = ['+', '-']
    high_proxy = ['*', '÷']
    if low in low_proxy:
        return 1
    else:
        return 2

def processeFormula( formula ):
    #将算式分割存入list
    list1 =[]
    for i in range(len(formula)):
        if formula[i] =='/' and formula[i-1] == ' ' and formula[i+1] == ' ':
            list1.append('÷')
        else:
            list1.append(formula[i])
    formula_change = ""
    for i in range(len(list1)):
        formula_change +=list1[i]
    formula = re.sub(' ', '', formula)
    l = list(filter(None, re.split('([\+\-\*\÷\(\)])', formula_change)))
    for i in range(len(formula)):
        #去掉式子括号
        if formula[i] == '(':
            for j in range(len(formula)):
               if formula[j] == ')' :
                   if j-i ==4:
                       num = calculate(formula[i+1],formula[j-1],formula[i+2])
                       l=[]
                       for k in range(len(formula)):
                           if k < i or k > j:
                               l.append(formula[k])
                           if k == i:
                               l.append(num)
                   else:
                       l = []
                       for k in range(len(formula)):
                           if k > i and k < j:
                               l.append(formula[k])
    return l