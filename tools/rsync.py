import subprocess

def rsync(host, projects_dir, src, component, distro = None) -> None:
    dest = f"{host}:{projects_dir}"

    subprocess.run(["ssh", "-q", host, "mkdir", "-p", f"{projects_dir}/{component}"])

    if component == "blueprints":
        dest = f"{host}:{projects_dir}/{component}"
        subprocess.run(["rsync", "-aP", f"{src}/common/.", dest])
        if distro:
            subprocess.run(["rsync", "-aP", f"{src}/{distro}/.", dest])
        return

    exclude = ["--exclude", "bin", "--exclude", "build", "--exclude", "rpmbuild"]
    subprocess.run(["rsync", "-aP", *exclude, "--delete-excluded", "--delete", src, dest])
