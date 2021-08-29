
import pandas as pd

df = pd.DataFrame([[1, 2], [3, 4]], columns = ["a", "b"])
print(df)


# to_append = dict()
#
# df_length = len(df)
# df.loc[df_length] = to_append
#
# print(df)

df2 = pd.read_excel("savedData/blahajData.xlsx", sheet_name="win")
print(df2)

print(df2.loc[0]["score"])