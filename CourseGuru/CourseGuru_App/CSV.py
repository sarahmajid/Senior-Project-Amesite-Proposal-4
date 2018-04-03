import csv
import io

from django.http import HttpResponse
from django.contrib.auth.models import User

from CourseGuru_App.models import courseusers
from CourseGuru_App.sendEmail import sendEmailExistingUser
from CourseGuru_App.createTempUser import createUser

def downloadCSV():
    file = HttpResponse(content_type='text/csv')
    file['Content-Disposition'] = 'attachment; filename=CSVTemplate.csv'
    writer = csv.writer(file)
    writer.writerow(["Email"])
    writer.writerow(["User1 Email"])
    writer.writerow(["User2 Email"])
    writer.writerow(["User3 Email"])
    writer.writerow(["..."])
    return file
    
def readCSV(csvFile, courseId, courseName):
    csvF = csvFile.read().decode()
    #sniffing for the delimiter in csv
    sniffer = csv.Sniffer().sniff(csvF)         
    #reading csv using DictReader     
    reader = csv.DictReader(((io.StringIO(csvF))), delimiter=sniffer.delimiter)   
    #converts all field names to lowercase
    reader.fieldnames = [header.strip().lower() for header in reader.fieldnames]
           
    #variable initialization 
    str1 = "The following "
    str2 = " users will need to create an account: "
    strNotAdded = ""
    notAddedUsers = []
    addedUsers = []
    numUserNotAdded=0
    
    #Adds students according to the csv content. If DictReader is changed code below must be edited.            
    for n in reader:
        try:
            if(User.objects.filter(email = n['email'])):
                addUser = User.objects.get(email = n['email'])
                if (courseusers.objects.filter(user_id = addUser.id, course_id = courseId).exists()==False):
                    courseusers.objects.create(user_id = addUser.id, course_id = courseId)
                    addedUsers.append(n['email'])
            else: 
                notAddedUsers.append(n['email']) 
                numUserNotAdded+=1   
                strNotAdded = str1 + str(numUserNotAdded) + str2
        except KeyError: 
            return 'CSV header error! Please make sure CSV file contain "Email" as the header for all of the emails.'
    
    #sending out emails to the added users  
    for n in addedUsers: 
        sendEmailExistingUser(courseName, n)
    for n in notAddedUsers: 
        createUser(n, courseId, courseName)
        #=======================================================================
        # notRegistered = 'No-Credential'
        # userName = autoCredential()
        # while userName == User.objects.filter(username = userName).exists():
        #     userName = autoCredential()
        # password = autoCredential()
        # newUser = User.objects.create_user(userName, n, password) 
        # newUser.first_name = notRegistered
        # newUser.last_name = notRegistered
        # newUser.status = notRegistered
        # newUser.save()
        # addUser = User.objects.get(email = n)
        # courseusers.objects.create(user_id = addUser.id, course_id = cid)
        # sendEmailNonExistingUser(cName.courseName, n, userName, password)
        #=======================================================================
    
    #creates a list of none existing users.         
    if(len(notAddedUsers)>0):
        for n in notAddedUsers:
            if n != notAddedUsers[len(notAddedUsers)-1]:
                strNotAdded += n + ", "
            else:
                if (len(notAddedUsers)==1):
                    strNotAdded += n + "."
                    return strNotAdded
                else:
                    strNotAdded += "and " + n +"."
                    return strNotAdded
    else: 
        strNotAdded = "All Users Added Successfully!"        
        return strNotAdded