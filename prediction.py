import pandas as pd
import pickle as pk
from sklearn.preprocessing import LabelEncoder

def preprocess(df):

    """""
    Pre-process akan melakukan drop column, mapping, encoding, dan PCA
    """""
    
    # dropping features with only one value and primary key
    df = df.drop(['Over18', 'EmployeeCount', 'StandardHours', 'EmployeeId'], axis = 1)

    # mapping categorical and ordinal features.
    mapOvertime = {'No' : 0, 'Yes' : 1}
    df = df.replace({'OverTime' : mapOvertime})

    mapTravel = {'Non-Travel' : 1, 'Travel_Rarely' : 2, 'Travel_Frequently':3}
    df = df.replace({'BusinessTravel' : mapTravel})

    mapGender = {'Female' : 0, 'Male' : 1}
    df = df.replace({'Gender' : mapGender})

    # encoding other categorical columns
    categorical_column = ['Department', 'JobRole', 'MaritalStatus','EducationField']
    encoder=LabelEncoder()
    df[categorical_column]=df[categorical_column].apply(encoder.fit_transform)

    if 'Attrition' in df.columns: df = df.drop(['Attrition'], axis = 1)
    
    # PCA
    pca_reload = pk.load(open("pca.pkl",'rb'))
    result_new = pca_reload.transform(df)
    return result_new

if __name__ == '__main__':

    model = pk.load(open('KNN_CV.pkl', 'rb'))
    df = pd.read_csv('df_predict.csv')
    preprocessed_df = preprocess(df)
    
    predictions = model.predict(preprocessed_df)
    df['Attrition'] = predictions
    
    print(df['Attrition'])
    
    df_predict = df[['EmployeeId', 'Attrition']].copy()
    df_predict.to_csv('df_predict_results.csv', index = False)