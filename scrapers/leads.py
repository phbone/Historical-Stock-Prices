__author__ = 'bryanwan'
from validate_email import validate_email

email = raw_input("Enter an Email: ")
is_valid = validate_email(email, verify=True)

print is_valid