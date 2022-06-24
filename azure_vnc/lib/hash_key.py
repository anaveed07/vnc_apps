import hashlib
import logging
log = logging.getLogger(__name__)

class GenerateHash:

  def generate_token(self, vm_name, vm_id, sec_key):
    return self._make_token_with_vm(vm_name, vm_id, sec_key)

  def check_token(self, vm_name, vm_id, token, sec_key):
    """
    Check that a token is correct for a given user.
    """
    if self._make_token_with_vm(vm_name, vm_id, sec_key) != token:
      return False

    return True

  def _make_token_with_vm(self, vm_name, vm_id, sec_key):
    hash = hashlib.sha512(str(sec_key).encode('utf-8') + str(vm_name).encode('utf-8') +
       str(vm_id).encode('utf-8')).hexdigest()[::3]
    
    return hash

#if __name__ == '__main__':
#  hash = GenerateHash()
#  hs = hash.generate_token('Centos6', 12)
#  print hs
