

from ansible import errors

try:
    import boto.utils
except ImportError:
    raise errors.AnsibleError(
        "Can't LOOKUP(aws_region): module boto is not installed")

from ansible.plugins.lookup import LookupBase

class LookupModule(LookupBase):

    def run(self, terms=None, inject=None, **kwargs):
      try:
        instance_identity = boto.utils.get_instance_identity()
        aws_region = instance_identity['document']['region']
      except:
        aws_region = None

      return [aws_region]
