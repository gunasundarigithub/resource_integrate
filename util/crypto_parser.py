"""
Copyright July 2020, TCS

File Name: crypto_parser.py
Description: Utility Encryption and Decryption. (Private|Secret-Key Encryption)

Change Log:
Release Date    Revision Date     Changes By      Description
------------    -------------     -----------     ------------
                31 July 2020      Sabarish AC       Initial
"""
# ------------------------------------------- Builtin Modules --------------------------------------------------------------------
import base64
import hashlib
from Crypto.Cipher import AES
import os
from Crypto.Hash import MD5
import sys

# ------------------------------------------- Customized Modules --------------------------------------------------------------------
from util import util   # Internal Module import
sys.path.append('E:\\Sabs Learning\\resource_integrate\\util')  # Paste your appropriate path

config = util.get_conf()
log = util.get_logger_obj()

# Custom Exception Class.
class CredentialLookupException(Exception):
  pass

class ShiftPlanCrypto(object):
  def __init__(self):
    # Assume a randome string as seed to perform encryption
    _seed = b'SabpNRI00shiXNoEW3g'
    # Generate Hash Value encoded data in hexadecimal format.
    self.secret_key = MD5.new(_seed).hexdigest()
    print('secret key : ' + str(self.secret_key))
    # Create sha256 hash object for secret key.
    self.secret_key_obj = hashlib.sha256(self.secret_key.encode()).digest()
    
  """
  Perform encryption using cryptograhic method. Define Initialization Vector, Cipher and 
  perform b64 encoding on IV+Cipher combination.
  """
  def do_encrypt(self, raw_str):
    raw_str_padded = self._pad(raw_str)
    # Generate a Initialization vector (random byte object) for cryptographic encryption 
    # wuth arg: byte size (AES.block_size defaults to 16 bytes)
    IV = os.urandom(AES.block_size)
    # Using Mode CBC Mode, IV is a data block to be transmitted to the receiver. It must be authenticated by
    # the receiver and it should be picked randomly.
    cipher = AES.new(self.secret_key_obj, AES.MODE_CBC, IV)
    encoded_pwd = self.b64encode(IV + cipher.encrypt(raw_str_padded))
    return encoded_pwd

  """
  Perform decryption using Initialization vector and cipher, decrypted cipher text is decoded with 
  base64 decoding to get actual user text.
  """
  def do_decrypt(self, enc_pwd):
    enc = base64.b64decode(enc_pwd)
    # Create an initialization vector from encrypted key.
    IV = enc[:AES.block_size]
    print(IV)
    cipher = AES.new(self.secret_key_obj, AES.MODE_CBC, IV)
    cipher_text = cipher.decrypt(enc[AES.block_size:])
    decoded_pwd = self.b64decode(cipher_text)
    return decoded_pwd
  
  """
  Base64 Encoding
  """
  def b64encode(self, enc_string):
    encoded_text = base64.b64encode(enc_string)
    return encoded_text
  
  """
  Base64 Decoding
  """
  def b64decode(self, ciph_text):
    decode_text = self._unpad(ciph_text).decode('utf-8')
    return decode_text

  """
  Add Padded Characters for the given integer unicode.
  """
  @staticmethod
  def _pad(s):
    bit_size = 32
    return s + (bit_size - len(s) % bit_size) * chr(bit_size - len (s) % bit_size)
  
  """
  UnPad Characters for decoding.
  """
  @staticmethod
  def _unpad(s):
    return s[:-ord(s[len(s)-1:])]
  
  """
  Get Creds for the user.
  """
  def get_credentials(self, pwd, appname=''):
    env_file = util.get_env_file()
    credential={}
    if config['app']['secret_key'] == self.secret_key:
      if appname:
        if pwd:
          credential["pass"]= self.do_decrypt(pwd)
        else:
          raise CredentialLookupException(f"Empty password in {env_file}")
      else:
        raise CredentialLookupException(f"Appname: {appname} is not found")
    else:
      raise CredentialLookupException(f"Secret key doesn't match")
    return credential
  
  if __name__=="__main__":
    criptic_obj = ShiftplanCrypto()
    plain_pwd= "MyPassword"
    enc_pwd= criptic_obj.do_encrypt(plain_pwd)
    print("encoded password :------", enc_pwd)
    print("Actual Password : --------", criptic_obj.get_credetials(enc_pwd, appname="app-sift-mgmt"))
