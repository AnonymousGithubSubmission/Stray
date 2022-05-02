from random import choice, choices

import ast
from klara.core.cfg import Cfg
from klara.core.tree_rewriter import AstBuilder
from textwrap import dedent
from collections import deque
# as_tree = AstBuilder().string_build(
#             dedent(
#                 """\
#             a = 1
#             y = 2
#             z = a + y"""
#             )
#         )

# cfg = Cfg(as_tree)
# cfg.root.nxt_block_list[0].enumerate()
# expected_ssa_dict = {"z": deque([0]), "a": deque([0]), "y": deque([0])}
# real_ssa_dict = as_tree.ssa_record.var_version_list
# assert real_ssa_dict == expected_ssa_dict
builtins = ['int', 'float','bool','str', 'byte', 'callable', 'none', 'object']
third = ['ndarray', 'tensor', 'namespace', 'vocabulary', 'textfieldembedder', 'jsondict', 'instance', 'socket', 'token']


projects = ['seagull','tinychain','relex','htmlark', 'pendulum'][-1:]
returnses = [
[3,5,8,10,12,14,16,18,20,22,24,26,31,35,37,39,40,41,43,47,48,49,50,51,52,53,55,56,57,58,59,60,61,64,65,66,67,68,69],
[3,6,9,10,12,15,18,19,21,22,28,31,34,36,39,40,42,47,51,53,55,57,59,62,64,66,68,70,72,77,80,81,83,85,88,91,94,97,100,103],
[10, 17, 20, 23, 26, 28, 33, 36, 38, 40, 47, 49, 51],
[2, 4, 7, 15, 16], 
[2,5,8,10,12,14,16,20,21,22,23,24,25,27,29,31,34,36,37,40,43,44,47,50,51,54,59,60,61,62,65,72,73,74,75,76,77,78,81,83,86,88,90,92,94,97,98,99,101,105,107,109,113,117,120,124,125,126,127,128,129,130,131,133,135,136,138,139,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,165,166,167,169,171,172,173,175,177,179,181,183,188,193,195,197,198,199,201,203,204,206,208,212,213,214,215,220,222,224,226,229,231,233,236,239,242,245,249,251,254,257,258,261,264,269,274,276,278,280,282,284,287,291,297,298,300,301,303,307,308,309,310,311,312,313,314,315,316,317,318,319,320,323,326,327,328,330,332,334,335,337,339,341,343,345,346,347,348,350,352,353,355,356,358,367,368,369,370,371,372,373,374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 387, 392, 394, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 413, 414, 415, 419, 423, 424, 425, 426, 428, 430, 432, 434, 437, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 462, 465, 467, 469, 472, 474, 476, 479, 481, 483, 486, 488, 490, 492, 494, 496, 499, 501, 503, 506, 508, 509, 511, 512, 514, 517, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 534, 537, 538, 539, 540, 541, 543, 545, 550, 555, 557, 559, 561, 563, 566, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 584, 586, 588, 590, 593, 595, 597, 600, 602, 604, 607, 609, 613, 616, 617, 620, 628, 631, 633, 636, 638, 640, 642, 644, 645, 646, 649, 650, 652, 654, 656, 658, 660, 661, 663, 664, 665, 666, 667, 669, 671, 674, 676, 679, 680, 682, 683, 685, 689, 691, 694, 697, 700, 703, 707, 709, 712, 715, 717, 727, 735, 743, 747, 752, 754, 756, 758, 760, 763, 773]
][-1:]


# with open('rerrr', 'w+') as f:
#     returnses[-1] = [x-1 for x in returnses[-1]]
#     f.write(str(returnses[-1])) 
model = 'pytype'
lower = True
all_precisions = 0
all_recalls = 0
all_f1s = 0
all_cnt = 0
no_match_ground = []
def pure(typ):
    typ = typ.replace('*','').replace('?','')
    if typ.startswith('optional[') and typ.endswith(']'):
        typ = typ[9:-1]
    # if typ.startswith('Optional[') and typ.endswith(']'):
    #     typ = typ[9:-1]
    
    return typ
