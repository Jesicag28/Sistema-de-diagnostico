import sys 
from PyQt5.QtWidgets import QApplication,QDialog, QButtonGroup, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtCore import QDate
from PyQt5.uic import loadUi
import matplotlib.pyplot as plt
# biblioteca para la generacion de graficas a partir de datos contenidas en arrays  o list 
import smtplib
class Sistema(QDialog):
    def __init__(self):
        super(Sistema, self).__init__()
        loadUi('IRA_principal.ui', self)
        #Boton para ingresar un paciente al sistema
        self.ingresar_paciente=IngresarP()
        self.ipaciente.clicked.connect(self.boton)
        #Boton para eliminar un paciente al sistema
        self.eliminar_paciente=EliminarP()
        self.epaciente.clicked.connect(self.boton1)
        #Boton para ver el historial de un paciente registrado en el sistema
        self.historial1= Historial()
        self.historial.clicked.connect(self.boton2)
        #Boton para consultar el diagnostico de un paciente registrado en el sistema
        self.consultarDiagnostico= cDiagnostico()
        self.diagnostico1.clicked.connect(self.iDiagnostico)
        #Boton para graficar las estadisticas del  sistema
        self.grafican= Grafica()
        self.grafica.clicked.connect(self.graficar1)

    def boton(self):
        self.ingresar_paciente.show()
    def boton1(self):
        self.eliminar_paciente.show()
    def boton2(self):
        self.historial1.show()
    def iDiagnostico(self):
        self.consultarDiagnostico.show()
    def graficar1(self):
        self.grafican.show()
    

class IngresarP(QDialog):
    # Se lanza a partir de un constructor la ventana -infopaciente.ui- para llenar los campos 
    # de un paciente nuevo para el sistema 
    def __init__(self):
        super(IngresarP, self).__init__()
        loadUi('informacionPaciente.ui', self)
        #Se define una varible para el cliqueo de la ventana conectada al metodo on_clicked
        iok=self.ok.clicked.connect(self.on_clicked)
        self.cancel.clicked.connect(self.Cancel)
        # setValidator ayuda a que los campos no puedan ingresar letras
        self.pcedula.setValidator(QtGui.QDoubleValidator())
        self.peso.setValidator(QtGui.QDoubleValidator())
        self.fc.setValidator(QtGui.QDoubleValidator())
        self.p=QButtonGroup()
        self.p.addButton(self.femenino)
        self.p.addButton(self.masculino)
        self.Fecha.setDate(QDate().currentDate())
        
        self.mi_paciente = None;
        if iok:
        # si se cliquea ok se hace el borrado de todos los campos    
            self.pnombre.setText('')
            self.pcedula.setText('')
            self.peso.setText('')
            self.fc.setText('')
            self.p.setExclusive(False)
            self.femenino.setChecked(False)
            self.masculino.setChecked(False)
            self.infante.setChecked(False)
            self.joven.setChecked(False)
            self.adulto.setChecked(False)
            self.anciano.setChecked(False)
            self.p.setExclusive(True)
        else:
        #si los campos siguen vacios y no se ha dado click se muestra el siguiente label
            self.mensaje.setText('Para guardar los campos haga click en OK')
    #Si se da click en cancel los campos se borran 
    def Cancel(self):
        self.p.setExclusive(False)
        self.femenino.setChecked(False)
        self.masculino.setChecked(False)
        self.infante.setChecked(False)
        self.joven.setChecked(False)
        self.adulto.setChecked(False)
        self.anciano.setChecked(False)
        self.p.setExclusive(True)
#funcion que retorna la edad segun el chequeo que se realice para el ingreso de un paciente
    def edad(self):
        if self.infante.isChecked():
            Edad='Infante'
        elif self.joven.isChecked():
            Edad='Joven'
        elif self.adulto.isChecked():
            Edad='Adulto'
        elif self.anciano.isChecked():
            Edad='Anciano'
        else:
            Edad=''
        return Edad
    #si genero es chequeado entonces se retorna un genero para el conteo de los pacientes, que la vez sirve
    #para el ingreso
    def Fechaf(self):
        return str(self.Fecha.date().toPyDate())
