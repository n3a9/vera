import json
import httplib, urllib, base64
import string

def getSuggestion(statement, word):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '567bcf0b64d645e2880d710995d3ff88'
    }
    
    params = urllib.urlencode({
        # Request parameters
        'model': 'body',
        'words': statement,
        'order': '5',
        'maxNumOfCandidatesReturned': '10',
    })
    
    try:
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/text/weblm/v1.0/generateNextWords?%s" % params, "", headers)
        response = conn.getresponse()  
        data = json.loads(response.read())
        #print(data)
        conn.close()

        for candidate in data['candidates']:
            if word == candidate['word']:
                #print word
                return True
        
        #print 'no suggestions'
        return False

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def getTags(statement):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '2bb694121f48499293a61a070aa8e6ad',
    }
    
    params = urllib.urlencode({
    })
    
    try:
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        data = '{ "language" : "en", "analyzerIds" : ["4fa79af1-f22c-408d-98bb-b7d7aeef7f04", "08EA174B-BFDB-4E64-987E-602F85DA7F72"], "text" : "' + statement +'" }'
        
        conn.request("POST", "/linguistics/v1.0/analyze?%s" % params, data, headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        #print(data)
        conn.close()

        tags = []
        for tag in data[0]['result'][0]:
            tag = str(tag[:2])
            if tag == 'JJ':
                tags.append('adjective')
            elif tag == 'NN':
                tags.append('noun')
            elif tag == 'VB':
                tags.append('verb')
            elif tag == 'CD':
                tags.append('number')
            else:
                tags.append('other')
        
        tokens = []
        for token in data[1]['result'][0]['Tokens']:
            tokens.append(str(token["NormalizedToken"]))
        
        return [tags, tokens]
        
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    
def getAntonym(word, parsedStatement):
    params = word
    wordTag = ""
    
        # Request parameters
    
    try:
        conn = httplib.HTTPSConnection('words.bighugelabs.com')
        
        conn.request("POST", "/api/2/488536c4454c0a90bc703a2ac6670578/%s/" % params)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        conn.close()
        
        for i, _ in enumerate(parsedStatement[1]):
            if parsedStatement[1][i] == word:
                wordTag = parsedStatement[0][i]
                break
        
        antStart = data.find(wordTag + '|ant|')
        if antStart != -1:
            antEnd = data.find('\n', antStart)
            #print "antonym found: " + data[(len(wordTag) + antStart + 5):antEnd]
            return data[(len(wordTag) + antStart + 5):antEnd]
        else:
            return "Null"
        
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))    
    
def getTopic(entity):
    params = urllib.urlencode({
        # Request parameters
        'input': entity
    })
    
    try:
        conn = httplib.HTTPSConnection('www.wolframcloud.com')
        conn.request("POST", "/objects/f00dc79e-44d0-478e-bf45-9db34fa8da85?%s" % params)
        response = conn.getresponse()
        data = json.loads(response.read())
        #print(data)
        conn.close()
                                
        return str(data['Result']).strip(string.punctuation)
    
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))    
    
def getSamples(entity):
    
    params = urllib.urlencode({
        # Request parameters
        'input': entity
    })
    
    try:
        conn = httplib.HTTPSConnection('www.wolframcloud.com')
        conn.request("POST", "/objects/794b2d41-2e30-4ccc-a5ce-0b698c03d1b2?%s" % params)
        response = conn.getresponse()
        data = json.loads(response.read())
        #print(data)
        conn.close()
                                
        roughText = data['Result'].replace(',','').split()  
        samples = []
        for word in roughText:
           samples.append(str(word).strip(string.punctuation))
        return samples
    
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def getScore(statement):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '567bcf0b64d645e2880d710995d3ff88',
    }
    
    params = urllib.urlencode({
        # Request parameters
        'model': 'body',
        'order': '5'
    })
    
    try:
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        data = '{"queries":["' + statement + '"]}'
        
        conn.request("POST", "/text/weblm/v1.0/calculateJointProbability?%s" % params, data, headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        conn.close()
        #print float(str(data['results'][0]['probability']))       
        return float(str(data['results'][0]['probability']))       
        
        
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    
def recombine(tokens, replacement='', index=-1):
    combinedStatement = ""    
    
    if index != -1:
        tokens[index] = replacement
    
    for token in tokens:
        if token:
            combinedStatement += token + " "
    #print combinedStatement[:len(combinedStatement) -1]        
    return combinedStatement[:len(combinedStatement) -1]

def truthme(statement):
    parsedStatement = getTags(statement) # tags, tokens
    #print parsedStatement
    verbIndex = 0   
    notExists = False
    fullySuggested = False
    
    # find the verb    
    
    for i, tag in enumerate(parsedStatement[0]):
        if tag == 'verb':
            verbIndex = i
            break
        
    #print verbIndex
    
    # check for a not    
    
    for i, token in enumerate(parsedStatement[1]):
        if token.lower() == 'not' or token.lower() == 'n\'t':
            notExists = True
            parsedStatement[1][i] = ''
            break
        
    # check if the descriptor is commonly associated with the subject
        
    fullySuggested = False        
        
    for i in range(verbIndex + 1, len(parsedStatement[0])):
        if parsedStatement[0][i] == 'number' or parsedStatement[0][i] == 'noun':
            if getSuggestion(recombine(parsedStatement[1][:i]), 
                             parsedStatement[1][i]):
                fullySuggested = True
            else:
                break
    
    if fullySuggested:
        return (True != notExists)    
    
    # check for an antonym adjective, and compare    
    
    for i in range(verbIndex + 1, len(parsedStatement[0])):
        if parsedStatement[0][i] == 'adjective':
            antonym = getAntonym(parsedStatement[1][i], parsedStatement)
            if antonym != "Null":
                if (getScore(recombine(parsedStatement[1])) >
                getScore(recombine(parsedStatement[1], antonym, i))):
                    return (True != notExists)
                else: 
                    return (False != notExists)
                      
    # check for an antonym noun, and compare                      
                        
    for i in range(verbIndex + 1, len(parsedStatement[0])):
        if parsedStatement[0][i] == 'noun':
            antonym = getAntonym(parsedStatement[1][i], parsedStatement)
            if antonym != "Null":
                if (getScore(recombine(parsedStatement[1])) >
                getScore(recombine(parsedStatement[1], antonym, i))):
                    return (True != notExists)
                else: 
                    return (False != notExists)                        
                        
    # check for the most probable word in a category of similar words
    
    for i in range(verbIndex + 1, len(parsedStatement[0])):
        if parsedStatement[0][i] == 'noun':
            topic = getTopic(parsedStatement[0][i]).lower()
            if (topic == 'word' or topic == 'icon' or topic == 'grammaticalunit'):
                continue
            samples = getSamples(parsedStatement[1][i])
            ourScore = getScore(recombine(parsedStatement[1]))            
            
            for sample in samples:
                if getScore(recombine(parsedStatement[1], sample, i)) > ourScore:
                    return (False != notExists)
            return (True != notExists)

    # evaluate the general likelihood of the statement

    return ((getScore(recombine(parsedStatement[1])) > -10.0) != notExists)

#data = truthme("Eight hours of sleep is healthy")
#data = truthme("Ducks are aquatic animals")
#data = truthme("UCLA wasn't founded in 1991")
#data = truthme("Caltech is a great university")
#data = truthme("Boeing is an American company")


#print data