from sklearn.model_selection import train_test_split, cross_val_score, KFold

def get_acc_score(X, Y, clf):

    # Train Test Split Variables
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)

    # Train Model
    clf.fit(X_train, y_train)

    # Get Prediction
    y_predict = clf.predict(X_test)

    # Get Accuracy
    acc = accuracy_score(y_predict, y_test) * 100.0

    return acc


def get_acc_score_kcv(X, Y, clf):

    # K-Fold Cross Validation
    kf = KFold(n_splits=10, shuffle=True)
    cv = kf.split(df_X)

    acc = 0

    for train_index, test_index in cv:
        clf.fit(X.iloc[train_index], Y.iloc[train_index])
        y_predict = clf.predict(X.iloc[test_index])
        acc_tmp = accuracy_score(Y.iloc[test_index], y_predict) * 100.0
        acc += acc_tmp

    acc = float(acc) / 10

    return acc
