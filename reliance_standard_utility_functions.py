# ============================================================
def log(obj):  # log to the engine log
    obj = prepObjectForLogging(obj)
    t1 = Rdate.getTimeStamp()
    Rutilities.debug("\n!!~" + str((t1,float(t1-t0))) + "~" + thisDocument.getFormName() + thisDocument.getID() + "~" + str(obj) + "~" + thisDocument.getEncodedFieldText("ETQ$NUMBER") + ":" + thisUser.getName() + "~")


# ============================================================
def logList(objList):  # log to the engine log
    log("\n~logList start ***********************************************\n" + (
        thisDocument.getEncodedFieldText("ETQ$NUMBER")) + ":" + thisUser.getName())
    for obj in objList:
        log(obj)
    log("\n~logList End  ***********************************************\n")


# ============================================================
def prepObjectForLogging(obj):  # to make debugging easier and to avoid the null pointer exception
    if obj is None:
        obj = "None"  # else
    elif obj == "":
        obj = "empty string"
    return obj


# ============================================================
def businessLog(obj):  # for logs that should not be removed when releasing the package.
    log(obj)


# ============================================================
def log2(obj1, obj2):  # log to the engine log
    obj1 = prepObjectForLogging(obj1)
    obj2 = prepObjectForLogging(obj2)
    Rutilities.debug("\n~" + str(obj1) + ":=:" + str(obj2) + "~" + (
        thisDocument.getEncodedFieldText("ETQ$NUMBER")) + ":" + thisUser.getName() + "~" + (
                         thisDocument.getEncodedFieldText("ETQ$ASSIGNED")))


# ============================================================
# the difference between showBusinessError and showError is just the name to indicate this error is not intended for the customer.
# The error here is only to speed up development, and it should never be reached  once the module is mature.
def showError(message):
    # noinspection PyPep8
    message = "*** Exception: " + toString(message)
    log('showError ' + message)
    raise ValidationException, message


# ============================================================
# the difference between showBusinessError and showError is just the name to indicate this error is not intended for the customer.
# The error here is only to speed up development, and it should never be reached  once the module is mature.
def showBusinessError(message):
    # noinspection PyPep8
    message = "*** Error: " + toString(message)
    log('showBusinessError ' + message)
    raise ValidationException, message


# ============================================================
def showLocalizedBusinessError(errorKey):  # The error key is in common\localization\script\errors.properties
    # noinspection PyPep8
    message = Rstring.getError(errorKey, thisUser.getLocale())
    log('showLocalizedBusinessError ' + message)
    raise ValidationException, message


# ============================================================
def getMessageByKey(key):
    return Rstring.getError(key, thisUser.getLocale())


# ============================================================
def showDynamicLocalizedBusinessError(errorKey, dynamicPart):  # The error key is in common\localization\script\errors.properties
    # noinspection PyPep8
    message = Rstring.getError(errorKey, thisUser.getLocale().format(dynamicPart))
    log('showDynamicLocalizedBusinessError ' + message)
    raise ValidationException, message


# ============================================================
# the difference between showWarning and showBusinessWarning is just the name to indicate this error is not intended for the customer.
# The error here is only to speed up development, and it should never be reached  once the module is mature.
def showBusinessWarning(message):
    thisDocument.addWarning(message)
    log('showBusinessWarning ' + message)


# ============================================================
def showWarning(message):
    thisDocument.addWarning(message)
    log('showWarning ' + message)


# ============================================================
def addBusinessError(message):
    thisDocument.addError(message)
    log('addBusinessError ' + message)


# ============================================================
def addBusinessErrorToSubformRecord(record, message):
    record.addError(message)
    log('addBusinessErrorToSubformRecord ' + message)


# ============================================================
def addBusinessErrorToField(doc, fieldDn, message):
    field = doc.getField(fieldDn)
    field.addError(message)
    log('addBusinessErrorToField ' + message)

# ============================================================
def showDeveloperWarning(message):
    thisDocument.addWarning(message)
    log('showDeveloperWarning ' + message)


# ============================================================
def showLocalizedBusinessWarning(errorKey):
    message = getLocalizedString(errorKey)
    thisDocument.addWarning(message)
    log('showLocalizedBusinessWarning ' + message)


# ============================================================
def showLocalizedBusinessInformation(errorKey):
    message = getLocalizedString(errorKey)
    thisDocument.addInformation(message)
    log('showLocalizedBusinessInformation ' + message)


# ============================================================
def addInformation(message):
    thisDocument.addInformation(message)
    log('addInformation ' + message)


# ============================================================
def addWarning(message):
    thisDocument.addWarning(message)
    log('addWarning ' + message)


# ============================================================
def showDynamicLocalizedBusinessWarning(errorKey, dynamicPart):
    message = getLocalizedString(errorKey).format(dynamicPart)
    thisDocument.addWarning(message)
    log('showDynamicLocalizedBusinessWarning ' + message)

# ============================================================
def showLocalizedBusinessErrorOnField(doc, fieldDn, errorKey):
    message = getLocalizedString(errorKey)
    doc.getField(fieldDn).addError(message)
    log('showLocalizedBusinessErrorOnField ' + message)

# ============================================================
def getLocalizedString(errorKey):
    return Rstring.getError(errorKey, thisUser.getLocale())


# ============================================================
def showMsg(message):
    # noinspection PyPep8
    log('showMsg ' + message)
    raise ValidationException, toString(message)


# ============================================================
def unique(theList):
    if theList:
        return Rlist.unique(theList)
    return []


# ============================================================
def isFound(haystack, needle):
    return Rstring.containsCaseInsensitive(haystack, needle)


# ============================================================
def isSelectedValue(doc, fieldDn, selection):  # no try except
    # I use this method, because using the ID instead will break after promotion.
    # using the display text will break based on localization.
    field = doc.getField(fieldDn)
    if selection is None:
        return field.getValue() is None
    if isinstance(selection, str):
        fieldDisplayTextList = field.getUnlocalizedDisplayTextList()
        return Rlist.isMember(fieldDisplayTextList, selection)
    # This condition should only be used for a core system keyword list like the ENGINE_BOOLEAN MKL. 
    # The IDs in these keyword lists don't change across instances.
    fieldValue = field.getValue()
    # Known issue where unsaved single select checkboxes return None 
    # instead of 0 as their value.
    if fieldValue == None and not field.getSetting().isMultiValue() and field.getSetting().getFieldType() == 10:
        fieldValue = 0
    return selection == fieldValue


# ============================================================
def isSelectedValueInList(doc, fieldDn, selectionList):  # no try except
    field = doc.getField(fieldDn)
    if not selectionList:
        return field.getValue() is None
    fieldDisplayTextList = field.getUnlocalizedDisplayTextList()
    for selection in selectionList:
        if Rlist.isMember(fieldDisplayTextList, selection):
            return True
    return False


# ============================================================
def isFieldSelectedValue(fieldObj, selection):  # no try except
    # I use this method, because using the ID instead will break after promotion.
    # using the display text will break based on localization.
    if selection is None:
        return fieldObj.getValue() is None
    fieldDisplayTextList = fieldObj.getUnlocalizedDisplayTextList()
    return Rlist.isMember(fieldDisplayTextList, selection)


# ============================================================
def doesFieldTextContain(doc, fieldDn, substring, ignoreCase=False):
    displayText = doc.getField(fieldDn).getDisplayText()
    if ignoreCase:
        return Rstring.containsCaseInsensitive(displayText, substring)
    else:
        return Rstring.contains(displayText, substring)


# ============================================================
def isFieldValueInThisList(doc, fieldDn, selections):
    for s in selections:
        if isSelectedValue(doc, fieldDn, s):
            return True
    return False


# ============================================================
def doesMultiValueFieldHaveSelection(doc, fieldDn, selection):
    fieldDisplayTextList = doc.getField(fieldDn).getUnlocalizedDisplayTextList()
    return Rlist.isMember(fieldDisplayTextList, selection)


# ============================================================
def doesMultiValueFieldHaveOnlyThisSelection(doc, fieldDn, selection):
    fieldDisplayTextList = doc.getField(fieldDn).getUnlocalizedDisplayTextList()
    return fieldDisplayTextList == [selection]


