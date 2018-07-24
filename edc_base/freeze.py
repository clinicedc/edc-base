from subprocess import Popen, PIPE

with Popen(["pip", "freeze"], stdout=PIPE, encoding='utf8') as proc:
    freeze = proc.stdout.read()


freeze = freeze.split('\n')
edc_packages = [x for x in freeze if 'clinicedc' in x or 'erikvw' in x]
third_party_packages = [x for x in freeze if x and x not in edc_packages]
edc_packages.sort()
third_party_packages.sort()
