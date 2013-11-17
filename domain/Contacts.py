'''
Created on 09/08/2011

@author: nelson687
'''
import facebook

def get(token):
        
    graph = facebook.GraphAPI(token)
    friendsJson = graph.get_connections("me", "friends")
    
    #transform the json in a dictionary
    friendsDict = dict()
    for friend in friendsJson['data']: 
        friendsDict[friend['id']] = friend['name'] 
        
    return friendsDict


def getFormer(user, newFriendsList):
    
    oldFriendsList = user.contactos
    
    formerFriends = {}
    for key, value in oldFriendsList.iteritems():
        if not newFriendsList.has_key(key):
            formerFriends[key] = value
            
    return formerFriends

def getAdded(user, newFriendsList):
    
    oldFriendsList = user.contactos
    
    friendsAdded = {}
    for key, value in newFriendsList.iteritems():
        if not oldFriendsList.has_key(key):
            friendsAdded[key] = value
            
    return friendsAdded

def updateList(user, newFriendsList, formerFriends):
    
    user.contactos = newFriendsList
    
    try:
        newHistoryList = dict(user.historico.items() + formerFriends.items())
        user.historico = newHistoryList
    except:
        user.historico = formerFriends
       
    user.put()