# ============================================================
def doesMultiValueFieldHaveAtLeastOneOfTheFollowingSelections(doc, fieldDn, selections):
    fieldDisplayTextList = doc.getField(fieldDn).getUnlocalizedDisplayTextList()
    for s in selections:
        if Rlist.isMember(fieldDisplayTextList, s):
            return True
    return False


# ============================================================
def doesMultiValueFieldHaveAllTheFollowingSelections(doc, fieldDn, selections):
    fieldDisplayTextList = doc.getField(fieldDn).getUnlocalizedDisplayTextList()
    for s in selections:
        if not Rlist.isMember(fieldDisplayTextList, s):
            return False
    return True


# ============================================================
def doesMultiValueFieldHaveSelectionSubstring(doc, fieldDn, selectionSubstring):
    fieldDisplayTextList = doc.getField(fieldDn).getUnlocalizedDisplayTextList()
    for selection in fieldDisplayTextList:
        if Rstring.contains(selection, selectionSubstring):
            return True
    return False


# ============================================================
def doesMultiValueFieldHaveAtLeastOneOfTheFollowingSelectionSubstrings(doc, fieldDn, selectionSubstrings):
    for selectionSubstring in selectionSubstrings:
        if doesMultiValueFieldHaveSelectionSubstring(doc, fieldDn, selectionSubstring):
            return True
    return False


# ============================================================
def doesMultiValueFieldHaveAllTheFollowingSelectionSubstrings(doc, fieldDn, selectionSubstrings):
    for selectionSubstring in selectionSubstrings:
        if not doesMultiValueFieldHaveSelectionSubstring(doc, fieldDn, selectionSubstring):
            return False
    return True


# ============================================================
def isFieldEmpty(doc, fieldDn):  # Checks whether a field is None or an empty string
    return doc.getField(fieldDn).isEmpty()


# ============================================================
def isFieldObjEmpty(field):  # Checks whether a field is None or an empty string
    value = field.getField()
    return (value is None) or (value == "")


# ============================================================
def isFieldFilled(doc, fieldDn):  # Checks whether a field is None or an empty string
    return not isFieldEmpty(doc, fieldDn)


# ============================================================
def isMultiFieldEmpty(doc, fieldDn):
    return doc.getFieldValues(fieldDn) == []


# ============================================================
def areAllMultiFieldsEmpty(doc, fieldDnList):
    for fieldDn in fieldDnList:
        if isMultiFieldFilled(doc, fieldDn):
            return False
    return True


# ============================================================
def isMultiFieldFilled(doc, fieldDn):
    return doc.getFieldValues(fieldDn) != []


# ============================================================
def isLinkFieldEmpty(doc, fieldDn):
    return doc.getField(fieldDn).getDocLinks() == []


# ============================================================
def isLinkFieldFilled(doc, fieldDn):
    return doc.getField(fieldDn).getDocLinks() != []


# ============================================================
def isSubformEmpty(doc, subformDn):
    return doc.getSubform(subformDn).size() == 0


# ============================================================
def getDocumentById(application, formDn, docId):
    # noinspection PyPep8
    try:
        return application.getDocumentByKey(formDn, str(docId))
    except:
        log('getDocumentById: the document ID was not found: ' + formDn + ', ' + str(docId))
        return None


# ============================================================
def getDocumentByIdInEditMode(application, formDn, docId):
    log(('getDocumentByIdInEditMode', 'application, formDn, docId', application, formDn, docId))
    # noinspection PyPep8
    try:
        return application.getDocumentByKeyInEditMode(formDn, str(docId))
    except:
        log('getDocumentByIdInEditMode:Error: could not edit the document : formDn, docId: ' + formDn + ', ' + str(docId) + '\n ')
        # logList(('because of exception :', exception))
        return None


# ============================================================
def appendFieldValues(doc, fieldDn, valueList):
    oldValueList = doc.getFieldValues(fieldDn)
    oldValueList.extend(valueList)
    doc.setFieldValues(fieldDn, oldValueList)


# ============================================================
def appendTextFieldValue(doc, fieldDn, value, separator):
    oldValue = doc.getField(fieldDn).getDisplayText()
    oldValue += toString(value) + separator
    doc.setFieldValue(fieldDn, oldValue)


# ============================================================
def isDisplayText(applicationDn, linkTargetFormDn, intDocId, fieldDn, displayText):
    fieldValueDisplayText = getFieldDisplayText(applicationDn, linkTargetFormDn, intDocId, fieldDn)
    return fieldValueDisplayText == displayText


# ============================================================
# noinspection SpellCheckingInspection
def getDocumentFieldValue(docId, schema, mainTable, mainTablePK, tableFieldName):
    if docId:
        params = {"VAR$DOCID": str(docId), "VAR$SCHEMA": schema, "VAR$MAIN_TABLE": mainTable,
                  "VAR$TABLE_FIELD_NAME": tableFieldName,
                  "VAR$MTPK": mainTablePK}
        dao = thisApplication.executeQueryFromDatasource("ETQ_TRAINING_GET_DOCUMENT_FIELD_VALUE", params)
        if dao.next():
            return dao.getValue("FIELD_VALUE")
        else:
            businessLog(
                "getDocumentFieldValue: The target document is deleted or the FIELD_VALUE does not exist for docId: " + str(
                    docId) + "for mainTable: " + schema + "." + mainTable + ", for field column: " + tableFieldName)
            return None
    else:
        showError("getDocumentFieldValue: docId is None: " + tableFieldName)
        return None


# ============================================================
def getFieldBackendValuesByDocumentId(docId, schema, docPrimaryKey, joinTableName, joinTablePrimaryKey):
    if docId:
        params = {"ETQ$SCHEMA": schema, "ETQ$JOIN_TABLE_NAME": joinTableName, "ETQ$DOC_ID": str(docId),
                  "ETQ$DOC_PRIMARY_KEY": docPrimaryKey, "ETQ$JOIN_TABLE_PRIMARY_KEY": joinTablePrimaryKey}
        dao = thisApplication.executeQueryFromDatasource("ETQ_TRAINING_GET_MULTI_SELECT_FIELD_VALUES", params)
        values = []
        while dao.next():
            values.append(dao.getValue("VALUE_ID"))
        return values
    else:
        showError(
            'getFieldBackendValuesByDocumentId: docId is None: ' + docPrimaryKey + ',' + joinTableName + ',' + joinTablePrimaryKey)


# ============================================================
# the isChangedOnBackend does not work on multi select fields.
# this function does not work on link fields because they get auto-sent
# to the database as soon you change the field even if you did not save!
def areNonLinkMultiSelectFieldValuesInFrontendNotMatchBackend(doc, docId, fieldDn, schema, docPrimaryKey, joinTableName, joinTablePrimaryKey):
    backendValues = getFieldBackendValuesByDocumentId(docId, schema, docPrimaryKey, joinTableName, joinTablePrimaryKey)
    frontendValues = doc.getFieldValues(fieldDn)
    if len(backendValues) != len(frontendValues):
        return True
    for frontendValue in frontendValues:
        if frontendValue is not None:
            # for some reason the front end values are as a list of unicode strings!
            if int(frontendValue) in backendValues:
                backendValues.remove(int(frontendValue))
            else:
                return True
    if backendValues:
        return True
    return False


# ============================================================
def isSingleSelectFieldValueChanged(doc, fieldDn):  # does not work on link fields.
    if doc.getField(fieldDn).isValuesChangedLocally():
        return True
    return doc.getField(fieldDn).isValueChangedOnBackend()


# ============================================================
def getFormattedSqlListString(myList):
    if myList:
        return str(tuple(myList)).replace(',)', ')')
    return '(NULL)'


# ============================================================
def getDocumentSubformSingleSelectFieldValueList(docId, schema, docPrimaryKey, joinTableName, joinTablePrimaryKey):
    return getFieldBackendValuesByDocumentId(docId, schema, docPrimaryKey, joinTableName, joinTablePrimaryKey)


