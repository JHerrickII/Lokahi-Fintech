import urllib
import json, requests, pprint
import html2text
import re
import time
from encryption import encrypt_file_file, decrypt_file_file
from Crypto.PublicKey import RSA

#right now, encrypt and decrypt from the same public key. could make the person encode a message with the field to know
#it was them, but probably best to keep it like this and make sure messages private/public key works.
def main():
    #first part gets session cookie from website for login.
    session  = requests.Session()
    session.cookies.get_dict()
    red = session.get('http://polar-earth-53083.herokuapp.com/login/') #parse and find the value portion of csrfmiddleware token
    redlist= str(red.text).split()
    #print("name='csrfmiddlewaretoken'")
    csrf = redlist.index("name='csrfmiddlewaretoken'")  +1
    #print(csrf)
    #print(redlist[csrf])
    val = redlist[csrf].strip('value=')
    val = val.strip("'")
    #print(val)
    username = ""
    password = ""
    logged_in = False
    print("Welcome to Lokahi's FDA!")
    time.sleep(1)
    while not logged_in:

        username = input("Enter your username: ")
        password = input("Enter your password: ")

        login_data = {
            'csrfmiddlewaretoken': val,
        'username': username,
                'password': password
            }


        r= session.post('http://polar-earth-53083.herokuapp.com/login/', data=login_data)
        if r.status_code ==200 and 'login' in r.url :
            logged_in = True
        else:
            print("That is not correct. Please try again. \n")
# --- from here down, manual html parsing and showing of web page.
    # data= r.text
    #
    # command = "s"
    # while command is not "":
    #     print(html2text.html2text(data))
    #     command = input("Enter the function you would like to do: ")
    #     if command == 'viewReports':
    #         r = session.get('http://http://polar-earth-53083.herokuapp.com/' + command)
    #         data = r.text
    #         print(html2text.html2text(data))
    #         report = input("Choose a report you would like to download: ")
    #         report2 = report.replace(" ", "%20")
    #         urllib.request.urlretrieve('http://http://polar-earth-53083.herokuapp.com/'+command+"/"+report2, report)
    #         print("Success")
    #         command = 'welcome'  # go back to beginning after done
    #     r = session.get('http://http://polar-earth-53083.herokuapp.com/' + command)
    #     data = r.text

