from WinBioAuth import WinBioAuthenticator

authenticator = WinBioAuthenticator()

size = authenticator.enumerateBiometricUnits().response
print("{0} Units found.".format(size))
if(size > 0):
    authenticator.locateSensor()
    input("Identifizierung?")
    authenticator.identify()
    input("Verifizierung?")
    authenticator.verify()
