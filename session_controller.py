import database_manager


######### REFRESHING SESSION AND RETURNING AN USER ID ###########
                                                                #
def session_refresh(session):                                   #
    if 'username' in session:                                   #
        session.permanent = True                                #
        session['username'] = session['username']               #
        username = session['username']                          #
        userID = database_manager.getUserIDbyUsername(username) #
        return userID                                           #
    else:                                                       #
        return False                                            #
                                                                #
#################################################################