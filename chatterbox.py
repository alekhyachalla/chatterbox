# A simple python terminal chatbot named "Chatterbox" for installing yum packages
import re
from nltk.corpus import wordnet
import os  

# list of keys
words=['hello','packages','day','name','bad' ,'ok','fine','good','yes','no']
keys={}
keys_dict={}
synonym_dict={}

for word in words:
    keys[word]=[]

# stripping special characters from the synonyms
for word in words:
    synonyms=[]
    for opt in wordnet.synsets(word):
        for tk in opt.lemmas():
            stripped_lemma = re.sub('[^a-zA-Z0-9 \n\.]', ' ', tk.name())
            synonyms.append(stripped_lemma)
   
    synonym_dict[word]=set(synonyms)

#concatenating RegEx metacharacters to the keys dictinary values and joining 
for word in words:
    for synonym in list(synonym_dict[word]):
        keys[word].append('.*\\b'+synonym+'\\b.*')

for rule, keys in keys.items():
    keys_dict[rule]=re.compile('|'.join(keys))


# Replies key value pairs 
replies={
    'hello':'> How are you?',
    'good': '> Do you want to install a package?',
    'bad': '> Cheer up! Do you want to install a package?',
    'fine': '> Do you want to install a package?',
    'yes': '> Please list the name of the package to install',
    'no': '> Got it! To exit, type quit',
    'name': '> I am called chatter box',      
    'default':'> I dont quite understand. Could you repeat that?',
    'error': '> Please only re-enter the correct name of package',
    'another': '> Do you want to install another package?'
}

print ("To stop chatting, type quit\n")
print ("> I am called chatterbox. Hello!")

matched_rule = None 
# Run in loop
while (True):  
    
    user_input = input().lower()
    # exit condition
    if user_input == 'quit': 
        print ("Thank you. Have a great time!")
        break    
    
    
    # Logic for installing the given package(s)
    if matched_rule == 'yes':
        info_output = os.popen('yum install' +' '+ user_input + ' '+ "-y").read()
        print(info_output)
        if info_output.find("succeeded"):
            matched_rule = "another"
        else:
            matched_rule = "error"
     

    if matched_rule != 'another' and matched_rule != 'error':
        matched_rule = None 
    
    # searching for pattern matches in user input
    for rule,pattern in keys_dict.items():
        if re.search(pattern, user_input): 
            matched_rule=rule 

    # default reply
    key='default' 
    if matched_rule in replies:
        key = matched_rule 
    
    #Replies from Chatterbox
    print (replies[key]) 
