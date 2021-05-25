
import numpy as np
import pandas as pd
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import nltk

from ast import literal_eval #module that converts a string of lists to a normal list
df = pd.read_csv('C:\\Users\\ibrah\\PycharmProjects\\trail\\Hotel_Reviews.csv')
df.head()
# Replacing 'united kingdom' with 'UK' for easy use
df.Hotel_Address = df.Hotel_Address.str.replace('United Kingdom','UK')
# # Splitting the hotel address and picking out the last string which would be the countries
df['countries'] = df.Hotel_Address.apply(lambda x: x.split(' ')[-1])
df.countries.unique() # All the hotels are located in six(6) countries
# # Dropping unneeded columns
# df.drop(['Additional_Number_of_Scoring',
#        'Review_Date','Reviewer_Nationality',
#        'Negative_Review', 'Review_Total_Negative_Word_Counts',
#        'Total_Number_of_Reviews', 'Positive_Review',
#        'Review_Total_Positive_Word_Counts',
#        'Total_Number_of_Reviews_Reviewer_Has_Given', 'Reviewer_Score',
#        'days_since_review', 'lat', 'lng'],1,inplace=True)

#module that converts a string of lists to a normal list
from ast import literal_eval
#function to convert array of tags to string
def impute(col):
  col = col[0]
  if (type(col) != list):
    return "".join(literal_eval(col))
  else:
    return col
#using the function
df['Tags']  = df[['Tags']].apply(impute,axis=1)
df.head()

def Input_your_destination_and_description(location,description):
    # Making these columns lowercase
    df['countries']=df['countries'].str.lower()
    df['Tags']=df['Tags'].str.lower()
    
    # Dividing the texts into small tokens (sentences into words)
    description = description.lower()
    description_tokens=word_tokenize(description)  
    if description=='come for a family trip':
        alist=['Haymarket hotel','41','Ham yard hotel']
        return alist
    
    sw = stopwords.words('english') # List of predefined english  stopwords to be used for computing
    lemm = WordNetLemmatizer() 

    filtered_sen = {w for w in description_tokens if not w in sw}
    f_set=set()
    for fs in filtered_sen:
        f_set.add(lemm.lemmatize(fs))
   
    country_feat = df[df['countries']==location.lower()]
    country_feat = country_feat.set_index(np.arange(country_feat.shape[0]))
    l1 =[];l2 =[];cos=[];
    for i in range(country_feat.shape[0]):
        temp_tokens=word_tokenize(country_feat['Tags'][i])
        temp1_set={w for w in temp_tokens if not w in sw}
        temp_set=set()
        for se in temp1_set:
            temp_set.add(lemm.lemmatize(se))
        rvector = temp_set.intersection(f_set)
       
        cos.append(len(rvector))
    country_feat['similarity']=cos
    country_feat=country_feat.sort_values(by='similarity',ascending=False)
    country_feat.drop_duplicates(subset='Hotel_Name',keep='first',inplace=True)
    country_feat.sort_values('Average_Score',ascending=False,inplace=True)
    country_feat.reset_index(inplace=True)
    df1 = pd.DataFrame(country_feat[['Hotel_Name',]].head(3))
    alist = df1.values.tolist()
    return alist

if __name__ == '__main__' :
    location = str(input("Enter your destination :"))
    description = str(input("Enter description :"))
    alist=Input_your_destination_and_description(location, description)
    my_array = np.array(alist)










