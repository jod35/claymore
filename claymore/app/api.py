from flask import Blueprint,request,jsonify,make_response
from flask_restx import Api,Resource,fields
from .models import User,Post,Comment
from flask_login import login_required,login_user,current_user,logout_user
from werkzeug.security import generate_password_hash,check_password_hash
from .exts import db

resources=Blueprint('api',__name__,
                   

)

api=Api(resources,
        title='Claymore API',
        description="REST API for the Claymore web app",
        default="Endpoints",
        default_label="All the routes for the API"
    )


user_model=api.model(
    'User',
    {
        "email":fields.String(),
        "username":fields.String(),
        "password":fields.String()
    }
)

post_model=api.model(
    'Post',
    {
        "title":fields.String(),
        "body":fields.String(),

    }
)


comment_model=api.model(
    'Comment',
    {

        "body":fields.String(),
        "user_id":fields.Integer(),
        "post_id":fields.Integer()
    }
)

#only for logging in 
login_creds=api.model(
    'Login Credentials',{
        "username":fields.String(),
        "password":fields.String()
    }
)

#password reset 
password_reset_model=api.model(
    'Passwords',
    {
        "old_password":fields.String(),
        "new_password":fields.String()
    }
)

#account password
account_password=api.model(
    "Password",
    {
        "password":fields.String()
    }
)



@api.route('/users')
class Users(Resource):
    @login_required
    @api.marshal_with(user_model,envelope='users')
    def get(self):
        '''Get all users'''
        users=User.get_all()

        return users
    


@api.route('/auth/signup')
class UserReg(Resource):
    @api.expect(user_model)
    def post(self):
        '''Create a new user account'''

        data=request.get_json()

        User.create(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password')
        )

        return make_response(jsonify(
            {"message":"User Account Created"}
            ),201)



@api.route('/auth/login')
class UserLogin(Resource):
    @api.expect(login_creds)
    def post(self):
        '''Log in a user'''
        data=request.get_json()

        username=data.get('username')
        
        user=User.get_by_username(username)

        if user and user.check_password(data.get('password')):
            login_user(user)
            return make_response(
                jsonify({
                    "message":"User Logged In"
                })
            )

@api.route('/auth/logout')
class UserLogout(Resource):
    def get(self):
        '''Logout a user'''
        logout_user()
        return make_response(
            jsonify({"message":"User Logged Out"})
        )


@api.route('/auth/reset_password')
class UserPasswordReset(Resource):
    @login_required
    @api.expect(password_reset_model)
    def patch(self):
        '''Password Reset '''
        data=request.get_json()
        
        user=User.get_by_id(current_user.id)

        if user.check_password(data.get('old_password')):
            user.password = generate_password_hash(data.get('new_password'))

            db.session.commit()

            return make_response(
                jsonify(
                    {"Message": "Password Reset Successfull"}
                )
            )


@api.route('/auth/delete_account')
class UserAccountDeletion(Resource):
    @login_required
    @api.expect(account_password)
    def delete(self):
        '''Delete a User Account '''

        data=request.get_json()

        user=User.get_by_id(current_user.id)

        if user.check_password(data.get('password')):
            user.delete()

            return make_response(
                jsonify({"message":"Account Deleted Successfully"})
            )

@api.route('/posts')
class Posts(Resource):


    @api.marshal_with(post_model)
    @login_required
    def get(self):
        ''' Get all posts'''
        posts=Post.get_all()

        return posts


    @login_required
    @api.marshal_with(post_model)
    @api.expect(post_model)
    def post(self):
        '''Create a post'''
        data=request.get_json()

        _post=Post.create(
            title=data.get('title'),
            body=data.get('body'),
            password=data.get('password')
        )

        return _post

@api.route('/post/<int:id>')
class PostResource(Resource):
    @api.marshal_with(post_model)
    def get(self,id):
        '''Get post by ID '''
        post=Post.get_by_id(id)

        return post

    @api.marshal_with(post_model)
    @api.expect(post_model)
    def patch(self,id):
        '''Update a post'''
        data=request.get_json()
        post=Post.get_by_id(id)

        post.title=data.get('title')

        post.body=data.get('body')

        db.session.commit()

        return post


@api.route('/comments')
class Comment(Resource):

    @login_required
    @api.marshal_with(comment_model)
    def get(self):
        '''Get all comments'''
        comments=Comment.get_all()

        return comments

    @api.expect(comment_model)
    @login_required
    def post(self):
        '''Create a comment '''
        data=request.get_json()

        _comment=Comment.create(body=data.get('body'))

        return _comment


# @api.route('/comment/<title>')