for i, project in enumerate(projects):
    if i == 4:
        lower = False
    print(project)
    print('----------------------')
    ground_truth = []
    returns = returnses[i]
    with open(f'evaluation/GT_{project}.txt') as f:
        
        for i, line in enumerate(f):
            if i == 0:
                continue
            if lower:
                line = line.lower()
            ground_truth.append(line.strip().split('/'))
    PIG = []
    with open(f'evaluation/{model}_{project}.txt') as f:
        
        for i, line in enumerate(f):
            if i == 0:
                continue
            if lower:
                line = line.lower()
            qualifier_names = line.strip().split('/')
            PIG.append([pure(x.split('.')[-1]) for x in qualifier_names])
    precisions = 0
    recalls = 0
    f1s = 0
    cnt = 0

    def remove_nan(p):
        return [x for x in p if x  != 'nan']
    def remove_none(p):
        return [x for x in p if x  != 'none']
    
    ds = ['list','set','tuple','dict']
    def same_ds(x, g):

        # if x == 'object':
        #     return True
        # for d in ds:
        #     if x.find(d) != -1:
        #         for g_ in g:
        #             if g_.find(d) != -1:
        #                 return True

        return False
    def same_type(x, g):
        if x in g:
            return True
        if x.find('literal') != -1:
            if 'int' in g:
                return True
            if 'str' in g:
                return True
        if 'any' in g:
            return True
        if 'bool' in g and ('float' == x or 'int' == x or 'object' == x):
            return True
        # if 'int' in g and ('float' == x):
        #     return True
        # if 'float' in g and ('int' == x):
        #     return True
        
        # if x == 'object':
        #     return True
        # for d in ds:
        #     if x.find(d) != -1:
        #         for g_ in g:
        #             if g_.find(d) != -1:
        #                 return True

        return False

    def is_builtin(g):
        for g_ in g:
            if any(g_.find(x) != -1 for x in builtins):
                return True
        return False
    def is_third(g):
        for g_ in g:
            if any(g_.find(x) != -1 for x in third):
                return True
        return False
    c = 0
    for i, p in enumerate(PIG):
        p = remove_none(p)
        p = remove_nan(p)
        
        # p = p[:1]
        if i + 2 in returns:
            
            g = ground_truth[i]
            if 'none' in g:
                continue
            if len(g) == 1 and g[0]=='':
                continue
            # if is_builtin(g):
            #     continue
            # elif is_third(g):
            #     continue
            # else:
            #     pass
            
            if len(p) > 0 and p[0] != '' or True:
                
                cnt += 1
                hit_accuracy = sum([same_type(x, g) or same_ds(x, g) for x in p])
                hit_recall = sum([same_type(x, p) or same_ds(x, p) for x in g])
                # with open('xxx', 'a+') as f:

                #     f.write(str(i) + ' ' + str(hit_accuracy)+'\n')
                if not hit_accuracy and p[0]!='any':
                    # print(i)
                    no_match_ground.append((project, i, p ,g))
                    c +=1
                precision = hit_accuracy/len(p)
                recall = hit_recall/len(g)
                if precision + recall == 0:
                    f1 = 0
                else:
                    f1 = (2*precision*recall)/(precision + recall)
                precisions += precision
                recalls += recall
                f1s += f1
    if cnt == 0:
        print(0)
        print(0)
        print(0)
        print(cnt)    
    else:
        print(precisions/cnt)
        print(recalls/cnt)
        print(f1s/cnt)
        print(cnt)
    all_precisions += precisions
    all_recalls += recalls
    all_f1s += f1s
    all_cnt += cnt


with open('evaluation/examined_arg', 'w+') as f:
    # c = choices(no_match_ground, k = 100)
    for n in no_match_ground:
        f.write(str(n)+'\n')
# print('all')
# print('----------------------')
# print(all_precisions/all_cnt)
# print(all_recalls/all_cnt)
# print(all_f1s/all_cnt)
# print(all_cnt)
