import subprocess

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

result = subprocess.run(command, capture_output=True, text=True)

if result.returncode != 0:
    raise RuntimeError(f"Installation failed. Error: {result.stderr}")
else:
    print("Installation successful")

