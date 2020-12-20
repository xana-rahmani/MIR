import math


Train = {
    1: [[("Chinese", 2), ("Beijing", 1)], 1],
    2: [[("Chinese", 2), ("Shanghai", 1)], 1],
    3: [[("Chinese", 1), ("Macao", 1)], 1],
    4: [[("Chinese", 1), ("Tokyo", 1), ("Japan", 1)], -1],
}

Test1 = ["Chinese", "Chinese", "Chinese", "Tokyo", "Japan"]
Test2 = ["Chinese", "Tokyo", "Japan", "Tokyo", "Tokyo"]
Test3 = ["Chinese", "Iran", "Japan", "Tokyo", "Tokyo"]


# Global Naive Bayes Variable
NaiveBayes___Pt1 = {}  # P(t|view = +1)
NaiveBayes___Pt0 = {}  # P(t|view = -1)
NaiveBayes___P_c1 = 0  # probability of view = +1
NaiveBayes___P_c0 = 0  # probability of view = -1


def Train___NaiveBayes(train):
    global NaiveBayes___Pt1
    global NaiveBayes___Pt0
    global NaiveBayes___P_c1
    global NaiveBayes___P_c0

    B = 0          # B = |V|  >>  |V| is number of unique tokens in all docs
    T_ctp1 = 0     # number of token in doc with view +1
    T_ctp0 = 0     # number of token in doc with view -1
    NumToken1 = {} # dictionary of tokens and numbers in class view = +1
    NumToken0 = {} # dictionary of tokens and numbers in class view = -1

    Nc1 = 0  # number of docs in class view = +1
    Nc0 = 0  # number of docs in class view = -1
    N = 0    # number of all docs
    Tokens = set()
    for doc_id, value in train.items():
        N += 1
        if value[1] == 1:
            Nc1 += 1
        else:
            Nc0 += 1

        for (token, num_token) in value[0]:
            if value[1] == 1:
                T_ctp1 += num_token
                if NumToken1.get(token, None) is None:
                    NumToken1[token] = num_token
                else:
                    NumToken1[token] += num_token
            else:
                T_ctp0 += num_token
                if NumToken0.get(token, None) is None:
                    NumToken0[token] = num_token
                else:
                    NumToken0[token] += num_token
            Tokens.add(token)

    NaiveBayes___P_c1 = Nc1 / N  # P(c ) = Nc  / N
    NaiveBayes___P_c0 = Nc0 / N  # P(c') = Nc' / N
    B = len(Tokens)

    for t in Tokens:
        p_tc1 = (NumToken1.get(t, 0) + 1) / (T_ctp1 + B)
        p_tc0 = (NumToken0.get(t, 0) + 1) / (T_ctp0 + B)

        NaiveBayes___Pt1[t] = p_tc1
        NaiveBayes___Pt0[t] = p_tc0


def Test____NaiveBayes(test):
    global NaiveBayes___Pt1
    global NaiveBayes___Pt0
    global NaiveBayes___P_c1
    global NaiveBayes___P_c0

    temp1 = 0
    temp0 = 0
    for t in test:
        temp1 += math.log(NaiveBayes___Pt1.get(t, 1))
        temp0 += math.log(NaiveBayes___Pt0.get(t, 1))

    P_ct1 = temp1 + math.log(NaiveBayes___P_c1)
    P_ct0 = temp0 + math.log(NaiveBayes___P_c0)

    if P_ct1 > P_ct0:
        return +1
    else:
        return -1


# Train
Train___NaiveBayes(Train)

# Test
print(Test____NaiveBayes(Test1))
print(Test____NaiveBayes(Test2))
print(Test____NaiveBayes(Test3))
