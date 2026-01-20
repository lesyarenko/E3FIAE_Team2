import secrets
import hashlib
import uuid
import subprocess

def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    if salt is None:
        salt = secrets.token_hex(16)
    hash_bytes = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100_000)
    return hash_bytes.hex(), salt

def verify_password(stored_hash_hex: str, salt: str, password: str) -> bool:
    computed_hash, _ = hash_password(password, salt=salt)
    return computed_hash == stored_hash_hex

def generate_id6():
    return str(uuid.uuid4())[:6]

def generate_id8():
    return str(uuid.uuid4())[:8]

def get_git_info():
    try:
        commit_id = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD']
        ).strip().decode('utf-8')
        git_tag = subprocess.check_output(
            ['git', 'describe', '--tags']
        ).strip().decode('utf-8')
        git_tag = git_tag.split('-')[0]   # nur der erste Teil = Sprint_2
        return commit_id, git_tag
    except subprocess.CalledProcessError:
        # Falls keine Tags existieren oder Git nicht verfügbar ist
        return None, None
