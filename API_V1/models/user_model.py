from configuration import db
from flask_restful import Resource, reqparse, abort, fields, marshal_with





class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key= True)
    first_name = db.Column(db.String(100), nullable= False)
    middle_name = db.Column(db.String(100), nullable= False)
    last_name = db.Column(db.String(100), nullable= False)
    phone_number = db.Column(db.String(100), nullable= False)
    password_hash = db.Column(db.String(100), nullable= False)
    messages = db.relationship("MessageModel", backref="users")


    def __repr__(self):
        return f"User(first_name = {first_name}, middle_name = {middle_name},last_name = {last_name}, phone_number= {phone_number}, password_hash={password_hash})"





#db.create_all() #Run this only once if your db is not already created. The .db file will appears after the session.commit() command

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("first_name", type=str, help="First name required", required=True)
user_put_args.add_argument("middle_name", type=str, help="Middle name required", required=True)
user_put_args.add_argument("last_name", type=str, help="Last name required", required=True)
user_put_args.add_argument("phone_number", type=str, help="Phone number required", required=True)
user_put_args.add_argument("password_hash", type=str, help="Password required", required=True)



user_update_args = reqparse.RequestParser()
user_update_args.add_argument("first_name", type=str, help="First name required")
user_update_args.add_argument("middle_name", type=str, help="Middle name required")
user_update_args.add_argument("last_name", type=str, help="Last name required")
user_update_args.add_argument("phone_number", type=str, help="Phone number required")
user_update_args.add_argument("password_hash", type=str, help="Password required")



resource_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'middle_name': fields.String,
    'last_name': fields.String,
    'phone_number': fields.String,
    'password_hash': fields.String,
}

#USER API
class User(Resource):


    #GET METHOD
    @marshal_with(resource_fields)
    def get(self, user_id):
        result = UserModel.query.filter_by(id=user_id).first()

        if not result:
            abort(404, message="Could not find an user with that ID")
        return result

    #PUT METHOD
    @marshal_with(resource_fields)
    def put(self, user_id):
        args = user_put_args.parse_args()
        result = UserModel.query.filter_by(id=user_id).first()

        if result:
            abort(409, message= "User ID already taken...")

        user = UserModel(
            id=user_id, 
            first_name=args['first_name'], 
            middle_name=args['middle_name'], 
            last_name=args['last_name'], 
            phone_number=args['phone_number'], 
            password_hash=args['password_hash'])


        db.session.add(user)
        db.session.commit()
        return user, 201

    #PATCH METHOD
    @marshal_with(resource_fields)
    def patch(self, user_id):
        args = user_update_args.parse_args()
        result = UserModel.query.filter_by(id=user_id).first()

        if not result:
            abort(404, message= "User does not exist, cannot update...")

        if args['first_name']: 
            result.first_name = args['first_name']
        if args['middle_name']: 
            result.middle_name = args['middle_name']
        if args['last_name']: 
            result.last_name = args['last_name']
        if args['phone_number']: 
            result.phone_number = args['phone_number']
        if args['password_hash']: 
            result.password_hash = args['password_hash']

        db.session.commit()

    #DELETE METHOD
    @marshal_with(resource_fields)
    def delete(self, user_id):
        result = UserModel.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message= "Video does not exist, cannot delete it...")
        
        db.session.delete(result)
        db.session.commit()


