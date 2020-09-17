import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from ML_Framework.utility.global_variables import model_name, training_file_name


DATASET_PATH = "ML_Framework/Dataset/"
CSVS_PATH = DATASET_PATH + "csvs/"
MODELS_PATH = DATASET_PATH + "models/"

def train_model(test_size=0.3):
    print('training start**********************')
    # training data
    train_data = pd.read_csv(CSVS_PATH + training_file_name + '.csv')
    X = train_data.drop(['label'], axis=1)
    y = train_data['label']

    # Split training and testing dataset
    print('Training data %', test_size*100)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)

    # model
    classifier = DecisionTreeClassifier()

    # actual training
    classifier.fit(X_train, y_train)

    # dumping model for further use
    pickle.dump(classifier, open(MODELS_PATH + model_name + '.pkl', 'wb'))

    # testing
    y_pred = classifier.predict(X_test)
    print('Confusion matrix:')
    print(metrics.confusion_matrix(y_test, y_pred))
    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
    print("Precision:",metrics.precision_score(y_test, y_pred))
    print("Recall:",metrics.recall_score(y_test, y_pred))


if __name__ == '__main__':
    train_model(float(input('Enter training data ratio : ')))