# ============================================================
def getSubformMultiSelectFieldBackendValuesByDocumentId(docId, schema, docPrimaryKey, subformTableName, subformTablePk,
                                                        fieldJoinTableName, fieldJoinTablePrimaryKey):
    query = getSubformMultiSelectFieldBackendValuesByDocumentIdSqlQuery(docId, schema, docPrimaryKey, subformTableName,
                                                                        subformTablePk,
                                                                        fieldJoinTableName, fieldJoinTablePrimaryKey)
    params = {"VAR$DAO": query}
    dao = thisApplication.executeQueryFromDatasource("ETQ_TRAINING_FULLY_CONSTRUCTED_DAO", params)
    values = []
    while dao.next():
        values.append(dao.getValue("VALUE_ID"))
    return unique(values)


# ============================================================
def getSubformMultiSelectFieldBackendValuesByDocumentIdSqlQuery(docId, schema, docPrimaryKey, subformTableName,
                                                                subformTablePk,
                                                                fieldJoinTableName, fieldJoinTablePrimaryKey):
    query = "SELECT\n"
    query += fieldJoinTablePrimaryKey + " VALUE_ID\n"
    query += "FROM\n"
    query += schema + "." + fieldJoinTableName + " " + fieldJoinTableName + "\n"
    query += "LEFT JOIN\n"
    query += schema + "." + subformTableName + " " + subformTableName
    query += " on (" + fieldJoinTableName + "." + subformTablePk + "=" + subformTableName + "." + subformTablePk + ")"
    query += "WHERE\n"
    query += subformTableName + "." + docPrimaryKey + "=" + str(docId)
    return query


# SELECT
# BASIC_JOB_STEPS_PPE_ID
# FROM
# JSA.BASIC_JOB_STEPS_PPE BASIC_JOB_STEPS_PPE
# LEFT JOIN
# JSA.BASIC_JOB_STEPS BASIC_JOB_STEPS ON (BASIC_JOB_STEPS_PPE.BASIC_JOB_STEPS_ID = BASIC_JOB_STEPS.BASIC_JOB_STEPS_ID)
# WHERE
# BASIC_JOB_STEPS.JSA_DOCUMENT_ID = 1
# ============================================================
def getDocumentSingleSelectFieldValueDictionary(docId, schema, mainTable, mainTablePK, tableFieldNameList):
    if docId and tableFieldNameList:
        query = getSqlQueryForSingleSelectFieldsValues(docId, schema, mainTable, mainTablePK, tableFieldNameList)
        params = {"VAR$DAO": query}
        dictionary = {}
        dao = thisApplication.executeQueryFromDatasource("ETQ_TRAINING_FULLY_CONSTRUCTED_DAO", params)
        if dao.next():
            for column in tableFieldNameList:
                dictionary[column] = dao.getValue(column)
        return dictionary
    else:
        businessLog("getDocumentFieldsValuesDictionary: invalid inputs")
        return {}


# ============================================================
def getSqlQueryForSingleSelectFieldsValues(docId, schema, mainTable, mainTablePK, tableFieldNameList):
    query = "SELECT\n"
    i = 0
    numberOfFields = len(tableFieldNameList)
    for column in tableFieldNameList:
        query += mainTable + "." + column + " " + column
        i += 1
        if i < numberOfFields:
            query += ",\n"
    query += "\nFROM\n"
    query += schema + "." + mainTable + " " + mainTable
    query += "\nWHERE\n"
    query += mainTable + "." + mainTablePK + " = " + str(docId)
    return query


# ============================================================
def getParentDocumentId():
    return getTargetDocIdFromLinkField(thisDocument, "ETQ$SOURCE_LINK")


# ============================================================
def getDocumentFieldValueByDocumentLink(doc, linkDn, schema, mainTable, mainTablePK, tableFieldName):
    linkedDocId = getTargetDocIdFromLinkField(doc, linkDn)
    if linkedDocId is None:
        return None
    return getDocumentFieldValue(linkedDocId, schema, mainTable, mainTablePK, tableFieldName)


# ============================================================
def getFieldDescriptionByValue(schema, tableName, primaryKey, descriptionColName, valueId):
    if (descriptionColName != "DESCRIPTION") or (primaryKey != "LOOKUP_ID"):
        log(('getFieldDescriptionByValue', schema, tableName, primaryKey, descriptionColName, valueId))
    if valueId:
        query = "SELECT " + descriptionColName + " DESCRIPTION FROM " + schema + "." + tableName
        query += "\nWHERE " + primaryKey + " = '" + str(valueId) + "'"
        params = {"VAR$DAO": query}
        dao = thisApplication.executeQueryFromDatasource("ETQ_TRAINING_FULLY_CONSTRUCTED_DAO", params)
        if dao.next():
            return dao.getValue("DESCRIPTION")
    return None


# ============================================================
def isTester():
    return True  # return thisUser.getName() in ("EtQAdministrator", "mjamal", "mjamal2")


# ============================================================
def isDocName(docName):
    return thisDocument.getEncodedFieldText("ETQ$NUMBER") == docName


# ============================================================
def warnAssignees():
    warn2("logAssignees", thisDocument.getFieldValues("ETQ$ASSIGNED"))


# ============================================================
def toString(s):  # to avoid the null pointer exception, especially when reading text values from DAO.
    if s is None:
        return ""
    return Rstring.toString(s)


# ============================================================
def isEmptyString(str_):
    if str_ is None:
        return True
    return Rstring.trim(str_) == ""


# ============================================================
def logField(FieldDn, doc=thisDocument):
    displayText = doc.getField(FieldDn).getDisplayText()
    log2(FieldDn, displayText)


# ============================================================
def readTableInfo(tableName):
    dictionary = {"ETQ$TABLE_NAME": tableName}
    dao = thisApplication.executeQueryFromDatasource("READ_TABLE_INFO", dictionary)
    while dao.next():
        log2(tableName, dao.getValue("COLUMN_NAME"))


# ============================================================
def warn(msg):
    if isTester():
        addWarning(str(msg))


# ============================================================
def warnField(doc, fieldDn):
    warn2(fieldDn, doc.getField(fieldDn).getDisplayText())


# ============================================================
def warn2(msg1, msg2):
    if isTester():
        addWarning(str(msg1) + "~" + str(msg2))


# ============================================================
def getCurrentDateAndTimeString():
    return Rdate.getDateTime(Rdate.currentDateTime(), 2, 3, thisUser)


# ============================================================
def addHoursToDate(date, hours):
    adjustedDate = None
    if date and hours:
        adjustedDate = Rdate.adjustDate(date, 0, 0, 0, hours, 0, 0)
    log(('addHoursToDate', 'date, hours, adjustedDate', date, hours, adjustedDate))
    return adjustedDate


# ============================================================
def addDaysToDate(date, days):
    return Rdate.adjustDate(date, 0, 0, days, 0, 0, 0)


# ============================================================
def addMonthsToDate(date, months):
    return Rdate.adjustDate(date, 0, months, 0, 0, 0, 0)


# ============================================================
# Rdate.adjustDate(Date date, int year, int month, int day, int hour, int minute, int second)
def addYearsToDate(date, years):
    return Rdate.adjustDate(date, years, 0, 0, 0, 0, 0)


# ============================================================
def isFirstDayDateBiggerThanSecondDate(date1, date2):  # this ignores the hour, it goes by the day
    if (date1 is None) or (date2 is None):
        return False
    date1 = Rdate.adjustTimeToMiddleOfDayGMT(date1)  # to make sure the time is ready for comparison.
    date2 = Rdate.adjustTimeToMiddleOfDayGMT(date2)
    return Rdate.compare(date1, date2) == 1


# ============================================================
def isFirstDateTimeBiggerThanSecondDateTime(date1, date2):  # this ignores the hour, it goes by the day
    if (date1 is None) or (date2 is None):
        return False
    return Rdate.compare(date1, date2, thisUser) == 1


# ============================================================
def isCurrentDateValue(dueDate):
    if not Rdate.compare(dueDate, Rdate.currentDate(thisUser)):
        return True
    return False


# ============================================================
def isFutureDateValue(date):  # this ignores the hour, it goes by the day
    return isFirstDayDateBiggerThanSecondDate(date, Rdate.currentDate(thisUser))


