from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

# 建立 Flask 應用程式
app = Flask(__name__)

# 設定資料庫連線參數
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(
    user='admin',
    password='rootroot',
    host='database-4.cyytgedqlpjr.us-east-1.rds.amazonaws.com',
    port=3306,
    database='table4'
)

db = SQLAlchemy(app)

# 建立 Swagger 實例
swagger = Swagger(app)

# 建立資料表模型
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))

# # 建立 API 資源
class UsersResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=int)
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('email', type=str)
        super(UsersResource, self).__init__()
        
    def get(self):#已完成
        """
        Get a list of all users
        ---
        responses:
          200:
            description: A list of all users
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  email:
                    type: string
          500:
            description: 伺服器錯誤
        """
        try:
            users = User.query.all()
            user_list = []
            for user in users:
                user_dict = {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email
                }
                user_list.append(user_dict)
            return jsonify(user_list)
        except:
            return {'message': 'error'}, 500
    
    def post(self):#已完成
        """
        說明: 新增使用者資料
        ---
        parameters:
          - in: body
            name: user
            schema:
              type: object
              properties:
                name:
                  type: string
                email:
                  type: string
            required: true
        responses:
          200:
            description: 已新增使用者的資料
          404:
            description: 信箱名稱重複
          500:
            description: 伺服器錯誤
        """
        try:
            args = self.parser.parse_args()
            print(args)
            user = User.query.filter(User.email == args['email']).first()
            if not user:
                new_user = User(name=args['name'], email=args['email'])
                db.session.add(new_user)
                db.session.commit()
                message = {'message': '已新增資料'}, 200
            else:
                message = {'message': '信箱名稱重複'}, 404
            return message
        except:
            return {'message': 'error'}, 500
    def delete(self):#已完成
        """
        說明: 新增使用者資料
        ---
        parameters:
          - in: body
            name: user_id
            schema:
              type: object
              properties:
                id:
                  type: integer
            required: true
        responses:
          200:
            description: 已刪除使用者
          404:
            description: 指定ID的使用者不存在
          500:
            description: 伺服器錯誤
        """
        try:
            args = self.parser.parse_args()
            user = User.query.filter(User.id == args['id']).first()
            if user:
                db.session.delete(user)
                db.session.commit()
                message = {'message': '刪除使用者成功'}, 200
            else:
                message = {'message': '此ID不存在'}, 404
            return message
        except:
            return {'message': 'error'}, 500  
    def put(self):#已完成
        """
        說明: 修改使用者資料
        ---
        parameters:
          - in: body
            name: user
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                email:
                  type: string
            required: true
        responses:
          200:
            description: 已修改使用者
          404:
            description: 此ID或信箱有誤
          500:
            description: 伺服器錯誤
        """
        try:
            args = self.parser.parse_args()
            user = User.query.filter(User.id == args['id']).first()
            #確認使用者存在
            if user:
                email_only = User.query.filter(User.email == args['email']).first()
                # 確認信箱唯一
                if user == email_only or not email_only:
                    user.email = args['email']
                    user.name = args['name']
                    db.session.commit()
                    message = {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email
                    }, 200
                else:
                    message = {'message': '信箱名稱重複'},404
            else:
                message = {'message': '此ID不存在'}, 404
            return message
        except:
            return {'message': 'error'}, 500
    
# # 註冊 API 路由
api = Api(app)
api.add_resource(UsersResource, '/users')

# 建立 Flask 應用程式的入口
if __name__ == '__main__':
    app.run(debug=True)