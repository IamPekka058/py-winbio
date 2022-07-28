from WinBioAuth import WinBioAuthenticator

authenticator = WinBioAuthenticator()

size = authenticator.enumerateBiometricUnits().response
print(size)
if(size > 0):
    authenticator.identify()
    authenticator.verify()
