
class Executer():
    name = ""
    value_func = 0
    answer = ""

    def __init__(self, pars):
        self.pars = pars

    def execute(self):
        index = 0
        key = False
        args = []
        ind_arr = 0
        array = []
        while index < len(self.pars.poliz):
            pc_el = self.pars.poliz[index]
            if pc_el[0] == "bool" or pc_el[0] == "int" or pc_el[0] == "poliz_address" or pc_el[0] == "poliz_label":
                args.append(pc_el[1])
                '''if pc_el[1] in self.pars.dict and self.pars.dict[pc_el[1]][2] == "array":
                    key = True'''
                '''if len(pc_el) > 2:
                                    if type(pc_el[2]) is str:
                                        if self.pars.dict[pc_el[2]][1]:
                                            pc_el = (pc_el[0], pc_el[1], self.pars.dict[pc_el[2]][3])
                                            if pc_el[2] in range(self.pars.dict[pc_el[1]][4], self.pars.dict[pc_el[1]][5] + 1):
                                                pass
                                            else:
                                                raise Exception("Error: not in range of array")
                                        else:
                                            raise Exception("POLIZ: undefined elem")
                                    ind_arr = pc_el[2]
                                args.append(pc_el[1])'''
            elif pc_el[0] == "ID":
                '''if (self.pars.dict[pc_el[1]])[2] == "array":
                    if type(pc_el[2]) is str:
                        if self.pars.dict[pc_el[2]][1]:
                            pc_el = (pc_el[0], pc_el[1], self.pars.dict[pc_el[2]][3])
                            if pc_el[2] in range(self.pars.dict[pc_el[1]][4], self.pars.dict[pc_el[1]][5] + 1):
                                pass
                            else:
                                raise Exception("Error: not in range of array")
                        else:
                            raise Exception("POLIZ: undefined elem")
                    ind_arr = pc_el[2]
                    if ((self.pars.dict[pc_el[1]])[6])[ind_arr - 1] != "no":
                        args.append((self.pars.dict[pc_el[1]])[6][ind_arr - 1])
                    else:
                        raise Exception("POLIZ: indefinite identifier")'''
                if pc_el[1] in self.pars.dict and self.pars.dict[pc_el[1]][2] == "array":
                    # key = True
                    args.append(pc_el[1])
                elif (len(self.pars.dict[pc_el[1]]) > 3):
                        args.append((self.pars.dict[pc_el[1]])[3])
                else:
                    raise Exception("POLIZ: indefinite identifier")
            elif pc_el[0] == "not":
                i = args[-1]
                args.pop()
                args.append(not (i))
            elif pc_el[0] == "or":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(i or j)
            elif pc_el[0] == "and":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(i and j)
            elif pc_el[0] == "poliz_go":
                i = args[-1]
                args.pop()
                index = i - 1
            elif pc_el[0] == "poliz_fgo":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if (not j):
                    index = i - 1
            elif pc_el[0] == "write":
                j = args[-1]
                args.pop()
                if args != []:
                    ind_arr = j
                    j = args[-1]
                    if j in self.pars.dict and self.pars.dict[j][2] == "array":
                        args.pop()
                        array = self.pars.dict[j][6]
                        if ind_arr < (self.pars.dict[j])[4] or ind_arr > (self.pars.dict[j])[5]:
                            raise Exception("Error: not in range of array")
                        else:
                            if array[ind_arr - 1] == "no":
                                raise Exception("POLIZ: indefinite identifier")
                            else:
                                # print(array[ind_arr - 1], end='')
                                self.answer += str(array[ind_arr - 1])
                else:
                    # print(j)
                    self.answer += str(j)
            elif pc_el[0] == "writeln":
                j = args[-1]
                args.pop()
                if args != []:
                    ind_arr = j
                    j = args[-1]
                    if j in self.pars.dict and self.pars.dict[j][2] == "array":
                        args.pop()
                        array = self.pars.dict[j][6]
                        if ind_arr < (self.pars.dict[j])[4] or ind_arr > (self.pars.dict[j])[5]:
                            raise Exception("Error: not in range of array")
                        else:
                            if array[ind_arr - 1] == "no":
                                raise Exception("POLIZ: indefinite identifier")
                            else:
                                # print(array[ind_arr - 1], end='')
                                self.answer += str(array[ind_arr - 1])
                                self.answer += '\n'
                else:
                    # print(j)
                    self.answer += str(j)
                    self.answer += '\n'
            elif pc_el[0] == "read":
                value = 0
                i = args[-1]
                args.pop()
                if args != []:
                    ind_arr = i
                    i = args[-1]
                    args.pop()
                    if (self.pars.dict[i])[2] == "array":
                        if (self.pars.dict[i])[3] == "integer":
                            while True:
                                print("Input int value for " + i + '[' + str(ind_arr) + ']')
                                value = input()
                                if value.isdigit():
                                    break
                                else:
                                    print("Error in input: expect int number")
                                    continue
                        else:
                            while True:
                                print("Input boolean value (true or false) for" + i + '[' + str(ind_arr) + ']')
                                j = input()
                                if j != "true" and j != "false":
                                    print("Error in input:true/false")
                                    continue
                                if j == "false":
                                    value = 0
                                else:
                                    value = 1
                                break
                        array = self.pars.dict[i][6]
                        if ind_arr < (self.pars.dict[i])[4] or ind_arr > (self.pars.dict[i])[5]:
                            raise Exception("Error: not in range of array")
                        else:
                            array[ind_arr - 1] = int(value)
                            self.pars.dict[i] = ("ID", True, (self.pars.dict[i])[2], (self.pars.dict[i])[3], (self.pars.dict[i])[4], (self.pars.dict[i])[5], array)
                else:
                    if (self.pars.dict[i])[2] == "integer":
                        while True:
                            print("Input int value for ", i)
                            value = input()
                            if value.isdigit():
                                break
                            else:
                                print("Error in input: expect int number")
                                continue
                    else:
                        while True:
                            print("Input boolean value (true or false) for", i)
                            j = input()
                            if j != "true" and j != "false":
                                print("Error in input:true/false")
                                continue
                            if j == "false":
                                value = 0
                            else:
                                value = 1
                            break
                    self.pars.dict[i] = ("ID", True, (self.pars.dict[i])[2], int(value))
            elif pc_el[0] == "+":
                if self.value_func != 0:
                    args.append(self.value_func)
                    self.value_func = 0
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if key:
                    args.append(j + i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] + self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i + self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i + self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] + i)
                    else:
                        args.append(j + i)
                else:
                    args.append(j + i)
            elif pc_el[0] == "*":
                if self.value_func != 0:
                    args.append(self.value_func)
                    self.value_func = 0
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if key:
                    args.append(j * i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] * self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i * self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i * self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] * i)
                    else:
                        args.append(j * i)
                else:
                    args.append(j * i)
            elif pc_el[0] == "-":
                if self.value_func != 0:
                    args.append(self.value_func)
                    self.value_func = 0
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if key:
                    args.append(j - i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] - self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i - self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i - self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] and not(key) == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] - i)
                    else:
                        args.append(j - i)
                else:
                    args.append(j - i)
            elif pc_el[0] == "/":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if i == 0:
                    raise Exception("POLIZ:divide by zero")
                else:
                    args.append(j / i)
            elif pc_el[0] == "=":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if key:
                    args.append(j == i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] == self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i == self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i == self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] == i)
                    else:
                        args.append(j == i)
                else:
                    args.append(j == i)
            elif pc_el[0] == "<>":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if key:
                    args.append(j != i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] != self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i != self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i != self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] != i)
                    else:
                        args.append(j != i)
                else:
                    args.append(j != i)
            elif pc_el[0] == "<":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if key:
                    args.append(j < i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] < self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i < self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i < self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] < i)
                    else:
                        args.append(j < i)
                else:
                    args.append(j < i)
            elif pc_el[0] == ">":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if key:
                    args.append(j > i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] > self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i > self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i > self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] > i)
                    else:
                        args.append(j > i)
                else:
                    args.append(j > i)
            elif pc_el[0] == "<=":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if key:
                    args.append(j <= i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] <= self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i <= self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i <= self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] > i)
                    else:
                        args.append(j <= i)
                else:
                    args.append(j <= i)
            elif pc_el[0] == ">=":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if key:
                    args.append(j >= i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] >= self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i >= self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i >= self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] >= i)
                    else:
                        args.append(j >= i)
                else:
                    args.append(j >= i)
            elif pc_el[0] == "-":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(j != i)
            elif pc_el[0] == "assign":
                '''if len(args) < 2 and self.value_func != 0:
                    args.append(self.value_func)
                    self.value_func = 0'''
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                '''if self.pars.dict[j][2] == "array":
                    array = self.pars.dict[j][6]
                    if type(pc_el[2]) is str:
                        if self.pars.dict[pc_el[2]][1]:
                            pc_el = (pc_el[0], pc_el[1], self.pars.dict[pc_el[2]][3])
                            if pc_el[2] in range(self.pars.dict[j][4], self.pars.dict[j][5] + 1):
                                pass
                            else:
                                raise Exception("Error: not in range of array")
                        else:
                            raise Exception("POLIZ: undefined elem")
                    array[pc_el[2] - 1] = i
                    self.pars.dict[j] = ("ID", True, (self.pars.dict[j])[2], (self.pars.dict[j])[3], (self.pars.dict[j])[4], (self.pars.dict[j])[5], array)
                else:
                    self.pars.dict[j] = ("ID", True, (self.pars.dict[j])[2], i)'''
                if args != []:
                    ind_arr = j
                    j = args[-1]
                    args.pop()
                    # key = False
                    if j in self.pars.dict and self.pars.dict[j][2] == "array":
                        array = self.pars.dict[j][6]
                        if ind_arr < (self.pars.dict[j])[4] or ind_arr > (self.pars.dict[j])[5]:
                            raise Exception("Error: not in range of array")
                        else:
                            array[ind_arr - 1] = i
                            self.pars.dict[j] = ("ID", True, (self.pars.dict[j])[2], (self.pars.dict[j])[3], (self.pars.dict[j])[4], (self.pars.dict[j])[5], array)
                else:
                    self.pars.dict[j] = ("ID", True, (self.pars.dict[j])[2], i)
            elif pc_el[0] == "beg_ind_arr":
                key = True
            elif pc_el[0] == "end_ind_arr":
                key = False
            elif pc_el[0] == "begin_args":
                self.execute_proc(index + 1)
                self.execute_proc_poliz()
                while pc_el[0] != "end_args":
                    index += 1
                    pc_el = self.pars.poliz[index]
                if self.value_func != 0:
                    args.append(self.value_func)
                    self.value_func = 0
            else:
                raise Exception("POLIZ: unexpected elem")
            index += 1
        print(self.answer)

    def execute_proc_poliz(self):
        poliz = self.pars.all_poliz_proc[self.name]
        index = 0
        key = False
        args = []
        ind_arr = 0
        array = []
        while index < len(poliz):
            pc_el = poliz[index]
            if pc_el[0] == "bool" or pc_el[0] == "int" or pc_el[0] == "poliz_address" or pc_el[0] == "poliz_label":
                args.append(pc_el[1])
            elif pc_el[0] == "ID":
                cond = False
                for elem in self.pars.param_proc[self.name]:
                    if pc_el[1] in elem:
                        break
                if elem[3] == 'array':
                        cond = True
                if cond:
                    # key = True
                    args.append(pc_el[1])
                elif (len(elem) > 5):
                    args.append(elem[5])
                elif (len(elem) > 4) and (type(elem[-1]) == int):
                    args.append(elem[4])
                else:
                    raise Exception("POLIZ: indefinite identifier")
            elif pc_el[0] == "not":
                i = args[-1]
                args.pop()
                args.append(not (i))
            elif pc_el[0] == "or":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(i or j)
            elif pc_el[0] == "and":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(i and j)
            elif pc_el[0] == "poliz_go":
                i = args[-1]
                args.pop()
                index = i - 1
            elif pc_el[0] == "poliz_fgo":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if (not j):
                    index = i - 1
            elif pc_el[0] == "write":
                j = args[-1]
                args.pop()
                # print(j)
                self.answer += str(j)
            elif pc_el[0] == "writeln":
                j = args[-1]
                args.pop()
                # print(j)
                self.answer += str(j)
                self.answer += '\n'
            elif pc_el[0] == "read":
                value = 0
                i = args[-1]
                args.pop()
                if args != []:
                    ind_arr = i
                    i = args[-1]
                    args.pop()
                    if (self.pars.dict[i])[2] == "array":
                        if (self.pars.dict[i])[3] == "integer":
                            while True:
                                print("Input int value for " + i + '[' + str(ind_arr) + ']')
                                value = input()
                                if value.isdigit():
                                    break
                                else:
                                    print("Error in input: expect int number")
                                    continue
                        else:
                            while True:
                                print("Input boolean value (true or false) for" + i + '[' + str(ind_arr) + ']')
                                j = input()
                                if j != "true" and j != "false":
                                    print("Error in input:true/false")
                                    continue
                                if j == "false":
                                    value = 0
                                else:
                                    value = 1
                                break
                        array = self.pars.dict[i][6]
                        if ind_arr < (self.pars.dict[i])[4] or ind_arr > (self.pars.dict[i])[5]:
                            raise Exception("Error: not in range of array")
                        else:
                            array[ind_arr - 1] = int(value)
                            self.pars.dict[i] = (
                            "ID", True, (self.pars.dict[i])[2], (self.pars.dict[i])[3], (self.pars.dict[i])[4],
                            (self.pars.dict[i])[5], array)
                else:
                    if (self.pars.dict[i])[2] == "integer":
                        while True:
                            print("Input int value for ", i)
                            value = input()
                            if value.isdigit():
                                break
                            else:
                                print("Error in input: expect int number")
                                continue
                    else:
                        while True:
                            print("Input boolean value (true or false) for", i)
                            j = input()
                            if j != "true" and j != "false":
                                print("Error in input:true/false")
                                continue
                            if j == "false":
                                value = 0
                            else:
                                value = 1
                            break
                    self.pars.dict[i] = ("ID", True, (self.pars.dict[i])[2], int(value))
            elif pc_el[0] == "+":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(j + i)  # если массив нужно убрать и раскомментировать код ниже
                '''if key:
                    args.append(j + i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] + self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i + self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i + self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] + i)
                    else:
                        args.append(j + i)
                else:
                    args.append(j + i)'''
            elif pc_el[0] == "*":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(j * i) # если массив нужно убрать и раскомментировать код ниже
                '''if key:
                    args.append(j * i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] * self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i * self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i * self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] * i)
                    else:
                        args.append(j * i)
                else:
                    args.append(j * i)'''
            elif pc_el[0] == "-":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(j - i)  # если массив нужно убрать и раскомментировать код ниже
                '''if key:
                    args.append(j - i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] - self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i - self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i - self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] and not (key) == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] - i)
                    else:
                        args.append(j - i)
                else:
                    args.append(j - i)'''
            elif pc_el[0] == "/":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if i == 0:
                    raise Exception("POLIZ:divide by zero")
                else:
                    args.append(j / i)
            elif pc_el[0] == "=":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(j == i)  # если массив нужно убрать и раскомментировать код ниже
                '''if key:
                    args.append(j == i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] == self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i == self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i == self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] == i)
                    else:
                        args.append(j == i)
                else:
                    args.append(j == i)'''
            elif pc_el[0] == "<":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(j < i)  # если массив нужно убрать и раскомментировать код ниже
                '''if key:
                    args.append(j < i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] < self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i < self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i < self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] < i)
                    else:
                        args.append(j < i)
                else:
                    args.append(j < i)'''
            elif pc_el[0] == ">":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(j > i)  # если массив нужно убрать и раскомментировать код ниже
                '''if key:
                    args.append(j > i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] > self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i > self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i > self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] > i)
                    else:
                        args.append(j > i)
                else:
                    args.append(j > i)'''
            elif pc_el[0] == "<=":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(j <= i)  # если массив нужно убрать и раскомментировать код ниже
                '''if key:
                    args.append(j <= i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] <= self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i <= self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i <= self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] > i)
                    else:
                        args.append(j <= i)
                else:
                    args.append(j <= i)'''
            elif pc_el[0] == ">=":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(j >= i)  # если массив нужно убрать и раскомментировать код ниже
                '''if key:
                    args.append(j >= i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] >= self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i >= self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i >= self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] >= i)
                    else:
                        args.append(j >= i)
                else:
                    args.append(j >= i)'''
            elif pc_el[0] == "-":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(j != i)
            elif pc_el[0] == "assign":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                for ind in range(len(self.pars.param_proc[self.name])):
                    if j in self.pars.param_proc[self.name][ind]:
                        break
                if len(self.pars.param_proc[self.name][ind]) > 5:
                    tmp = list(self.pars.param_proc[self.name][ind])
                    tmp[len(tmp) - 1] = i
                    self.pars.param_proc[self.name][ind] = tuple(tmp)
                else:
                    self.pars.param_proc[self.name][ind] += (i, )
                    if self.pars.param_proc[self.name][ind][0] == self.name:
                        self.value_func = i
                '''for u in self.pars.param_proc:
                    if u == self.name:
                        
                        self.value_func = i'''
            elif pc_el[0] == "beg_ind_arr":
                key = True
            elif pc_el[0] == "end_ind_arr":
                key = False
            elif pc_el[0] == "begin_args":
                self.execute_proc(index + 1)
                self.execute_proc_poliz()
                while pc_el[0] != "end_args":
                    index += 1
                    pc_el = self.pars.poliz[index]
            else:
                raise Exception("POLIZ: unexpected elem")
            index += 1


    def execute_proc(self, index):
        key = False
        count = 0
        args = []
        ind_arr = 0
        array = []
        while index < len(self.pars.poliz):
            pc_el = self.pars.poliz[index]
            if pc_el[0] == "end_args":
                break
            elif pc_el[0] == 'name_proc':
                self.name = pc_el[1]
            elif pc_el[0] == "bool" or pc_el[0] == "int":
                args.append(pc_el[1])
            elif pc_el[0] == "ID":
                if pc_el[1] in self.pars.dict and self.pars.dict[pc_el[1]][2] == "array":
                    # key = True
                    args.append(pc_el[1])
                elif (len(self.pars.dict[pc_el[1]]) > 3):
                    args.append((self.pars.dict[pc_el[1]])[3])
                else:
                    raise Exception("POLIZ: indefinite identifier")
            elif pc_el[0] == "assign_args":
                i = args[-1]
                args.pop()
                if len(self.pars.param_proc[self.name]) == count or len(self.pars.param_proc[self.name][count]) < 5:
                    raise Exception("POLIZ: argument mismatch")
                self.pars.param_proc[self.name][count] += (i, )
                count += 1
            elif pc_el[0] == "+":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if key:
                    args.append(j + i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] + self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i + self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i + self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] + i)
                    else:
                        args.append(j + i)
                else:
                    args.append(j + i)
            elif pc_el[0] == "*":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if key:
                    args.append(j * i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] * self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i * self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i * self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] * i)
                    else:
                        args.append(j * i)
                else:
                    args.append(j * i)
            elif pc_el[0] == "-":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if key:
                    args.append(j - i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] - self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i - self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i - self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] and not (key) == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] - i)
                    else:
                        args.append(j - i)
                else:
                    args.append(j - i)
            elif pc_el[0] == "/":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if i == 0:
                    raise Exception("POLIZ:divide by zero")
                else:
                    args.append(j / i)
            elif pc_el[0] == "=":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if key:
                    args.append(j == i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] == self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i == self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i == self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] == i)
                    else:
                        args.append(j == i)
                else:
                    args.append(j == i)
            elif pc_el[0] == "<":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if key:
                    args.append(j < i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] < self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i < self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i < self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] < i)
                    else:
                        args.append(j < i)
                else:
                    args.append(j < i)
            elif pc_el[0] == ">":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if key:
                    args.append(j > i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] > self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i > self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i > self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] > i)
                    else:
                        args.append(j > i)
                else:
                    args.append(j > i)
            elif pc_el[0] == "<=":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if key:
                    args.append(j <= i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] <= self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i <= self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i <= self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] > i)
                    else:
                        args.append(j <= i)
                else:
                    args.append(j <= i)
            elif pc_el[0] == ">=":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                if key:
                    args.append(j >= i)
                elif j in self.pars.dict and self.pars.dict[j][2] == "array":
                    ind_arr = i
                    # key = False
                    i = args[-1]
                    args.pop()
                    if args != []:
                        t = args[-1]
                        if t in self.pars.dict and self.pars.dict[t][2] == "array":
                            args.pop()
                            args.append(self.pars.dict[t][6][i - 1] >= self.pars.dict[j][6][ind_arr - 1])
                        else:
                            args.append(i >= self.pars.dict[j][6][ind_arr - 1])
                    else:
                        args.append(i >= self.pars.dict[j][6][ind_arr - 1])
                elif args != []:
                    t = args[-1]
                    if t in self.pars.dict and self.pars.dict[t][2] == "array":
                        args.pop()
                        # key = False
                        args.append(self.pars.dict[t][6][j - 1] >= i)
                    else:
                        args.append(j >= i)
                else:
                    args.append(j >= i)
            elif pc_el[0] == "-":
                i = args[-1]
                args.pop()
                j = args[-1]
                args.pop()
                args.append(j != i)
            elif pc_el[0] == "beg_ind_arr":
                key = True
            elif pc_el[0] == "end_ind_arr":
                key = False
            else:
                raise Exception("POLIZ: unexpected elem")
            index += 1