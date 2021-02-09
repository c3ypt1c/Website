from HelperFunctions import getLogger
import requests

localLogger = getLogger()


def getDynamicLogger(messageType):
    if messageType == "error":
        return localLogger.error
    elif messageType == "warning":
        return localLogger.warning
    else:
        return localLogger.info


def validateAndLog(data):
    r = requests.post('https://validator.w3.org/nu/',
                      data=data, params={'out': 'json'},
                      headers={'Content-Type': 'text/html; charset=UTF-8'})

    messages = r.json()["messages"]
    for message in messages:
        log = getDynamicLogger(str(message["type"]))

        log("Type:         " + str(message["type"]))
        log("Line:         " + str(message["lastLine"]))
        try:
            log("Start Column: " + str(message["firstColumn"]))
            log("End Column:   " + str(message["lastColumn"]))
        except KeyError:
            pass

        log("Message:      " + str(message["message"]) + "\n")
