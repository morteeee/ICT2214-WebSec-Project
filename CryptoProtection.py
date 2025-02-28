from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA256

class CryptoProtection:
    def __init__(self):
        self.rsa_key = RSA.generate(2048)
        self.private_key = self.rsa_key
        self.public_key = self.rsa_key.publickey()

    def get_public_key_pem(self):
        return self.public_key.export_key().decode('utf-8')

    def decrypt_aes_key(self, encrypted_aes_key):
        cipher_rsa = PKCS1_OAEP.new(self.private_key, hashAlgo=SHA256)
        aes_key = cipher_rsa.decrypt(encrypted_aes_key)
        return aes_key

    def aes_encrypt(self, plaintext, aes_key):
        cipher_aes = AES.new(aes_key, AES.MODE_GCM)
        ciphertext, tag = cipher_aes.encrypt_and_digest(plaintext.encode('utf-8'))
        return {
            'ciphertext': ciphertext.hex(),
            'nonce': cipher_aes.nonce.hex(),
            'tag': tag.hex()
        }

    def aes_decrypt(self, ciphertext_hex, nonce_hex, tag_hex, aes_key):
        ciphertext = bytes.fromhex(ciphertext_hex)
        nonce = bytes.fromhex(nonce_hex)
        tag = bytes.fromhex(tag_hex)
        cipher_aes = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher_aes.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode('utf-8')