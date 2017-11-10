from sklearn.externals import joblib
print('In asf')
nb2 = joblib.load('spam_filter/spam_data_pugaar.pkl')


def check(description=None):
    if description is not None:
        try:
            return bool(nb2.predict([description]))
        except Exception :
            return False
    else:
        return True