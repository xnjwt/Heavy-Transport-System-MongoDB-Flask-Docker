from flask import render_template
from data_manager import DataManager
# importar dependencias
from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, flash

def clientes_home(data_manager):
    clientes = data_manager.get_clientes()
    return render_template('clientes/index.html', clientes=clientes)

def cliente_form(mongo):
    genero = mongo.db.genero.find()
    provincias = mongo.db.provincias.find()
    return render_template('clientes/agregarCliente.html', provincias=provincias, genero=genero)

def add_cliente(data_manager):
    if request.method == 'POST':
        nombres = request.form.get('nombres')
        cedula = request.form.get('cedula')
        correo = request.form.get('correo')
        direccion = request.form.get('direccion')
        provincia_id = int(request.form.get('provincia'))
        genero_id = int(request.form.get('genero'))

        data_manager.add_cliente(nombres, cedula, correo, direccion, provincia_id, genero_id)

        flash('Cliente agregado correctamente', 'success')
        return redirect(url_for('index_clientes'))
    
def update_cliente(mongo, cliente_id, data_manager):
    cliente = mongo.db.clientes.find_one({'_id': ObjectId(cliente_id)})

    if request.method == 'POST':
        # Obtén los datos actualizados del formulario y actualiza el cliente
        nuevo_nombres = request.form.get('nombres')
        nueva_cedula = request.form.get('cedula')
        nuevo_correo = request.form.get('correo')
        nueva_direccion = request.form.get('direccion')
        nueva_provincia_id = int(request.form.get('provincia'))
        nuevo_genero_id = int(request.form.get('genero'))

        data_manager.edit_cliente_by_id(cliente_id, nuevo_nombres, nueva_cedula, nuevo_correo, nueva_direccion, nueva_provincia_id, nuevo_genero_id)
        flash('Cliente actualizado correctamente', 'success')
        return redirect(url_for('index_clientes'))

    provincias = mongo.db.provincias.find()
    genero = mongo.db.genero.find()

    return render_template('clientes/actualizarCliente.html', cliente=cliente, provincias=provincias, genero=genero)

def delete_cliente(cliente_id, mongo, data_manager):
    generos = mongo.db.genero.find()
    provincias = mongo.db.provincias.find()
    cliente = mongo.db.clientes.find_one({'_id': ObjectId(cliente_id)})

    # Obtener información de la provincia y el genero utilizando sus IDs en el cliente
    provincia_id = cliente.get('provincia_id')
    genero_id = cliente.get('genero_id')

    provincia = mongo.db.provincias.find_one({'_id': provincia_id})
    genero = mongo.db.genero.find_one({'_id': genero_id})

    if request.method == 'POST' and 'confirm_delete' in request.form:
        # Eliminar el cliente
        data_manager.delete_cliente(cliente_id)
        flash('Cliente eliminado correctamente', 'success')
        return redirect(url_for('index_clientes'))

    return render_template('clientes/eliminarCliente.html', cliente=cliente, provincia=provincia, genero=genero, generos=generos, provincias=provincias, url_for=url_for)