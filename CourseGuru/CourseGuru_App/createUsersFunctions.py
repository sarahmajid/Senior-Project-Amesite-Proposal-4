from django.contrib.auth.models import User

from CourseGuru_App.models import courseusers
from CourseGuru_App.sendEmail import sendEmailNonExistingUser


def autoGenUsernameCredential():
    username = User.objects.make_random_password(8, 'abcdefghijklmnopqrstuvwxyz0123456789')
    return username

def autoGenPasswordCredential():
    genCredential = User.objects.make_random_password(8)
    return genCredential  

def createTempUser(userEmail, courseId, courseName, stat):
    notRegistered = 'No-Credential'
    userName = autoGenUsernameCredential()
    while userName == User.objects.filter(username = userName).exists():
        userName = autoGenUsernameCredential()
    password = autoGenPasswordCredential()
    if stat == '':
        stat = 'Student' 
    createNewUser(userName, userEmail, password, notRegistered, notRegistered, stat)
    addUser = User.objects.get(email = userEmail)
    courseusers.objects.create(user_id = addUser.id, course_id = courseId)
    sendEmailNonExistingUser(courseName, userEmail, userName, password)

def createNewUser(userName, userEmail, password, fName, lName, stat):
    addUser = User.objects.create_user(userName, userEmail, password) 
    addUser.first_name = fName
    addUser.last_name = lName
    addUser.status = stat
    addUser.save()
    
def updateUserInfo(userName, userEmail, password, fName, lName, stat):
    newUserInfo = User.objects.get(email = userEmail) 
    newUserInfo.username = userName 
    newUserInfo.set_password(password)
    newUserInfo.first_name = fName
    newUserInfo.last_name = lName
    newUserInfo.status = stat
    newUserInfo.save()
