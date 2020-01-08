#!/usr/bin/env python

import sys
import getopt
import json
from math import ceil
from pathlib import Path
import numpy as np
import joblib
import yaml
from sklearn import svm
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import classification_report
from tdlib.features.drlbp import TdFeatureDRLBP

def usage():
    ''' 显示帮助
    '''
    print("Build SVC Tool\n" +\
          "    -i 训练样本路径，多个路径以半角逗号(,)分隔\n" +\
          "    -s 参数搜索空间配置文件\n" +\
          "    -g 生成参数搜索空间基本配置文件\n" +\
          "    -p 指定训练样本与测试样本比例 (0.0, 1.0) 之间\n" +\
          "    -n 模型名称\n" +\
          "    -h 显示帮助\n" +\
          "\n" +\
          "  Examples:\n" +\
         "")
    sys.exit(0)


def svcGridSearch(X, y, tuned_params, split_ratio):
    ''' SVC 参数搜索
    '''
    X_train, X_test, y_train, y_test = train_test_split(fts, labels, test_size=split_ratio) \
                                       if 0 < split_ratio < 1 else \
                                       X, X, y, y
    scores, best_params = ['f1'], []
    for score in scores:
        clf = GridSearchCV(svm.SVC(), tuned_params, scoring='%s_macro'%score, cv=5, n_jobs=-1)
        clf.fit(X_train, y_train)
        print("Best parameters set found on development set:\n")
        best_params.append(clf.best_params_)
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
    return best_params[0]


def generateGridSpace():
    ''' 生成参数所搜空间
    '''
    grid_space_template = [
        {
            'kernel': ['poly'],
            'gamma': ['scale', 'auto'],
            'degree': [5, 15, 25, 35, 45, 55],
            'C': [1, 10, 100, 1000],
            'coef0': [0.0],
            'shrinking': [True],
            'probability': [False],
            'max_iter': [10000000],
        }
    ]
    with open("conf/grid/small_space.txt", 'w', encoding='utf-8') as f:
        f.write(json.dumps(grid_space_template, indent=4))
    grid_space_template[0]['gamma'].extend([float(i) for i in np.logspace(1, 60, 60, base=1.2)*0.000001])
    grid_space_template[0]['degree'].extend([int(i) for i in np.linspace(1, 100, 50)])
    grid_space_template[0]['C'].extend([float(i) for i in np.logspace(1, 36, 36, base=2)*0.00001])
    with open("conf/grid/big_space.txt", 'w', encoding='utf-8') as f:
        f.write(json.dumps(grid_space_template, indent=4))
    sys.exit(0)


def errorOccur(msg):
    ''' Error Occur
    '''
    print("Error:%s"%msg)
    sys.exit(1)


if __name__ == "__main__":
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "i:s:gp:n:h", ["help"])
    except getopt.GetoptError:
        print("argv error")
        sys.exit(1)

    ctgs_dirs, grid_space, split_ratio, model_name = None, None, -1, None
    drlbp_points, drlbp_radius, drlbp_occupied, drlbp_k_c = 8, 1, 0.8, 10
    for cmd, arg in opts:
        if cmd in "-i":
            ctgs_dirs = arg.split(',')
        if cmd in '-s':
            grid_space_fpath = arg
        if cmd in '-g':
            generateGridSpace()
        if cmd in '-n':
            model_name = arg
        if cmd in '-d':
            drlbp_points, drlbp_radius, drlbp_occupied, drlbp_k_c = arg.split(',')
            drlbp_points = int(drlbp_points)
            drlbp_radius = int(drlbp_radius)
            drlbp_occupied = float(drlbp_occupied)
            drlbp_k_c = int(drlbp_k_c)
        if cmd in '-p':
            split_ratio = float(arg)
            if not 0 < split_ratio < 1:
                errorOccur("Arg -p Error.")
        if cmd in '-h':
            usage()


    if None in [ctgs_dirs, grid_space_fpath, model_name]:
        errorOccur("Args Error.")

    print("Calculating DRLBP features ...")
    drlbp, datas = TdFeatureDRLBP(drlbp_points, drlbp_radius, drlbp_occupied, drlbp_k_c), []
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
    with open(grid_space_fpath, 'r', encoding='utf-8') as f:
        tuned_params = json.load(f)
    svc_params = svcGridSearch(fts, labels, tuned_params, split_ratio)
    print("SVC Model Built.")

    svc = svm.SVC(C=svc_params['C'],
                  coef0=svc_params['coef0'],
                  degree=svc_params['degree'],
                  gamma=svc_params['gamma'],
                  kernel=svc_params['kernel'],
                  max_iter=svc_params['max_iter'],
                  probability=svc_params['probability'],
                  shrinking=svc_params['shrinking'])
    svc.fit(fts, labels)
    mpath = "conf/svc/%s.model"%model_name
    joblib.dump(svc, mpath)
    print("SVC Model Saved to %s ."%mpath)

    ypath = "conf/svc/%s.yaml"%model_name
    if Path(ypath).exists():
        with open(ypath, "r") as f:
            model_conf = yaml.load(f, Loader=yaml.FullLoader)
    model_conf['mpath'] = mpath
    model_conf['k'] = drlbp.k - drlbp_k_c
    model_conf['drlbp'] = [drlbp_points, drlbp_radius, drlbp_occupied, drlbp_k_c]
    with open(ypath, 'w') as f:
        f.write(yaml.dump(model_conf))
    print("SVC Model Config Saved to %s ."%ypath)
