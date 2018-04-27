from io import BytesIO

from datetime import datetime

import gpgme

_ctx = gpgme.Context()
_ctx.armor=True

class User(object):
    """Represents a user of the communications system"""
    def __init__(self, gpg_uid, key):
        self.email = gpg_uid.email
        self.name = gpg_uid.name
        self.comment = gpg_uid.comment
        self.key = key
        
    def export_public_key(self, fn):
        """Export the user's public key to an ascii-armored file at `fn`"""

        # look for a valid subkey
        with open(fn, "wb") as f:
            for subkey in self.key.subkeys:
                if not (subkey.invalid or
                        subkey.expired or
                        subkey.disabled):
                    _ctx.export(subkey.fpr, f)
                    return True
        return False
    
    def export_private_key(self, fn):
        """Export the user's private key to an ascii-armored file at `fn`"""

        # look for a subkey that's valid and secret
        with open(fn, "wb") as f:
            for subkey in self.key.subkeys:
                if not (subkey.invalid or
                        subkey.expired or
                        subkey.disabled):
                    if subkey.secret:
                        _ctx.export(subkey.fpr, f, True)
                        return True
        return False
    
    def public_key(self):
        """Return an ascii-armored string of the user's public key"""
        
        bio = BytesIO()
        
        for subkey in self.key.subkeys:
            if not (subkey.invalid or subkey.expired or subkey.disabled):
                _ctx.export(subkey.fpr, bio)
                return bio.getvalue().decode("ascii")
            
        return None
    
    def __repr__(self):
        """Make a comprehensible representation of the user's info"""
        
        return "%s (%s) <%s>" % (self.name, self.comment, self.email)

def _users(query=None, secret=False):
    """Return a list of users that contain the specified query elements,
    and who have secret or public keys as specified"""
    
    out = []
    
    if query:
        keys = _ctx.keylist(query, secret)
    else:
        keys = _ctx.keylist("", secret)
        
    for key in keys:
        for uid in key.uids:
            out.append(User(uid, key))
            
    return out

def contacts(query=None):
    """Return a list of users with public keys which match the specified
    query

    """
    return _users(query, secret=False)

def identities(query=None):
    """Return a list of users with private keys which match the
    specified query
    """
    return _users(query, secret=True)

if __name__ == "__main__":
    print(identities()[0].public_key())
    # print(identities())
    # print(contacts())