# funcion para retornar el tipo de genero una vez chequeado y asi se captura para el
# ingreso de un paciente al sistema    
    def genero(self):
            if self.femenino.isChecked():
                Genero='Femenino'
            elif self.masculino.isChecked():
                Genero= 'Masculino'
            else:
                Genero=''
            return Genero
        
    def on_clicked(self):
        Cedula=self.pcedula.text()
        e=medico.existePaciente(Cedula)
        if e==False:
            Nombre=self.pnombre.text()
            Peso=self.peso.text()
            Genero= self.genero()
            fcardiaca=self.fc.text()
            Edad= self.edad()
            Fecha= self.Fechaf()
            if Nombre=='' or Peso== ''or Genero=='' or Cedula=='' or Edad=='':
                QMessageBox.about(self, 'Aviso', '*Faltan datos obligatorios')
            else:
                #Se utiliza la clase Paciente que recibe cada uno de los atributos para que un 
                #medico pueda ingresarlo al sistema
                paciente=Paciente(Nombre, Cedula, Peso, Genero,  fcardiaca,Edad, Fecha)
                #se utiliza la clase medico con el metodo de ingresarPaciente correspondiente 
                #para que puedar ser ingresado al sistema 
                resultado=medico.ingresarPaciente(paciente)
                #Se retorna la funcion ingresarPaciente a partir de un setText 
                if resultado =='Paciente ha sido ingresado':
                    QMessageBox.about(self, 'Aviso', resultado)
                    resultado=paciente
                    self.sintomas=Sintomas(resultado)
                    self.continuar.clicked.connect(self.boton2)
                else:
                    self.continuar.clicked.connect(self.aviso)
                self.mi_paciente = resultado
                return resultado 
      
        else:
            #si la cedula del paciente ya existe una vez clickeado ok le va mostrar que la cedula ya existe 
            #en el sistema 
            QMessageBox.about(self, 'Aviso', 'El paciente ya esta registrado en el sistema')
        self.p.setExclusive(False)
        self.femenino.setChecked(False)
        self.masculino.setChecked(False)

        self.infante.setChecked(False)
        self.joven.setChecked(False)
        self.adulto.setChecked(False)
        self.anciano.setChecked(False)
        self.p.setExclusive(True)
    
        self.pnombre.setText('')
        self.pcedula.setText('')
        self.peso.setText('')
        self.fc.setText('')
#Se muestra la ventana de sintomas que permite chequearlos a partir de otra ventana que se genera
    def boton2(self):
        self.sintomas.show()
#    ventana emergente para el aviso de faltan datos 
    def aviso(self):
        QMessageBox.about(self, 'Aviso1', 'Falta datos obligatorios ')
        
class EliminarP(QDialog):
    #Se crea la clase EliminarP que va generar  una ventana con el fin de eliminar un paciente del sistema
    def __init__(self):
        super(EliminarP, self).__init__()
        loadUi('eliminarpac.ui', self)
        self.ok1.clicked.connect(self.on_clicked2)
        self.cancel2.clicked.connect(self.cancel)
        self.cedulape.setValidator(QtGui.QDoubleValidator())
    def on_clicked2(self):
        Cedula=self.cedulape.text()
        if Cedula=='':
           QMessageBox.about(self, 'Aviso1', 'Falta datos obligatorios ')
        else:
            e=medico.existePaciente(Cedula)
            if e:
                #Se utiliza el metodo eliminarPaciente de la clase Medico para poder eliminar un paciente
                # del sistema a partir de una cedula 
                eliminado=medico.eliminarPaciente(Cedula)
                QMessageBox.about(self, 'Aviso1', eliminado)
                # se le retorna al medico que el paciente ha sido eliminado del sistema 
            else:
                QMessageBox.about(self, 'Aviso1', 'El paciente no esta en el sistema ')
        self.cedulape.setText('')
    def cancel(self):
        # se borran los campos del label emensaje  
        self.emensaje.setText('')
