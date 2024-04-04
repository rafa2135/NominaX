#main.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import widget_creator
import database_manager
import pyodbc
import re
from decimal import Decimal

#constantest
BA = Decimal('0.4')     # 40% del salario base
BP = Decimal('0.6')     # 60% del salario base
SSO = Decimal('0.02')   # 2% del salario base
SHCM = Decimal('0.15')  # 15% del salario base
root = tk.Tk()

#funciones

def insert_db(empleados_data, bonos_data):
    
    try:
        with database_manager.connect() as conn:
            if conn:
                completado = database_manager.insert_data(conn, empleados_data, bonos_data)
               
            if completado:
                messagebox.showinfo("Añadido","El usuario fue Añadido")   
                return True         
    except pyodbc.IntegrityError as e:  
        tipo_error = type(e).__name__
        mensaje_error = errores.get(tipo_error, "Error desconocido")
        messagebox.showerror("Error de inserción", mensaje_error) 
    except pyodbc.Error as e:                
        tipo_error = type(e).__name__
        mensaje_error = errores.get(tipo_error, "Error desconocido")
        messagebox.showerror("Error de inserción", mensaje_error)    
    except Exception as e:             
        tipo_error = type(e).__name__
        mensaje_error = errores.get(tipo_error, "Error desconocido")
        messagebox.showerror("Error de inserción", mensaje_error)       

def modificar_db(empleados_data, bonos_data):    
    try:
        
        with database_manager.connect() as conn:
            if conn:
                completado = database_manager.update_data(conn, empleados_data, bonos_data)               
            if completado:
                messagebox.showinfo("Modificado","El usuario fue modificado correctamente")   
                return True  
            else:
                messagebox.showerror("Error","la cedula no existe en la base de datos")       
    except pyodbc.IntegrityError as e:    
        tipo_error = type(e).__name__
        mensaje_error = errores.get(tipo_error, "Error desconocido")
        messagebox.showerror("Error de modificación", mensaje_error) 
    except pyodbc.Error as e:               
        tipo_error = type(e).__name__
        mensaje_error = errores.get(tipo_error, "Error desconocido")
        messagebox.showerror("Error de modificación", mensaje_error)    
    except Exception as e:              
        tipo_error = type(e).__name__
        mensaje_error = errores.get(tipo_error, "Error desconocido")
        messagebox.showerror("Error de modificación", mensaje_error)  

def borrar_db(cedula): #funcion para conectar y borrar un usuario
    conn=database_manager.connect()
    if conn:
        compledado=database_manager.borrar_usuario(conn,cedula)

        if compledado:
            messagebox.showinfo("completado","El usuario fue borrado")
            mostrar_datos()            
        else:
            messagebox.showerror("Error", "El usuario no existe en la base de datos.")            
          #cerrar coneccion
        database_manager.close_connection(conn)
    else:
        messagebox.showerror("Error", "coneccion fallida.")
        

def validate_input(empleados_data): #validando data
    cedula = empleados_data[0][0]
    nombre = empleados_data[0][1]
    apellido = empleados_data[0][2]
    seguro_social = empleados_data[0][3]
    seguro_hcm = empleados_data[0][4]
    sueldo_basico = empleados_data[0][5]

    # Validando campos vacíos
    if '' in (cedula, nombre, apellido, seguro_social, seguro_hcm, sueldo_basico):
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return False
    # Validando cedula
    if not (cedula.isdigit() and 6 <= len(cedula) <= 10):
        messagebox.showerror("Error", "Cedula tiene que ser un numero entero y con mas de 6 characteres")
        return False
    # Validando nombre
    if len(nombre) > 50:
        messagebox.showerror("Error", "Nombre debe tener 50 caracteres como máximo.")
        return False
    
    # Validando apellido
    if len(apellido) > 50:
        messagebox.showerror("Error", "Apellido debe tener 50 caracteres como máximo.")
        return False
    
    # Validando seguro_social
    if not seguro_social.isdigit():
        messagebox.showerror("Error", "Seguro Social debe ser un número entero.")
        return False
    
    # Validando seguro_hcm
    if len(seguro_hcm) > 50:
        messagebox.showerror("Error", "Seguro HCM debe tener 50 caracteres como máximo.")
        return False
    if not re.match(r'^\d{1,8}(\.\d{1,2})?$', str(sueldo_basico)):
        messagebox.showerror("Error", "Sueldo Basico debe tener menos de  10 characteres y maximo 2 decimales.")
        return False
    return True
    
