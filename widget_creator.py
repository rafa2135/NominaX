#widget_creator.py
import tkinter as tk
from tkinter import ttk

colm_nombres = ["Cedula", "Nombre", "Apellido", "Sueldo Básico", "Bono Productividad"]

def create_entry_widget(parent, text, row, column): #crear entradas de datos con un label
    lable= ttk.Label(parent,text=text)
    lable.grid(row=row, column=column,sticky="e")
    entry = ttk.Entry(parent)
    #entry.insert(0, text)
    #entry.bind("<FocusIn>", lambda e: entry.delete('0', 'end'))
    entry.grid(row=row, column=column+1, sticky="ew")
    return entry

def create_mostrar_widget(parent, text, row, column,value): #crear entradas de datos con un label para mostar datos
    lable= ttk.Label(parent,text=text)
    lable.grid(row=row, column=column,sticky="e")
    entry = ttk.Entry(parent)
    entry.insert(0, value)    
    entry.grid(row=row+1, column=column, sticky="ew")
    return entry

def create_button(parent, text, command, row, column): #crear botones
    button = ttk.Button(parent, text=text, command=command)
    button.grid(row=row, column=column, columnspan=2, pady=8,sticky="ew")
    return button

def create_frame_widget(parent,text,value,row,colum):
    frame=ttk.Frame(parent, padding=(5, 5), relief="solid")
    frame.grid(row=row,column=colum,sticky="nsew")
    label_name=ttk.Label(frame,text=text,anchor="center", width=17)
    label_name.grid(row=0,column=0,sticky="e")
    label_value=ttk.Label(frame,text=value,anchor="center", width=17)
    label_value.grid(row=1,column=0,sticky="e")
    return label_value
 
def create_frame_entry(parent,text,value,row,colum):
    frame=ttk.Frame(parent, padding=(5, 5), relief="solid")
    frame.grid(row=row,column=colum,sticky="nsew")
    label_name=ttk.Label(frame,text=text,anchor="center", width=17)
    label_name.grid(row=0,column=0,sticky="e")
    entry = ttk.Entry(frame,width=17)
    entry.insert(0, value) 
    entry.grid(row=1,column=0,sticky="e")
    return entry
    


