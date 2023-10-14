   # if studentInfo['in_hospital'] == True:
                        studentInfo['in_hospital'] = False
                        ref.child('in_hospital').set(studentInfo['in_hospital'])