def get_insert_data():    #get datos del usuario y insertar on la db    
    cedula = cedula_entry.get()    
    sueldo_basico = sueldo_basico_entry.get()
    empleados_data = [
        (cedula, nombre_entry.get(), apellido_entry.get(),seguro_social_entry.get(), seguro_hcm_entry.get(),sueldo_basico)
    ]    
    if not validate_input(empleados_data):
        return
    bonos_data=calculo_bonos(cedula,float(sueldo_basico))    
    if insert_db(empleados_data, bonos_data):   
        mostrar_datos()

def get_persona_data():    #get datos del usuario y insertar on la db    
    cedula = str(cedula_frame.cget("text"))  
    sueldo_basico = sueldo_basico_frame.get()
    empleados_data = [
        (cedula, nombre_frame.get(), apellido_frame.get(),seguro_social_frame.get(), seguro_hcm_frame.get(),sueldo_basico)
    ]    
    if not validate_input(empleados_data):
        return
    bonos_data=calculo_bonos(cedula,float(sueldo_basico))   
    modificar_db(empleados_data, bonos_data)   
    mostrar_datos()
    
   
def get_borrar_data():      # get cedula para borrar usuario
    cedula=borrar_cedula_entry.get()
    # Validating cedula
    if not (cedula.isdigit() and 6 <= len(cedula) <= 10):
        messagebox.showerror("Error", "Cedula tiene que ser un numero entero y con mas de 6 characteres")
        return False    
    borrar_db(cedula)

def calculo_bonos(cedula, sueldo):
    sueldo_decimal = Decimal(str(sueldo))  # Convertir sueldo a Decimal
    bonos_data = [
        (cedula, sueldo_decimal * BP, sueldo_decimal * BA)        
        # Añade más datos según sea necesario
    ]
    return bonos_data

def calcular_sueldo_neto(sueldo_base): #calcular sueldo neto
    sueldo_bonos = sueldo_base * (Decimal('1') + BA + BP)
    sueldo_descuentos = sueldo_base * (SSO + SHCM)
    sueldo_neto= sueldo_bonos-sueldo_descuentos
    return sueldo_neto

def mostrar_datos():  
    conn = database_manager.connect()
    data = database_manager.fetch_todo(conn)
    
    if data:
        # Limpiar cualquier dato anterior del treeview
        for item in treeview.get_children():
            treeview.delete(item)

        # Insertar los nuevos datos limpios en el treeview
        for row in data:
            sueldo_basico = Decimal(row[3])
            sueldo_neto = calcular_sueldo_neto(sueldo_basico)
            row_with_sueldo_neto = tuple(row) + (sueldo_neto,)
            clean_row = [str(item).strip("(),'") if not isinstance(item, Decimal) else item for item in row_with_sueldo_neto]
            treeview.insert('', 'end', values=clean_row)

