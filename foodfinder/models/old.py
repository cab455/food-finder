
#creating association table for roles/users
#roles_users = db.Table('roles_users', 
#    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#    db.Column('role_id', db.Integer, db.ForeignKey('role.id')))


#e.g., admin, regular user, etc
#many-to-many relationship between user and role
#class Role(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(40))
#    description = db.Column(db.String(255))