# ============================================================
def isFutureDate(dateFieldObj):  # this ignores the hour, it goes by the day
    return isFirstDayDateBiggerThanSecondDate(dateFieldObj.getValue(), Rdate.currentDate(thisUser))


# ============================================================
def isFutureDateTime(date):  # this ignores the hour, it goes by the day
    currentTime = thisDocument.getFieldValue("ETQ_ASSIGNMENT_CURRENT_DATETIME_HIDDEN")
    return isFirstDateTimeBiggerThanSecondDateTime(date, currentTime)


# ============================================================
def isPastDate(dateFieldObj):  # this ignores the hour, it goes by the day
    return isFirstDayDateBiggerThanSecondDate(Rdate.currentDate(thisUser), dateFieldObj.getValue())


# ============================================================
def isAfterDate(dateFieldObj, afterDateFieldObj):  # this ignores the hour, it goes by the day
    return isFirstDayDateBiggerThanSecondDate(dateFieldObj.getValue(), afterDateFieldObj.getValue())


# ============================================================
def isLeftDateOnlyFieldAfterRightDateOnlyField(doc, leftDateDn, rightDateDn):
    leftDateField = doc.getField(leftDateDn)
    rightDateField = doc.getField(rightDateDn)
    return isAfterDate(leftDateField, rightDateField)


# ============================================================
def isThisDateFieldAfterTheFollowingDateField(doc, dateFieldDn):
    dateField = doc.getField(dateFieldDn)
    return isAfterDate(thisField, dateField)


# ============================================================
def validateToGiveErrorIfThisDateFieldIsOnOrAfterOtherField(doc, fieldDn, errorKey):
    beforeDateFieldObj = doc.getField(fieldDn)
    if beforeDateFieldObj.getValue() and thisField.getValue():
        if not isBeforeDate(thisField, beforeDateFieldObj):
            showLocalizedBusinessError(errorKey)
            print False
        else:
            print True
    else:
        print True


# ============================================================
def isBeforeDate(dateFieldObj, beforeDateFieldObj):  # this ignores the hour, it goes by the day
    return isFirstDayDateBiggerThanSecondDate(beforeDateFieldObj.getValue(), dateFieldObj.getValue())


# ============================================================
def getTargetDocKeywordFieldValue(doc, linkDn, schema, mainTable, mainTablePK, tableFieldName):
    docId = getTargetDocIdFromLinkField(doc, linkDn)
    if docId is None:
        return None
    return getDocumentFieldValue(docId, schema, mainTable, mainTablePK, tableFieldName)


# ============================================================
def getTargetDocIdFromLinkField(doc, linkDn):
    links = doc.getField(linkDn).getDocLinks()
    if not links:
        return None
    if links[0]:  # to avoid null links for documents that are deleted after the link is created.
        if links[0].isDocumentExisting():
            return int(links[0].getDocKey().getKeyValue())
        return None
    else:
        return None


# ============================================================
def getTargetDocumentFromLinkField(doc, linkDn, linkTargetApplicationObject):
    links = doc.getField(linkDn).getDocLinks()
    if not links:
        return None
    if links[0]:  # to avoid null links for documents that are deleted after the link is created.
        if links[0].isDocumentExisting():
            return linkTargetApplicationObject.getDocument(links[0].getDocKey())
        else:
            return None
    else:
        return None


# ============================================================
def getTargetDocIdsFromLinksField(doc, linkDn):
    links = doc.getField(linkDn).getDocLinks()
    docIds = []
    for link in links:
        if link:  # to avoid null links for documents that are deleted after the link is created.
            if link.isDocumentExisting():
                if link.getDocKey():
                    if link.getDocKey().getKeyValue():
                        docIds.append(int(link.getDocKey().getKeyValue()))
    return docIds


# ============================================================
def haveLinkedDocuments(doc, linkDn):
    links = doc.getField(linkDn).getDocLinks()
    if links:
        return True
    return False


# ============================================================
def hasNoLinkedDocuments(doc, linkDn):
    return not haveLinkedDocuments(doc, linkDn)


# ============================================================
def areLinkedDocumentsCompleted(doc, linkDn):
    links = doc.getField(linkDn).getDocLinks()
    if links:
        for link in links:
            if link:  # in case the linked document is deleted, as it gives null
                if link.isDocumentExisting():
                    if not link.isLinkedDocumentCompleted():
                        return False
                else:
                    return False
            else:
                return False
        return True
    return False


# ============================================================
def areLinkedDocumentsClosed(doc, linkDn):
    links = doc.getField(linkDn).getDocLinks()
    if links:
        for link in links:
            if link:  # in case the linked document is deleted, as it gives null
                if link.isDocumentExisting():
                    if not (link.isLinkedDocumentCompleted() or link.isLinkedDocumentRejected()):
                        return False
                else:
                    return False
            else:
                return False
        return True
    return False


# ============================================================
def areLinkedDocumentsVoided(doc, linkDn):
    links = doc.getField(linkDn).getDocLinks()
    if links:
        for link in links:
            if link:  # in case the linked document is deleted, as it gives null
                if link.isDocumentExisting():
                    if not link.isLinkedDocumentRejected():
                        return False
                else:
                    return False
            else:
                return False
        return True
    return False


# ============================================================
def isAtLeastOneLinkedDocumentVoided(doc, linkDn):
    links = doc.getField(linkDn).getDocLinks()
    if links:
        for link in links:
            if link:  # in case the linked document is deleted, as it gives null
                if link.isDocumentExisting():
                    if link.isLinkedDocumentRejected():
                        return True
    return False


# ============================================================
def isAtLeastOneLinkedDocumentsCompleted(doc, linkDn):
    links = doc.getField(linkDn).getDocLinks()
    if links:
        for link in links:
            if link:  # in case the linked document is deleted, as it gives null
                if link.isDocumentExisting():
                    if link.isLinkedDocumentCompleted():
                        return True
    return False


# ============================================================
def isAtLeastOneLinkedDocumentsOpen(doc, linkDn):
    links = doc.getField(linkDn).getDocLinks()
    if links:
        for link in links:
            if link:  # in case the linked document is deleted, as it gives null
                if link.isDocumentExisting():
                    if link.isLinkedDocumentNormal():
                        return True
    return False


# ============================================================
# does not work for text areas, gets profile or document display text of a field!
def getFieldDisplayText(applicationDn, linkTargetFormDn, intDocId, fieldDn):
    # noinspection PyBroadException
    try:
        if intDocId is None:
            return None
        linkObj = PublicDocLink.createDocLink(applicationDn, linkTargetFormDn, int(intDocId))
        if linkObj.isDocumentExisting():
            fieldsValuesDict = linkObj.getFieldsValues([fieldDn])
            return fieldsValuesDict[fieldDn]
        else:
            return None
    except Exception:
        businessLog("getFieldDisplayText:" + fieldDn)
        return None


# ============================================================
def getParentDocFieldDisplayText(childDoc, applicationDn, formDn, fieldDn):
    parentDocKey = childDoc.getParentDocKey()
    if parentDocKey is None:
        return None
    parentDocKeyVal = parentDocKey.getKeyValue()
    if parentDocKeyVal is not None:
        displayTextDictionary = getFieldDisplayText(applicationDn, formDn, int(parentDocKeyVal), fieldDn)
        return displayTextDictionary[fieldDn]
    else:
        return None


# ============================================================
def getGroupIdByItsDesignName(groupDn):
    # noinspection PyBroadException
    try:
        userSetting = PublicSettingManager().getUserSetting(groupDn)
        if userSetting:
            return userSetting.getID()
        return None
    except Exception:
        businessLog("getGroupIdByItsDesignName")
        return None


# ============================================================
def getUserLoginName(userId):
    profile = PublicECCProfileManager().getUserProfile(userId)
    return profile.getUserName()


# ============================================================
def getPhaseIdByDesignName(designName):
    dictionary = {"ETQ$PHASE_DESIGN_NAME": designName}
    dao = thisApplication.executeQueryFromDatasource("ETQ_DAO_GET_FORM_ID_BY_DESIGN_NAME", dictionary)

    if dao.next():
        return dao.getValue("PHASE_ID")
    else:
        businessLog("getPhaseIdByDesignName: Invalid Phase Design Name" + toString(designName))
        return None


