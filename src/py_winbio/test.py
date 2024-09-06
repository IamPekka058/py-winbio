from WinBioAuth import WinBioAuthenticator

authenticator = WinBioAuthenticator()
authenticator.openSession()
size = authenticator.enumerateBiometricUnits().response['size']
print("{0} Units found.".format(size.value))
if size.value > 0:
    authenticator.locateSensor()
    authenticator.identify()
authenticator.closeSession()
