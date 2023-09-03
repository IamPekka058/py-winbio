from WinBioAuth import WinBioAuthenticator

authenticator = WinBioAuthenticator()

size = authenticator.enumerateBiometricUnits().response
print("{0} Units found.".format(size))
if(size > 0):
    #authenticator.acquireFocus()
    #input("Hallo?")
    #authenticator.locateSensor()
    #input("Identifizierung?")
    #authenticator.identify()
    authenticator.enrollBegin()
    authenticator.enrollCapture()
    input("Verifizierung?")
    #authenticator.verify()
