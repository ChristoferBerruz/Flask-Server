from app.database.models import Admin
from pony.orm import db_session, ObjectNotFound


class JWTCallbacks():

    """
    Binds multiple callbacks to the jwt object
    """
    def __init__(self, jwt):

        @jwt.user_identity_loader
        def identity_callback(user):
            return self.get_user_identifier(user)

            
        @jwt.user_lookup_loader
        def lookup_callback(_jwt_header, jwt_data):
            return self.lookup_user(_jwt_header, jwt_data)


    """
    Specifies which parameter to use as identity for JWTManager. For example,
    a password, email, or id.

    Parameters:
        - user: A Pony ORM Entity instance

    Returns:
        - user.id: The parameters of the user to use as identity
    """
    def get_user_identifier(self, user):
        return user.id

    
    """
    This callback is executed right after a protected route is accesed.
    If not None is return, the User instance that generated the token
    will be available as current_user inside the function decorated by
    jwt_required() 

    Parameters:
        - _jwt_header: Header of JWT
        - jwt_data: Data of JWT

    Returns:
        User instance if sucessful lookup. None otherwise.
    """
    def lookup_user(self, _jwt_header, jwt_data):

        identity = jwt_data['sub']

        with db_session:
            try:
                return Admin[identity]
            except ObjectNotFound as e:
                return None
