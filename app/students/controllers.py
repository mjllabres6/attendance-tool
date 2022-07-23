from app import db
import json
from flask import jsonify
from bson.objectid import ObjectId
from http import HTTPStatus
import pymongo


class StudentManager(object):
    @classmethod
    def get_students(cls):
        data = list(db.students.find())
        for student in data:
            student["_id"] = str(student["_id"])
        return jsonify({"data": data})

    @classmethod
    def get_student_by_id(cls, id):
        data = db.students.find_one({"_id": ObjectId(id)})
        print(data)
        data["_id"] = str(data["_id"])
        return jsonify({"data": data})

    @classmethod
    def create_student(cls, body):
        user_body = {
            "srcode": body.get("srcode"),
            "name": body.get("name"),
            "password": body.get("password"),
        }

        try:
            db.students.insert_one(user_body)
            return {"message": "Successfully created student record."}, 200
        except pymongo.errors.DuplicateKeyError:
            return {"message": "You have entered an existing  sr-code."}, 500
        except Exception:
            return {"message": "There was a problem creating student record"}, 500

    @classmethod
    def login_student(cls, body):
        user_body = {"srcode": body.get("srcode"), "password": body.get("password")}

        student = db.students.find_one(
            {"srcode": user_body["srcode"], "password": user_body["password"]}
        )
        if student:
            return {"message": "Found a match on a student record."}, 200

        return {"message": "Invalid login credentials."}, 500
