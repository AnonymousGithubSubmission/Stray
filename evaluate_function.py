import itertools
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
    ds = ['list','set','tuple','dict']
    def same_ds(x, g):


        if x == 'object':
            return True
        # for d in ds:
        #     if x.find(d) != -1:
        #         for g_ in g:
        #             if g_.find(d) != -1:
        #                 return True

        return False
    previous = 0
    for f in returns:

        ground_annotation = ground_truth[previous:f-1]
        ground_annotation = '->'.join([str(x[0]) for x in ground_annotation])
        types = PIG[previous:f-1]
        types = [x[:1] for x in types]
        previous = f-1
        annotations = itertools.product(*types)
        annotations = ['->'.join(x) for x in annotations]
        hit = any([x == ground_annotation for x in annotations])
        if hit:
            print(f)
        precision = hit/len(annotations)
        recall = hit
        if precision + recall == 0:
            f1 = 0
        else:
            f1 = (2*precision*recall)/(precision + recall)
        precisions += precision
        recalls += recall
        f1s += f1
        cnt += 1

    print(precisions/cnt)
    print(recalls/cnt)
    print(f1s/cnt)
    print(cnt)
    all_precisions += precisions
    all_recalls += recalls
    all_f1s += f1s
    all_cnt += cnt

    def remove_none(p):
        return [x for x in p if x  != 'none']

print('all')
print('----------------------')
print(all_precisions/all_cnt)
print(all_recalls/all_cnt)
print(all_f1s/all_cnt)
print(all_cnt)
