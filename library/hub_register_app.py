#!/usr/bin/python
import yaml

def main():
  module = AnsibleModule(
    supports_check_mode = False,
    argument_spec = dict(
      name      = dict(required=True),
      host      = dict(required=True),
      type      = dict(required=True),
      hub_dir   = dict(default='/u/apps/hub')
    )
  )

  cmd = "docker-compose run --rm -T web rake shared_connectors:register['{}','{}',{}]".format(*[module.params[p] for p in ['name', 'host', 'type']])
  rc, out, err = module.run_command(cmd, cwd=module.params['hub_dir'])

  if rc == 0:
    output = yaml.load(out)
    module.exit_json(changed=True, guid=output['guid'], secret_token=output['secret_token'])
  else:
    module.fail_json(msg="Registration in hub failed", reason=err)


from ansible.module_utils.basic import *
if __name__ == '__main__':
  main()
