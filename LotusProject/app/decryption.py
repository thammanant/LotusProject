import jwt


def decrypt(key, encrypted_message):
    # decrypt the data using the key
    decode = jwt.decode(encrypted_message, key, algorithms=['HS256'])
    return decode


# if __name__ == "__main__":
#     print(decrypt("c435d980d70d", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
#                                   ".eyJwb2ludHMiOjEwLCJpYXQiOjE3MTcxNDkzNzQuMDA5MzQ4Mn0"
#                                   ".3JTmUQoipyt1RQjyfeh4h4RZcrioMj1Q290SWT-xgPw"))