# ============================================================
def getFormIdByDesignName(designName):
    dictionary = {"ETQ$FORM_DESIGN_NAME": designName}
    dao = thisApplication.executeQueryFromDatasource("ETQ_DAO_GET_FORM_ID_BY_DESIGN_NAME", dictionary)

    if dao.next():
        return dao.getValue("FORM_ID")
    else:
        showError("getFormIdByDesignName: Invalid Form Design Name" + toString(designName))


# ============================================================
def getFieldIdByDesignName(designName):
    dictionary = {"VAR$FIELD_DESIGN_NAME": designName}
    dao = thisApplication.executeQueryFromDatasource("GET_FIELD_ID_BY_DESIGN_NAME", dictionary)
    if dao.next():
        return dao.getValue("FIELD_ID")
    else:
        businessLog("getFieldIdByDesignName: Invalid Field Design Name" + toString(designName))
        return None


# ============================================================
def formatListToString(myList, separator, prefix, Suffix):
    if (myList == []) or (myList == ['']) or (myList == [""]) or (myList == [None]) or (myList == ()):
        return "('-1')"  # "('')" is not good
    s = prefix
    i = -1
    for item in myList:
        i += 1
        if item is None:
            item = "-1"
        s += "'" + str(item) + "'"
        if i < len(myList) - 1:  # if not last element
            s += separator
    return s + Suffix


# ============================================================
def isMemberOfAny(groupList):
    for g in groupList:
        if thisUser.isMember(g):
            return True
    return False


# ============================================================
def isSendingForwardToPhase(phaseName):  # only works in the on-save formula.
    # noinspection PyBroadException
    try:
        if not thisPhase.isSendingForward():
            return False
        return thisPhase.getNextPhase().getName() == phaseName
    except Exception:
        return False  # for some reason. the if thisPhase==None line throws an exception when you assign to the next Person.


# ============================================================
def isSendingToPhase(phaseName):  # only works in the on-save formula.
    # noinspection PyBroadException
    try:
        if not (thisPhase.isSendingForward() or thisPhase.isSendingBackward() or thisPhase.isRejecting()):
            return False
        return thisPhase.getNextPhase().getName() == phaseName
    except Exception:
        return False  # for some reason. the if thisPhase==None line throws an exception when you assign to the next Person.


# ============================================================
def isSendingToTheCompletedPhase():  # only works in the on-save formula.
    # noinspection PyBroadException
    try:
        if thisPhase.isSendingForward():
            nextPhase = thisPhase.getNextPhase()  # this could return None if you have multiple assignees, and we are not at the last assigned.
            if nextPhase:
                return nextPhase.isCompleted()
        return False
    except Exception:
        return False


# ============================================================
def isSendingForwardToPhases(phaseNames):  # only works in the on-save formula.
    # noinspection PyBroadException
    try:
        if thisPhase.isSendingForward() or thisPhase.isRejecting():
            return thisPhase.getNextPhase().getName() in phaseNames
        else:
            return False
    except Exception:
        return False  # for some reason. the if thisPhase==None line throws an exception when you assign to the next Person.


# ============================================================
def isSending():  # only works in the on-save formula.
    # noinspection PyBroadException
    try:
        return thisPhase.isSendingForward() or thisPhase.isSendingBackward() or thisPhase.isRejecting()
    except Exception:
        return False  # for some reason. the if thisPhase==None line throws an exception when you assign to the next Person.


# ============================================================
def isSendingForwardToPhaseOtherThan(phaseName):  # only works in the on-save formula.
    # noinspection PyBroadException
    try:
        if not (thisPhase.isSendingForward()):
            return False
        return thisPhase.getNextPhase().getName() != phaseName
    except Exception:
        return False  # for some reason. the if thisPhase==None line throws an exception when you assign to the next Person.


# ============================================================
def isSendingForwardToPhasesOtherThan(phaseNameList):  # only works in the on-save formula.
    # noinspection PyBroadException
    try:
        if not (thisPhase.isSendingForward()):
            return False
        return not (thisPhase.getNextPhase().getName() in phaseNameList)
    except Exception:
        return False  # for some reason. the if thisPhase==None line throws an exception when you assign to the next Person.


# ============================================================
def isSendingToPhasesOtherThan(phaseNameList):
    # noinspection PyBroadException
    try:
        if not (thisPhase.isSendingForward() or thisPhase.isSendingBackward() or thisPhase.isRejecting()):
            return False
        return not (thisPhase.getNextPhase().getName() in phaseNameList)
    except Exception:
        return False  # for some reason. the if thisPhase==None line throws an exception when you assign to the next Person.


# ============================================================
def isSendingToPhaseOtherThan(phaseName):
    # noinspection PyBroadException
    try:
        if not (thisPhase.isSendingForward() or thisPhase.isSendingBackward() or thisPhase.isRejecting()):
            return False
        return thisPhase.getNextPhase().getName() != phaseName
    except Exception:
        return False  # for some reason. the if thisPhase==None line throws an exception when you assign to the next Person.


# ============================================================
def isSendingForwardOutOfPhase(phaseName):
    # noinspection PyBroadException
    try:
        if not thisPhase.isSendingForward():
            return False
        if thisPhase.getNextPhase().getName() == phaseName:  # if rerouting to the same phase.
            return False
        return thisPhase.getName() == phaseName
    except Exception:
        return False  # for some reason. the if thisPhase==None line throws an exception when you assign to the next Person.


# ============================================================
def isSendingOutOfPhase(phaseName):
    # noinspection PyBroadException
    try:
        if not (thisPhase.isSendingForward() or thisPhase.isSendingBackward() or thisPhase.isRejecting()):
            return False
        if thisPhase.getNextPhase().getName() == phaseName:  # if rerouting to the same phase.
            return False
        return thisPhase.getName() == phaseName
    except Exception:
        return False  # for some reason. the if thisPhase==None line throws an exception when you assign to the next Person.


# ============================================================
def isInTheFollowingPhaseForTheFirstTime(schema, formTableName, formPK, phaseDn):
    phaseList = getPhasesNameListFromPhaseTracking(schema, formTableName, formPK)
    count = 0
    for phase in phaseList:
        if phase == phaseDn:
            count += 1
    return count == 1


# ============================================================
# noinspection SpellCheckingInspection
def getPhasesNameListFromPhaseTracking(schema, formTableName, formPK):
    # noinspection PyBroadException
    try:
        phasesList = []
        formPhaseTrackingTable = "ETQ$" + str(formTableName) + "_PT"
        formPhaseTrackingAssigneeTable = "ETQ$" + formTableName + "_PTASN"
        params = {"ETQ$DOCID": str(thisDocument.getID()), "ETQ$SCHEMA": schema,
                  "ETQ$FORM_PHASE_TRACKING": formPhaseTrackingTable,
                  "ETQ$FORM_PHASE_TRACKING_ASN": formPhaseTrackingAssigneeTable, "ETQ_FORM_PK": formPK}
        dao = thisApplication.executeQueryFromDatasource("SH_GET_PHASE_TRACKING_INFO", params)
        while dao.next():
            phasesList.append(str(dao.getValue("PHASE_NAME")))
        return phasesList
    except Exception:
        businessLog("getPhasesNameListFromPhaseTracking")
        return None


# ============================================================
# noinspection SpellCheckingInspection
def getAssigneeIDListListFromPhaseTracking(documentId, schema, formTableName, formPK):
    # noinspection PyBroadException
    try:
        assigneeList = []
        formPhaseTrackingTable = "ETQ$" + str(formTableName) + "_PT"
        formPhaseTrackingAssigneeTable = "ETQ$" + formTableName + "_PTASN"
        params = {"ETQ$DOCID": str(documentId), "ETQ$SCHEMA": schema, "ETQ$FORM_PHASE_TRACKING": formPhaseTrackingTable,
                  "ETQ$FORM_PHASE_TRACKING_ASN": formPhaseTrackingAssigneeTable, "ETQ_FORM_PK": formPK}
        dao = thisApplication.executeQueryFromDatasource("SH_GET_ASSIGNEES_FROM_PHASE_TRACKING", params)
        while dao.next():
            assigneeList.append(str(dao.getValue("ASSIGNEE")))
        return unique(assigneeList)
    except Exception:
        businessLog("getAssigneeIDListListFromPhaseTracking")
        return None