def bucar_persona():
    cedula=buscar_persona_entry.get()    
    if not (cedula.isdigit() and 6 <= len(cedula) <= 10):
        messagebox.showerror("Error", "Cedula tiene que ser un numero entero y con mas de 6 characteres")
        return False    
    cedula = int(cedula) 
    conn=database_manager.connect()
    data=database_manager.fetch_persona(conn,cedula)
    if data:
        #assignar los valores     
        cedula_frame.config(text=cedula)   
        nombre_frame.delete(0, "end")
        nombre_frame.insert(0, data[0][0])

        apellido_frame.delete(0, "end")
        apellido_frame.insert(0, data[0][1])
        
        seguro_social_frame.delete(0, "end")
        seguro_social_frame.insert(0, data[0][2])
        
        seguro_hcm_frame.delete(0, "end")
        seguro_hcm_frame.insert(0, data[0][3])

        sueldo_basico_frame.delete(0, "end")
        sueldo_basico_frame.insert(0, data[0][4])

        bono_productividad_frame.config(text=data[0][5])

        bono_alimentacion_frame.config(text=data[0][6])

        sueldo_base=Decimal(data[0][4])
        sueldo_neto_frame.config(text=calcular_sueldo_neto(sueldo_base))

        #calculando SHCM y SSO y sueldo neto
        shcm=sueldo_base*SHCM
        sso=sueldo_base*SSO

        shcm_frame.config(text=shcm)

        sso_frame.config(text=sso)     
    
        return True
    else:
        messagebox.showerror("error","esta cedula no se encuentra en la base de datos")

def modificar_persona():    
    get_persona_data()

def limpiar_datos():

    cedula_frame.config(text="")
    nombre_frame.delete(0, 'end')
    apellido_frame.delete(0, 'end')
    seguro_social_frame.delete(0, 'end')
    seguro_hcm_frame.delete(0, 'end')    
    bono_productividad_frame.config(text="")
    bono_alimentacion_frame.config(text="")
    shcm_frame.config(text="")
    sso_frame.config(text="")
    sueldo_basico_frame.delete(0, 'end')    
    sueldo_neto_frame.config(text="")

    nombre_entry.delete(0, 'end')
    apellido_entry.delete(0, 'end')
    cedula_entry.delete(0, 'end')
    seguro_social_entry.delete(0, 'end')
    seguro_hcm_entry.delete(0, 'end')
    sueldo_basico_entry.delete(0, 'end')

errores = {
    "IntegrityError": "No se puede insertar un usuario con una cédula que ya existe en la base de datos.",
    "Error de conexión": "No se pudo conectar a la base de datos.",
    "Error desconocido": "Se produjo un error desconocido al insertar el usuario.",
}
#set style
            
root.tk.call("source","forest-dark.tcl")
ttk.Style().theme_use('forest-dark')

#set main frame
frame = ttk.Frame(root)
frame.pack()


#setup left widget
left_frame = ttk.Frame(frame,padding=(5,5),relief="solid")
left_frame.grid(row=0,column=0,pady=5)

# set up lable
insert_frame=ttk.LabelFrame(left_frame,text="insertar")
insert_frame.grid(row=0,column=0,pady=5)

#setup widgets para insert 
# Nombre entry
nombre_entry = widget_creator.create_entry_widget(insert_frame,"Nombre",0,0)

# Apellido entry
apellido_entry = widget_creator.create_entry_widget(insert_frame,"Apellido",1,0)

# Cedula entry
cedula_entry = widget_creator.create_entry_widget(insert_frame,"Cedula",2,0)

# Seguro Social entry
seguro_social_entry = widget_creator.create_entry_widget(insert_frame,"Seguro Social",3,0)

# Seguro HCM entry
seguro_hcm_entry = widget_creator.create_entry_widget(insert_frame,"Seguro HCM",4,0)

# Sueldo Basico entry
sueldo_basico_entry = widget_creator.create_entry_widget(insert_frame,"Sueldo Basico",5,0)

# Button get input
insert_button= widget_creator.create_button(insert_frame,"Añadir",get_insert_data,6,0)

# setup widgets para borrar persona
# lable para borrar persona
borar_frame=ttk.LabelFrame(left_frame,text="Borrar")
borar_frame.grid(row=1,column=0,pady=5)
# entry para borrar persona
borrar_cedula_entry = widget_creator.create_entry_widget(borar_frame,"Cedula",0,0)
# Button para borrar persona
borrar_button= widget_creator.create_button(borar_frame,"Borrar",get_borrar_data,1,0)

