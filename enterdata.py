import mechanize

# Set chargeback clients
cbclients = []

# Set password
timetrackpass = ""


def enterEntry(branchval, projectnum, dept, pdate, ptime, cat):
    # Set fixed values
    dept = ["14"]   # Set department
    cat = ["4"]    # Set the category number

    # Open up the browser
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open("http://time.hodes.com/")

    # Selecting our login form
    br.form = list(br.forms())[0]
    # Entering data and submitting
    branchfield = br.form.find_control("27.1")
    branchfield.value = branchval
    passwordfield = br.form.find_control("27.3")
    passwordfield.value = timetrackpass
    response = br.submit()
    
    # Determine if it's a chargeback
    # If so, enter it as a chargeback. Otherwise, enter as a normal entry.
    # Bug: need to determine that it's both a chargeback AND that the client
    # is in the proper branch/region... to add a branch column.
    if str(projectnum) in cbclients:
        chargeback(br, pdate, ptime)
    else:
        normalentry(br, projectnum, dept, pdate, ptime, cat)


def normalentry(br, projectnum, dept, pdate, ptime, cat):
    # PAGE NUMBER 2
    # Selecting our nameless form and filling out Project Time Entry
    br.form = list(br.forms())[2]

    jobnumber = br.form.find_control("jobID")
    jobnumber.value = str(projectnum)

    givedept = br.form.find_control("49.7.3")
    givedept.value = dept

    givedate = br.form.find_control("49.15")
    givedate.value = str(pdate)

    givetime = br.form.find_control("time")
    givetime.value = str(ptime)

    givecategory = br.form.find_control("49.21.1")
    givecategory.value = cat

    response = br.submit()      # Submission of the form


def chargeback(br, pdate, ptime):
    # PAGE NUMBER 2
    # Selecting our 'Time Entry Type' as a Task and not a Project
    br.form = list(br.forms())[1]
    maketask = br.form.find_control("43.1.1")
    maketask.value = ["2"]
    response = br.submit()

    # PAGE NUMBER 3
    br.form = list(br.forms())[2]
    # Selecting it as a sales chargeback
    entrytype = br.form.find_control("49.11.1")
    entrytype.value = ["1"]

    givedate = br.form.find_control("49.15")
    givedate.value = pdate
    givetime = br.form.find_control("time")
    givetime.value = ptime

    response = br.submit()