#-----end of manual html parsing.

    print("Welcome, " + username + "! What would you like to do?")
    command = "start"
    while command is not "":
        print("1. View and Download Reports \n2. Encrypt Files \n3. Decrypt Files")


        print("Please enter the number corresponding to what you would like to do. \n"
              "If you would like to end this session, hit the return key")
        command = input()
        print("\n")
        if command == '1':
            r = session.get('http://polar-earth-53083.herokuapp.com/' + 'viewReports')
            data = r.text
            data_edited = str(html2text.html2text(data)).replace("#", "")
            source_url = {}
            data = urllib.request.urlopen('http://polar-earth-53083.herokuapp.com/' + 'viewReports')
            for line in data:
                line = str(line).strip("b'")
                line = line.strip()
                if "/singleReport/" in line:

                    line = re.sub(r'\<a\shref="', '', line)
                    y = re.findall(r'\>(.+)\<',line)
                    #y finds the report name
                    line = re.sub(r'\"\>', ' ', line)
                    line = re.sub(r'\</a\>', '', line)
                    line = re.sub(r'\\\\n', '', line)
                    line = line.replace('"', "")
                    #line list's first element will be url
                    line = line.split(" ")

                    #
                    source_url[y[0]] = line[0]

            x = re.sub(r'\(.+\)', '', data_edited)
            x = re.sub(r'Public Reports', '--Public Reports--', x)
            x = re.sub(r'Private Reports', '--Private Reports--', x)
            x= re.sub(r'\[Back to Profile\]', '', x)
            print(x+'\n')

            check= True
            report_input = input("Choose a report you would like to download. \n"
                                 "If you would like to go back, hit the return key:  ")
            time.sleep(2)
            while report_input is not "" and report_input in source_url:
                rc = session.get('http://polar-earth-53083.herokuapp.com' +  source_url[report_input])
                datum = rc.text
                datum_edited = str(html2text.html2text(datum)).replace("#", "")
                datum_edited = re.sub(r'\[\sfile\s\]', '', datum_edited)
                datum_edited = datum_edited.replace("()", "")
                datum_edited = re.sub(r'/attachments/tmp/', '', datum_edited)
                datum_edited = re.sub(r'\[Edit\sReport\]\(\/editReport\/\d+\/\)\s\[Back\sto\sProfile\]\(\/welcome\)', "", datum_edited)
                datum_edited = re.sub(r'\(.+\)', "", datum_edited)
                datum_edited = datum_edited.replace("[ ]", "")
                datum_edited = datum_edited.replace("[", "")
                datum_edited = datum_edited.replace("]", "")
                time.sleep(1)
                if "Encrypted: True" in datum_edited and check:
                    download_key = input("This report contains encrypted files. Would you like to download the decrypt key? \n"
                                         "you can decrypt files downloaded after you download the files with this key. Press Y for yes or N for no: ")
                    if download_key == "Y":
                        check = False
                        datum = str(datum).strip('\n')
                        datum = datum.strip('\t')
                        sec_key = re.findall(r'value\s=((.|\n)+)\-\>', str(datum))
                        sec_val = str(sec_key[0][0]).strip('\n')  # value of public key
                        files_key = open(report_input + ".txt", 'w')
                        files_key.write(sec_val)
                        files_key.close()
                        time.sleep(1)
                        print("Download key aquired. Returning to report display... "+"\n")
                        time.sleep(2)
                print(datum_edited)
                report_input2 = input("Showing report. Choose file(s) you would like to download, separated by spaces. \n"
                                     "If you would like to go back, hit the return key: ")
                if report_input2 == "":
                    report_input = ""
                    print('Going back... \n\n')
                if report_input2 != "":
                    if "Encrypted: True" in datum_edited:
                        check = False
                        files_all = report_input2.split()
                        for files in files_all:
                            try:
                                urllib.request.urlretrieve(
                                    "http://polar-earth-53083.herokuapp.com/" + "attachments/tmp/" + files,
                                    files)

                            except:
                                print("File " + files + " not found. Going back to report...")
                        time.sleep(2)

                    else:
                        check = False
                        files_all =report_input2.split()
                        for files in files_all:
                            try:
                                urllib.request.urlretrieve("http://polar-earth-53083.herokuapp.com/"+"attachments/tmp/"+files,
                                files)
                            except:
                                print("File "+files+" not found. Going back to report...")

                    print("\n\n\n...File download(s) successful. Returning to previous menu... \n")
                    check  = False
                    time.sleep(3)
                check = False
                if report_input not in source_url:
                    report_input = ("Report does not exist. Please enter another report name: ")
        elif command == '2':
            file_in = input("Enter the name of the file/ path of the file to encrypt: ")
            pri_key = input("Enter the name of the text file that contain's the key. \n If"
                            " you require a specific key for the report, you can download that when viewing reports: ")
            work = encrypt_file_file(file_in, pri_key)
            if work:
                print("File encrypted. Check your computer folder. \n\n")
                time.sleep(2)
        elif command == '3':
            file_in = input("Enter the name of the file/ path of the file to decrypt: ")
            pub_key = input("Enter the text file containing the key to decrypt. This should be under a format like [name of report].txt. \n"
                            "If you need to get the key for a specific report, you can do so while viewing reports: " )
            work = decrypt_file_file(file_in, pub_key)
            if work:
                print("File decrypted. Check your computer folder. If unable to open file, the person who attached this may have bad intentions. \n\n")
                time.sleep(3)
        elif command != "":
            print("Unrecognized command. Try again?")
        else:
            print("Thank you for using the Lokahi FDA. Come again soon!")



main()
