
import pandas as pd

df = pd.DataFrame([[1, 2], [3, 4]], columns = ["a", "b"])
print(df)


to_append = dict()

df_length = len(df)
df.loc[df_length] = to_append

print(df)