class Sintomas(QDialog):
    def __init__(self,p):
        super(Sintomas, self).__init__()
        loadUi('sintomas.ui', self)
        self.ok1.clicked.connect(self.Sintomasp)
        self.resultados = []
        self.paciente = p;
        self.ok1.clicked.connect(self.boton)
#Se define una funcion para capturar los sintomas que puede presentar un paciente
#con la finalidad de mostrar que diagnostico y tratamiento se puede generar de acuerdo a un chequeo
    def Sintomasp(self):
        sintomas=[]
        if self.tos.isChecked():
            sintomas.append('Tos')
        if self.rinorrea.isChecked():
            sintomas.append('Rinorrea')
        if self.exudado.isChecked():
            sintomas.append('Exudado purulento en faringe')
        if self.fiebre.isChecked():
            sintomas.append('Fiebre')
        if self.otalgia.isChecked():
            sintomas.append('Otalgia')
        if self.otorrea.isChecked():
            sintomas.append('Otorrea')
        if self.disfonia.isChecked():
            sintomas.append('Disfonia')
        if self.odinofagia.isChecked():
            sintomas.append('Odinofagia')
        if self.taquipnea.isChecked():
            sintomas.append('Taquipnea')
        if self.drespiratoria.isChecked():
            sintomas.append('Dificultad respiratoria')
        if self.tiraje.isChecked():
            sintomas.append('Tiraje')
        if self.cianosis.isChecked():
            sintomas.append('Cianosis')
        if self.hipotermia.isChecked():
            sintomas.append('Hipotermia')
        if self.ninguno.isChecked():
            sintomas.append('No presenta ningun sintoma')
            
            
        if 'Tos' in sintomas and  'Rinorrea' in sintomas and  'Exudado purulento en faringe' in sintomas and  'Fiebre' in sintomas and' Otalgia' in sintomas and 'Otorrea' in sintomas and 'Disfonia' in sintomas and'Odinofagia'in sintomas and'Dificultad respiratoria' or 'Tiraje' in sintomas or 'Hipotermia' in sintomas or 'Cianosis' in sintomas:
            Diagnostico='El paciente presenta IRA con neumonia grave'
            Tratamiento='Envio inmediato al hospital mas cercano'+ '\n'+'Traslado con oxigeno si es necesario: 4 a 6 litros por mn'
        elif 'Taquipnea'  in sintomas:
            Diagnostico='El paciente presenta IRA con neumonia leve'
            Tratamiento='Tratamiento ambulatorio'+ '\n'+'Anbiotico cada 12h por 7 dias:trimetoprim con sulfametoxasol '+ '\n'+'Controlar temperatura'+ '\n'+'Revalorar en 24h o antes si se agrava'
        elif 'Odinofagia' in sintomas and 'Taquipnea' not in sintomas:
            Diagnostico='El paciente presenta IRA sin neumonia'
            Tratamiento='Incrementar ingesta de liquidos'+ '\n'+'Si hay otorrea realizar limpieza del conjunto auditivo externo'+ '\n'+'Control del dolor y malestar:Acetamonofen-via oral'+ '\n'+'No utilizar antitusivos'
        else:
            Diagnostico='El paciente no presenta ningun grado de complicacion respiratoria'
            Tratamiento='Para prevenir IRA se aconseja lo siguiente '+ '\n'+'Tomar abundantes liquidos'+ '\n'+'Evitar el hacinamiento'+ '\n'+'Evitar cambios bruscos de temperatura '+'\n'+'No fumar cerca de los ninos'
        Sintomas='\n'.join(sintomas)