# ============================================================
def getLastPhaseDesignNameFromPhaseTracking(schema, formTableName, formPK):
    return getDesignNameOfPhaseBeforeLastPhase(schema, formTableName, formPK)


# ============================================================
def getLastPhaseNameFromPhaseTracking(schema, formTableName, formPK):
    return getDesignNameOfPhaseBeforeLastPhase(schema, formTableName, formPK)


# ============================================================
# noinspection SpellCheckingInspection
def getDesignNameOfPhaseBeforeLastPhase(schema, formTableName, formPK):
    # noinspection PyBroadException
    try:
        phasesList = []
        formPhaseTrackingTable = "ETQ$" + str(formTableName) + "_PT"
        formPhaseTrackingAssigneeTable = "ETQ$" + formTableName + "_PTASN"
        params = {"ETQ$DOCID": str(thisDocument.getID()), "ETQ$SCHEMA": schema,
                  "ETQ$FORM_PHASE_TRACKING": formPhaseTrackingTable,
                  "ETQ$FORM_PHASE_TRACKING_ASN": formPhaseTrackingAssigneeTable, "ETQ_FORM_PK": formPK}
        dao = thisApplication.executeQueryFromDatasource("SH_GET_PHASE_TRACKING_INFO", params)
        while dao.next():
            phasesList.append(str(dao.getValue("PHASE_NAME")))
        if len(phasesList) < 2:
            return None
        return phasesList[len(phasesList) - 2]
    except Exception:
        businessLog("getDesignNameOfPhaseBeforeLastPhase")
        return None


# ============================================================
def getSingleSelectNameFieldUserIdList(doc, nameFieldDn):  # does not return group ids
    groupOrUserId = doc.getFieldValue(nameFieldDn)
    return unique(PublicUserManager.getUsersIDs([groupOrUserId]))


# ============================================================
def getMultiSelectNameFieldUserIdList(doc, nameFieldDn):  # does not return group ids
    groupOrUserIdList = doc.getFieldValues(nameFieldDn)
    return unique(PublicUserManager.getUsersIDs(groupOrUserIdList))


# ============================================================
def getSingleSelectNameFieldListUserIdList(doc, nameFieldDnList):
    userIdList = []
    for nameFieldDn in nameFieldDnList:
        userIdList.extend(getSingleSelectNameFieldUserIdList(doc, nameFieldDn))
    return unique(userIdList)


# ============================================================
def isThisUserMemberOfMultiSelectNameFieldList(doc, nameFieldDnList):
    for nameFieldDn in nameFieldDnList:
        if isThisUserMemberOfNamesField(doc, nameFieldDn):
            return True
    return False


# ============================================================
def isThisUserMemberOfNamesField(doc, nameFieldDn):
    field = doc.getField(nameFieldDn)
    if field is None:  # if the field is in a subform
        businessLog("isThisUserMemberOfNamesField: " + nameFieldDn)
        return False
    return isThisUserMemberOfNameOrGroupIDs(field.getValues())


# ============================================================
def isThisUserMemberOfNameOrGroupID(id_):
    if id_ is None:
        return False
    if toString(thisUser.getID()) == toString(id_):
        return True
    try:
        userProfile = PublicECCProfileManager().getUserProfile(id_)
    except Exception, exception:
        showWarning("isThisUserMemberOfNameOrGroupID: ID does not exist " + str(id_) + str(exception))
        return False
    if not userProfile.isGroup():
        return False
    userOrGroupDn = userProfile.getUserName()  # convert the user or the group ID to a group design name
    return thisUser.isMember(userOrGroupDn)


# ============================================================
def isThisUserMemberOfNameOrGroupIDs(idList):
    if not idList:
        return False
    for id_ in idList:
        if isThisUserMemberOfNameOrGroupID(id_):
            return True
    return False


# ============================================================
def clearFieldDnList(doc, FieldDnList):
    for filedDn in FieldDnList:
        doc.getField(filedDn).clear()


# ============================================================
def autoCreateFirstSubformRecordIfNoRecords(doc, subformDn):
    subform = doc.getSubform(subformDn)
    if subform.size() == 0:
        subform.newRecord()


# ============================================================
def getTargetDocIdFromLinkObject(link):
    if link is None:
        return None
    return link.getDocKey().getKeyValue()


# ============================================================
def doesFieldValueAlreadyExistInOtherDocuments(doc, fieldDn, schema, mainTable, mainTablePk, fieldColumnName):
    fieldValue = doc.getFieldValue(fieldDn)
    docId = doc.getID()
    query = getSqlQueryForFieldValueAlreadyExistInOtherDocuments(docId, fieldValue, schema, mainTable, mainTablePk,
                                                                 fieldColumnName)
    params = {"VAR$DAO": query}
    dao = thisApplication.executeQueryFromDatasource("ETQ_TRAINING_FULLY_CONSTRUCTED_DAO", params)
    if dao.next():
        return dao.getValue("TOTAL_COUNT") != 0

    businessLog("doesFieldValueAlreadyExistInOtherDocuments: Failed")
    return False


# ============================================================
def getSqlQueryForFieldValueAlreadyExistInOtherDocuments(docId, fieldValue, schema, mainTable, mainTablePk,
                                                         fieldColumnName):
    query = "SELECT COUNT(*) TOTAL_COUNT\n"
    query += "FROM " + schema + "." + mainTable
    if fieldValue:
        fieldValue = str(fieldValue).replace("'", "''")
        query += "\nWHERE " + fieldColumnName + " = '" + fieldValue + "'"
    else:
        query += "\nWHERE " + fieldColumnName + " is null"
    query += " and " + mainTablePk + " != " + str(docId)
    return query


# ============================================================
def getMklIdByOptionText(schema, mainTable, mainTablePk, descriptionColumnName, optionText):
    query = getSqlQueryForGetIdMklOptionText(schema, mainTable, mainTablePk, descriptionColumnName, optionText)
    params = {"VAR$DAO": query}
    dao = thisApplication.executeQueryFromDatasource("ETQ_TRAINING_FULLY_CONSTRUCTED_DAO", params)
    if dao.next():
        return dao.getValue("OPTION_ID")
    businessLog("getIdOfTheGivenFieldOptionText: Failed")
    return None


# ============================================================
def getSqlQueryForGetIdMklOptionText(schema, mainTable, mainTablePk, descriptionColumnName, optionText):
    query = "SELECT " + mainTablePk + " OPTION_ID"
    query += " FROM " + schema + "." + mainTable
    optionText = str(optionText).replace("'", "''")
    query += "\nWHERE " + descriptionColumnName + " = '" + optionText + "'"
    return query


# ============================================================
def getMklIdByOptionTextWithAdditionalConstraint(schema, mainTable, mainTablePk, descriptionColumnName, optionText,
                                                 constraint):
    query = getSqlQueryForGetIdMklOptionTextWithAdditionalConstraint(
        schema, mainTable, mainTablePk, descriptionColumnName, optionText, constraint)
    params = {"VAR$DAO": query}
    dao = thisApplication.executeQueryFromDatasource("ETQ_TRAINING_FULLY_CONSTRUCTED_DAO", params)
    if dao.next():
        return dao.getValue("OPTION_ID")
    businessLog("getIdOfTheGivenFieldOptionText: Failed")
    return None


# ============================================================
def getSqlQueryForGetIdMklOptionTextWithAdditionalConstraint(schema, mainTable, mainTablePk, descriptionColumnName,
                                                             optionText,
                                                             constraint):
    query = "SELECT " + mainTablePk + " OPTION_ID"
    query += " FROM " + schema + "." + mainTable
    optionText = str(optionText).replace("'", "''")
    query += "\nWHERE (" + descriptionColumnName + " = '" + optionText + "') " + constraint
    return query


