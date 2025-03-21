ND = 10
PERCENTILE = 0.95

def calc_percentile(x, p):
    x = sorted(x)
    p = 0.95
    n = len(x)
    k = int(n * p)
    return x[k]


def calc_segment(x, nd):
    # 在值域上，每 nd 长度为一个段
    x = sorted(x)
    st = (x[0] // nd) * nd

    ran = [(st, st + nd)]
    for elem in x:
        while elem >= st + nd:
            st += nd
            ran.append((st, st + nd))
    return ran


if __name__ == '__main__':

    # (1) 计算 EYE_HT-SITTING 的 95% 分位数
    x = []
    with open('EYE_HT-SITTING.in', 'r') as f:
        lines = f.readlines()
        for line in lines:
            x.append(int(line))
    print(calc_percentile(x, PERCENTILE))

    # (2) 按照 ND 对 FOOT_BRTH_LNTH 进行分段统计个数
    xy = []
    with open('FOOT_BRTH_LNTH.in', 'r') as f:
        lines = f.readlines()
        for line in lines:
            a = line.split()[0]
            b = line.split()[1]
            xy.append((int(a), int(b)))
            assert(line == f'{a}\t{b}\n')

    # 统计二维分布
    ran_x = calc_segment([elem[0] for elem in xy], ND // 2)
    ran_y = calc_segment([elem[1] for elem in xy], ND // 2)

    # 表头
    result = '\t'
    result += '\t'.join([
        f'{elem[0]}~{elem[1]}' if i != 0 and i != len(ran_x) - 1 else
        f'~{elem[1]}' if i == 0 else
        f'{elem[0]}~' for i, elem in enumerate(ran_x)
    ]) + '\tSum(%)\n'
    # 表内容
    for i, y in enumerate(ran_y):
        if i == 0:
            result += f'~{y[1]}\t'
        elif i == len(ran_y) - 1:
            result += f'{y[0]}~\t'
        else:
            result += f'{y[0]}~{y[1]}\t'
        sum = 0
        for x in ran_x:
            cnt = 0
            for elem in xy:
                if elem[0] >= x[0] and elem[0] < x[1] and elem[1] >= y[0] and elem[1] < y[1]:
                    cnt += 1
            sum += cnt
            result += "{:.2f}\t".format(cnt * 100 / len(xy))
        result += "{:.2f}\n".format(sum * 100 / len(xy))
    # 最后一行
    result += 'Sum(%)\t'
    for x in ran_x:
        cnt = 0
        for elem in xy:
            if elem[0] >= x[0] and elem[0] < x[1]:
                cnt += 1
        result += "{:.2f}\t".format(cnt * 100 / len(xy))
    result += "{:.2f}\n".format(100)

    with open('FOOT_BRTH_LNTH.out', 'w') as f:
        f.write(result)
