import subprocess

proc = subprocess.Popen(['pip', 'freeze'], stdout=subprocess.PIPE)
freeze = proc.communicate()[0]
freeze = freeze.split('\n')
edc_packages = [
    x for x in freeze if 'clinicedc' in x or 'erikvw' in x or 'edc-'in x]
third_party_packages = [x for x in freeze if x and x not in edc_packages]
edc_packages.sort()
third_party_packages.sort()
