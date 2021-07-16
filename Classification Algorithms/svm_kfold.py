# -*- coding: utf-8 -*-
"""SVM_kfold.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1abPX3TKIcP6WrBIHkWJhEk4t_Jr5sRYW
"""

#Importamos las librerias necesarias para leer y procesar los datos
import pandas as pd
import numpy as np

#Importamos librerias para construir y entrenar los modelos a implementar

from sklearn import datasets, metrics
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.neural_network import MLPClassifier

#Importamos Librerias, usadas para evaluar y probar los resultados de los modelos

from sklearn.metrics import classification_report, accuracy_score,confusion_matrix
from sklearn.metrics import roc_curve, roc_auc_score,auc
from sklearn import  metrics

#Importamos la libreria para mostrar las Imagenes

import matplotlib.pyplot as plt
from mlxtend.plotting import  plot_confusion_matrix

#Importamos libreria para guardar el modelo.
import joblib

# Cargamos los Datos de entranmiento
Datatrain= pd.read_csv('train_prueba.csv', sep=",") 
dataframe=pd.DataFrame(Datatrain)
print(Datatrain)

# Se dividen los datos de entrenamiento en variables de entrada(X) y salida(Y)

X_train=(dataframe[["Mean RR","SDNN","RMSSD","TINN","VLF","LF","HF","LF/HF"]])
Y_train=(dataframe["Label"])

#Cargamos los datos de validación
Datatest= pd.read_csv('test_prueba.csv', sep=",") 
dataframe=pd.DataFrame(Datatest)
print(Datatest)

# Se dividen los datos de validación en variables de entrada(X) y salida(Y)

X_test=(dataframe[["Mean RR","SDNN","RMSSD","TINN","VLF","LF","HF","LF/HF"]])
Y_test=(dataframe["Label"])

# Se carga el modelo y se entrena
modelo=SVC(kernel='linear',random_state=123 ,probability=1, C=0.000001, gamma=1)
modelo.fit(X_train,Y_train)

# Presición del modelo
score= modelo.score(X_train,Y_train)
print("metrica del modelo",score*100,"%")

# Se aplica la tecnica de k-fold
kf=KFold(n_splits=5, random_state=7)
scores = cross_val_score(modelo, X_train, Y_train, cv=kf, scoring="accuracy")
print("metricas cross_validation",scores*100,"%")

print("Media de cross_validation", scores.mean()*100,"%")

#validación del modelo
Y_pred = modelo.predict(X_test)

score_pred = metrics.accuracy_score(Y_test, Y_pred)
 
print("Precisión validación", score_pred*100,"%")

# Matriz de confusión
cm=confusion_matrix(Y_test,Y_pred)
print(cm)

import itertools
plt.clf()
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Wistia)
classNames = ['Normal','Taquicardia','Bradicardia']
plt.title('Matriz confusion SVM')
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.colorbar()
tick_marks = np.arange(len(classNames))
plt.xticks(tick_marks, classNames, rotation=45)
plt.yticks(tick_marks, classNames)
ax = plt.gca()
#ax.set_xticklabels((ax.get_xticks() +1).astype(str))

thresh = cm.max() / 2.
for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

plt.show()

# Reporte de clasificación del modelo
 print(classification_report(Y_test,Y_pred))

# Obtimización del parámetro C
 from  sklearn.model_selection  import  GridSearchCV 

param_grid  =  {"C":[ 0.00001 ,  0.0001 ,  0.001 , 
                        0.01 ,  0.1 ,  1.0 ,10.0 ,  
                        100.0 ,  1000.0 ]} 
grid  =  GridSearchCV ( estimator = modelo , 
                       param_grid = param_grid , cv = kf ) 

grid . fit (X_train , Y_train) 
print( grid . best_estimator_ . C ) 
print( grid . best_score_ * 100 ,  "%" )

# Curva RAUC-ROC
from sklearn.metrics import roc_curve, roc_auc_score,auc
Y_pred_probs=modelo.predict_proba(X_test)

roc_auc=roc_auc_score(Y_test, Y_pred_probs,multi_class='ovr')
print("AUC of ROC curve:",roc_auc)

# Grafica de la curva ROC
from itertools import cycle
#roc curve for classes
fpr = {}
tpr = {}
thresh ={}
lw=2
n_class = 3

for i in range(n_class):    
    fpr[i], tpr[i], thresh[i] = roc_curve(Y_test, Y_pred_probs[:,i], pos_label=i)
    
    
# plotting  
#plt.plot([0, 1], [0, 1], 'k--', lw=lw)  
#plt.plot(fpr[0], tpr[0],linestyle='--',color='blue', label= 'Class 1 vs Rest')
#plt.plot(fpr[1], tpr[1], linestyle='-.',color='green', label='Class 1 vs Rest')
#plt.plot(fpr[2], tpr[2],color='red', label='Class 2 vs Rest')
#plt.title('Multiclass ROC curve')
#plt.xlabel('False Positive Rate')
#plt.ylabel('True Positive rate')
#plt.legend(loc='best')
#plt.savefig('Multiclass ROC',dpi=300);

from scipy import interp 
fpr = dict()  
tpr = dict()  
roc_auc = dict()  
for i in range(n_class):  
  fpr[i], tpr[i], thresh[i] = roc_curve(Y_test, Y_pred_probs[:,i], pos_label=i)
  roc_auc[i] = auc(fpr[i], tpr[i])



# First aggregate all false positive rates
all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_class)]))

# Then interpolate all ROC curves at this points
mean_tpr = np.zeros_like(all_fpr)  
for i in range(n_class):  
    mean_tpr += interp(all_fpr, fpr[i], tpr[i])

# Finally average it and compute AUC
mean_tpr /= n_class



colors = cycle(['aqua', 'darkorange', 'cornflowerblue'])  
for i, color in zip(range(n_class), colors):  
    plt.plot(fpr[i], tpr[i], color=color, lw=lw, linestyle='--',
             label='ROC curve of class {0} (area = {1:0.2f})'
             ''.format(i, roc_auc[i]))

plt.plot([0, 1], [0, 1], 'k--', lw=lw)  
plt.xlabel('FPR(1-especificidad)')  
plt.ylabel('TPR(sensibilidad)')  
plt.title('Curva ROC para clasificador SVM')  
plt.legend(loc="lower right")  
plt.show()

# Modelo Guardado
import joblib
joblib.dump(modelo,'modelo_entenadoSVM_elmejor.pkl')