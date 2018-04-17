import os
from io import BytesIO

import gpgme



_ctx = gpgme.Context()
_ctx.armor=True



def encrypt(data, recipients):

    # use bytes, or else encode string as bytes
    if type(data) == bytes:
        bio_in = BytesIO(data)
    elif type(data) == str:
        bio_in = BytesIO(data.encode("utf-8"))
    else:
        raise TypeError("Unable to encrypt data of type '%s'." % type(data))

    bio_out = BytesIO()

    _ctx.encrypt([r.key for r in recipients],
                 0,
                 bio_in,
                 bio_out)

    bio_out.seek(0)

    # the encrypted data is ascii-armored
    return bio_out.getvalue().decode("ascii")



def encrypt_file(plain_fn, crypt_fn, recipients):
    
    if not os.path.exists(plain_fn):
        raise FileNotFoundError("Cleartext file '%s' not found." % plain_fn)
        
    with open(plain_fn, "rb") as inf:
        with open(crypt_fn, "wb") as outf:
            keys = [r.key for r in recipients]
            _ctx.encrypt(keys, 0, inf, outf)



def decrypt(data):
    bio_in = BytesIO(data)
    bio_out = BytesIO()

    _ctx.decrypt(bio_in, bio_out)

    bio_out.seek(0)
    
    return bio_out.getvalue()



if __name__ == "__main__":
    import users
    print(users.contacts("groundhog"))
    data = encrypt("This is a test", users.contacts("groundhog"))
    print(data)
    print(decrypt(data))
