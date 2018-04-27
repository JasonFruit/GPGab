import os
from io import BytesIO

import gpgme



_ctx = gpgme.Context()
_ctx.armor = True

class VerificationError(Exception):
    pass

def sign(data, signers, clear=False):

    """Return an ascii-armored signed version of `data`.
       `data`: the data to sign
       `signers`: the private-key identities with which to sign
       `clear`: whether to sign in cleartext or not, default False
    """
    
    if type(data) == str:
        data = data.encode("utf-8")
        
    bio_in = BytesIO(data)
    bio_out = BytesIO()

    # signers are stored in the context
    _ctx.signers = [s.key for s in signers]

    if clear:
        sigs = _ctx.sign(bio_in, bio_out, gpgme.SIG_MODE_CLEAR)
    else:
        sigs = _ctx.sign(bio_in, bio_out)

    # reset the context's signers to empty
    _ctx.signers = ()
        
    return bio_out.getvalue()



def verify(signature, user):
    """Check the signature on some data.  Return a list of fingerprints of
    signing keys and the unsigned data

    """
    
    bio_in = BytesIO(signature)
    bio_out = BytesIO()

    signatures = _ctx.verify(bio_in, None, bio_out)

    in_sigs = False

    for sig in signatures:
        if sig.fpr in [sk.fpr for sk in user.key.subkeys]:
            if sig.status == None:
                in_sigs = True
            else:
                raise VerificationError(sig.status.args[0])
            
    return in_sigs, bio_out.getvalue()



if __name__ == "__main__":
    import users
    identities = users.identities()[:0]
    me = users.identities()[1]

    data = sign("This is a test.", identities)

    print(verify(data, me))