# Button mostrar todo
widget_creator.create_button(left_frame,"Buscar todo",mostrar_datos,7,0)


# setup widgets para Buscar persona
# lable para Buscar persona
buscar_persona_frame=ttk.LabelFrame(left_frame,text="Buscar Persona")
buscar_persona_frame.grid(row=2,column=0,pady=5)
#entry para Buscar persona
buscar_persona_entry=widget_creator.create_entry_widget(buscar_persona_frame,"Cedula",0,0)
#button para buscar persona
buscar_persona_button=widget_creator.create_button(buscar_persona_frame,"Buscar persona",bucar_persona,1,0)

# Set right widget
right_frame = ttk.Frame(frame, padding=(5, 5), relief="solid")
right_frame.grid(row=0, column=1,)

#setup buscar todo frame
buscar_todo_frame=ttk.Frame(right_frame,padding=(5,5),relief="solid")
buscar_todo_frame.pack()
# Scrollbar
right_scrollbar = ttk.Scrollbar(buscar_todo_frame)
right_scrollbar.pack(side="right",fill="y")
# Table data
colm_nombres = ["Cedula", "Nombre", "Apellido", "Sueldo Básico", "Bono Productividad","sueldo neto"]
# Treeview
treeview = ttk.Treeview(buscar_todo_frame,show="headings", columns=colm_nombres,height=10,yscrollcommand=right_scrollbar.set)
treeview.pack()
# Insert column headings
for col in colm_nombres:
    treeview.heading(col, text=col,anchor=tk.W)
# configurando espacio
treeview.column("Cedula",width=70)
treeview.column("Nombre",width=90)
treeview.column("Apellido",width=90)
treeview.column("Sueldo Básico",width=90)
treeview.column("Bono Productividad",width=120)
treeview.column("sueldo neto",width=80)

#set up mostrar buscar persona frame
buscar_persona_frame=ttk.Frame(right_frame,padding=(5,5),relief="solid")
buscar_persona_frame.pack()
#cedula
cedula_frame=widget_creator.create_frame_widget(buscar_persona_frame,"Cedula","",0,0)
#nombre
nombre_frame=widget_creator.create_frame_entry(buscar_persona_frame,"Nombre","",0,1)
#apellido
apellido_frame=widget_creator.create_frame_entry(buscar_persona_frame,"Apellido","",0,2)
#Seguro Social
seguro_social_frame=widget_creator.create_frame_entry(buscar_persona_frame,"Seguro Social","",0,3)
#Seguro HCM
seguro_hcm_frame=widget_creator.create_frame_entry(buscar_persona_frame,"Seguro HCM","",0,4)
#bono productividad
bono_productividad_frame=widget_creator.create_frame_widget(buscar_persona_frame,"Bono Productividad","",1,0)
#Bono Alimentacion
bono_alimentacion_frame=widget_creator.create_frame_widget(buscar_persona_frame,"Bono Alimentacion","",1,1)
#SHCM
shcm_frame=widget_creator.create_frame_widget(buscar_persona_frame,"SHCM","",1,2)
#SSO
sso_frame=widget_creator.create_frame_widget(buscar_persona_frame,"SSO","",1,3)
#Sueldo basico
sueldo_basico_frame=widget_creator.create_frame_entry(buscar_persona_frame,"Sueldo Basico","",1,4)
#Sueldo neto
sueldo_neto_frame=widget_creator.create_frame_widget(buscar_persona_frame,"Sueldo Neto","",2,2)
#button modificar
modificar_button=widget_creator.create_button(buscar_persona_frame,"Modificar",modificar_persona,2,0)
#button Limpiar
limpiar_button=widget_creator.create_button(buscar_persona_frame,"Limpiar",limpiar_datos,2,3)



right_scrollbar.config(command=treeview.yview)


root.mainloop()