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

#Replace links and names
def replace_links(email):
    '''Takes in the template contents and returns the new email with names and links replaced.'''
    link_email = ""
    for line in email:
        #If a url is found in the line
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
    '''Takes in the contents of an email and returns the new email with images replaced.'''
    new_email = ""
    for line in email:
        #If the value of fake_person is found and an image, replace the image
        if fake_person in line:
            #replace image with the sender image
            if(re.sub(img_reg, 'src=\"' + fake_img + '"', line, 10)):
                line = (re.sub(img_reg, 'src=\"' + fake_img + '"', line, 10))
                new_email = new_email + line + "\n"
        #replace the image with the target image
        elif target in line:
            if(re.sub(img_reg, 'src=\"' + target_img + '"', line, 10)):
                line = (re.sub(img_reg, 'src=\"' + target_img + '"', line, 10))
                new_email = new_email + line + "\n"
        #if this string is found in the line, we'll replace it with the user input.
        #this is this way because the only time the sender's job is found is on the
        #same line as the image. This should be rewritten to be more expandable
        elif "SENDERJOB" in line:
           new_email = new_email + replace_job(line, fake_job) + "\n"
        else:
            new_email = new_email + line + "\n"
    return(new_email)

#Returns a modified line with a place holder replaced with user input
#Also replaces the job information as this script works line by line
def replace_name(line, person):
    '''Takes in a line and user input person and returns the line replaced.'''
    if person == "FROM":
        line = (re.sub(person, fake_person, line, 10))
        line = replace_job(line, fake_job)
    elif person == "TARGET":
        line = (re.sub(person, target, line, 10))
        #This is put here because the JOB flag is right next to the name
        #Should be modified in the future to increase exapandability
        line = replace_job(line, job)
    return(line)

#Replace JOB in the template with input
def replace_job(line, job):
    '''Takes in a line and user input job and returns the line replaced.'''
    if "SENDERJOB" in line:
        line = (re.sub("SENDERJOB", job, line, 10))
        line = (re.sub("SENDERWORK", fake_work, line, 10))
    elif "JOB" in line:
        line = (re.sub("JOB", job, line, 10))
    return(line)

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

#Write the email
content = replace_images(replace_links(email).splitlines())
email = open("email.html", "w+")
email.write(content)
email.close()
