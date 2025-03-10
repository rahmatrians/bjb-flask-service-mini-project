from flask import Flask, jsonify, request
from app.db import SessionLocal
from app.models import ClientDummy, ApiLogs

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def clients():
    db = SessionLocal()
    if request.method == "GET":
        try:
            clients = db.query(ClientDummy).all()
            response = [{"id": str(c.id), "nama": c.nama, "alamat": c.alamat} for c in clients]
            log = ApiLogs(request_payload=None, response_payloads=response)
            db.add(log)
            db.commit()
            return jsonify(response)
        except Exception as e:
            return jsonify({"message": str(e)}), 500
        finally:
            db.close()
    elif request.method == "POST":
        try:
            data = request.json
            new_client = ClientDummy(nama=data["nama"], alamat=data.get("alamat"))
            db.add(new_client)
            response = {"message": "Client added!", "id": str(new_client.id)}
            log = ApiLogs(request_payload=data, response_payloads=response)
            db.add(log)
            db.commit()
            return jsonify({"message": "Client added!", "id": str(new_client.id)})
        except Exception as e:
            return jsonify({"message": str(e)}), 500
        finally:
            db.close()

@app.route("/<string:client_id>", methods=["GET", "PUT", "DELETE"])
def client(client_id):
    db = SessionLocal()
    if request.method == "GET":
        try:
            client = db.query(ClientDummy).filter_by(id=client_id).first()
            if client:
                response = {"id": str(client.id), "nama": client.nama, "alamat": client.alamat}
                log = ApiLogs(request_payload=None, response_payloads=response)
                db.add(log)
                db.commit()
                return jsonify(response)
        except Exception as e:
            return jsonify({"message": "Client not found"}), 404
        finally:
            db.close()
    elif request.method == "PUT":
        try:
            data = request.json
            client = db.query(ClientDummy).filter_by(id=client_id).first()
            if not client:
                return jsonify({"message": "Client not found"}), 404
            if "nama" in data:
                client.nama = data["nama"]
            if "alamat" in data:
                client.alamat = data["alamat"]
            response = {"id": str(client.id), "nama": client.nama, "alamat": client.alamat, "message": "Client updated!"} 
            log = ApiLogs(request_payload=data, response_payloads=response)
            db.add(log)
            db.commit()
            return jsonify(response)
        except Exception as e:
            return jsonify({"message": str(e)}), 500
        finally:
            db.close()
    elif request.method == "DELETE":
        try:
            client = db.query(ClientDummy).filter_by(id=client_id).first()
            if client:
                db.delete(client)
                log = ApiLogs(request_payload=None, response_payloads={"message": "Client deleted!"})
                db.add(log)
                db.commit()
                return jsonify({"message": "Client deleted!"})
        except Exception as e:
            return jsonify({"message": "Client not found"}), 404
        finally:
            db.close()    
