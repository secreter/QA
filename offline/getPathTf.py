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
    # print(PSlstArr)
    s=''
    for lstItem in PSlstArr:
      s+='\t'+'\t'.join(lstItem)  #最前面多了一个'\t'
    s=s[1:]
    # print(s)
    PSstrArr=s.split('\t')
    # print(PSstrArr)
    m=int(lst[2])

    
    PS=[]
    for p in PSstrArr:
      times=0
      for pArr in PSlstArr:
        if p in pArr:
          times=times+1
      # print(p+" %d" % (times))
      tf=round(times/m,8)
      if abs(tf-0)<0.00000001:
        print(p)
        print(times)
        print(tf)
      #存在[['write',0.5],['write',0.5],['write',0.5]]
      #的情况，但在前面还不能去重，因为要统计多少个数组中出现过write
      #现在写个函数去重
      res=str([p,tf])
      if res not in PS:
        PS.append(res)
    dist.write(pid+'\t\t\t'+str(PS)+'\n')
    # print(PS)

    if i%1000==0:
      print(i)
      # break
