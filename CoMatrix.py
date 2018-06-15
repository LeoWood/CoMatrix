# -*- coding: utf-8 -*-
# @Time    : 2018-06-13 10:21:27
# @Author  : Liu Huan (liuhuan@mail.las.ac.cn)

import pandas as pd
import numpy as np


def authors_stat(co_authors_list):
    au_dict = {}  # 单个作者频次统计
    au_group = {}  # 两两作者合作
    for authors in co_authors_list:
        authors = authors.split(',')  # 按照逗号分开每个作者
        authors_co = authors  # 合作者同样构建一个样本
        for au in authors:
            # 统计单个作者出现的频次
            if au not in au_dict:
                au_dict[au] = 1
            else:
                au_dict[au] += 1
            # 统计合作的频次
            authors_co = authors_co[1:]  # 去掉当前作者
            for au_c in authors_co:
                if au > au_c:
                    au, au_c = au_c, au  # 保持两个作者名字顺序一致
                co_au = au+','+au_c  # 将两个作者合并起来，依然以逗号隔开
                if co_au not in au_group:
                    au_group[co_au] = 1
                else:
                    au_group[co_au] += 1
    return au_group, au_dict


def generate_matrix(au_group, matrix):
    for key, value in au_group.items():
        A = key.split(',')[0]
        B = key.split(',')[1]
        Fi = au_dict[A]
        Fj = au_dict[B]
        Eij = value*value/(Fi*Fj)
        # 按照作者进行索引，更新矩阵
        matrix.ix[A, B] = Eij
        matrix.ix[B, A] = Eij
    return matrix


if __name__ == '__main__':
    co_authors = 'a,b,n,g,d,y//v,b,d,a,s//a,n,d,b,s'
    co_authors_list = co_authors.split('//')
    au_group, au_dict = authors_stat(co_authors_list)
    print(au_group)
    print(au_dict)
    au_list = list(au_dict.keys())
    # 新建一个空矩阵
    matrix = pd.DataFrame(np.identity(len(au_list)), columns=au_list, index=au_list)
    print(matrix)
    matrix = generate_matrix(au_group, matrix)
    print(matrix)
