'''
Created on 08/08/2011

@author: nelson687
'''

import pickle
from google.appengine.ext import db

class ObjectProperty(db.BlobProperty):
    def validate(self, value):
        try:
            result = pickle.dumps(value)
            return value
        except pickle.PicklingError, e:
            return super(ObjectProperty, self).validate(value)

    def get_value_for_datastore(self, model_instance):
        result = super(ObjectProperty, self).get_value_for_datastore(model_instance)
        result = pickle.dumps(result)
        return db.Blob(result)

    def make_value_from_datastore(self, value):
        try:
            value = pickle.loads(str(value))
        except:
            pass
        return super(ObjectProperty, self).make_value_from_datastore(value)

class User(db.Model):
    id = db.StringProperty(required=True)
    creado = db.DateTimeProperty(auto_now_add=True)
    actualizado = db.DateTimeProperty(auto_now=True)
    nombre = db.StringProperty(required=True)
    url_perfil = db.StringProperty(required=True)
    access_token = db.StringProperty(required=True)
    contactos = ObjectProperty()
    historico = ObjectProperty()
    
