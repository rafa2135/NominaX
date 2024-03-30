import tkinter as tk
from tkinter import ttk

colm_nombres = ["Cedula", "Nombre", "Apellido", "Sueldo Básico", "Bono Productividad"]

def create_entry_widget(parent, text, row, column): #crear entradas de datos con un label
    lable= ttk.Label(parent,text=text)
    lable.grid(row=row, column=column,sticky="e")
    entry = ttk.Entry(parent)
    entry.insert(0, text)
    entry.bind("<FocusIn>", lambda e: entry.delete('0', 'end'))
    entry.grid(row=row, column=column+1, sticky="ew")
    return entry

def create_button(parent, text, command, row, column): #crear botones
    button = ttk.Button(parent, text=text, command=command)
    button.grid(row=row, column=column, columnspan=2, pady=5,sticky="ew")
    return button

def mostrar_datos(parent, data):    #crear tabla de datos
    for i, row in enumerate(data):
        for j, value in enumerate(row):
            label = ttk.Label(parent, text=value)
            label.pack(sticky="ew")

            