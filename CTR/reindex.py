import pandas as pd
import numpy as np
df = pd.read_csv(r'D:\tencentvideos\交叉特征\test150.txt',header=None,sep=',')
df =pd.DataFrame(df)
df = df.reindex(np.random.permutation(df.index))
df.to_csv(r'D:\tencentvideos\交叉特征\test15.txt',index=False,header = False, encoding='utf-8')
