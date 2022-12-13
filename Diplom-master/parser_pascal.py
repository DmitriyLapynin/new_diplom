from scanner import Scanner


class Parser():
    mode = 1
    dict = {}
    buf = ""
    dict_func = {}
    st_lex = []
    one_sym = ''
    poliz = []
    poliz_proc = []
    all_poliz_proc = {}
    curr_name_func = ""
    param_proc = {}
    index_assign = 0
    index_assign_str = ""
    key = False
    key_proc = False


    def __init__(self, mode):
        self.mode = mode

    def gl(self, f, dict):
        s = Scanner()
        self.buf, self.dict, self.one_sym = s.get_lex(f, dict, self.one_sym)

    def gl_proc(self, f, dict_func):
        s = Scanner()
        self.buf, self.dict_func, self.one_sym = s.get_lex(f, dict_func, self.one_sym)

    def program(self, f):
        self.gl(f, self.dict)
        if self.buf == "program":
            pass
        else:
            raise Exception("Error: expect 'program'")
        self.gl(f, self.dict)
        if self.buf in self.dict:
            if self.dict[self.buf][0] == "ID":
                pass
            else:
                raise Exception("Error: expect name program")
        else:
            raise Exception("Error: expect name program")
        self.gl(f, self.dict)
        '''if self.buf == '(':
            pass
        else:
            raise Exception("Error: expect left bracket")
        self.gl(f, self.dict)
        while True:
            if self.buf in self.dict:
                if self.dict[self.buf][0] == "ID":
                    pass
                else:
                    raise Exception("Error: expect arg program")
            else:
                raise Exception("Error: expect arg program")
            self.gl(f, self.dict)
            if self.buf == ',':
                self.gl(f, self.dict)
            elif self.buf == ')':
                self.gl(f, self.dict)'''
        if self.buf == ';':
            return
        else:
            raise Exception("Error: expect semicolon")


    def block(self, f):
        if self.buf == "var":
            self.var(f)
        else:
            pass
        '''if self.buf == 'procedure':
            self.procedure(f)
            if self.buf == "var":
                self.var_pr(f)
            else:
                pass
            self.key_proc = True
            self.begin_proc(f)
        self.key_proc = False
        self.gl(f, self.dict)
        print(self.buf)
        self.begin(f)'''
        while self.buf != "begin":
            if self.buf == 'procedure':
                self.procedure(f)
                if self.buf == "var":
                    self.var_pr(f)
                else:
                    pass
                self.key_proc = True
                self.begin_proc(f)
            elif self.buf == 'function':
                self.function(f)
                if self.buf == "var":
                    self.var_pr(f)
                else:
                    pass
                self.key_proc = True
                self.begin_proc(f)
            else:
                raise Exception("expect procedure or begin")
            self.key_proc = False
            self.gl(f, self.dict)
            self.all_poliz_proc[self.curr_name_func] = self.poliz_proc
            self.poliz_proc = []
        print(self.all_poliz_proc, "asd")
        self.begin(f)
        if self.buf != ".":
            raise Exception("expect .")


    def begin_proc(self, f):
        self.gl_proc(f, self.dict_func)
        self.operators_proc(f)
        self.one_sym = ''
        while self.buf == ';':
            self.gl_proc(f, self.dict_func)
            if self.buf == 'end':
                if self.one_sym == ".":
                    raise Exception("error")
                else:
                    break
            self.operators_proc(f)
            if self.buf == 'end':
                break
            else:
                self.one_sym = ''
        if self.buf == 'end':
            self.gl_proc(f, self.dict_func)
        else:
            raise Exception("unexpected:", self.buf)

    def operators_proc(self, f):
        id_arr = ""
        '''if self.buf == "if":
            if self.mode == 1 or self.mode == 3:
                raise Exception("unexpected:", self.buf)
            else:
                self.condPascal(f)
        elif self.buf == "while":
            if self.mode == 1 or self.mode == 2:
                raise Exception("unexpected:", self.buf)
            else:
                self.whilePascal(f)
        elif self.buf == "repeat":
            if self.mode == 1 or self.mode == 2:
                raise Exception("unexpected:", self.buf)
            else:
                self.repeatPascal(f)
        elif self.buf == "for":
            if self.mode == 1 or self.mode == 2:
                raise Exception("unexpected:", self.buf)
            else:
                self.forPascal(f)
        elif self.buf == "read":
            self.readPascal(f)'''
        if self.buf == "write":
            self.writePascal_proc(f)
            print(self.poliz_proc)
        elif (self.buf in self.dict_func) and (self.dict_func[self.buf][0] == "ID"):
            self.checkID_proc()
            # self.poliz.append(("poliz_address", self.buf))
            self.poliz_proc.append(("poliz_address", self.buf))
            if self.dict_func[self.buf][2] == "array":
                id_arr = self.buf
                self.gl_proc(f, self.dict_func)
                if self.buf == '[':
                    self.poliz_proc.append(("beg_ind_arr", 0))
                    self.gl_proc(f, self.dict_func)
                    self.E(f)
                    if self.buf == ']':
                        self.poliz_proc.append(("end_ind_arr", 0))
                    else:
                        raise Exception("Error: expect \"]\" ")
                else:
                    raise Exception("Error: expect \"[\" ")
            return self.assignPascal_proc(f)
        else:
            self.begin_proc(f)

    def writePascal_proc(self, f):
        self.gl_proc(f, self.dict_func)
        if self.buf == '(':
            self.gl_proc(f, self.dict_func)
            self.E_proc(f)
            if self.buf == ')':
                self.gl_proc(f, self.dict_func)
                self.poliz_proc.append(("write", 0))
                return
            else:
                raise Exception("expected: )")
        else:
            raise Exception("expected: (")

    def assignPascal_proc(self, f):
        self.gl_proc(f, self.dict_func)
        if self.buf == ":=":
            self.gl_proc(f, self.dict_func)
            self.E_proc(f)
            self.eqType_proc()
            self.poliz_proc.append(("assign", 0))
        return

    def E_proc(self, f):
        self.E1_proc(f)
        if (self.buf == "=") or (self.buf == "<=") or (self.buf == ">=") or (self.buf == "<") or (self.buf == ">") or (
                self.buf == "!="):
            self.st_lex.append(self.buf)
            self.gl_proc(f, self.dict_func)
            self.E1_proc(f)
            self.checkOp_proc()

    def E1_proc(self, f):
        self.T_proc(f)
        if (self.buf == "+") or (self.buf == "-") or (self.buf == "or"):
            self.st_lex.append(self.buf)
            self.gl_proc(f, self.dict_func)
            self.T_proc(f)
            self.checkOp_proc()

    def T_proc(self, f):
        self.F_proc(f)
        if (self.buf == "*") or (self.buf == "/") or (self.buf == "and"):
            self.st_lex.append(self.buf)
            self.gl_proc(f, self.dict_func)
            self.F_proc(f)
            self.checkOp_proc()

    def F_proc(self, f):
        if (self.buf in self.dict_func) and (self.dict_func[self.buf][0] == "ID"):
            self.checkID_proc()
            self.poliz_proc.append(("ID", self.buf))
            if self.dict_func[self.buf][2] == "array":
                id_arr = self.buf
                self.key = True
                self.gl_proc(f, self.dict_func)
                if self.buf == '[':
                    self.poliz_proc.append(("beg_ind_arr", 0))
                    self.gl_proc(f, self.dict_func)
                    '''if str(self.buf).isdigit():
                        if int(self.buf) in range(self.dict[id_arr][4], self.dict[id_arr][5] + 1):
                            self.poliz[len(self.poliz) - 1] = ("ID", self.poliz[len(self.poliz) - 1][1], self.buf)
                        else:
                            raise Exception("Error: not in range of array")
                    elif (self.buf in self.dict) and (self.dict[self.buf][0] == "ID"):
                        self.poliz[len(self.poliz) - 1] = ("ID", self.poliz[len(self.poliz) - 1][1], self.buf)
                    else:
                        raise Exception("Error: expected ID or const")
                    # elif self.buf in self.dict:
                    self.gl(f, self.dict)'''
                    self.E_proc(f)
                    if self.buf == ']':
                        self.poliz_proc.append(("end_ind_arr", 0))
                        self.st_lex.pop()
                        self.st_lex.append("int")
                        print(self.st_lex, self.buf)
                    else:
                        raise Exception("Error: expect \"]\" ")
                else:
                    raise Exception("Error: expect \"[\" ")
            self.gl_proc(f, self.dict_func)
        elif (self.buf in self.dict_func) and (self.dict_func[self.buf][0] == "Const"):
            self.poliz_proc.append(("const", self.buf))
            self.gl_proc(f, self.dict_func)
        elif str(self.buf).isdigit():
            self.st_lex.append("int")
            self.poliz_proc.append(("int", self.buf))
            self.gl_proc(f, self.dict_func)
        elif self.buf == "true":
            self.st_lex.append("bool")
            self.poliz_proc.append(("bool", 1))
            self.gl_proc(f, self.dict_func)
        elif self.buf == "false":
            self.st_lex.append("bool")
            self.poliz_proc.append(("bool", 0))
            self.gl_proc(f, self.dict_func)
        elif self.buf == "not":
            self.gl_proc(f, self.dict_func)
            self.F_proc(f)
            self.checkNot_proc()
        elif self.buf == "(":
            self.gl_proc(f, self.dict_func)
            self.E_proc(f)
            if self.buf == ")":
                self.gl_proc(f, self.dict_func)
            else:
                raise Exception("expect \")\"")
        else:
            raise Exception("error")

    def checkNot_proc(self):
        if self.st_lex == [] or self.st_lex[-1] != "bool":
            raise Exception("error, wrong type")
        else:
            self.poliz_proc.append(("not", 0))

    def checkID_proc(self):
        if (self.buf in self.dict_func):
            if (self.dict_func[self.buf][0] == "ID") and (len(self.dict_func[self.buf]) > 2):
                if self.dict_func[self.buf][2] == "integer":
                    self.st_lex.append("int")
                elif self.dict_func[self.buf][2] == "array":
                    #   self.st_lex.append("int")
                    pass
                else:
                    self.st_lex.append("bool")
            elif (self.dict_func[self.buf][0] == "Const"):
                self.st_lex.append("const")
            else:
                raise Exception(self.buf + " not declared")
        else:
            raise Exception(self.buf + " not declared")

    def checkIDRead_proc(self):
        if (self.buf in self.dict_func) and (self.dict_func[self.buf][0] == "ID") and (len(self.dict_func[self.buf]) > 2):
            pass
        else:
            raise Exception(self.buf + " not declared")

    def checkOp_proc(self):
        t = "int"
        r = "bool"
        fst_arg = self.st_lex[-1]
        self.st_lex.pop()
        op = self.st_lex[-1]
        self.st_lex.pop()
        snd_arg = self.st_lex[-1]
        self.st_lex.pop()
        if op == "+" or op == "-" or op == "*" or op == "/":
            r = "int"
        if op == "and" or op == "or":
            t = "bool"
        if (fst_arg == snd_arg) and (fst_arg == t):
            self.st_lex.append(r)
        else:
            raise Exception("wrong types are in operation")
        self.poliz_proc.append((op, 0))
        return

    def eqType_proc(self):
        fst_arg = self.st_lex[-1]
        self.st_lex.pop()
        if fst_arg != self.st_lex[-1]:
            raise Exception("wrong types are in operation :=")
        self.st_lex.pop()

    def eqBool_proc(self):
        if self.st_lex[-1] != "bool":
            raise Exception("expression is not boolean")
        self.st_lex.pop()

    def function(self, f):
        list_proc = []
        arg = []
        self.gl_proc(f, self.dict_func)
        self.curr_name_func = self.buf
        list_proc.append(self.buf)
        self.gl_proc(f, self.dict_func)
        if self.buf == '(':
            self.gl_proc(f, self.dict_func)
            self.args_pr(f, arg)
            list_proc[-1] = ((list_proc[-1], arg))
            self.param_proc[list_proc[0][0]] = list_proc[0][1]
            # self.param_proc.append(list_proc[0])
            list_proc = []
            if self.buf == ')':
                self.gl_proc(f, self.dict_func)
                if self.buf == ':':
                    self.gl_proc(f, self.dict_func)
                    self.gl_proc(f, self.dict_func)
                    if self.buf == ';':
                        self.gl_proc(f, self.dict_func)
                        self.dict_func[self.curr_name_func] = ("ID", False, "integer")
                        self.param_proc[self.curr_name_func].append((self.curr_name_func, "ID", False, "integer"))
                        return
                    else:
                        raise Exception("Error: expect \";\" ")
                else:
                    raise Exception("Error: expect \":\" ")

    def procedure(self, f):
        list_proc = []
        arg = []
        self.gl_proc(f, self.dict_func)
        self.curr_name_func = self.buf
        list_proc.append(self.buf)
        self.gl_proc(f, self.dict_func)
        if self.buf == '(':
            self.gl_proc(f, self.dict_func)
            self.args_pr(f, arg)
            list_proc[-1] = ((list_proc[-1], arg))
            self.param_proc[list_proc[0][0]] = list_proc[0][1]
            # self.param_proc.append(list_proc[0])
            list_proc = []
            if self.buf == ')':
                self.gl_proc(f, self.dict_func)
                if self.buf == ';':
                    self.gl_proc(f, self.dict_func)
                    return
                else:
                    raise Exception("Error: expect \";\" ")

    def var_pr(self, f):
        tmp_var = []
        init_array = []
        first_ind = 0
        second_ind = 0
        self.gl_proc(f, self.dict_func)
        if self.buf == 'begin':
            return
        else:
            if self.buf in self.dict_func:
                if self.dict_func[self.buf][0] == "ID":
                    tmp_var.append(self.buf)
                else:
                    raise Exception("Error: error name of variable")
            else:
                raise Exception("Error: expect name of variable")
            self.gl_proc(f, self.dict_func)
            while self.buf == ',':
                self.gl_proc(f, self.dict_func)
                if self.buf in self.dict_func:
                    if self.dict_func[self.buf][0] == "ID":
                        tmp_var.append(self.buf)
                    else:
                        raise Exception("Error: expect name of variable")
                else:
                    raise Exception("Error: error name of variable")
                self.gl_proc(f, self.dict_func)
            if self.buf != ':':
                raise Exception("Error: expect \":\" ")
            else:
                self.gl_proc(f, self.dict_func)
                if (self.buf == "integer" or self.buf == "bool" or self.buf == "array"):
                    for i in tmp_var:
                        self.dict_func[i] = ("ID", False, self.buf)
                        self.param_proc[self.curr_name_func].append((i, "ID", False, self.buf))
                else:
                    raise Exception("Error: expect type of variables ")
                if self.buf == "array":
                    self.gl_proc(f, self.dict_func)
                    if self.buf == '[':
                        self.gl_proc(f, self.dict_func)
                        if str(self.buf).isdigit():
                            first_ind = int(self.buf)
                            self.gl_proc(f, self.dict_func)
                            if self.buf == '.':
                                self.gl_proc(f, self.dict_func)
                                if self.buf == '.':
                                    self.gl_proc(f, self.dict_func)
                                    if str(self.buf).isdigit():
                                        if first_ind <= int(self.buf):
                                            second_ind = int(self.buf)
                                            self.gl_proc(f, self.dict_func)
                                            if self.buf == ']':
                                                self.gl_proc(f, self.dict_func)
                                                if self.buf == "of":
                                                    self.gl_proc(f, self.dict_func)
                                                    if self.buf == "integer" or self.buf == "bool":
                                                        for i in range(first_ind, second_ind + 1):
                                                            init_array.append('no')
                                                        for i in tmp_var:
                                                            self.dict_func[i] = ("ID", False, "array", self.buf, first_ind, second_ind, init_array)
                                                            self.param_proc[self.curr_name_func].append((i, "ID", False, "array", self.buf, first_ind, second_ind, init_array))
                                                        init_array = []
                                                else:
                                                    raise Exception("Error: expect keyword of ")
                                            else:
                                                raise Exception("Error: expect \"]\" ")
                                        else:
                                            raise Exception("Error: expect const number less ")
                                    else:
                                        raise Exception("Error: expect const number ")

                                else:
                                    raise Exception("Error: expect \".\" ")
                            else:
                                raise Exception("Error: expect \".\" ")
                        else:
                            raise Exception("Error: expect const number ")
                    else:
                        raise Exception("Error: expect \"[\" ")
                self.gl_proc(f, self.dict_func)
                if self.buf == ';':
                    return self.var_pr(f)
                else:
                    raise Exception("Error: expect \";\" ")



    def args_pr(self, f, args_proc):
        key_var = False
        tmp_var = []
        init_array = []
        first_ind = 0
        second_ind = 0
        if self.buf == 'var':
            key_var = True
            self.gl_proc(f, self.dict_func)
        if self.buf in self.dict_func:
            if self.dict_func[self.buf][0] == "ID":
                tmp_var.append(self.buf)
            else:
                raise Exception("Error: error name of variable")
        else:
            raise Exception("Error: expect name of variable")
        self.gl_proc(f, self.dict_func)
        while self.buf == ',':
            self.gl_proc(f, self.dict_func)
            if self.buf in self.dict_func:
                if self.dict_func[self.buf][0] == "ID":
                    tmp_var.append(self.buf)
                else:
                    raise Exception("Error: expect name of variable")
            else:
                raise Exception("Error: error name of variable")
            self.gl_proc(f, self.dict_func)
        if self.buf != ':':
                raise Exception("Error: expect \":\" ")
        else:
            self.gl_proc(f, self.dict_func)
            if (self.buf == "integer" or self.buf == "bool" or self.buf == "array"):
                for i in tmp_var:
                    self.dict_func[i] = ("ID", False, self.buf)
                    args_proc.append((i, self.dict_func[i][0], self.dict_func[i][1], self.dict_func[i][2], key_var))
            else:
                raise Exception("Error: expect type of variables ")
            if self.buf == "array":
                self.gl_proc(f, self.dict_func)
                if self.buf == '[':
                    self.gl_proc(f, self.dict_func)
                    if str(self.buf).isdigit():
                        first_ind = int(self.buf)
                        self.gl_proc(f, self.dict_func)
                        if self.buf == '.':
                            self.gl_proc(f, self.dict_func)
                            if self.buf == '.':
                                self.gl_proc(f, self.dict_func)
                                if str(self.buf).isdigit():
                                    if first_ind <= int(self.buf):
                                        second_ind = int(self.buf)
                                        self.gl_proc(f, self.dict_func)
                                        if self.buf == ']':
                                            self.gl_proc(f, self.dict_func)
                                            if self.buf == "of":
                                                self.gl_proc(f, self.dict_func)
                                                if self.buf == "integer" or self.buf == "bool":
                                                    for i in range(first_ind, second_ind + 1):
                                                        init_array.append('no')
                                                    for i in tmp_var:
                                                        self.dict_func[i] = ("ID", False, "array", self.buf, first_ind, second_ind, init_array)
                                                        args_proc.append((i, key_var))
                                                        init_array = []
                                            else:
                                                raise Exception("Error: expect keyword of ")
                                        else:
                                            raise Exception("Error: expect \"]\" ")
                                    else:
                                        raise Exception("Error: expect const number less ")
                                else:
                                    raise Exception("Error: expect const number ")
                            else:
                                raise Exception("Error: expect \".\" ")
                        else:
                            raise Exception("Error: expect \".\" ")
                    else:
                        raise Exception("Error: expect const number ")
                else:
                    raise Exception("Error: expect \"[\" ")
            self.gl_proc(f, self.dict_func)
            if self.buf == ',':
                key_var = False
                self.gl_proc(f, self.dict_func)
                self.args_pr(f, args_proc)
            else:
                return args_proc


    def var(self, f):
        tmp_var = []
        init_array = []
        first_ind = 0
        second_ind = 0
        self.gl(f, self.dict)
        if self.buf == 'begin':
            return
        elif self.buf == 'procedure':
            return
        else:
            if self.buf in self.dict:
                if self.dict[self.buf][0] == "ID":
                    tmp_var.append(self.buf)
                else:
                    raise Exception("Error: error name of variable")
            else:
                raise Exception("Error: expect name of variable")
            self.gl(f, self.dict)
            while self.buf == ',':
                self.gl(f, self.dict)
                if self.buf in self.dict:
                    if self.dict[self.buf][0] == "ID":
                        tmp_var.append(self.buf)
                    else:
                        raise Exception("Error: expect name of variable")
                else:
                    raise Exception("Error: error name of variable")
                self.gl(f, self.dict)
            if self.buf != ':':
                raise Exception("Error: expect \":\" ")
            else:
                self.gl(f, self.dict)
                if (self.buf == "integer" or self.buf == "bool" or self.buf == "array"):
                    for i in tmp_var:
                        self.dict[i] = ("ID", False, self.buf)
                else:
                    raise Exception("Error: expect type of variables ")
                if self.buf == "array":
                    self.gl(f, self.dict)
                    if self.buf == '[':
                        self.gl(f, self.dict)
                        if str(self.buf).isdigit():
                            first_ind = int(self.buf)
                            self.gl(f, self.dict)
                            if self.buf == '.':
                                self.gl(f, self.dict)
                                if self.buf == '.':
                                    self.gl(f, self.dict)
                                    if str(self.buf).isdigit():
                                        if first_ind <= int(self.buf):
                                            second_ind = int(self.buf)
                                            self.gl(f, self.dict)
                                            if self.buf == ']':
                                                self.gl(f, self.dict)
                                                if self.buf == "of":
                                                    self.gl(f, self.dict)
                                                    if self.buf == "integer" or self.buf == "bool":
                                                        for i in range(first_ind, second_ind + 1):
                                                            init_array.append('no')
                                                        for i in tmp_var:
                                                            self.dict[i] = ("ID", False, "array", self.buf, first_ind, second_ind, init_array)
                                                        init_array = []
                                                else:
                                                    raise Exception("Error: expect keyword of ")
                                            else:
                                                raise Exception("Error: expect \"]\" ")
                                        else:
                                            raise Exception("Error: expect const number less ")
                                    else:
                                        raise Exception("Error: expect const number ")

                                else:
                                    raise Exception("Error: expect \".\" ")
                            else:
                                raise Exception("Error: expect \".\" ")
                        else:
                            raise Exception("Error: expect const number ")
                    else:
                        raise Exception("Error: expect \"[\" ")
                self.gl(f, self.dict)
                if self.buf == ';':
                    return self.var(f)
                else:
                    raise Exception("Error: expect \";\" ")

    def begin(self, f):
        self.gl(f, self.dict)
        self.operators(f)
        self.one_sym = ''
        while self.buf == ';':
            self.gl(f, self.dict)
            if self.buf == 'end':
                if self.one_sym == ".":
                    raise Exception("error")
                else:
                    break
            self.operators(f)
            if self.buf == 'end':
                break
            else:
                self.one_sym = ''
        if self.buf == 'end':
            self.gl(f, self.dict)
        else:
            raise Exception("unexpected:", self.buf)

    def operators(self, f):
        id_arr = ""
        if self.buf == "if":
            if self.mode == 1 or self.mode == 3:
                raise Exception("unexpected:", self.buf)
            else:
                self.condPascal(f)
        elif self.buf == "while":
            if self.mode == 1 or self.mode == 2:
                raise Exception("unexpected:", self.buf)
            else:
                self.whilePascal(f)
        elif self.buf == "repeat":
            if self.mode == 1 or self.mode == 2:
                raise Exception("unexpected:", self.buf)
            else:
                self.repeatPascal(f)
        elif self.buf == "for":
            if self.mode == 1 or self.mode == 2:
                raise Exception("unexpected:", self.buf)
            else:
                self.forPascal(f)
        elif self.buf == "read":
            self.readPascal(f)
        elif self.buf == "write":
            self.writePascal(f)
        elif self.buf in self.all_poliz_proc:
            self.add_poliz_proc(f, self.buf)
        elif (self.buf in self.dict) and (self.dict[self.buf][0] == "ID"):
            self.checkID()
            self.poliz.append(("poliz_address", self.buf))
            if self.dict[self.buf][2] == "array":
                id_arr = self.buf
                self.gl(f, self.dict)
                if self.buf == '[':
                    self.poliz.append(("beg_ind_arr", 0))
                    self.gl(f, self.dict)
                    '''if str(self.buf).isdigit():
                        if int(self.buf) in range(self.dict[id_arr][4], self.dict[id_arr][5] + 1):
                            self.index_assign = self.buf
                            self.poliz[len(self.poliz) - 1] = ("poliz_address", self.poliz[len(self.poliz) - 1][1], self.buf)
                        else:
                            raise Exception("Error: not in range of array")
                    elif (self.buf in self.dict) and (self.dict[self.buf][0] == "ID"):
                        self.index_assign_str = self.buf

                        self.poliz[len(self.poliz) - 1] = ("poliz_address", self.poliz[len(self.poliz) - 1][1], self.buf)
                    else:
                        raise Exception("Error: expected ID or const")
                    self.gl(f, self.dict)'''
                    self.E(f)
                    if self.buf == ']':
                        self.poliz.append(("end_ind_arr", 0))
                    else:
                        raise Exception("Error: expect \"]\" ")
                else:
                    raise Exception("Error: expect \"[\" ")

            return self.assignPascal(f)
        else:
            self.begin(f)

    def add_poliz_proc(self, f, name_proc):
        self.gl(f, self.dict)
        if self.buf == '(':
            self.gl(f, self.dict)
            self.poliz.append(("begin_args", 0))
            self.poliz.append(("name_proc", name_proc))
            self.E(f)
            self.poliz.append(("assign_args", 0))
            while self.buf == ',':
                self.gl(f, self.dict)
                self.E(f)
                self.poliz.append(("assign_args", 0))
            if self.buf == ')':
                self.poliz.append(("end_args", 0))
                self.gl(f, self.dict)
            else:
                raise Exception("expect \")\"")
        else:
            raise Exception("expect \"(\"")


    def forPascal(self, f):
        self.gl(f, self.dict)
        if (self.buf in self.dict) and (self.dict[self.buf][0] == "ID"):
            self.dict[self.buf] = ("ID", False, "integer")
            tmp = self.buf
            self.checkID()
            self.poliz.append(("poliz_address", self.buf))
            self.assignPascal(f)
            pl0 = len(self.poliz)
            self.poliz.append(("ID", tmp))
        else:
            raise Exception("expect ident")
        if self.buf == "to":
            self.gl(f, self.dict)
            self.poliz.append(("int", self.buf))
            self.poliz.append(("<", 0))
            pl1 = len(self.poliz)
            self.poliz.append(("null", 0))
            self.poliz.append(("poliz_fgo", 0))
            self.gl(f, self.dict)
            if self.buf == "do":
                self.gl(f, self.dict)
                self.operators(f)
                self.poliz.append(("poliz_address", tmp))
                self.poliz.append(("ID", tmp))
                self.poliz.append(("int", 1))
                self.poliz.append(("+", 0))
                self.poliz.append(("assign", 0))
                self.poliz.append(("poliz_label", pl0))
                self.poliz.append(("poliz_go", 0))
                self.poliz[pl1] = ("poliz_label", len(self.poliz))
            else:
                raise Exception("expect do")
        else:
            raise Exception("expect to")



    def repeatPascal(self, f):
        pl0 = len(self.poliz)
        self.gl(f, self.dict)
        self.operators(f)
        if self.buf == ";":
            self.gl(f, self.dict)
        if self.buf == "until":
            self.gl(f, self.dict)
            self.E(f)
            self.checkNot()
            self.eqBool()
            pl1 = len(self.poliz)
            self.poliz.append(("null", 0))
            self.poliz.append(("poliz_fgo", 0))
            self.poliz.append(("poliz_label", pl0))
            self.poliz.append(("poliz_go", 0))
            self.poliz[pl1] = (("poliz_label", len(self.poliz)))
        else:
            raise Exception("expect until")


    def whilePascal(self, f):
        pl0 = len(self.poliz)
        self.gl(f, self.dict)
        self.E(f)
        self.eqBool()
        pl1 = len(self.poliz)
        self.poliz.append(("null", 0))
        self.poliz.append(("poliz_fgo", 0))
        if self.buf == "do":
            self.gl(f, self.dict)
            self.operators(f)
            self.poliz.append(("poliz_label", pl0))
            self.poliz.append(("poliz_go", 0))
            self.poliz[pl1] = ("poliz_label", len(self.poliz))
        else:
            raise Exception("expect do")

    def condPascal(self, f):
        self.gl(f, self.dict)
        self.E(f)
        self.eqBool()
        pl2 = len(self.poliz)
        self.poliz.append(("null", 0))
        self.poliz.append(("poliz_fgo", 0))
        if self.buf == "then":
            self.gl(f, self.dict)
            self.operators(f)
            pl3 = len(self.poliz)
            self.poliz.append(("null", 0))
            self.poliz.append(("poliz_go", 0))
            self.poliz[pl2] = (("poliz_label", len(self.poliz)))
            if self.buf == "else":
                self.gl(f, self.dict)
                self.operators(f)
                self.poliz[pl3] = (("poliz_label", len(self.poliz)))
            else:
                raise Exception("expected else")
        else:
            raise Exception("expected then")



    def assignPascal(self, f):
        self.gl(f, self.dict)
        if self.buf == ":=":
            self.gl(f, self.dict)
            self.E(f)
            self.eqType()
            self.poliz.append(("assign", 0))
            '''if self.index_assign_str != "":
                self.poliz.append(("assign", 0, self.index_assign_str))
            else:
                self.poliz.append(("assign", 0, self.index_assign))
            self.index_assign = 0
            self.index_assign_str = ""'''
        return

    def E(self, f):
        self.E1(f)
        if (self.buf == "=") or (self.buf == "<=") or (self.buf == ">=") or (self.buf == "<") or (self.buf == ">") or (self.buf == "!="):
            self.st_lex.append(self.buf)
            self.gl(f, self.dict)
            self.E1(f)
            self.checkOp()

    def E1(self, f):
        self.T(f)
        if (self.buf == "+") or (self.buf == "-") or (self.buf == "or"):
            self.st_lex.append(self.buf)
            self.gl(f, self.dict)
            self.T(f)
            self.checkOp()

    def T(self, f):
        self.F(f)
        if (self.buf == "*") or (self.buf == "/") or (self.buf == "and"):
            self.st_lex.append(self.buf)
            self.gl(f, self.dict)
            self.F(f)
            self.checkOp()

    def F(self, f):
        if (self.buf in self.dict) and (self.dict[self.buf][0] == "ID"):
            self.checkID()
            self.poliz.append(("ID", self.buf))
            if self.dict[self.buf][2] == "array":
                id_arr = self.buf
                self.key = True
                self.gl(f, self.dict)
                if self.buf == '[':
                    self.poliz.append(("beg_ind_arr", 0))
                    self.gl(f, self.dict)
                    '''if str(self.buf).isdigit():
                        if int(self.buf) in range(self.dict[id_arr][4], self.dict[id_arr][5] + 1):
                            self.poliz[len(self.poliz) - 1] = ("ID", self.poliz[len(self.poliz) - 1][1], self.buf)
                        else:
                            raise Exception("Error: not in range of array")
                    elif (self.buf in self.dict) and (self.dict[self.buf][0] == "ID"):
                        self.poliz[len(self.poliz) - 1] = ("ID", self.poliz[len(self.poliz) - 1][1], self.buf)
                    else:
                        raise Exception("Error: expected ID or const")
                    # elif self.buf in self.dict:
                    self.gl(f, self.dict)'''
                    self.E(f)
                    if self.buf == ']':
                        self.poliz.append(("end_ind_arr", 0))
                        self.st_lex.pop()
                        self.st_lex.append("int")
                        print(self.st_lex, self.buf)
                    else:
                        raise Exception("Error: expect \"]\" ")
                else:
                    raise Exception("Error: expect \"[\" ")
            self.gl(f, self.dict)
        elif (self.buf in self.dict) and (self.dict[self.buf][0] == "Const"):
            self.poliz.append(("const", self.buf))
            self.gl(f, self.dict)
        elif str(self.buf).isdigit():
            self.st_lex.append("int")
            self.poliz.append(("int", self.buf))
            self.gl(f, self.dict)
        elif self.buf == "true":
            self.st_lex.append("bool")
            self.poliz.append(("bool", 1))
            self.gl(f, self.dict)
        elif self.buf == "false":
            self.st_lex.append("bool")
            self.poliz.append(("bool", 0))
            self.gl(f, self.dict)
        elif self.buf == "not":
            self.gl(f, self.dict)
            self.F(f)
            self.checkNot()
        elif self.buf == "(":
            self.gl(f, self.dict)
            self.E(f)
            if self.buf == ")":
                self.gl(f, self.dict)
            else:
                raise Exception("expect \")\"")
        else:
            raise Exception("error")

    def checkNot(self):
        if self.st_lex == [] or self.st_lex[-1] != "bool":
            raise Exception("error, wrong type")
        else:
            self.poliz.append(("not", 0))

    def checkID(self):
        if (self.buf in self.dict):
            if (self.dict[self.buf][0] == "ID") and (len(self.dict[self.buf]) > 2):
                if self.dict[self.buf][2] == "integer":
                    self.st_lex.append("int")
                elif self.dict[self.buf][2] == "array":
                #   self.st_lex.append("int")
                    pass
                else:
                    self.st_lex.append("bool")
            elif (self.dict[self.buf][0] == "Const"):
                self.st_lex.append("const")
            else:
                raise Exception(self.buf + " not declared")
        else:
            raise Exception(self.buf + " not declared")

    def checkIDRead(self):
        if (self.buf in self.dict) and (self.dict[self.buf][0] == "ID") and (len(self.dict[self.buf]) > 2):
            pass
        else:
            raise Exception(self.buf + " not declared")

    def checkOp(self):
        t = "int"
        r = "bool"
        fst_arg = self.st_lex[-1]
        self.st_lex.pop()
        op = self.st_lex[-1]
        self.st_lex.pop()
        snd_arg = self.st_lex[-1]
        self.st_lex.pop()
        if op == "+" or op == "-" or op == "*" or op == "/":
            r = "int"
        if op == "and" or op == "or":
            t = "bool"
        if (fst_arg == snd_arg) and (fst_arg == t):
            self.st_lex.append(r)
        else:
            raise Exception("wrong types are in operation")
        self.poliz.append((op, 0))
        return

    def eqType(self):
        fst_arg = self.st_lex[-1]
        self.st_lex.pop()
        if fst_arg != self.st_lex[-1]:
            raise Exception("wrong types are in operation :=")
        self.st_lex.pop()

    def eqBool(self):
        if self.st_lex[-1] != "bool":
            raise Exception("expression is not boolean")
        self.st_lex.pop()



    def readPascal(self, f):
        self.gl(f, self.dict)
        if self.buf == '(':
            self.gl(f, self.dict)
            if self.buf in self.dict:
                if self.dict[self.buf][0] == "ID":
                    self.checkIDRead()
                    self.poliz.append(("poliz_address", self.buf))
                else:
                    raise Exception("Error: error name of variable")
            else:
                raise Exception("Error: error name of variable")
        if self.dict[self.buf][2] == "array":
            id_arr = self.buf
            self.gl(f, self.dict)
            if self.buf == '[':
                self.poliz.append(("beg_ind_arr", 0))
                self.gl(f, self.dict)
                '''if str(self.buf).isdigit():
                    if int(self.buf) in range(self.dict[id_arr][4], self.dict[id_arr][5] + 1):
                        self.poliz[len(self.poliz) - 1] = ("poliz_address", self.poliz[len(self.poliz) - 1][1], self.buf)
                    else:
                        raise Exception("Error: not in range of array")
                elif (self.buf in self.dict) and (self.dict[self.buf][0] == "ID"):
                    self.poliz[len(self.poliz) - 1] = ("poliz_address", self.poliz[len(self.poliz) - 1][1], self.buf)
                else:
                    raise Exception("Error: expected ID or const")
                # elif self.buf in self.dict:
                self.gl(f, self.dict)'''
                self.E(f)
                '''print(self.index_assign_str)
                print(self.index_assign)
                if self.index_assign_str != "":
                    self.poliz.append(("assign", 0, self.index_assign_str))
                else:
                    self.poliz.append(("assign", 0, self.index_assign))
                self.index_assign = 0
                self.index_assign_str = ""'''
                if self.buf == ']':
                    self.poliz.append(("end_ind_arr", 0))
                else:
                    raise Exception("Error: expect \"]\" ")
            else:
                raise Exception("Error: expect \"[\" ")
        self.gl(f, self.dict)
        if self.buf == ')':
            self.gl(f, self.dict)
            self.poliz.append(("read", 0))
            return
        else:
            raise Exception("expected: )")

    def writePascal(self, f):
        self.gl(f, self.dict)
        if self.buf == '(':
            self.gl(f, self.dict)
            self.E(f)
            if self.buf == ')':
                self.gl(f, self.dict)
                self.poliz.append(("write", 0))
                return
            else:
                raise Exception("expected: )")
        else:
            raise Exception("expected: (")

    def analyze(self, f):
        p = Parser(self.mode)
        p.program(f)
        p.gl(f, self.dict)
        p.block(f)
        print(p.dict, "qqq")
        print(p.dict_func, "aaa")
        print(p.poliz)
        print(p.param_proc)