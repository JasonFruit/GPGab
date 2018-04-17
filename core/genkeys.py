from io import BytesIO

from datetime import datetime

import gpgme

_ctx = gpgme.Context()
_ctx.armor=True

full_use_param = """
<GnupgKeyParms format="internal">
Key-Type: RSA
Key-Length: 4096
Name-Real: %(name)s
Name-Comment: %(comment)s
Name-Email: %(email)s
Expire-Date: 0
Passphrase: %(passphrase)s
</GnupgKeyParms>
"""

signing_only_param = """
<GnupgKeyParms format="internal">
  Key-Type: RSA
  Key-Usage: sign
  Key-Length: 1024
  Name-Real: Testing
  Name-Comment: comment
  Name-Email: someone@example.com
  Expire-Date: 0
</GnupgKeyParms>
"""

def gen_keypair(name, email, comment, passphrase):
    """Generate a new public and private key for the specified user info,
    locked with `passphrase`"""
    
    params = full_use_param % {"name": name,
                               "email": email,
                               "comment": comment,
                               "passphrase": passphrase}
    
    keypair = _ctx.genkey(params)

    return keypair

if __name__ == "__main__":
    
    print(gen_keypair("Jimbo Joebob",
                      "jimjo@gmail.com",
                      "Wat",
                      "This is Jimbo's passphrase"))


