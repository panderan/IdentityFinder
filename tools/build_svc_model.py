#!/usr/bin/env python

import sys
import getopt
import sklearn.exceptions
import warnings
import numpy as np
from math import ceil
from sklearn import svm
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import classification_report
from tdlib.features.drlbp import TdFeatureDRLBP

def usage():
    ''' 显示帮助
    '''
    print("Build SVC Tool")

def svcGridSearch(X, y):
    ''' SVC 参数搜索
    '''
    tuned_params = [
        {
            'kernel': ['poly'],
            'gamma': ['scale', 'auto'],
            'degree': [],
            'C': [],
            'coef': [0.0],
            'shrinking': [True],
            'probability': [False],
        }
    ]
    tuned_params[0]['gamma'].extend(np.logspace(1, 60, 60, base=1.2)*0.000001)
    tuned_params[0]['degree'].extend(np.int32(np.linspace(1, 100, 50)))
    tuned_params[0]['C'].extend(np.logspace(1, 36, 36, base=2)*0.00001)


    # X_train, X_test, y_train, y_test = train_test_split(fts, labels, test_size=0.5)
    X_train, X_test, y_train, y_test = X, X, y, y
    scores = ['precision', 'recall']
    for score in scores:
        clf = GridSearchCV(svm.SVC(), tuned_params, scoring='%s_macro'%score, cv=5)
        clf.fit(X_train, y_train)
        print("Best parameters set found on development set:\n")
        print(clf.best_params_)
        print("\nGrid scores on development set:\n")
        means = clf.cv_results_['mean_test_score']
        stds = clf.cv_results_['std_test_score']
        for mean, std, params in zip(means, stds, clf.cv_results_['params']):
            print("%0.3f (+/-%0.03f) for %r"
                  % (mean, std * 2, params))
        print()
        print("Detailed classification report:\n")
        print("The model is trained on the full development set.")
        print("The scores are computed on the full evaluation set.\n")
        y_true, y_pred = y_test, clf.predict(X_test)
        print(classification_report(y_true, y_pred))
        print()

if __name__ == "__main__":
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "i:", ["help"])
    except getopt.GetoptError:
        print("argv error")
        sys.exit(1)

    ctgs_dirs = None
    for cmd, arg in opts:
        if cmd in "-i":
            ctgs_dirs = arg.split(',')
    if ctgs_dirs is None:
        print("Args Error.")
        sys.exit(1)

    print("Calculating DRLBP features ...")
    drlbp, datas = TdFeatureDRLBP(8, 1, 0.8, 10), []
    for dirpath in ctgs_dirs:
        data = drlbp.training_k(dirpath)
        datas.append(data)

    print("Preparing feature and label vectors ...")
    drlbp.k = ceil(max(i[0] for i in datas))
    fts, labels = [], []
    for data in datas:
        _, data = data
        for item in data:
            vtr, label = item
            vtr = vtr[:drlbp.k]
            fts.append(vtr)
            labels.append(label)

    print("Building SVC Model ...")
    warnings.filterwarnings('ignore', category=sklearn.exceptions.UndefinedMetricWarning)
    svcGridSearch(fts, labels)
    print("SVC Model Built.")
