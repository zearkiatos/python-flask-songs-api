from flaskr import create_app
from .dataContext.sqlAlchemyContext import db
from .models import User, UserSchema

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

#Test
with app.app_context():
    user_schema = UserSchema()
    user = User(username="Zearkiatos", password="P@$$w0rd")
    db.session.add(user)
    db.session.commit()
    print(User.query.all())
    print([user_schema.dumps(user) for user in User.query.all()])