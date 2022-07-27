from configuration import db
from flask_restful import Resource, reqparse, abort, fields, marshal_with

from API_V1.models import user_model


class MessageModel(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key= True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    timestamp = db.Column(db.String(100), nullable= False)
    direction = db.Column(db.String(100), nullable= False)
    media_type = db.Column(db.Integer, nullable= False)
    data = db.Column(db.String(100), nullable= False)
    status = db.Column(db.String(100), nullable= False)


    def __repr__(self):
        return f'"timestamp"="{self.timestamp}", "data"="{self.data}"...'


#db.create_all() #Run this only once if your db is not already created. The .db file will appears after the session.commit() command

message_put_args = reqparse.RequestParser()
message_put_args.add_argument("timestamp", type=str, help="Timestamp required", required=True)
message_put_args.add_argument("direction", type=str, help="Direction required", required=True)
message_put_args.add_argument("media_type", type=int, help="Media type required", required=True)
message_put_args.add_argument("data", type=str, help="Data required", required=True)
message_put_args.add_argument("status", type=str, help="Status required", required=True)

resource_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'timestamp': fields.String,
    'direction': fields.String,
    'media_type': fields.Integer,
    'data': fields.String,
    'status': fields.String,
}



#Inbox API
class Message(Resource):
    #GET METHOD
    @marshal_with(resource_fields)
    def get(self, user_id, message_id):

        message = MessageModel.query.filter_by(user_id=user_id).all()

        if not message:
            abort(404, message="Could not find any message related with that user ID")

        return message

    #PUT METHOD
    @marshal_with(resource_fields)
    def put(self, user_id, message_id):
        args = message_put_args.parse_args()

        querryUser = user_model.UserModel.query.filter_by(id=user_id).first()
        if not querryUser:
            abort(404, message="Could not find any user related with that user ID")


        querryMessage = MessageModel.query.filter_by(id=message_id).first()
        if querryMessage:
            abort(409, message= "Message ID already taken...")

        message = MessageModel(
            id=message_id, 
            user_id=user_id, 
            timestamp=args['timestamp'], 
            direction=args['direction'], 
            media_type=args['media_type'], 
            data=args['data'],
            status=args['status'])


        db.session.add(message)
        db.session.commit()
        return message, 201
