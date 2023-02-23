import pandas as pd
from analysis_data import rms_voltage_power_spectrum


def calculating_rms(df, display_df, frequency):
    L = []
    for i in [8, 10, 12, 14, 16, 20, 24, 28]:
        __, rms = rms_voltage_power_spectrum(df, i, i, 860, 4300)
        L.append(rms)
    return display_df.append({'8Hz': L[0], '10Hz': L[1], '12Hz': L[2], '14Hz': L[3], '16Hz': L[4], 
                          '20Hz': L[5], '24Hz': L[6], '28Hz': L[7], 'Y': frequency}, ignore_index=True)

df1 = pd.read_csv('ML/8Hz.csv', header=None)
df2 = pd.read_csv('ML/10Hz.csv', header=None)
df3 = pd.read_csv('ML/12Hz.csv', header=None)
df4 = pd.read_csv('ML/14Hz.csv', header=None)

print(df1.shape, df2.shape, df3.shape, df4.shape)

#.stack().reset_index(drop=True)
df = pd.DataFrame(columns=['8Hz', '10Hz', '12Hz', '14Hz', '16Hz', '20Hz', '24Hz', '28Hz', 'Y'])
for i in range(30):
    df = calculating_rms(df1.iloc[i], df, 8)
    df = calculating_rms(df2.iloc[i], df, 10)
    df = calculating_rms(df3.iloc[i], df, 12)
    df = calculating_rms(df4.iloc[i], df, 14)

print(df)

from pyts.datasets import make_cylinder_bell_funnel
from sklearn.model_selection import train_test_split
from pyts.classification import LearningShapelets


X_train, X_test, y_train, y_test = train_test_split(df.iloc[:, :-4], df.iloc[:, -1], test_size=0.2, random_state=42)

# Create a LearningShapelets object
clf = LearningShapelets(random_state=42)

# Fit the classifier to the training data
clf.fit(X_train, y_train)

# Predict the classes of the test data
y_pred = clf.predict(X_test)

# Evaluate the performance of the classifier
accuracy = clf.score(X_test, y_test)
print('Accuracy:', accuracy)

