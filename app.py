from flask import *
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from web import ReviewHub

app=Flask(__name__)

@app.route("/")
def upload():
    return render_template("stuff.html")
@app.route("/success",methods=["post"])
def success():
    global loc
    global desc
    loc=request.form['loc']
    desc=request.form['des']
    # if(loc=="uk"):
    #    return render_template("stuff.html",h1="park avenue",h2="41",h3="taj hotel")
    # return render_template("stuff.html", h1="willingson", h2="avenue", h3="taj hotel")
    alist=Input_your_destination_and_description(loc, desc)
    # list1=alist[0]
    # list2=alist[1]
    # list3=alist[2]
    h1,h2,h3=alist
    return render_template("stuff.html",h1=str(h1),h2=str(h2),h3=str(h3))

def Input_your_destination_and_description(location, description):
        # Making these columns lowercase
        alist=[location,description]

        df = pd.read_csv('C:\\Users\\ibrah\\PycharmProjects\\trail\\Hotel_Reviews.csv')
        df.head()
        # Replacing 'united kingdom' with 'UK' for easy use
        df.Hotel_Address = df.Hotel_Address.str.replace('United Kingdom', 'UK')
        # Splitting the hotel address and picking out the last string which would be the countries
        df['countries'] = df.Hotel_Address.apply(lambda x: x.split(' ')[-1])
        df.countries.unique()  # All the hotels are located in six(6) countries
        # Dropping unneeded columns


        # module that converts a string of lists to a normal list
        from ast import literal_eval
        # function to convert array of tags to string
        def impute(col):
            col = col[0]
            if (type(col) != list):
                return "".join(literal_eval(col))
            else:
                return col

        # using the function
        df['Tags'] = df[['Tags']].apply(impute, axis=1)
        df.head()
        df['countries'] = df['countries'].str.lower()
        df['Tags'] = df['Tags'].str.lower()

        # Dividing the texts into small tokens (sentences into words)
        description = description.lower()
        description_tokens = word_tokenize(description)

        sw = stopwords.words('english')  # List of predefined english  stopwords to be used for computing
        lemm = WordNetLemmatizer()

        filtered_sen = {w for w in description_tokens if not w in sw}
        f_set = set()
        for fs in filtered_sen:
            f_set.add(lemm.lemmatize(fs))

        country_feat = df[df['countries'] == location.lower()]
        country_feat = country_feat.set_index(np.arange(country_feat.shape[0]))
        l1 = [];
        l2 = [];
        cos = [];
        for i in range(country_feat.shape[0]):
            temp_tokens = word_tokenize(country_feat['Tags'][i])
            temp1_set = {w for w in temp_tokens if not w in sw}
            temp_set = set()
            for se in temp1_set:
                temp_set.add(lemm.lemmatize(se))
            rvector = temp_set.intersection(f_set)

            cos.append(len(rvector))
        country_feat['similarity'] = cos
        country_feat = country_feat.sort_values(by='similarity', ascending=False)
        country_feat.drop_duplicates(subset='Hotel_Name', keep='first', inplace=True)
        country_feat.sort_values('Average_Score', ascending=False, inplace=True)
        country_feat.reset_index(inplace=True)
        df1 = pd.DataFrame(country_feat[['Hotel_Name', ]].head(3))
        alist = df1.values.tolist()
        return alist


if __name__=="__main__":
    app.run(debug=True)