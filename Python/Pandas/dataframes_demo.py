import pandas as pd



df1 = pd.DataFrame({0: [0,1,2], 2:["A","B","C"]})

print(f"{df1.iloc[0]=}")
x = df.iterrows() # generator object
print(f"{next(x)=}")

a = None
b = None
for i, j in df1.iterrows():
    a = i
    b = j
    print(f"i='{i}', j='{j}', {type(i)=}, {type(j)=}")
	
n_rows, n_cols = df1.shape
	
print(f"{list(b)=}")  # [2, 'C']
print(f"{b.keys()=}")  # Int64Index([0, 2], dtype='int64')
print(f"{list(b.keys())=}")  # [0, 2]
print(f"{list(b.values)}")  # [2, 'C']
print(f"{n_rows=}, {n_cols=}")  # n_rows=3, n_cols=2
print(f"{}")
print(f"{}")