# se utiliza join en la lista sintomas para que cuando muestre lo haga de forma ordenada
        resultadosf=[Sintomas,Diagnostico,Tratamiento]
        self.resultados = resultadosf 
#se retorna una lista que va almacenar los datos de sintomas, diagnostico y tratamiento dentro 
#de una lista que nos va servir para enviar la informacion a un correo cuando se muestre la ventana de resultados
        return resultadosf 
    def boton(self):
        resultadosf= self.Sintomasp()
        if resultadosf[0]=='':
            QMessageBox.about(self, 'AVISO', 'Ingrese al menos un sintoma')
        else:
# Se llama la funcion DiagnosticoP que tiene la informacion del resultado evaluado para ser enviado
# a un correo 
            self.diagnostico=DiagnosticoP(self.paciente,self.resultados)
            self.diagnostico.show()
              
class DiagnosticoP(QDialog):
#Se lanza la ventana de Diagnostico que recibe un resultado, que contiene sintomas, tratamiento y diagnostico
# y se conecta con la funcion de enviar que crea archivos de texto guardados con la cedula del paciente
    def __init__(self, paciente,resultados):
        super(DiagnosticoP, self).__init__()
        loadUi('resultado.ui', self)
        self.consultar1.clicked.connect(self.on_clicked3)
        self.enviar.clicked.connect(self.Enviar)
        self.__resultados = resultados
        self.__paciente = paciente
    def getResultado(self):
        return self.__resultados
    def ver(self):
#Se toma toda la informacion del paciente que se esta ingresando para enviar al correo 
        infopaciente=self.__paciente
        datosintomas=self.__resultados
        datosintomas1= 'Sintomas que presenta:'+str(datosintomas[0])+'\n'+'Grado de complicacion:'+str(datosintomas[1])+'\n'+'Tratamiento:'+str(datosintomas[2])+'\n'
        informacion= 'Fecha:' + infopaciente.getFecha() + '\n' + 'Nombre:'+ infopaciente.getNombre()+'\n' +'Cedula:'+ infopaciente.getCedula()+'\n'+'Peso:'+ infopaciente.getPeso()+'\n'+'Genero:'+ infopaciente.getGenero()+ '\n'+'Frecuencia cardiaca:'+infopaciente.getFrecuencia()+ '\n'+'Edad:'+infopaciente.getEdad()
        historial= 'INFORMACION DEL PACIENTE'+'\n'+informacion+'\n'+'RESULTADOS'+'\n'+datosintomas1
        return historial
# se muestra en label toda la informacion de resultados para luego ser enviada   
    def on_clicked3(self):
        sintomas = self.__resultados
        self.resgrado.setText(str(sintomas[1]))
        self.ressintomas.setText(str(sintomas[0]))
        self.tratamiento_2.setText(str(sintomas[2]))
#Se guarda toda la informacion del paciente en un archivo de texto que va ser único para cada paciente
# cada vez que se le diagnostique algun sintoma con sus debidos resultados 
    def generarArchivo(self, ncedula, datos):
        file = open(str(ncedula)+'.txt', 'a')
        file.writelines('\n'+ datos)
        file.close()
#Se crea la funcion enviar que va permitirle mandar toda la informacion de acuerdo a los resultados obtenidos
#al paciente, tomados de un archivo de tipo txt
    def Enviar(self):
        datos=self.ver()
        correopaciente= self.correo1.text()
        if correopaciente=='':
            QMessageBox.about(self, 'Aviso', '*Faltan datos obligatorios')
        else:

            cedula2=self.__paciente.getCedula()
            self.generarArchivo(cedula2,datos)
            files = open(str(cedula2)+'.txt', 'r')
            files = files.readlines()
            files = ''.join(datos)
            SUBJECT= 'DIAGNOSTICO SISTEMA IRA'
            msg = '''Subject: {}
{}'''.format(SUBJECT, files)
    #            msg =  '''
    #{} '''.format(files)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            servidor=self.correo.currentText()
            if servidor == '@udea.edu.co' :
                
                correopaciente= correopaciente+ '@udea.edu.co'
            elif servidor== '@gmail.com':
            
                correopaciente= correopaciente+ '@gmail.com'
            elif servidor== '@hotmail.com':
                
                correopaciente= correopaciente+ '@hotmail.com'
            else:
                 QMessageBox.about(self, 'Aviso', 'Elija un servidor ')
            server.starttls()   
            server.login("jesica.gil@udea.edu.co", "jesicagg0298") #correo y contrasena
            server.sendmail("jesica.gil@udea.edu.co", correopaciente ,msg)
            server.quit()
            QMessageBox.about(self, 'Aviso', 'envio exitoso')
