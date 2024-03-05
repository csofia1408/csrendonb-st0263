from flask import Flask
from flask_restful import Api,Resource,reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db = SQLAlchemy(app)

class NodeModel(db.Model):
    username = db.Column(db.String(100), primary_key=True, nullable=False)
    password = db.Column(db.String(100),nullable=False)
    state = db.Column(db.String(100),nullable=False)
    url = db.Column(db.String(100),nullable=False)

    def __repr__(self):
        return f"Nodes(username = {self.username}, password = {self.password },url={self.url})"

class IndexationModel(db.Model):
    username = db.Column(db.String(100),primary_key=True)
    files = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Files(username = {self.username}, files = {self.files })"

db.create_all()
users_post_args = reqparse.RequestParser()
users_post_args.add_argument("username", type=str, help="You need to add a username", required=True)
users_post_args.add_argument("password", type=str, help="You need to add a password", required=True)
users_post_args.add_argument("url", type=str, help="You need to add URL", required=True)

resource_fields = {
	'username': fields.String,
	'password': fields.String,
    'state': fields.String,
	'url': fields.String
}

        
class AddNode(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = users_post_args.parse_args()
        result = NodeModel.query.filter_by(username=args.username).first()
        if result:
            result.state = "up"
            db.session.commit()
            return result, 200
        node = NodeModel(username=args.username, password=args.password, state="up", url=args.url)
        db.session.add(node)
        db.session.commit()
        return node, 200
    
    def get(self):
        result = NodeModel.query.all()
        return {"nodes": str(result)}

api.add_resource(AddNode, "/login")


logout_post_args = reqparse.RequestParser()
logout_post_args.add_argument("username", type=str, help="You need to add the peer's name you want to log out from", required=True)

class logoutPeer(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = logout_post_args.parse_args()
        result = NodeModel.query.filter_by(username=args.username).first()
        if not result:
            return {"message": f"The peer you want to log out from does not exist"}
        result.state = "down"
        db.session.commit()
        return result, 200

api.add_resource(logoutPeer, "/logout")


files_post_args = reqparse.RequestParser()
files_post_args.add_argument("username", type=str, help="You need to add the username", required=True)
files_post_args.add_argument("files", type=str, help="You need to add at least one file", required=True)

files_get_args = reqparse.RequestParser()
files_get_args.add_argument("username", type=str, help="You need to add the username", required=True)

resource_fields2 = {
	'username': fields.String,
	'files': fields.String
}

class indexFiles(Resource):
    @marshal_with(resource_fields2)
    def post(self):
        args = files_post_args.parse_args()
        username = NodeModel.query.filter_by(username=args.username).first()
        if not username:
            abort(409, message="username does not exist")
        existing_indexation = IndexationModel.query.filter_by(username=args.username).first()
        if existing_indexation:
            existing_indexation.files = args.files
            db.session.commit()
            return existing_indexation, 200
        indexation = IndexationModel(username=args.username, files=args.files)
        db.session.add(indexation)
        db.session.commit()
        return indexation, 200
    
    @marshal_with(resource_fields2)
    def get(self):
        args = files_get_args.parse_args()
        result = IndexationModel.query.filter_by(username=args.username).first()
        return result, 200
    
    
api.add_resource(indexFiles, "/indexFiles")

search_post_args = reqparse.RequestParser()
search_post_args.add_argument("username", type=str, help="You need to add the username of the peer searching for files", required=True)
search_post_args.add_argument("file", type=str, help="You need to add the file you are looking for", required=True)

class SearchFiles(Resource):
    def get(self):
        args = search_post_args.parse_args()
        username = args.username
        archivo = args.file

        user_files = IndexationModel.query.filter_by(username=username).first()

        if user_files and archivo in user_files.files.split(','):
            return {"message": f"User {username} already has file {archivo} downloaded"}

        indexationPeers = IndexationModel.query.filter(IndexationModel.files.contains(archivo)).filter(IndexationModel.username != username).all()

        result = []
        for peer in indexationPeers:
            cuurentPeer = NodeModel.query.filter_by(username=peer.username).first()
            print("peer.username", cuurentPeer.username)
            print("PEER STATE", cuurentPeer.state, cuurentPeer.username)
            if cuurentPeer.state == "up":
                result = [peer, cuurentPeer.url]
                break

        if result:
            return {"peer": result[0].username, "url": f"{result[1]}/{archivo}"}
        else:
            return {"message": "No other peer has that file available"}

api.add_resource(SearchFiles, "/searchFiles")

if __name__== "__main__":
    app.run(debug=True)