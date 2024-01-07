# ==============================================================================================
# Base script for creating consistent emails throughout the NREL system
# chad.neal@scesconsulting.com | 5/19/2022
# ==============================================================================================
# use following script to call method: 
# exec(publicEtQScriptProfilesManager.getScriptProfile("EMAIL_ETQSCRIPT_PROFILE").getFormula())
# ==============================================================================================

ENABLE_DEBUGGING = True
def addToLog(message):
 if ENABLE_DEBUGGING:
  Rutilities.debug(str(message))

# -------------------------------------------------------------------------------------------------
def getLastComment():
 overallLastComment = ""
 lastComment = ""
 commentSubform = thisDocument.getSubform("ETQ$COMMENT_HISTORY")
 if (commentSubform != None and commentSubform.size() > 0):
  lastRecord = commentSubform.getRecord(commentSubform.size() - 1)
  lastComment =  lastRecord.getEncodedFieldText("ETQ$COMMENT_HISTORY_TEXT")
  if lastComment == None or lastComment == "":
   lastComment = "<i> no comments recorded </i>"
 return lastComment

# -------------------------------------------------------------------------------------------------
def printAssignEmailSubject():
 subject = thisDocument.getDisplayName()
 subject += " - "
 subject += thisDocument.getField("ETQ$CURRENT_PHASE").getUnlocalizedEncodedDisplayText()
 subject += " - "
 subject += " [DUE: "
 subject += thisDocument.getField("ETQ$DUE_DATE").getUnlocalizedEncodedDisplayText()
 subject += "]"
 print subject

# -------------------------------------------------------------------------------------------------
def printAssignEmailBody():
 message = "<b>-Action Required-</b><br> "
 message +=  "<b>Type</b>: " + thisDocument.getField("ETQ$CURRENT_PHASE").getEncodedDisplayText() + " in " + thisDocument.getField("ETQ$CURRENT_WORKFLOW").getEncodedDisplayText() 
 message += "<br>"
 message +=   "<b>Due Date</b>: " + thisDocument.getField("ETQ$DUE_DATE").getEncodedDisplayText() 
 message +=   "<br>"
 #Last Comment in Email EtQScript
 message+= "<b>Last Comments: </b>"
 message+= getLastComment()
 message += " <br>"
 message += " You are assigned and required to complete this record."
 message += " <br>"
 message += " Please click link to open the document: "
 print message
 return None

# -------------------------------------------------------------------------------------------------
def printNotifyEmailSubject():
 subject = thisDocument.getField("ETQ$CURRENT_PHASE").getUnlocalizedEncodedDisplayText()
 subject += ": "
 subject += thisDocument.getField("ETQ$CURRENT_WORKFLOW").getUnlocalizedEncodedDisplayText()
 subject += " - "
 subject += " [DUE: "
 subject += thisDocument.getField("ETQ$DUE_DATE").getUnlocalizedEncodedDisplayText()
 subject += "]"
 print subject

# -------------------------------------------------------------------------------------------------
def printNotifyEmailBody():
 message = "<b>-Notification Only-</b><br> "
 message +=  "<b>Type</b>: " + thisDocument.getField("ETQ$CURRENT_PHASE").getEncodedDisplayText() + " in " + thisDocument.getField("ETQ$CURRENT_WORKFLOW").getEncodedDisplayText() 
 message += "<br>"
 message +=   "<b>Due Date</b>: " + thisDocument.getField("ETQ$DUE_DATE").getEncodedDisplayText() 
 message +=   "<br>"
 #Last Comment in Email EtQScript
 message+= "<b>Last Comments: </b>"
 message+= getLastComment()
 message += " <br>"
 message += " Please click link to open the document: "
 print message
 return None