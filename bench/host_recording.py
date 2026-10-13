"""Makes emulator_qa.dart record with the emulator (host side) instead of screenrecord inside Android."""

import sys

path = sys.argv[1]
source = open(path).read()
guest_start = "final recorder = await Process.start('adb', ['shell', 'screenrecord', '--bit-rate', '8000000', onDevice]);"
guest_stop = "await Process.run('adb', ['shell', 'pkill', '-INT', 'screenrecord']);"
host_start = (
    "final recorder = await Process.start('adb', ['emu', 'screenrecord', 'start', '--time-limit', '180', "
    "'--fps', '60', '${out.absolute.path}/$name.webm']);\n"
    "  recorder.stdout.listen(stdout.add);"
)
host_stop = "print((await Process.run('adb', ['emu', 'screenrecord', 'stop'])).stdout);"
assert guest_start in source and guest_stop in source, "emulator_qa.dart no longer records as expected"
open(path, "w").write(source.replace(guest_start, host_start).replace(guest_stop, host_stop))
