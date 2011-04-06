import hashlib

def email_hash(email):
    return hashlib.md5(email.strip().lower()).hexdigest()


            
        