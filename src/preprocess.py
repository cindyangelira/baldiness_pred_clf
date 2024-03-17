import pandas as pd
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler, LabelEncoder

class Preprocess():
  def __init__(self, df, cat_col:list, num_col:list, mapping:dict):
    self.df = df
    self.cat_col = cat_col
    self.num_col = num_col
    self.mapping = mapping

  # preprocess
  def preprocess_data(self):
    self.convert_col()
    self.drop_missing()
    self.drop_unused_col()
    self.encoding()
    self.label_encoding()
    self.scaler()
    self.generate_target()
    self.drop_missing()
    return self.df

  def convert_col(self):
    type_dict = {
      'umur' : 'Int64',
      'is_menikah' : 'Int64',
      'is_keturunan' : 'Int64',
      'is_merokok' : 'Int64',
    }
    self.df = self.df.astype(type_dict, errors = 'ignore')

  # lets drop any missing
  def drop_missing(self):
    self.df = self.df.dropna()

  # ohe (one hot encoding)
  def encoding(self):
    encoder = OneHotEncoder(drop='first')
    encoded_col = encoder.fit_transform(self.df[self.cat_col])
    encoded_df = pd.DataFrame(encoded_col.toarray(), columns = encoder.get_feature_names_out(self.cat_col))
    self.df = pd.concat([self.df.drop(columns=self.cat_col), encoded_df], axis = 1)
  
  # label encoding
  def label_encoding(self):
    label_encoder = LabelEncoder()
    for col, value in self.mapping.items():
      self.df[col] = label_encoder.fit_transform(self.df[col])

  # minmax scaler numerical col
  def scaler(self):
    scaler = MinMaxScaler()
    self.df[self.num_col] = scaler.fit_transform(self.df[self.num_col])

  # get target is_botak
  def generate_target(self):
    self.df['is_botak'] = (self.df['botak_prob'] > .5).astype(int)
  
  # drop unnecessary column
  def drop_unused_col(self):
    self.df = self.df.drop(columns =['pekerjaan', 'provinsi'])


  


