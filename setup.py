import sysconfig
import os
from setuptools import setup
from setuptools.command.install import install

def get_site_packages_path():
    return sysconfig.get_path("purelib")

class InstallWithPth(install):
    def run(self):
        super().run()
        site_packages = get_site_packages_path()
        pth_path = os.path.join(site_packages, "friendly_module_not_found_error.pth")
        with open(pth_path, "w", encoding="utf-8") as f:
            f.write("import friendly_module_not_found_error")

setup(cmdclass={"install": InstallWithPth})

