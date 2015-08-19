#!/usr/bin/python
import yaml

def main():
  module = AnsibleModule(
    supports_check_mode = False,
    argument_spec = dict(
      name      = dict(required=True),
      password  = dict(required=True),
      url       = dict(required=True),
      account_name   = dict(required=True),
      account_pass   = dict(required=True),
      interface      = dict(default='rss', choices=['rss', 'qst_client', 'http_get_callback', 'http_post_callback']),
      interface_user = dict(default=''),
      interface_pass = dict(default=''),
      nuntium_dir    = dict(default='/u/apps/nuntium')
    )
  )

  cmd = ("docker-compose run --rm -T "
         "-e NUNTIUM_URL={} "
         "-e NUNTIUM_ACCOUNT_NAME={} "
         "-e NUNTIUM_ACCOUNT_PASS={} "
         "-e NUNTIUM_APP_NAME={} "
         "-e NUNTIUM_APP_PASS={} "
         "-e NUNTIUM_APP_INTERFACE={} "
         "-e NUNTIUM_APP_INTERFACE_USER={} "
         "-e NUNTIUM_APP_INTERFACE_PASS={} "
         "web rake clients:register").format(*[module.params[p] for p in ['url', 'account_name', 'account_pass', 'name', 'password', 'interface', 'interface_user', 'interface_pass']])

  rc, out, err = module.run_command(cmd, cwd=module.params['nuntium_dir'])

  if rc == 0:
    output = yaml.load(out)
    output['changed'] = True
    module.exit_json(**output)
  else:
    module.fail_json(msg="Registration in nuntium failed", reason=err)


from ansible.module_utils.basic import *
if __name__ == '__main__':
  main()
