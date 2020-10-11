# -*- coding:utf-8 -*-
import math

def normal_p(x):    ## Φ 概率密度函数
    return math.exp(float(-(x**2.0)/2.0)) * (1.0 / math.sqrt(2.0*math.pi))

def normal(x):      ## Φ 函数实现   计算精度设置：Δx为0.0001，4KB的样本计算时间约为20min
    y = 0.000000
    if x > 0.0:     ## 当 x 位于 y 轴右侧的概率计算
        while True:
            a = normal_p(x)
            x -= 0.0001
            b = normal_p(x)
            y += ( a + b ) * 0.0001 / 2
            if x < 0.0:
                break
        y += 0.500000
        return y
    elif x < 0.0:   ## 当 x 位于 y 轴左侧的概率计算
        while True:
            a = normal_p(x)
            x += 0.0001
            b = normal_p(x)
            y += ( a + b ) * 0.0001 / 2
            if x > 0.0:
                break
        y = 0.500000 - y
        return y
    else:
        return 0.500000
            
def P_value(n,z):
    n = n
    sum1 = 0.0
    k = float((1.0-float(n/z))/4.0)                          #计算前一个求和公式中内容的结果
    while k <= float((float(n/z)-1.0)/4):
        sum1 += normal(float(((4.0*k+1.0)*z)/math.sqrt(n)))
        sum1 -= normal(float(((4.0*k-1.0)*z)/math.sqrt(n)))
        k += 1.0

    sum2 = 0.0
    k = float((-3.0-float(n/z))/4.0)                         #计算后一个求和公式中内容的结果
    while k <= float((float(n/z)-1.0)/4):
        sum2 += normal(float(((4.0*k+3.0)*z)/math.sqrt(n)))
        sum2 -= normal(float(((4.0*k+1.0)*z)/math.sqrt(n)))
        k += 1.0

    p_value = float(1.0 - sum1 + sum2)
    return (p_value)

filename = input("请输入待测文本文件名：")
mode = input("请输入 mode ：")
io = open(filename,'r').read()
n = len(io)*4
flag = bin(int(io[0],16))
flag_len = 6-len(flag)
m = bin(int(io,16)).replace(flag,'0'*flag_len+flag[2:])

X = []
for i in m:
    X.append(int(i)*2-1)           # 将二元序列标准化

S = [i for i in range(n)]
if mode == '0':                    # 根据 mode 值进行 重叠递增子序列的随机游走的计算
    for i in range(n):
        if i == 0:
            S[i] = X[i]
            continue
        S[i] = S[i-1] + X[i]
elif mode == '1':
    for i in range(n):
        if i == 0:
            S[i] = X[n-1]
            continue
        S[i] = S[i-1] + X[n-i-1]
else:
    print("mode必须为 1 或 0")

S_abs = []
for i in S:
    S_abs.append(abs(i))
Z = max(S)                        #取 S 的最大绝对值为统计量观察值 Zobs

pvalue = P_value(n,Z)             # 计算P-value
print("P-value: %f" %pvalue)

'''
假设显著性水平 α = 0.01，若 P-value < 0.01，则认为测试序列非随机；反之，
则认为测试序列随机。 
注意，如果 P-value 非常小，意味着 z 非常大。若 mode = 0，则说明在序列开
始阶段聚集了大量“0”或“1”；若 mode = 1，则说明在序列结束阶段聚集了大量
“0”或“1”。 
'''