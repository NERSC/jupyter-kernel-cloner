from setuptools import setup

setup(
    author='R. C. Thomas',
    author_email='rcthomas@lbl.gov',
    description="Clone sys.prefix kernelspec to user prefix kernelspec",
    name='jupyter-kernel-cloner',
    version='0.0.1',
    packages=['jupyter_kernel_cloner'],
    entry_points={
        'console_scripts': [
            'clone-jupyter-kernel=jupyter_kernel_cloner:main',
        ]
    }
)