#Se define una funcion historial con el objetivo de poder ver toda la informacion de un paciente
# en el proceso clinico que ha tenido, de acuerdo a fecha, y cambio de datos sin modificacion de cedula            
class Historial(QDialog):
    def __init__(self):
        super(Historial, self).__init__()
        loadUi('historial_cedula.ui', self)
        self.consultar.clicked.connect(self.onClicked4)
        self.pcedula.setValidator(QtGui.QDoubleValidator())
    def onClicked4(self) :
        Cedula=self.pcedula.text()
        e=medico.existePaciente(Cedula)
        if e==False:
            QMessageBox.about(self, 'Aviso', 'El paciente no se encuentra en el sistema')
        else:
            Datos1=medico.verPaciente(Cedula)
            cedula1= Datos1.getCedula()
            datos=self.abrir(cedula1)
            QMessageBox.about(self, 'Historial del paciente', str(datos))
#Se abre un archivo para mirar su informacion y asi poderla arrojar a una ventana emergente 
    def abrir(self,cedula):
        archivo=open(str(cedula)+'.txt')
        informacion=archivo.readlines()
        informacion = [element[:-1] for element in informacion]
        return '\n'.join(informacion)
#Se crea la funcion de grafica que permite conocer las estadisticas de los pacientes
#en sistema de acuerdo a un rango de edad para ver que porcentaje de personas 
#tienen mas avances en la enfermedad 
class Grafica(QDialog):
    def __init__(self):
        super(Grafica, self).__init__()
        loadUi('Grafico.ui', self)
        self.mostrar.clicked.connect(self.on_clicked)
    def on_clicked(self):
        fig= plt.figure()
        ax= fig.add_subplot(111)
        datos=medico.contarEdad()
        xx= range(len(datos))
#   Los datos que tomo para graficar es segun la poblacion que tenga IRA de acuerdo a la enfermedad
        pacientes=['Infante', 'Joven', 'Adulto', 'Anciano']
        ax.bar(xx, datos, width= 0.5, color='blue', align='center')
        ax.set_xticks(xx)
        ax.set_xticklabels(pacientes)
        plt.xlabel('\n'+'EDAD DE LOS PACIENTES')
        plt.ylabel('NUMERO DE LOS PACIENTES ENFERMOS ')
        plt.title('POBLACION IRA SEGUN EDAD')
        grafico=plt.savefig('Correlacion')
        grafico=plt.show()
        return grafico
#se crea la clase de Diagnostico para que una vez haya sido 
# ingresado un paciente se le pueda seguir ingresando diagnosticos y van a ser guardada la informacion
# en el mismo documento de tipo txt para llevar un registro
class cDiagnostico(QDialog):
    def __init__(self):
        super(cDiagnostico, self).__init__()
        loadUi('ingresarDiagnostico.ui',self)
        self.okd.clicked.connect(self.ingresodiag)
        self.ceduladiag.setValidator(QtGui.QDoubleValidator())
    def ingresodiag(self):
        cedula= self.ceduladiag.text()
        e=medico.existePaciente(cedula)
        if e==False:
            QMessageBox.about(self, 'Aviso', 'La cedula ingresada no esta en el sistema')
        else:
            paciente=medico.verPaciente(cedula)
            self.sintomas=Sintomas(paciente) 
            informacion= self.sintomas
            self.sintomas.show()
            return informacion
    def historial(self):
        cedula= self.ceduladiag.text()
        paciente=medico.verPaciente(cedula)
        historial=self.ingresodiag()
        Historial= medico.agregarHistorial(historial,paciente.getCedula())
        archivo=open(str(cedula)+'.txt','a')
        archivo.writelines('\n'+ Historial)
        archivo.close()
        
        
