#!/usr/bin/python3

import setuptools

setuptools.setup(
    name="tools",
    version="0.1",
    description="osbuild devtools",
    url="#",
    author="Kingsley Zissou",
    install_requires=["ruamel.yaml"],
    author_email="",
    packages=['tools', 'scripts.vm', 'scripts.compose', 'scripts.sync'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'vm = scripts.vm:main',
            'compose = scripts.compose:main',
            'rcp = scripts.sync:main'
        ],
        'vm_commands': [
            'up = scripts.vm:start',
            'dn = scripts.vm:stop',
            'rm = scripts.vm.remove'
        ]
    }
)
