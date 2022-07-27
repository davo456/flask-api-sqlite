from configuration import api
from API_V1.models import user_model 
from API_V1.models import inbox_model


api.add_resource(user_model.User, "/user/<int:user_id>")
api.add_resource(inbox_model.Message, "/message/<int:user_id>/<int:message_id>")

