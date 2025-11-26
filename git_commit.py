from git import Repo
import tempfile
import os
import shutil

def auto_commit(repo_url: str, branch: str, repo_path: str, files: list):
    \"\"\"
    Clone repo_url (using auth included in URL if needed), write files into repo_path inside the repo,
    ommit and push.

    repo_url: full clone URL (can include token for private repos)
    branch: branch name
    repo_path: path inside repo where to write files
    files: list of {path: \"relative/path.md\", content: \"...\"}
    \"\"\"
    tmpdir = tempfile.mkdtemp(prefix=\"speckit_repo_\")
    try:
        repo = Repo.clone_from(repo_url, tmpdir, branch=branch)
        target_dir = os.path.join(tmpdir, repo_path)
        os.makedirs(target_dir, exist_ok=True)

        for f in files or []:
            dest = os.path.join(tmpdir, f[\"path\"])
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, \"w\", encoding=\"utf8\") as fh:
                fh.write(f.get(\"content\", \"\"))

        repo.git.add(all=True)
        repo.index.commit(\"Auto: Speckit results\")
        origin = repo.remote(name=\"origin\")
        origin.push()
        return {\"status\": \"committed\", \"files_written\": len(files)}
    finally:
        shutil.rmtree(tmpdir)
