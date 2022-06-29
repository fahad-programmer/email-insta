email_file = open("email.txt", "r")
emails = email_file.readlines()
email_file.close()

username_file = open("username.txt", 'r')
usernames = username_file.readlines()
username_file.close()

final_lok = open("final.txt", "a")

for i in range(len(emails)):
    final_lok.write(f"{usernames[i].strip()}:{emails[i].strip()}\n")

final_lok.close()