# ============================================================
def getDocKeyFromDocId(docId, applicationName, formDn, primaryKey):
    return "ETQ$APPLICATION_NAME=" + toString(applicationName) + "&ETQ$FORM_NAME=" + toString(
        formDn) + "&ETQ$KEY_NAME=" + toString(
        primaryKey) + "&ETQ$KEY_VALUE=" + Rstring.toString(docId)


# ============================================================
def setRelatedLinks(doc, keyWordDn, linksDd, applicationName, formDn, primaryKey):
    docIds = doc.getFieldValues(keyWordDn)
    for docId in docIds:
        doc.getField(linksDd).addDocLink(getDocKeyFromDocId(docId, applicationName, formDn, primaryKey))
    doc.getField(keyWordDn).clear()


# ============================================================
def isInPhases(phaseList):
    return thisPhase.getName() in phaseList


# ============================================================
def defaultSubformWithOneNewRecord(doc, subformDn):
    subform = doc.getSubform(subformDn)
    if subform.size() == 0:
        subform.newRecord()


# ============================================================
def setDocLinks(fieldObj, links):
    fieldObj.clear()
    for link in links:
        fieldObj.addDocLink(link)


# ============================================================
def setDocLink(fieldObj, link):
    fieldObj.clear()
    fieldObj.addDocLink(link)


# ==============================================================
def copyFieldFromTo(sourceDoc, sourceFieldDn, targetDoc, targetFieldDn):
    sourceField = sourceDoc.getField(sourceFieldDn)
    targetDoc.getField(targetFieldDn).copy(sourceField)


# ==============================================================
def copyFieldsFromTo(parentDoc, childDoc, parentFieldDnChildFieldDnDictionary):
    for key, value in parentFieldDnChildFieldDnDictionary.iteritems():
        copyFieldFromTo(parentDoc, key, childDoc, value)


# ==============================================================
def inheritFieldValue(sourceDoc, targetDoc, sourceFieldDn, targetFieldDn):
    parentField = sourceDoc.getField(sourceFieldDn)
    targetDoc.getField(targetFieldDn).copy(parentField)


# ==============================================================
def inheritFieldsValues(parentDoc, childDoc, parentFieldDnChildFieldDnDictionary):
    for key, value in parentFieldDnChildFieldDnDictionary.iteritems():
        inheritFieldValue(parentDoc, childDoc, key, value)


# ==============================================================
def inheritLinkField(sourceDoc, targetDoc, sourceFieldDn, targetFieldDn):
    copyLinkField(sourceDoc, targetDoc, sourceFieldDn, targetFieldDn)


# ==============================================================
def inheritMainLinkToParentDocument(parentDoc, childDoc, childFieldDn, applicationDn, parentFormDn):
    if parentDoc:
        if parentDoc.getID():
            linkObj = PublicDocLink.createDocLink(applicationDn, parentFormDn, int(parentDoc.getID()))
            childDoc.getField(childFieldDn).clear()
            childDoc.getField(childFieldDn).addDocLink(linkObj)
            return
    businessLog("inheritMainLinkToParentDocument: None document: " + childFieldDn)


# ============================================================
def copyLinkField(sourceDoc, targetDoc, sourceFieldDn, targetFieldDn):
    targetDoc.getField(targetFieldDn).removeDocLinks()
    links = sourceDoc.getField(sourceFieldDn).getDocLinks()
    for link in links:
        if link:
            if link.isDocumentExisting():
                targetDoc.getField(targetFieldDn).addDocLink(link)


# ============================================================
def inheritSameLinkField(sourceDoc, targetDoc, fieldDn):
    copyLinkField(sourceDoc, targetDoc, fieldDn, fieldDn)


# ============================================================
def createDocLink(applicationId, linkTargetFormId,
                  docId):  # this used with DAO returned values from ETQ$DOCUMENT_LINKS table.
    if docId:
        applicationDn = getApplicationDesignNameById(applicationId)
        linkTargetFormDn = getFormDesignNameById(linkTargetFormId)
        link = PublicDocLink.createDocLink(applicationDn, linkTargetFormDn, int(docId))
        return link
    return None


# ============================================================
def getFormDesignNameById(formId):
    query = getFormDesignNameByIdDaoSqlQuery(formId)
    params = {"VAR$DAO": query}
    dao = thisApplication.executeQueryFromDatasource("ETQ_TRAINING_FULLY_CONSTRUCTED_DAO", params)
    if dao.next():
        return dao.getValue("FORM_NAME")
    showError("getFormDesignNameById: Form is not found by this ID: " + str(formId))


# ============================================================
def getFormDesignNameByIdDaoSqlQuery(formId):
    query = """
        SELECT
            FORM_ID FORM_ID,
            FORM_NAME FORM_NAME
            FROM
            ENGINE.FORM_SETTINGS
            WHERE FORM_ID = 'VAR$FROM_ID'
        """
    query = fillParameterInQuery(query, "VAR$FROM_ID", formId)
    return query


# ============================================================
def getPhaseDesignNameById(phaseId):
    query = getPhaseDesignNameByIdDaoSqlQuery(phaseId)
    params = {"VAR$DAO": query}
    dao = thisApplication.executeQueryFromDatasource("ETQ_TRAINING_FULLY_CONSTRUCTED_DAO", params)
    if dao.next():
        return dao.getValue("PHASE_NAME")
    showError("getPhaseDesignNameById: Phase is not found by this ID: " + str(phaseId))


# ============================================================
def getPhaseDesignNameByIdDaoSqlQuery(phaseId):
    query = """
            SELECT
            PHASE_ID PHASE_ID,
            PHASE_NAME PHASE_NAME
            FROM
            ENGINE.PHASE_SETTINGS
            WHERE PHASE_ID = 'VAR$PHASE_ID'
        """
    query = fillParameterInQuery(query, "VAR$PHASE_ID", phaseId)
    return query


# ============================================================
def getApplicationDesignNameById(ApplicationId):
    query = getApplicationDesignNameByIdDaoSqlQuery(ApplicationId)
    params = {"VAR$DAO": query}
    dao = thisApplication.executeQueryFromDatasource("ETQ_TRAINING_FULLY_CONSTRUCTED_DAO", params)
    if dao.next():
        return dao.getValue("APPLICATION_NAME")
    showError("getApplicationDesignNameById: Application is not found by this ID: " + str(ApplicationId))


# ============================================================
def getApplicationDesignNameByIdDaoSqlQuery(ApplicationId):
    query = """
        SELECT
            APPLICATION_ID APPLICATION_ID,
            APPLICATION_NAME APPLICATION_NAME
            FROM
            ENGINE.APPLICATION_SETTINGS
            WHERE APPLICATION_ID = 'VAR$APPLICATION_ID'
        """
    query = fillParameterInQuery(query, "VAR$APPLICATION_ID", ApplicationId)
    return query


# ============================================================
def getLinkAttributesDictionary(linkId, applicationSchema):
    query = getLinkAttributesDictionarySqlQuery(linkId, applicationSchema)
    params = {"VAR$DAO": query}
    dao = thisApplication.executeQueryFromDatasource("ETQ_TRAINING_FULLY_CONSTRUCTED_DAO", params)
    myDict = {}
    if dao.next():
        myDict["APPLICATION_ID"] = dao.getValue("APPLICATION_ID")
        myDict["FORM_ID"] = dao.getValue("FORM_ID")
        myDict["DOCUMENT_ID"] = dao.getValue("DOCUMENT_ID")
        return myDict
    else:
        showError("getLinkAttributesDictionary: failed " + str(linkId))


# ============================================================
def getLinkAttributesDictionarySqlQuery(linkId, applicationSchema):
    query = """
        SELECT
        LINK_ID LINK_ID,
        APPLICATION_ID APPLICATION_ID,
        FORM_ID FORM_ID,
        DOCUMENT_ID DOCUMENT_ID
        FROM
        VAR$APPLICATION_SCHEMA.ETQ$DOCUMENT_LINKS
        WHERE LINK_ID = 'VAR$LINK_ID'
        """
    query = fillParameterInQuery(query, "VAR$LINK_ID", linkId)
    query = fillParameterInQuery(query, "VAR$APPLICATION_SCHEMA", applicationSchema)
    return query


