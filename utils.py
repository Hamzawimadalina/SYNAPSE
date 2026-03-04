import hashlib

def hash_mdp(mdp):
    return hashlib.sha256(mdp.encode()).hexdigest()