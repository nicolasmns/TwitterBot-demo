import tweepy
import time
from sympy.solvers import solve
from sympy import Symbol, Eq

#Los datos se sacaron por seguridad
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACESS_SECRET = ''
FILE_NAME = "last_seen_id.txt"



def retrieve_last_seen_id(file_name):
    f_read = open(file_name, "r")
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def insert_asterisks(equation):
    if "*" in equation: return equation
    return equation.replace('x', '*x')

def resolve(text):
    text.pop(0)
    equation = insert_asterisks(text[0])
    left, right = equation.split("=")
    eq = Eq(eval(left), eval(right))
    result = solve(eq)
    return result

def reply_to_tweets():
    print("Recuperando y respondiendo tweets...")
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')

    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if "x" in mention.full_text.lower() and "=" in mention.full_text.lower():
            print("Respondiendo...")
            #[2x+2=8]
            text = mention.full_text.lower().strip().split()
            result = resolve(text)
            api.update_status("@" + mention.user.screen_name + " BEEP BOOP el resultado de tu ecuación es: "+ str(result[0]),mention.id)
    return

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)
x = Symbol('x')

while True:
    reply_to_tweets()
    time.sleep(5)