# ==============================================================
def inheritSameFieldValue(parentDoc, childDoc, fieldDn):
    parentField = parentDoc.getField(fieldDn)
    childField = childDoc.getField(fieldDn)
    childField.copy(parentField)


# ==============================================================
def inheritSameFields(parentDoc, childDoc, fieldDnList):
    for fieldDn in fieldDnList:
        inheritSameFieldValue(parentDoc, childDoc, fieldDn)


# ==============================================================
def inheritParentSubform(parentDoc, childDoc, subformDn, fieldDnList):
    records = parentDoc.getSubform(subformDn).getRecords()
    childSubform = childDoc.getSubform(subformDn)
    for r in records:
        childRecord = childSubform.newRecord()
        for fieldDn in fieldDnList:
            inheritSameFieldValue(r, childRecord, fieldDn)


# ============================================================
def copySourceFieldToTarget(sourceDoc, sourceDn, targetDoc, targetDn):
    targetDoc.getField(targetDn).copy(sourceDoc.getField(sourceDn))


# ============================================================
def setLinkFieldByTargetDocId(doc, fieldDn, targetDocId, targetApplicationDn, targetFormDn, targetFormPrimaryKey):
    doc.getField(fieldDn).removeDocLinks()
    if targetDocId:
        doc.getField(fieldDn).addDocLink(
            getDocKeyFromDocId(targetDocId, targetApplicationDn, targetFormDn, targetFormPrimaryKey))


# ============================================================
def appendLinkFieldByTargetDocId(doc, fieldDn, targetDocId, targetApplicationDn, targetFormDn, targetFormPrimaryKey):
    if targetDocId:
        doc.getField(fieldDn).addDocLink(
            getDocKeyFromDocId(targetDocId, targetApplicationDn, targetFormDn, targetFormPrimaryKey))


# ============================================================
def getListString(valueList):
    if valueList:
        valueList.sort()
        valueListString = ""
        for value in valueList:
            valueListString += " " + str(value) + ","
        valueListString = valueListString[:-1]  # remove last coma
        return valueListString
    return ""


# ============================================================
def getLatestDate(dateList):
    if not dateList:
        return None
    latestDate = dateList[0]
    for date in dateList:
        if date:
            if Rdate.compare(date, latestDate) == 1:
                latestDate = date
    return latestDate


# ============================================================
def fillParameterInQuery(query, parameter, value, escapeChars=True):
    if escapeChars:
        value = str(value).replace("'", "''")  # prevent sql injection error.
    return query.replace(parameter, str(value))


# ============================================================
def getUserProfile():
    userId = thisDocument.getFieldValue("ETQ_TRAINING_EMPLOYEE_PROFILE_EMPLOYEE_INFORMATION_USER")
    if userId:
        manager = PublicECCProfileManager()
        profile = manager.getUserProfile(userId)
        return profile
    else:
        return None


# ============================================================
#def setStatus(profile):
    #if profile:
        #if profile.isInactive():
            #thisDocument.getField("ETQ_TRAINING_EMPLOYEE_PROFILE_EMPLOYEE_INFORMATION_STATUS").setValueUsingDisplayText(
                #["Inactive"])
        #else:
            #thisDocument.getField("ETQ_TRAINING_EMPLOYEE_PROFILE_EMPLOYEE_INFORMATION_STATUS").setValueUsingDisplayText(
                #["Active"])


# ============================================================
#def setFirstName(profile):
    #firstName = profile.getFirstName()
    #thisDocument.setFieldValue("ETQ_TRAINING_EMPLOYEE_PROFILE_EMPLOYEE_INFORMATION_FIRST_NAME", firstName)


# ============================================================
#def setMiddleName(profile):
    #middleName = profile.getMiddleName()
    #thisDocument.setFieldValue("ETQ_TRAINING_EMPLOYEE_PROFILE_EMPLOYEE_INFORMATION_MIDDLE_NAME", middleName)


# ============================================================
#def setLastName(profile):
    #lastName = profile.getLastName()
    #thisDocument.setFieldValue("ETQ_TRAINING_EMPLOYEE_PROFILE_EMPLOYEE_INFORMATION_LAST_NAME", lastName)


# ============================================================
#def getReportsTo(userId):
    #query = """Select REPORTS_TO_ID REPORTS_TO_ID from ENGINE.USER_SETTINGS where USER_ID =  """ + "'" + str(
        #userId) + "'"
    #dictionary = {"VAR$DAO": query}
    #dao = thisApplication.executeQueryFromDatasource("ETQ_TRAINING_FULLY_CONSTRUCTED_DAO", dictionary)
    #if dao.next():
        #return dao.getValue("REPORTS_TO_ID")
    #return None


# ============================================================
def getUserTeam(userId):
    query = """Select USER_ID USER_ID from ENGINE.USER_SETTINGS where REPORTS_TO_ID =  """ + "'" + str(userId) + "'"
    dictionary = {"VAR$DAO": query}
    dao = thisApplication.executeQueryFromDatasource("ETQ_TRAINING_FULLY_CONSTRUCTED_DAO", dictionary)
    teamIds = []
    while dao.next():
        teamIds.append(dao.getValue("USER_ID"))  # do not filter out inactive users here, because all we need here is to know if the current user is a manager for the given userID
    return unique(teamIds)


# ============================================================
def isThisUserManagerOfGivenUser(userOrGroupId):
    teamIds = getUserTeam(thisUser.getID())
    teamUserIds = PublicUserManager.getUsersIDs(teamIds)
    if userOrGroupId:
        userIds = PublicUserManager.getUsersIDs([userOrGroupId])
        for userId in userIds:
            if doesUserReportsToLoggedInUser(userId, teamUserIds):
                return True
    return False


# ============================================================
def doesUserReportsToLoggedInUser(userId, teamUserIds):
    return userId in teamUserIds
  
  
# ============================================================
def validateModuleProfileExistence():
    log('validateModuleProfileExistence')
    if not doesTheModuleProfileExist():
        showLocalizedBusinessError('ETQ_TRAINING_MODULE_PROFILE_PLEASE_CREATE')
     
    
# ============================================================
#def setUserLocations(userId, doc):
    #primaryLocation = [getDocumentFieldValue(userId, "ENGINE", "USER_SETTINGS", "USER_ID", "PRIMARY_LOCATION_ID")]
    #otherLocations = getFieldBackendValuesByDocumentId(userId, "ENGINE", "USER_ID", "OTHER_LOCATIONS", "LOCATION_ID")
    #primaryLocation.extend(otherLocations)
    #locations = primaryLocation
    #doc.setFieldValues("ETQ$LOCATIONS", locations)


# ============================================================
def isForceAuthenticationEnabledOnEverySave(formDn):
    sql = "SELECT HISTORY_TYPE, AUTHENTICATION_OPTIONS_ID FROM ENGINE.FORM_SETTINGS FSETTINGS WHERE FSETTINGS.FORM_NAME = '{}'".format(formDn)
    params = {'VAR$DAO': sql}
    dao = thisApplication.executeQueryFromDatasource('ETQ_TRAINING_FULLY_CONSTRUCTED_DAO', params)
    if dao.next():
        historyType = dao.getValue('HISTORY_TYPE')
        authenticateOnEverySave = dao.getValue('AUTHENTICATION_OPTIONS_ID')
        if historyType == 3 and authenticateOnEverySave == 1:
            return True
    return False


# ============================================================
def getFormattedDateStr(date):
    if date:
        return Rdate.getDateTime(date, 0, 3, thisUser)
    else:
        return "getFormattedDateStr: None date"


# ============================================================
def getDocumentByID(application, formDn, docId):
    # noinspection PyPep8
    try:
        return application.getDocumentByKey(formDn, str(docId))
    except:
        log('getDocumentByID: the document ID was not found: ' + formDn + ', ' + str(docId))
        return None


# ============================================================
#  UTILITY FUNCTION
#  Attempts to open the document with the passed application design name and DocKey
#  Returns the document object or None if the document can't be opened
# noinspection PyPep8
def getDocumentFromApplicationAndDocKey(appName, docKey):
    try:
        return thisUser.getApplication(appName).getDocument(docKey)
    except:
        return None