import os, sys

sys.path.append(os.path.abspath(".."))

from core import users

def test_contacts_exist():
    assert len(users.contacts()) > 0

def test_identities_exist():
    assert len(users.identities()) > 0
    
def test_identities_have_private_keys():
    ids = users.identities()

    if len(ids) == 0:
        assert False, "No private keys available to test"
        
    for id in ids:
        has_private_sk = False
        for sk in id.key.subkeys:
            if sk.secret:
                has_private_sk = True
        assert has_private_sk

def test_contacts_only_have_public_keys():
    ids = users.contacts()

    if len(ids) == 0:
        assert False, "No public keys available to test"
    
    for id in ids:
        has_private_sk = False
        for sk in id.key.subkeys:
            if sk.secret:
                has_private_sk = True
        assert not has_private_sk

def has_valid_subkey(user):
    for subkey in user.key.subkeys:
        if not (subkey.invalid or subkey.expired or subkey.disabled):
            return True
    return False

def test_valid_subkeys_can_export_public_key():
    for id in users.identities():
        tested_one = False
        if has_valid_subkey(id):
            tested_one = True
            assert "PUBLIC KEY" in id.public_key()
    if not tested_one:
        assert False, "Unable to find valid subkeys for test"


