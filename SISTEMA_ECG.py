from serialToExcel import SerialToExcel
import time
import serial
import enviardato
import matlab.engine as me
import os
import pandas as pd
import numpy as np
from serial import Serial

from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC

import matplotlib.pyplot as plt
from sklearn import datasets, metrics
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.metrics import classification_report, accuracy_score,confusion_matrix
from mlxtend.plotting import  plot_confusion_matrix
from sklearn.metrics import roc_curve, roc_auc_score,auc
import joblib

from sklearn import  metrics

print('Sistema IoT para monitoreo de actividad cardiaca')
print('con variabilidad de frecuencia para el diagnóstico')
print('de enfermedades cardiovasculares')
print('\n')
print('------------------------------------')
print('-------------BIENVENIDO-------------')
print('------------------------------------')
print('\n')

#RECOLECCIÓN DE DATOS
Paciente=input("¿Cúal es el nombre del paciente?: ");

serialToExcel = SerialToExcel("COM3",9600);
columnas = ["Nro Lectura","Valor"]
print('---------------------------')
print('-----ADQUIRIENDO DATOS-----')
print('---------------------------')
serialToExcel.setColumns(["Nro Lectura","Valor"]);
serialToExcel.setRecordsNumber(60000);
serialToExcel.readPort();
serialToExcel.writeFile(Paciente + ".xls");

print('\n')
print('--------------------------')
print('-----DATOS ADQUIRIDOS-----')
print('--------------------------')
print('\n')
print('--------------------------')
print('-----PROCESANDO DATOS-----')
print('--------------------------')


####################################


#PROCESAMIENTO DE DATOS
#df=pd.read_excel(Paciente +'.xls')
#df=pd.DataFrame.to_string(df)
#Nombre="Senal.txt"
#archivo=open("Senal.txt","w")
#archivo.write(df)
f1=me.start_matlab()
inrr=f1.CORREGIR_EXCEL(Paciente)
f1.quit()
print('\n')
print('--------------------------')
print('-----DATOS PROCESADOS-----')
print('--------------------------')
#########################


print('\n')
print('--------------------------------------------')
print('-----INICIANDO PROCESO DE CLASIFICACIÓN-----')
print('--------------------------------------------')

#CLASIFICACIÓN
PacienteCar=input("Nombre de archivo de caracteristicas?: ")
Caracteristicas=PacienteCar + '.csv'
MeanRR=input('Ingrese el Mean RR: ')
SDNN=input('Ingrese el SDNN: ')
RMSSD=input('Ingrese el RMSSD: ')
TINN=input('Ingrese el TINN: ')
VLF=input('Ingrese el VLF: ')
LF=input('Ingrese el LF: ')
HF=input('Ingrese el HF: ')
Divi=input('Ingrese el LF/HF: ')
print("CARGANDO RED")
modelo_nuevo=joblib.load('modelo_entenadoregresion_elmejor.pkl')
print("RED CARGADA")
data = { 'Mean RR':[float(MeanRR)], 'SDNN':[float(SDNN)], 'RMSSD': [float(RMSSD)], 'TINN': [float(TINN)], 'VLF': [float(VLF)], 'LF': [float(LF)], 'HF': [float(HF)], 'LF/HF': [float(Divi)]};
dataframe = pd.DataFrame(data, columns = ['Mean RR', 'SDNN', 'RMSSD', 'TINN', 'VLF', 'LF', 'HF','LF/HF'])
X_test=(dataframe[["Mean RR","SDNN","RMSSD","TINN","VLF","LF","HF","LF/HF"]])
print(X_test)
nueva_predic=modelo_nuevo.predict(X_test)
X_test.to_csv('caracteristicas.csv', header=False, index=False)

print('\n')

print('-----PARA VISUALIZAR LOS DATOS POR FAVOR INGRESE A LA PAGINA WEB DEL Y CARGUE LA SEÑAL PARA OBSERVAR EL DIAGNÓSTICO-----')

#########################

#ENVIO DE DATOS

print("----ENVIANDO DIAGNOSTICO AL SERVIDOR-----")
serialArduino = serial.Serial('COM3',9600)
def enviar_dato(valor):
    '''Esta función recoge el valor a enviar hacia el arduino
    '''
    if valor ==1:
        cad = str(valor) #+ ","+ str(mot)
        serialArduino.write(cad.encode('ascii')) 
    elif valor==0:
        cad = str(valor) #+ ","+ str(mot)
        serialArduino.write(cad.encode('ascii')) 
    else:
        serialArduino.close()



enviar_dato(nueva_predic)
print("-----DIAGNOSTICO ENVIADO-----")
Salir=input('Presione cualquier letra y después enter para salir: ')


