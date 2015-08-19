#!/usr/bin/python
import yaml

def main():
  module = AnsibleModule(
    supports_check_mode = False,
    argument_spec = dict(
      name       = dict(required=True),
      host       = dict(required=True),
      trusted    = dict(default=False, choices=BOOLEANS),
      guisso_dir = dict(default='/u/apps/guisso')
    )
  )

  name = module.params['name']
  host = module.params['host']
  guisso_dir = module.params['guisso_dir']
  trusted = "trusted" if module.params['trusted'] else "false"

  rc, out, err = module.run_command("docker-compose run --rm -T web rake apps:create[{},{},{}]".format(name, host, trusted), cwd=guisso_dir)

  if rc == 0:
    guisso_output = yaml.load(out)
    module.exit_json(changed=True, client_id=guisso_output['client_id'], client_secret=guisso_output['client_secret'], client_name=name)
  else:
    module.fail_json(msg="Registration in guisso failed", reason=err)


from ansible.module_utils.basic import *
if __name__ == '__main__':
  main()
