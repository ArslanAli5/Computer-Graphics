import pandas as pd
df = pd.read_csv('locations.csv', sep=",")
pd.set_option('display.max_colwidth', None)
col1 = []
col2 = []
col3 = []
access_path = df['access_path']
for path in access_path:
  splited = path.split('::')
  if len(splited)==1:
    splited.append("N/A")
    splited.append("N/A")

  else:
    splited.append("N/A")
  col1.append(splited[0])
  col2.append(splited[1])
  col3.append(splited[2])
df['col1'] = col1
df['col2'] = col2
df['col3'] = col3
def get_location_descendants(ID):  
  desentandants = []
  if len(ID)==11:
    found = df.where(df['col1'] == ID).dropna()
  elif len(ID)==12:
    found = df.where(df['col2'] == ID).dropna()
  elif len(ID)==13:
    found = df.where(df['col3'] == ID).dropna()
  desentandants.append(found['name'].to_string().split(' ',1)[-1])
  return desentandants
print(get_location_descendants("location_32")) 
print(get_location_descendants("location_216")) 
print(get_location_descendants("location_1380")) 
