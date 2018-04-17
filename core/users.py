from io import BytesIO

from datetime import datetime

import gpgme

_ctx = gpgme.Context()
_ctx.armor=True

class User(object):
    def __init__(self, gpg_uid, key):
        self.email = gpg_uid.email
        self.name = gpg_uid.name
        self.comment = gpg_uid.comment
        self.key = key
        
    def export_public_key(self, fn):
        with open(fn, "wb") as f:
            for subkey in self.key.subkeys:
                if not (subkey.invalid or
                        subkey.expired or
                        subkey.disabled):
                    _ctx.export(subkey.fpr, f)
                    return True
        return False
    
    def export_private_key(self, fn):
        with open(fn, "wb") as f:
            for subkey in self.key.subkeys:
                if not (subkey.invalid or
                        subkey.expired or
                        subkey.disabled):
                    if subkey.secret:
                        _ctx.export_secret(subkey.fpr, f)
                        return True
        return False
    
    def public_key(self):
        bio = BytesIO()
        
        for subkey in self.key.subkeys:
            if not (subkey.invalid or subkey.expired or subkey.disabled):
                _ctx.export(subkey.fpr, bio)
                return bio.getvalue().decode("ascii")
            
        return None
    
    def __repr__(self):
        return "%s (%s) <%s>" % (self.name, self.comment, self.email)

def contacts(query=None, secret=False):
    out = []
    if query:
        keys = _ctx.keylist(query, secret)
    else:
        keys = _ctx.keylist("", secret)
        
    for key in keys:
        for uid in key.uids:
            out.append(User(uid, key))
            
    return out

def identities(query=None):
    return contacts(query, secret=True)

if __name__ == "__main__":
    print(identities()[0].public_key())
    # print(identities())
    # print(contacts())
