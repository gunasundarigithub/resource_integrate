import base64
import hashlib
from Crppto.Cipher import AES
import os
from Crypto.Hash import MD5
import sys
from util import util #internal Module import
sys.path.append('C:\\ctpt\\app-shift-mgmt\\') #paste your appropriate path

config=util.get_conf()
log=util.get_logger_obj()

class CredentialLookupException(Exception):
  pass

Class ShiftPlanCrypto(object):
  def _init_(self):
    #Assume a randome string as seed to perform encryption
    _seed = b'SabpNRI00shiXNoEW3g'
    self.secret_key=MD5.new(_seed).hexdigest()
    self.secret_key_obj=hashlib.sha256(slef.secret_key.encode()).digest()
    
    def do_encrypt(self, raw_str):
      raw_str_padded = self._pad(raw_str)
      IV= os.urandom(AES.block_size)
      cipher= AES.new(self.secret_key_obj, AES.MODE_CBC, IV)
      encoded_pwd= self.b64encode(IV + cipher.encrypt(raw_str_padded))
      return encoded_pwd
    
    def do_decrypt(self, enc_pwd):
      enc = base64.b64decode(enc_pwd)
      IV = enc[:AES.block_size]
      print(IV)
      cipher = AES.new(self.secret_key_obj, AES.MODE_CBC, IV)
      cipher_text = cipher.decrypt(enc[AES.block_size:])
      decoded_pwd=self.b64decode(cipher_text)
      return decoded_pwd
    
    def b64encode(self, enc_string):
      encoded_text = base64.b64encode(enc_string)
      return encoded_text
    
    @staticmethod
    def _pad(s):
      bit_size=32
      return s+ (bit_size- len(s) % bit_size) * chr(bit_size - len (s) % bit_size)
    
    @staticmethod
    def _unpad(s):
      return s[:-ord(s[len(s)-1:])]
    
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
    
    if __name__==__"main"__:
      criptic_obj = ShiftplanCrypto()
      plain_pwd= "MyPassword"
      enc_pwd= criptic_obj.do_encrypt(plain_pwd)
      print("encoded password :------", enc_pwd)
      print("Actual Password : --------", criptic_obj.get_credetials(enc_pwd, appname="app-sift-mgmt"))
