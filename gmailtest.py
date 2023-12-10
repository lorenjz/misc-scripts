

import pickle
import os.path
from apiclient import errors
import email
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from html.parser import HTMLParser


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify','https://mail.google.com/']

def get_code(user, search_str):
    list_ids = []
    myserv = get_service()
    theid = []
    theid = search_message(myserv, user, search_str)
    messagestuff = get_message(myserv, user, theid)
      
    txt = "Your verification code is"
    
    codeindex = messagestuff.index(txt)
    endindex = codeindex + 32
    codestart = endindex - 6
    
    print(messagestuff[codestart:endindex])
    kwikcode = messagestuff[codestart:endindex]
    delete_message(myserv, user, theid)
    return kwikcode


def delete_message(service, user_id, msg_id):
    service.users().messages().delete(userId=user_id, id=msg_id).execute()
    
def search_message(service, user_id, search_string):
    """
    Search the inbox for emails using standard gmail search parameters
    and return a list of email IDs for each result

    PARAMS:
        service: the google api service object already instantiated
        user_id: user id for google api service ('me' works here if
        already authenticated)
        search_string: search operators you can use with Gmail
        (see https://support.google.com/mail/answer/7190?hl=en for a list)

    RETURNS:
        List containing email IDs of search query
    """
    try:
        # initiate the list for returning
        list_ids = []

        # get the id of all messages that are in the search string
        search_ids = service.users().messages().list(userId=user_id, q=search_string).execute()
        
        # if there were no results, print warning and return empty string
        try:
            ids = search_ids['messages']

        except KeyError:
            print("WARNING: the search queried returned 0 results")
            print("returning an empty string")
            return ""

        if len(ids)>1:
            for msg_id in ids:
                list_ids.append(msg_id['id'])
            return(list_ids)

        else:
            for ele in ids:
                single_id = ele['id']
            #single_id = ids['id']
            #print(single_id)
            return (single_id)
        
    
    except errors.HttpError as error:
        print("An error occured: %s") %error


def get_message(service, user_id, msg_id):
    """
    Search the inbox for specific message by ID and return it back as a 
    clean string. String may contain Python escape characters for newline
    and return line. 
    
    PARAMS
        service: the google api service object already instantiated
        user_id: user id for google api service ('me' works here if
        already authenticated)
        msg_id: the unique id of the email you need

    RETURNS
        A string of encoded text containing the message body
    """
    try:
        # grab the message instance
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        for p in message["payload"]["parts"]:
            if p["mimeType"] in ["text/plain", "text/html"]:
                data = base64.urlsafe_b64decode(p["body"]["data"]).decode("utf-8")
                #print(data)
                return(data)

       
    # unsure why the usual exception doesn't work in this case, but 
    # having a standard Exception seems to do the trick
    except Exception:
        print("An error occured: %s") % error


def get_service():
    """
    Authenticate the google api client and return the service object 
    to make further calls

    PARAMS
        None

    RETURNS
        service api object from gmail for making calls
    """
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)


    service = build('gmail', 'v1', credentials=creds)

    return service
