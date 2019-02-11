from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.fernet import Fernet


def encrypt_two_key(bin_data, public_key):
    public_key_pem = serialization.load_pem_public_key(public_key, backend=default_backend())
    return public_key_pem.encrypt(
        bin_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    );


def decrypt_two_key(cipher_text, private_key):
    private_key_pem = serialization.load_pem_private_key(
        private_key,
        password=None,
        backend=default_backend()
    );
    return private_key_pem.decrypt(
        cipher_text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    );


def generate_public_private_key_pair():
    private_key_pair = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    );
    private_key = private_key_pair.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    );
    public_key = private_key_pair.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    );
    return public_key, private_key;


def encrypt_single_key(text, key):
    return Fernet(key).encrypt(text.encode('utf-8'));


def decrypt_single_key(token, key):
    return Fernet(key).decrypt(token).decode('utf-8');


def generate_new_single_key():
    return Fernet.generate_key();
