from .WinBioAuth import WinBioAuthenticator

def run_test():
    authenticator = WinBioAuthenticator()
    
    # Open a session
    job = authenticator.openSession()
    if not job.state:
        return

    # Enumerate biometric units
    job = authenticator.enumerateBiometricUnits()
    if not job.state:
        authenticator.closeSession()
        return

    units = job.response
    print(f"{len(units)} Units found.")

    if len(units) > 0:
        # Print unit information
        for unit in units:
            print(f"  Unit ID: {unit.UnitId}")
            # Use .value to get string from c_char_p
            if unit.Description:
                print(f"  Description: {unit.Description.decode('utf-8')}")
            if unit.Manufacturer:
                print(f"  Manufacturer: {unit.Manufacturer.decode('utf-8')}")
            if unit.Model:
                print(f"  Model: {unit.Model.decode('utf-8')}")

        # Try to identify
        print("\nAttempting to identify...")
        print("Please touch the fingerprint sensor.")
        job = authenticator.identify()
        if job.state:
            identity = job.response
            print(f"Identification successful.")
            # SID is in identity.Value.AccountSid.Data
            # A function would be needed to convert the SID to a string.
        else:
            print("Identification failed.")

    # Close the session
    authenticator.closeSession()

if __name__ == "__main__":
    run_test()