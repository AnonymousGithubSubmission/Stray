builtins = ['int', 'float','bool','str', 'byte', 'callable', 'none', 'object']
third = ['ndarray', 'tensor', 'namespace', 'vocabulary', 'textfieldembedder', 'jsondict', 'instance', 'socket', 'token']


projects = ['seagull','tinychain','relex','htmlark']
returnses = [
[3,5,8,10,12,14,16,18,20,22,24,26,31,35,37,39,40,41,43,47,48,49,50,51,52,53,55,56,57,58,59,60,61,64,65,66,67,68,69],
[3,6,9,10,12,15,18,19,21,22,28,31,34,36,39,40,42,47,51,53,55,57,59,62,64,66,68,70,72,77,80,81,83,85,88,91,94,97,100,103],
[10, 17, 20, 23, 26, 28, 33, 36, 38, 40, 47, 49, 51],
[2, 4, 7, 15, 16]
]
model = 'PIG'
all_precisions = 0
all_recalls = 0
all_f1s = 0
all_cnt = 0
for i, project in enumerate(projects):
    print(project)
    print('----------------------')
    ground_truth = []
    returns = returnses[i]
    with open(f'GT_{project}.txt') as f:
        
        for i, line in enumerate(f):
            if i == 0:
                continue
            ground_truth.append(line.strip().lower().split('/'))
    PIG = []
    with open(f'{model}_{project}.txt') as f:
        
        for i, line in enumerate(f):
            if i == 0:
                continue
            PIG.append(line.strip().lower().split('/'))
    precisions = 0
    recalls = 0
    f1s = 0
    cnt = 0

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
    
    for i, p in enumerate(PIG):
        p = remove_none(p)
        # p = p[:1]
        if i + 2 in returns:

            g = ground_truth[i]
            if 'none' in g:
                continue
            # if is_builtin(g):
            #     continue
            # elif is_third(g):
            #     continue
            # else:
            #     pass
            
            cnt += 1
            if len(p) > 0:
                hit = sum([x in g or same_ds(x, g) for x in p])
                precision = hit/len(p)
                recall = hit/len(g)
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



print('all')
print('----------------------')
print(all_precisions/all_cnt)
print(all_recalls/all_cnt)
print(all_f1s/all_cnt)
print(all_cnt)
