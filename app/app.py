from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from data import employee_list

app = Flask(__name__)
api = Api(app, version='1.0', title='Employee API', description='A simple Employee API')

# Namespace for employee-related routes
employee_ns = api.namespace('employee', description='Employee operations')


# GET - Ambil data pegawai
@employee_ns.route('/')
class EmployeeList(Resource):
    def get(self):
        """Get the list of employees"""
        return jsonify(employee_list)


# GET - Ambil data pegawai berdasarkan ID
@employee_ns.route('/<int:id>')
class Employee(Resource):
    def get(self, id):
        """Get employee by ID"""
        employee = next((m for m in employee_list if m['id'] == id), None)
        if employee:
            return jsonify(employee)
        return jsonify({'message': 'Employee not found'}), 404

    def put(self, id):
        """Update an employee by ID"""
        data = request.json
        employee = next((m for m in employee_list if m['id'] == id), None)
        if employee:
            employee['nama'] = data.get('nama', employee['nama'])
            employee['nip'] = data.get('nip', employee['nip'])
            employee['divisi'] = data.get('divisi', employee['divisi'])
            return jsonify(employee)
        return jsonify({'message': 'Employee not found'}), 404

    def delete(self, id):
        """Delete an employee by ID"""
        global employee_list
        employee_list = [m for m in employee_list if m['id'] != id]
        return jsonify({'message': 'Data employee has been deleted'})


# POST - Tambah data employee baru
@employee_ns.route('/')
class EmployeeCreate(Resource):
    def post(self):
        """Add a new employee"""
        data = request.json
        new_employee = {
            'id': len(employee_list) + 1,
            'nama': data['nama'],
            'nip': data['nip'],
            'divisi': data['divisi']
        }
        employee_list.append(new_employee)
        return jsonify(new_employee), 201


# Add the namespace to the API
api.add_namespace(employee_ns)

if __name__ == '__main__':
    app.run(debug=True)
