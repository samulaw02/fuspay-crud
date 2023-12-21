from marshmallow import Schema, fields, validate


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=5))


class CreateUserSchema(Schema):
    firstName = fields.Str(required=True, validate=validate.Length(max=80))
    lastName = fields.Str(required=True, validate=validate.Length(max=80))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=5))
    createdAt = fields.DateTime(dump_only=True)
    updatedAt = fields.DateTime(dump_only=True)
    
    

class UpdateUserSchema(Schema):
    firstName = fields.Str(required=True, validate=validate.Length(max=80))
    lastName = fields.Str(required=True, validate=validate.Length(max=80))
    createdAt = fields.DateTime(dump_only=True)
    updatedAt = fields.DateTime(dump_only=True)