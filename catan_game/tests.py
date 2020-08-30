# # from django.test import TestCase
# #
# # # Create your tests here.
# vertex = [None for i in range(0, 55)]
#
# vertex[1] = [1]
# vertex[2] = [2]
# vertex[3] = [3]
# vertex[4] = [1]
# vertex[5] = [1, 2]
# vertex[6] = [2, 3]
# vertex[7] = [3]
# vertex[8] = [1, 4]
# vertex[9] = [1, 2, 5]
# vertex[10] = [2, 3, 6]
# vertex[11] = [3, 7]
# vertex[12] = [4]
# vertex[13] = [1, 4, 5]
# vertex[14] = [2, 5, 6]
# vertex[15] = [3, 6, 7]
# vertex[16] = [7]
# vertex[17] = [4, 8]
# vertex[18] = [4, 5, 9]
# vertex[19] = [5, 6, 10]
# vertex[20] = [6, 7, 11]
# vertex[21] = [7, 12]
# vertex[22] = [8]
# vertex[23] = [4, 8, 9]
# vertex[24] = [5, 9, 10]
# vertex[25] = [6, 10, 11]
# vertex[26] = [7, 11, 12]
# vertex[27] = [12]
# vertex[28] = [8]
# vertex[29] = [8, 9, 13]
# vertex[30] = [9, 10, 14]
# vertex[31] = [10, 11, 15]
# vertex[32] = [11, 12, 16]
# vertex[33] = [12]
# vertex[34] = [8, 13]
# vertex[35] = [9, 13, 14]
# vertex[36] = [10, 14, 15]
# vertex[37] = [11, 15, 16]
# vertex[38] = [12, 16]
# vertex[39] = [13]
# vertex[40] = [13, 14, 17]
# vertex[41] = [14, 15, 18]
# vertex[42] = [15, 16, 19]
# vertex[43] = [16]
# vertex[44] = [13, 17]
# vertex[45] = [14, 17, 18]
# vertex[46] = [15, 18, 19]
# vertex[47] = [16, 19]
# vertex[48] = [17]
# vertex[49] = [17, 18]
# vertex[50] = [18, 19]
# vertex[51] = [19]
# vertex[52] = [17]
# vertex[53] = [18]
# vertex[54] = [19]
#
# for j in range(1, 20):
#     l = []
#     for index, ver in enumerate(vertex):
#         try:
#             if j in ver:
#                 l.append(index)
#         except:
#             pass
#     print("tile[{}]={}".format(j,l))
# import random
#
# # def shuffle_numbers():
# #     t1 = [2, 4, 5]
# #     t2 = [1, 3, 5, 6]
# #     t3 = [2, 6, 7]
# #     t4 = [1, 5, 8, 9]
# #     t5 = [1, 2, 4, 6, 9, 10]
# #     t6 = [2, 3, 5, 7, 10, 11]
# #     t7 = [3, 6, 11, 12]
# #     t8 = [4, 9, 13]
# #     t9 = [4, 5, 8, 10, 13, 14]
# #     t10 = [5, 6, 9, 11, 14, 15]
# #     t11 = [6, 7, 10, 12, 15, 16]
# #     t12 = [7, 11, 16]
# #     t13 = [8, 9, 14, 17]
# #     t14 = [9, 10, 13, 15, 17, 18]
# #     t15 = [10, 11, 14, 16, 18, 19]
# #     t16 = [11, 12, 15, 19]
# #     t17 = [13, 14, 18]
# #     t18 = [14, 15, 17, 19]
# #     t19 = [15, 16, 18]
# #     tiles = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19]
# #     result = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12, 7]
# #
# #     for i in range(0, 5):
# #
# #         flag = False
# #         random.shuffle(result)
# #         indexes = [i for i, x in enumerate(result) if x in [6, 8]]
# #         print(result)
# #         for index in indexes:
# #             if len([x for x in tiles[index] if x in indexes]) != 0:
# #                 flag = True
# #                 break
# #
# #         if not flag:
# #             return result
# #     return [10, 2, 9, 12, 6, 14, 10, 9, 11, 7, 3, 8, 8, 3, 4, 5, 5, 6, 11]
# #
# #
# # if __name__ == '__main__':
# #     print(shuffle_numbers())


import random

for i in range(100):
    print(random.randint(1,6))