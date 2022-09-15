from chalice import BadRequestError, Blueprint

from chalicelib.auth import get_jwt_token
from chalicelib.models import User, create_user, get_user

bp = Blueprint(__name__)


@bp.route("/login", methods=["POST"])
def login():
    body = bp.current_app.current_request.json_body
    user = get_user(body["username"])
    password = body["password"]
    if "username" not in body or "password" not in body:
        raise BadRequestError(f"username and password is required")
    if not user:
        return BadRequestError(f"user non exists : {body['username']}")

    hashed_pass = user.hashed_password
    jwt_token = get_jwt_token(user.username, password, hashed_pass)
    return {"token": jwt_token}


@bp.route("/register", methods=["POST"])
def register():
    body = bp.current_app.current_request.json_body
    if "username" not in body or "password" not in body:
        raise BadRequestError(f"username and password is required")
    user = User(**body)
    new_user = create_user(user)
    return f"created user {new_user.username} at {new_user.created_at}"
