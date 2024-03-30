import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import widget_creator
import database_manager
import sqlite3
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
                print("Inserción completada")
            else:
                print("Inserción fallida")
    
    except sqlite3.IntegrityError as e:
        print("Error de integridad:", e)
        messagebox.showerror("Error de inserción", "Error: No se puede insertar un usuario con una cédula que ya existe en la base de datos.")
    except sqlite3.Error as e:
        print("Error en la inserción:", e)
        messagebox.showerror("Error de inserción", f"Error en la inserción: {str(e)}")
    except Exception as e:
        print("Error desconocido:", e)
        messagebox.showerror("Error de inserción", f"Error desconocido: {str(e)}")


def borrar_db(cedula): #funcion para conectar y borrar un usuario
    conn=database_manager.connect()
    if conn:
        print("conectado")
        compledado=database_manager.borrar_usuario(conn,cedula)

        if compledado:
            messagebox.showinfo("completado","El usuario fue borrado")
            print("borrado completado")
        else:
            messagebox.showerror("Error", "El usuario no existe en la base de datos.")
            print("Borrado fallido")
          #cerrar coneccion
        database_manager.close_connection(conn)
    else:
        messagebox.showerror("Error", "coneccion fallida.")
        print("coneccion fallida")


def validate_input(empleados_data): #validando input integer
    cedula = empleados_data[0][0]
    nombre = empleados_data[0][1]
    apellido = empleados_data[0][2]
    seguro_social = empleados_data[0][3]
    seguro_hcm = empleados_data[0][4]
    sueldo_basico = empleados_data[0][5]

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
    print(empleados_data)
    bonos_data=calculo_bonos(cedula,float(sueldo_basico))
    print(bonos_data)
    insert_db(empleados_data,bonos_data)

def get_borrar_data():      # get cedula para borrar usuario
    cedula=borrar_cedula_entry.get()
    # Validating cedula
    if not (cedula.isdigit() and 6 <= len(cedula) <= 10):
        messagebox.showerror("Error", "Cedula tiene que ser un numero entero y con mas de 6 characteres")
        return False
    print (cedula)
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

# set up lable
borar_frame=ttk.LabelFrame(left_frame,text="Borrar")
borar_frame.grid(row=1,column=0,pady=5)

#setup widgets para borrar
borrar_cedula_entry = widget_creator.create_entry_widget(borar_frame,"Cedula",0,0)

# Button get input
borrar_button= widget_creator.create_button(borar_frame,"Borrar",get_borrar_data,1,0)

# Set right widget
right_frame = ttk.Frame(frame, padding=(5, 5), relief="solid")
right_frame.grid(row=0, column=1,)


# Scrollbar
right_scrollbar = ttk.Scrollbar(right_frame)
right_scrollbar.pack(side="right",fill="y")

# Table data
colm_nombres = ["Cedula", "Nombre", "Apellido", "Sueldo Básico", "Bono Productividad","sueldo neto"]

# Treeview
treeview = ttk.Treeview(right_frame,show="headings", columns=colm_nombres,height=10,yscrollcommand=right_scrollbar.set)
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


right_scrollbar.config(command=treeview.yview)

widget_creator.create_button(left_frame,"Buscar todo",mostrar_datos,7,0)
root.mainloop()