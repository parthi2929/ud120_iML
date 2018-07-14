def init():
    """
    Load the raw data_dict from Udacity's pickle data and return it
    """
    import sys
    import pickle
    sys.path.append("../tools/")
    ### Load the dictionary containing the dataset
    with open("final_project_dataset.pkl", "r") as data_file:
        data_dict = pickle.load(data_file)
        
    return data_dict

import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit
def split_data(my_dataset, features_list):
    # convert
    data = featureFormat(my_dataset, features_list, sort_keys = True)
    labels, features = targetFeatureSplit(data)
    return labels, features 

def tree_classify(random_state):
    # our classifier
    from sklearn import tree
    clf = tree.DecisionTreeClassifier(random_state=random_state)
    return clf

from IPython.utils.coloransi import TermColors as color # just for color gimmicks on output
from tester import dump_classifier_and_data, main

def evaluate(clf, my_dataset, features_list):
    dump_classifier_and_data(clf, my_dataset, features_list)
    print '{1}Udacity\'s Evaluation:{0}'.format(color.Normal, color.BlinkBlue)
    return main()  # from tester.py

#-------------- PANDAS AREA --------------------
# 1. PRE PROCESSING
# 1.1. Cleaning Invalid Values ('NaN')
import pandas as pd
def clean_df(raw_df):
    """
    Replace 'NaN' with 0 in all feature columns, except 'poi' and 'email_address'
    Return updated df
    """
    # replace NaN except poi and email_address (ref: https://stackoverflow.com/questions/42916989/replace-missing-values-in-all-columns-except-one-in-pandas-dataframe)
    data_panda_1 = raw_df.loc[:, raw_df.columns.difference(['poi','email_address'])].replace('NaN',0, regex=True)
    # caz we have to now concat caz of these cols lost in above df
    data_panda_2 = raw_df[['poi','email_address']]
    # concat (remember axis 1)
    data_panda = pd.concat([data_panda_1, data_panda_2],axis=1, sort=False)
    # fix exponential display formatdue to replace operaiton (ref: https://stackoverflow.com/questions/42735541/customized-float-formatting-in-a-pandas-dataframe)
    pd.options.display.float_format = lambda x : '{:.0f}'.format(x) # we dont both about decimal accuracies here for calculated means, stds etc.    
    return data_panda

# 1.2. Remove Outliers
# helper function for us to visualize the plots. I wrote using seaborn as I started with it, but simpler ones possible
import seaborn as sns
def stripplots(main_df, outlier_dict={}):
    """
    Given a dataframe, it plots all its individual features against their index number, hues as per label (poi)
    This is specifically useful to see if any feature stands out. 
    It is assumed incoming dataframe contains only all numerical features columns and label column 'poi'
    If outlier_dict given, with feature=value, those would be annoted as well
    """
    import matplotlib.axes as axes
    import matplotlib.pyplot as plt
    import numpy as np    
    
    # pre processing features list
    main_df = main_df.loc[:, main_df.columns.difference(['email_address'])]  # email_address not useful for visualizing
    all_numerical_features_df = main_df.loc[:, main_df.columns.difference(['poi'])]      
    all_numerical_features = list(all_numerical_features_df)
   
    # calculate reasonable figure size for each sub plot based on no of features
    n_features = all_numerical_features_df.shape[1]
    n_subplots = n_features if (n_features%2 == 0) else (n_features+1)
    n_subplots_row = n_subplots/2
    n_subplots_col = 1 if n_features == 1 else 2 #  if only one feature, then only one plot
    f = plt.figure(figsize=(7*n_subplots_col,5*n_subplots_row))
    
    # calculate x-axis as seaborn messes up order if not specifically given like this
    n_persons = main_df.shape[0]
    x_axis = x=range(0,n_persons)  # apparantly feeding index col messes up x axis order so..

    # red if poi, green if not
    flatui = ["#2ecc71", "#e74c3c"]
    sns.color_palette(flatui)

    # here we go..
    for index in range(len(all_numerical_features)):   

        # plot the graph
        feature = all_numerical_features[index]
        #print all_numerical_features[n_features_index]
        ax = f.add_subplot(n_subplots_row, n_subplots_col, index+1)
        ax = sns.stripplot(data=main_df,x=x_axis,y=feature,hue='poi', ax = ax, palette=flatui)        

        # outliers if any given
        if feature in outlier_dict:                      
            value = outlier_dict[feature]
            annotate_value(main_df, feature, value, ax)


    # rotating x axis for better view
    for ax in f.axes:
        plt.sca(ax)
        plt.xlabel('index')
        plt.xticks(rotation=90) # for better perception of how x axis scales as too many rows to fit
        plt.legend(bbox_to_anchor=(1, 1), loc='upper left') # to keep legend outside figure  
        

        
    f.tight_layout()
    plt.show()
    
def annotate_value(df, current_feature, value, axes):
    """
    Annotate given value of given feature on chart. Assumed it is available.
    """
    x_val = df[current_feature].values.tolist().index(value)
    y_val = value
    #print x_val,y_val
    axes.annotate('Outlier!', xy=(x_val, y_val*0.95), xytext=(x_val,y_val*0.80),arrowprops=dict(facecolor='black'))
    return axes

def get_feature_max(df, features_list):
    """
    Given a feature list and data frame this returns a dictionary with each key as feature, and its value, the max 
    of that feature column in the dataframe
    """
    feature_dict = {}
    for each_feature in features_list:
        y_val = df[each_feature].max()
        feature_dict.update({each_feature: y_val})
    return feature_dict

def get_feature_min(df, features_list):
    """
    Given a feature list and data frame this returns a dictionary with each key as feature, and its value, the min 
    of that feature column in the dataframe
    """
    feature_dict = {}
    for each_feature in features_list:
        y_val = df[each_feature].min()
        feature_dict.update({each_feature: y_val})
    return feature_dict

def get_index_label(input_df, feature, value):
    """
    Given an input data frame, a feature it has, and a value to spot, this function returns the index label of that cell
    """
    x = input_df[feature].values.tolist().index(value) # thanks: https://stackoverflow.com/questions/37502298/get-integer-row-index-in-dataframe-where-column-matches-specific-value
    x = input_df.index[x]
    return x

def is_POI(input_df, index_label):
    """
    Given a data frame and index label this function returns if given index label is POI (true) or not
    """
    return input_df.loc[index_label,'poi']

def remove_outliers(input_df, outlier_list):
    """
    Returns input df stripped off with given outliers list (list of index labels)
    """
    return input_df.drop(outlier_list)

def get_all_numerical_features_list(input_df):
    """
    Strips off ermail_address and poi in given df
    Creates list of features/columns
    Insert poi as list's first element
    Return the list
    """
    features_list = [x for x in input_df.columns.values if x != 'email_address' and x != 'poi']
    features_list.insert(0,'poi')   
    return features_list