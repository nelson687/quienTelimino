'''
Created on 01/08/2011

@author: nelson687
'''

#for security reasons, the developer should set with his own values this both variables
FACEBOOK_APP_ID = ""
FACEBOOK_APP_SECRET = ""

import facebook
import os
import webapp2
from google.appengine.ext.webapp import template
from domain.User import User
from auth import Signature
from domain import Contacts


class BaseHandler(webapp2.RequestHandler):
    _token = None
    _uid = None
    @property
    def current_user(self):
        
        if not hasattr(self, "_currentUser"):
            self._currentUser = None
            #check whether the user already exists in the BD
            user = User.get_by_key_name(BaseHandler._uid)
            #if no user is retrieved, this is the first time the user uses the app, we need to save the user data
            if not user:
                #get the user contacts list
                friends = Contacts.get(BaseHandler._token)
                graph = facebook.GraphAPI(BaseHandler._token)
                userProfile = graph.get_object("me")
                user = User(key_name=str(userProfile["id"]),id=str(userProfile["id"]),nombre=userProfile["name"],url_perfil=userProfile["link"],access_token=BaseHandler._token,contactos=friends)
                user.put()
                #check if the token is the same, otherwise we update it 
            elif user.access_token != BaseHandler._token:
                user.access_token = BaseHandler._token
                user.put()
                #set the user
            self._currentUser = user
    
        return self._currentUser
    

      
class HomeHandler(BaseHandler):
    _band = None
    template_path = "templates/template.html"
    def get(self):
        authorized = True
        path = os.path.join(os.path.dirname(__file__), self.template_path)
        user = self.current_user
        #get the current contacts list
        newContactsList = Contacts.get(user.access_token)
        #get the contacts who deleted the user
        formerContacts = Contacts.getFormer(user, newContactsList)
        deletedFlag = False
        if len(formerContacts) == 0:
            #if it's true, no one has deleted the user
            deletedFlag = True
        #get the added contacts
        addedContacts = Contacts.getAdded(user,newContactsList)
        addedFlag = False
        if len(addedContacts) != 0:
            addedFlag = True   
        
        template_values = {'current_user':user,'facebook_app_id':FACEBOOK_APP_ID,'eliminadores':formerContacts,'agregados':addedContacts,'bandElim':deletedFlag,'bandAgr':addedFlag,'autorizado':authorized,'contactosAntes':len(user.contactos),'contactosActual':len(newContactsList)}
        self.response.out.write(template.render(path, template_values))
        Contacts.updateList(user, newContactsList, formerContacts)
        
    def post(self):
        try:
            firma = self.request.get("signed_request")
            firmaDec = Signature.parsear(firma, FACEBOOK_APP_SECRET)
            BaseHandler._token = firmaDec["oauth_token"]
            BaseHandler._uid = firmaDec["user_id"]
            self.get()
        except:
            autorizado = False
            path = os.path.join(os.path.dirname(__file__), self.template_path)
            template_values = {'facebook_app_id':FACEBOOK_APP_ID,'autorizado':autorizado}
            self.response.out.write(template.render(path, template_values))
            
app = webapp2.WSGIApplication([('/', HomeHandler),], debug=True)