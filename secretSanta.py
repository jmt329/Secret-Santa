import smtplib
import copy
import random
import csv
import sys

DEBUG = True
server = None


# starts smtp server
def start_server():
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login("sender@example.com", "password")  # put in login and password


# sends <msg> to <recp_email>
def send_mail(recp_email, msg):
    server.sendmail("sender@example.com", recp_email, msg)  # change from email


# tells <recp> their match is >match>
def make_msg(recp, match):
    msg = "{},\n\nYour secret Santa is {}\n\nHappy Christmas!".format(recp,
                                                                      match)
    return msg


# returns a tuple of two lists where the elements from each list correspond to
# a match
def make_matches(santas):

    def have_themself(a, b):
        for i in xrange(len(a)):
            if (a[i] == b[i]):
                return True
        return False

    # suffle for randomness (and fun)
    santa_match = copy.deepcopy(santas)
    random.shuffle(santa_match)

    # shift by one
    s = santa_match.pop(0)
    santa_match.append(s)

    if have_themself(santas, santa_match):
        print "Something went wrong...quitting"
        sys.exit()

    return (santas, santa_match)


# reads from a csv file <file> with names and emails
def get_santas(file):
    with open(file, "rb") as f:
        reader = csv.reader(f)
        return list(reader)


if __name__ == "__main__":
    if not DEBUG:
        start_server()

    senders = []
    senders_emails = []
    for ep in get_santas("emails.csv"):
        senders.append(ep[0].strip())
        senders_emails.append(ep[1].strip())

    matches = make_matches(senders)

    for i in xrange(len(senders)):
        msg = make_msg(matches[0][i], matches[1][i])
        if DEBUG:
            print senders_emails[i]
            print msg + "\n\n"
        else:
            send_mail(senders_emails[i], msg)
