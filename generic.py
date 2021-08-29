
import pandas as pd

# df = pd.DataFrame([[1, 2], [3, 4]], columns = ["a", "b"])
# print(df)
#

# to_append = dict()
#
# df_length = len(df)
# df.loc[df_length] = to_append
#
# print(df)

df = pd.read_csv("savedData/blahajData.csv")
# print(df2)

player_name = "dssadf"
score = 12345

print(df.loc[0]["score"])

df.loc[len(df)] = [player_name, score]
print(df)
df = df.sort_values(by=['score'], ascending=False)
print(df)

df.to_csv("savedData/blahajData.csv")
