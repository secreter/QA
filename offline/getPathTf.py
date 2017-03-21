# 计算path的tf,同时对数组去重，tf=数组中出现的次数/实体对的个数
# 注意每个实体对对应一个数组，为空的没记录而已,数组里长度大于1的path可能出现多次
# 因为通过不同节点连接起来的路径可能用了同一个rel，这里根据论文，多次的暂时看为一次
# 不过应该有待商榷。具体实现就是子数组去重

file = open(r'./txt/dist/my/paths.txt', 'r', encoding='utf-8')
line=True
i=0
with open(r"./txt/dist/my/paths_tf.txt",'w',encoding='utf-8') as dist:
  while line:
    i=i+1
    line=file.readline()
    if line=='\n':
      continue
    lst=line[:-1].split('\t\t\t')
    if len(lst)<3:
      continue
    pid=lst[0]
    PS=lst[1].split('\t')
    PSlstArr=[] #二维数组
    PSstrArr=[] #抹平后的一维数组
    for index,item in enumerate(PS):
      PSlstArr.append( list(set(eval(item))) ) # str to lsit,然后去重

    s=''
    for lstItem in PSlstArr:
      s+='\t'.join(lstItem) 
    PSstrArr=s.split('\t')
    m=int(lst[2])

    times=0
    PS=[]
    for p in PSstrArr:
      for pArr in PSlstArr:
        if p in pArr:
          times=times+1
      tf=round(times/m,8)
      PS.append(str([p,tf]))
    dist.write(pid+'\t\t\t'+str(PS)+'\n')
    # print(PS)

    if i%1000==0:
      print(i)
      # break
