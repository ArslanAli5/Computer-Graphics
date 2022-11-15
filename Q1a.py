import pandas as pd
df = pd.read_csv('locations.csv')
pd.set_option('display.max_colwidth', None)
def get_location_ancestors(ID): 
  ancestor = []
  found = df.where(df['id'] == ID).dropna()
  ancestor.append(found['name'].to_string().split(' ',1)[-1])
  locations = found['access_path'].to_string().split(" ")[-1]
  locations = locations.split("::")[:-1]
  for location in locations:
    found = df.where(df['id'] == location).dropna()
    ancestor.append(found['name'].to_string().split(' ',1)[-1])
  return ancestor;
print(get_location_ancestors("location_1380"))
