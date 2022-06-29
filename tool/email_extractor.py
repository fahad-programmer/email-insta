usernames = open("usernames.txt", "r")
users = usernames.readlines()
usernames.close()

for user in users:
    emails = user.split(":")
    email_file = open("emails.txt", "a")
    email_file.write(f"{emails[2]}:{emails[3]}")

email_file.close()