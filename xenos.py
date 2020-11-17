#XENOS: A tool for cloning (currently) LinkedIn conenction emails.
#Use: You will need to provide the following:
  #A template
  #A link to replace the ones in the template
  #A sender name and profile picture
  #A sender's profession and place of work
  #A target name and profile picture
  #The target's current position
#The point of this is a proof of concept to showcase the ease at which this could be done
#This script could be modified to do a similar operation to any kind of email like these

import re
import sys

url_reg = "(a href=\"http[s]://([\w\-\.\?\&\$\/\=\;\%])+)"
img_reg = "(src=\"http[s]:\/\/([\w\-\.\?\&\$\/\=\;\%\#\:])+)"

#Get user input through a psudeo-menu
template = open(input("Template Path: "), "r")
email = template.readlines()
template.close()
link_to = input("Custom Link: ")
fake_person = input("Name of sender: ")
fake_img = input("Sender Profile Pic: ")
fake_job = input("Sender Profession: ")
fake_work = input("Sender Work Place: ")
target = input("Target Name: ")
target_img = input("Target Profile Pic: ")
job = input("Target Profession: ")

#Replace links and names
def replace_links(email):
    link_email = ""
    for line in email:
        if(re.sub(url_reg, 'a href="' + link_to + '"', line, 10)):
            line = (re.sub(url_reg, 'a href="' + link_to + '"', line, 10))
            #Replacing Names here
            if "FROM" in line:
                link_email = link_email + replace_name(line, "FROM") + "\n"
            elif "TARGET" in line:
                link_email = link_email + replace_name(line, "TARGET") + "\n"
            #If no name flags found, just append the line to the variable
            else:
                link_email = link_email + line + "\n"
        else:
            link_email = link_email + line + "\n"
    return(link_email)

#Replace images for the target and the fake person
def replace_images(email):
    new_email = ""
    for line in email:
        #If the value of fake_person is found and an image, replace the image
        if fake_person in line:
            if(re.sub(img_reg, 'src=\"' + fake_img + '"', line, 10)):
                line = (re.sub(img_reg, 'src=\"' + fake_img + '"', line, 10))
                new_email = new_email + line + "\n"
        elif target in line:
            if(re.sub(img_reg, 'src=\"' + target_img + '"', line, 10)):
                line = (re.sub(img_reg, 'src=\"' + target_img + '"', line, 10))
                new_email = new_email + line + "\n"
        elif "SENDERJOB" in line:
           new_email = new_email + replace_job(line, fake_job) + "\n"
        else:
            new_email = new_email + line + "\n"
    return(new_email)

#Returns a modified line with a place holder replaced with user input
def replace_name(line, person):
    if person == "FROM":
        line = (re.sub(person, fake_person, line, 10))
        line = replace_job(line, fake_job)
    elif person == "TARGET":
        line = (re.sub(person, target, line, 10))
        #This is put here because the JOB flag is right next to the name
        line = replace_job(line, job)
    return(line)

#Replace JOB in the template with input
def replace_job(line, job):
    if "SENDERJOB" in line:
        line = (re.sub("SENDERJOB", job, line, 10))
        line = (re.sub("SENDERWORK", fake_work, line, 10))
    elif "JOB" in line:
        line = (re.sub("JOB", job, line, 10))
    return(line)

content = replace_images(replace_links(email).splitlines())
email = open("email.html", "w+")
email.write(content)
email.close()

