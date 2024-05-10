import subprocess
import sys
import os
import git
import shutil
from tqdm.auto import tqdm
from git.remote import RemoteProgress

if sys.platform.startswith("win"):
    raise OSError("Onediff does not support Windows systems. "
                  "Please use WSL2: https://github.com/siliconflow/onediff/wiki")

class GitProgress(RemoteProgress):
    def __init__(self):
        super().__init__()
        self.pbar = tqdm()

    def update(self, op_code, cur_count, max_count=None, message=''):
        self.pbar.total = max_count
        self.pbar.n = cur_count
        self.pbar.pos = 0
        self.pbar.refresh()

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

onediff_url = "https://github.com/siliconflow/onediff"
comfy_path = os.environ.get('COMFYUI_PATH')
custom_nodes_path = os.path.join(comfy_path, 'custom_nodes')
repo_path = os.path.join(custom_nodes_path, "onediff")

print(f"Download: git clone '{onediff_url}'")
repo = git.Repo.clone_from(onediff_url, repo_path, recursive=True, progress=GitProgress())
repo.git.clear_cache()
repo.close()

onediff_path = os.path.join(custom_nodes_path, "onediff")
old_onediff_comfy_nodes_path = os.path.join(custom_nodes_path, "onediff_comfy_nodes")
new_onediff_comfy_nodes_path = os.path.join(onediff_path, "onediff_comfy_nodes")

shutil.move(os.path.abspath(__file__), onediff_path)
shutil.rmtree(old_onediff_comfy_nodes_path)
shutil.move(new_onediff_comfy_nodes_path, custom_nodes_path)
shutil.rmtree(onediff_path)

print("Onediff comfy nodes are ready.")