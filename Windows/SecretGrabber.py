def get_secret(secret_name, region_name):

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        print("I GOT IT: " + str(get_secret_value_response))
    except ClientError as e:
        print(e)
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            print("Secret not able to be found with the provided KMS key. Please make sure you have configured AWS boto3 correctly.")
            quit()
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            print("The secrets server has encountered an error. This likely isn't your fault, so run the program again.")
            quit()
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            print("One of your parameters (secret_name or region_name) is incorrect. Please verify their values and try again.")
            quit()
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            print("Your parameters are invalid for the current state of the resource. Please ensure you have set up your secret correctly.")
            quit()
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            print("The secrets server cannot find the secret you have requested. Please ensure you are using the correct secret_name")
            quit()
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            print("Successfully retrieved secret")
            secret = get_secret_value_response['SecretString']
            return secret
        else: #Probably isn't used in your situation but it depends on your situation. Still implemented it anyways though :P
            print("Successfully retrieved binary encoded secret, decrypting...")
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            print("Secret decrypted!")
            return decoded_binary_secret
 