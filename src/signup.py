import json
import re

class UserSignup:
    def __init__(self, requestData, database):
        emailRegex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        self.expectedFields = [
            "name",
            "email",
            "password",
        ]
        self.database = database
        self.requestData = requestData
        self.isValidEmail = lambda email: True if re.fullmatch(emailRegex, email) else False
    
    def signup(self):
        try:
            passedFields = dict(self.requestData)
            missingFields = []
            for field in self.expectedFields:
                if field not in passedFields.keys():
                    missingFields.append(field)
            
            if len(missingFields) > 0:
                return [None, {
                    "status": "error",
                    "code": 406,
                    "message": "Required fields are missing: " + str(missingFields),
                }]
            if not self.isValidEmail(passedFields["email"]):
                return [None, {
                    "status": "error",
                    "code": 403,
                    "message": "Email is invalid",
                }]
            if self.database.get(passedFields["email"]) is not None:
                return [None, {
                    "status": "error",
                    "code": 409,
                    "message": "User already registered",
                }]
            self.database[passedFields["email"]] = {
                "name": passedFields["name"],
                "password": passedFields["password"],
            }
            return [self.database, {
                "status": "success",
                "code": 200,
                "message": "User signed up successfully",
            }]
        except: 
            return [None, {
                "status": "error",
                "code": 500,
                "message": "Server failed to process user signup"
            }]
