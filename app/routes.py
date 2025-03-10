from flask import Flask, jsonify, request
from flask_restx import Api, Resource
from app.db import SessionLocal
from app.models import ClientDummy
from app.models import ApiLogs

app = Flask(__name__)
api = Api(app, version="1.0", title="Client API", description="API for managing clients")

ns = api.namespace("clients", description="Client operations")

# Database session
db = SessionLocal()

@ns.route("/")
class ClientList(Resource):
    def get(self):
        """Get all clients"""

        clients = db.query(ClientDummy).all()
        response_data = jsonify([{"id": str(c.id), "nama": c.nama, "alamat": c.alamat} for c in clients]).json
        
        log = ApiLogs(
            request_payload=None,
            response_payloads=response_data
        )
        db.add(log)
        db.commit()
        
        return response_data

    def post(self):
        """Add a new client"""
        data = request.json
        new_client = ClientDummy(nama=data["nama"], alamat=data.get("alamat"))
        
        response = jsonify({"message": "Client added!", "data": jsonify(data).json}).json

        log = ApiLogs(
            request_payload= data,
            response_payloads= response
        )
        
        db.add(new_client)
        db.add(log)
        db.commit()
        return response

@ns.route("/<string:client_id>")
class Client(Resource):
    def get(self, client_id):
        """Get a single client"""
        client = db.query(ClientDummy).filter_by(id=client_id).first()
        if client:
            return jsonify({"id": str(client.id), "nama": client.nama, "alamat": client.alamat})
        return jsonify({"message": "Client not found"}), 404

    def delete(self, client_id):
        """Delete a client"""
        client = db.query(ClientDummy).filter_by(id=client_id).first()
        if client:
            db.delete(client)
            db.commit()
            return jsonify({"message": "Client deleted"})
        return jsonify({"message": "Client not found"}), 404

api.add_namespace(ns)
