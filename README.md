# Invest Simulator

Aplicación web orientada al público general que simula inversiones en tiempo real.

# Integrantes:

- Rodrigo Lucero
- Agustin Gomez
- Igor Andruskiewitsch
- Marco Martinelli
- Federico Rivero
- Alexis Guerra

# Instalacion:
Requisitos previos:
- Homebrew.
- Git.
- Python 3.6/3.7.  

Se deben seguir los siguientes pasos, ejecutando cada comando en la terminal:
#### 1. Clonar repositorio de la aplicacion:
```
mkdir investsimulator
cd investsimulator
git clone https://gitlab.com/LocosXelAsado/investsimulator.git
```
#### 2. Instalar virtualenv:
En linux: 
```
sudo apt-get install python3-pip
sudo pip3 install virtualenv 
```
En MacOS:
```
brew install virtualenv
pip3 install virtualenv
```
#### 3. Crear entorno virtual:
```
virtualenv venv
```
#### 4. Activar entorno virtual:
```
source ./venv/bin/activate
```
#### 5. Instalar requerimientos:
```
pip3 install requirements.txt
```
Esto instalara los siguientes paquetes:
   - **Django==2.1.2**
   - **ipython==7.0.1**
   - **urllib3==1.23**    
   - **pillow**
   - **coverage**
#### 6. Activar el servidor:
```
python3 manage.py runserver
```