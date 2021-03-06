#!/usr/bin/env python

from collections import defaultdict
import difflib
import os
import sys


if not os.path.exists('versions.cfg'):
    print 'No "versions.cfg" in {}'.format(os.getcwd())
    sys.exit(1)


# read data
lines_before = []
lines_after = []
version_lines = []
section_started = False
section_stopped = False


with open('versions.cfg') as fio:
    original = map(str.rstrip, fio.readlines())


for line in original:
    if line.strip() == '[versions]':
        section_started = True
        lines_before.append(line)
        continue
    elif section_started and line.startswith('['):
        section_stopped = True
        lines_after.append(line)
    elif not section_started:
        lines_before.append(line)
    elif section_stopped:
        lines_after.append(line)
    elif section_started and not section_stopped:
        version_lines.append(line.strip())
    else:
        raise ValueError('Unkown state..')


versions_map = defaultdict(list)
for line in version_lines:
    if not line.strip():
        continue
    line = line.split('#')[0].strip()
    if not line:
        continue
    pkg, version = map(str.strip, line.split('='))
    versions_map[pkg].append(version)

new_version_lines = []
for pkg, versions in sorted(versions_map.items()):
    if len(versions) == 1:
        version = versions[0]
    else:
        print versions
        version = versions.pop()

        print pkg.ljust(30), u'\u2714\ufe0f  ', version
        for ignored in versions:
            print len(pkg.ljust(30)) * ' ', u'\U0001f6ab  ', ignored

    new_version_lines.append(' = '.join((pkg, version)))


raw_input('Press any key to continue...')

new_lines = lines_before + new_version_lines + lines_after
print '\n'.join(difflib.unified_diff(original, new_lines, 'versions.cfg - original', 'versions.cfg - new', n=5))
raw_input('Press any key to accept changes and write versions.cfg.')

with open('versions.cfg', 'w+') as fio:
    fio.write('\n'.join(new_lines).rstrip())
    fio.write('\n')