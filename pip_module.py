import pip

installed = pip.get_installed_distributions()
installed_list = sorted(["%s==%s" % (i.key, i.version) for i in installed])
print '\n'.join(installed_list)
