# Importing the Required Packages
import nltk
import re
import random
import time
from nltk.tokenize import RegexpTokenizer, word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize.regexp import WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer

# Defining Intents
intents = [
    ["greetings", 
     ["hi", 
      "hello"]],
    
    ["farewell", 
     ["bye"]]
]

# Defining Responses for each Intent
intent_responses = [
    ["greetings", 
     ["hi, how may I help you today?", 
      "hello, what can I do for you today?",  
      "it’s nice to meet you, how may we be of service?"]],
    
    ["farewell", 
     ["it was a pleasure to help you. do come back. type 'quit' to exit the program.",
      "see you later. let me know if you have any other queries. type 'quit' to exit the program.",
      "i hope the interaction was helpful. type 'quit' to exit the program.",
      "thank you for your time. type 'quit' to exit the program."]]
]

# Tokenizing Input Text
def tokenize_input(user_response):
    wst = WhitespaceTokenizer()
    return wst.tokenize(user_response)

# Removing Stopwords
def remove_stopwords(tokens):
    stop_words = set(stopwords.words('english'))
    new_tokens = list()
    for w in tokens:
        if w not in stop_words: new_tokens.append(w)
    return new_tokens

# Remove Punctuation
def remove_punct(user_tokens):
    punct_re = r"(.*)[?,.!]$"
    for i, word in enumerate(user_tokens):
        if re.match(punct_re, word):
            user_tokens[i] = word[:-1]
    return user_tokens

# Lemmatize Tokens
def lemmatize_tokens(tokens):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word) for word in tokens]

# Jaccard Similarity
def get_jaccard_sim(set1, set2): 
    set3 = set1.intersection(set2)
    set4 = set1.union(set2)
    return float( len(set3) / len(set4) )

# Matching Intent
def match_intents(lemma_tokens):
    intents_matched = list()
    for intent in intents:
        intents_matched.append([intent[0], get_jaccard_sim(set(lemma_tokens), set(intent[1]))])
    return intents_matched

# Finding the most suited Intent
def max_sim_intent(intents_matched):
    max_sim = 0
    user_intent = list()
    for i, intent in enumerate(intents_matched):
        if intent[1]>max_sim:
            max_sim = intent[1]
            user_intent = intents_matched[i]
    return user_intent

# Finding an appropriate response
def responses(user_intent):
    response = str()
    for intent_response in intent_responses:
        if intent_response[0] == user_intent[0]:
            response = random.choice(intent_response[1])
    
    return response

# Defining the logic that genrates the bot's response
def bot_response(user_response):
    # Input Text Preprocessing 
    tokens = tokenize_input(user_response)
    new_tokens = remove_stopwords(tokens)
    new_tokens = remove_punct(new_tokens)
    lemma_tokens = lemmatize_tokens(new_tokens)
    
    # Intent Matching
    intents_matched = match_intents(lemma_tokens)
    user_intent = max_sim_intent(intents_matched)
    
    # Generating an appropriate response for the intent matched
    return responses(user_intent)

# Main Function
print("Intent Classification BOT")
user_response = str()
while(user_response!="quit"):
    print()
    time.sleep(0.2)
    user_response = input("YOU: ")
    user_response = user_response.lower()
    if(user_response!='quit'):
        print("BOT: "+bot_response(user_response))
    else:
        time.sleep(0.2)
        print("BOT: Bye! take care..")
