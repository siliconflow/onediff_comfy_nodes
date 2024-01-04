import subprocess
import sys

command = [
    "python3",
    "-m",
    "pip",
    "install",
    "--pre",
    "oneflow",
    "-f",
    "https://oneflow-pro.oss-cn-beijing.aliyuncs.com/branch/community/cu118"
]

process = subprocess.Popen(
    command,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

while True:
    output = process.stdout.readline()
    error = process.stderr.readline()
    if output == '' and error == '' and process.poll() is not None:
        break
    if output:
        print(output.strip())
    if error:
        print(error.strip(), file=sys.stderr)

return_code = process.poll()

if return_code != 0:
    raise RuntimeError(f"Installation failed with return code {return_code}")
else:
    print("Installation successful")

