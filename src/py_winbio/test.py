from WinBioAuth import WinBioAuthenticator

authenticator = WinBioAuthenticator()

size = authenticator.enumerateBiometricUnits().response['size']
print("{0} Units found.".format(size.value))
if size.value > 0:
    authenticator.identify()
