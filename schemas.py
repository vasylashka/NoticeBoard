from marshmallow import Schema, fields

class NoteSchema(Schema):
    class Meta:
        fields = ('id', 'title', 'text', 'creation_date', 'user_id')

class UserSchema(Schema):
    class Meta:
        fields = ('id', 'username', 'email')