class Paciente():
    #el constructor recibe como argumentos cedula, nombre, peso, genero y antecedentes de un paciente
    def __init__(self, nombre, cedula, peso, genero, fc, edad, fecha):
        self.__nombre=nombre
        self.__cedula=cedula
        self.__peso=peso
        self.__genero=genero
        self.__fc=fc
        self.__edad=edad
        self.__historial={} 
        self.__fecha= fecha
#    se define los get() de cada uno de los atributos de un paciente    
    def getFecha(self):
        return self.__fecha
    def getNombre(self):
        return self.__nombre
    def getCedula(self):
        return self.__cedula
    def getPeso(self):
        return self.__peso
    def getGenero(self):
        return self.__genero
    def getComplicacion(self):
        return self.__gcomplicacion
    def getFrecuencia(self):
        return self.__fc
    def getEdad(self):
        return self.__edad
    def getHistorial(self):
        return self.__historial 
#    se define el set de un histroial 
    def setHistorial(self,historial):
        self.__historial=historial
        
        
class Medico():
    def __init__(self):
        self.__lista_pacientes={}
    def ingresarPaciente(self,pac):
#Para anadir un paciente a la lista de pacientes se toma la cedula
#Esta sera la llave del diccionario de lista_pacientes
        self.__lista_pacientes[pac.getCedula()] =pac
        return 'Paciente ha sido ingresado'
#La funcion existePaciente sirve para verificar que un paciente este en la lista de pacientes
#Esta funcion es necesaria para agregar un medicamento a un paciente
    def existePaciente(self,cedula):
        existe=False
        if cedula in self.__lista_pacientes:
            existe = True
        return existe
#Se define la funcion para eliminar un paciente
#recibe como argumento la cedula del paciente a eliminar    
    def verPaciente(self,cedula):
    #Inicialmente se verifica que la cedula exista en la lista de pacientes
            return self.__lista_pacientes[cedula]
        
    def eliminarPaciente(self,cedula):
#        existe = cedula in self.__lista_pacientes;
        if cedula in self.__lista_pacientes.keys():
            del self.__lista_pacientes[cedula];
            return 'Paciente ha sido eliminado' 
        else:
            return 'Paciente no existe'
    def agregarHistorial(self,historial, cedula):
        if cedula in self.__historial:
            self.__historial[cedula].setHistorial(historial)
            historial=self.__lista_pacientes[cedula].getHistorial()
        return 'HISTORIAL PACIENTE' +'\n'+ str(historial)
    def contarEdad(self):
        cedula= list(self.__lista_pacientes.keys())# captura las cedulas como una lista 
        cont = 0 #Variable auxiliar para recorrer la lista de cedulas de pacientes
        contj=0
        contad=0
        conta=0
        for i in range(0,len(cedula)):
            cedula1=  cedula[i]
            edad1=self.__lista_pacientes[cedula1].getEdad() #Por cada paciente en la lista, toma el genero 
            if edad1 == 'Infante': 
                cont += 1 #Cada que encuentra que un paciente es mujer, suma 1 al contador
            if edad1== 'Joven':
                contj += 1
            if edad1== 'Adulto':
                contad +=1
            if edad1== 'Anciano':
                conta +=1

        infante= cont
        joven= contj
        adulto= contad
        anciano= conta
        edad=[infante,joven,adulto,anciano]
        return edad
medico=Medico()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Sistema()
    widget.show()
    app.exec_()
    
