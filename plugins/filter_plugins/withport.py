def withport(value, port="80"):
  if port == None or str(port) == "80":
    return value
  else:
    return "{}:{}".format(value, port)

def withdomain(value, domain, port="80"):
  return withport("{}.{}".format(value, domain), port)

def withprotocol(value, protocol="http"):
  return "{}://{}".format(protocol, value)

def asurl(value, domain, port="80", protocol="http"):
  return withprotocol(withdomain(value, domain, port), protocol)

class FilterModule(object):
  def filters(self):
    return {
      'withport': withport,
      'withdomain': withdomain,
      'withprotocol': withprotocol,
      'asurl': asurl
    }
