# jupyter-kernel-cloner

## What

Copy a `sys.prefix` kernel resource directory to a user kernel resource
directory by name.
Any existing user resource directory by that name will be removed and replaced.

## How

    clone-jupyter-kernel
        [-h] [--display-name DISPLAY_NAME] [--name NAME] [--yes]
        {kernel-name}

### Positional Arguments

Just one, the name of the kernelspec you want to copy.
The output of `clone-jupyter-kernel --help` lists the kernelspecs you can copy.

### Optional Arguments

* `--help (-h)` 
    * Show a help message and exit
    * If kernelspecs are detected, includes a list of them
* `--display-name DISPLAY_NAME (-d DISPLAY_NAME)
    * If you want the cloned kernel to have a different display name, use this.
    * By default the original name is used.
* `--name NAME (-n NAME)`
    * If you want the cloned kernel to have a different name, use this.
    * By default the original name is used.
* `--yes (-y)`
    * Prevent the 'are you sure' confirmation prompt.
    * Not recommended for... anybody.

### What Kernelspecs Can I Clone?

This only looks at the `{sys.prefix}/share/jupyter/kernels` directory for
kernels to clone.
The output of `clone-jupyter-kernel --help` lists the kernelspecs you can copy.

### Examples, I Need Examples

To simply clone a kernel-spec:

    $ clone-jupyter-kernel python3

This will clone the kernel-spec 'python3' from, say,

    /usr/local/share/jupyter/kernels/python3

to

    /homes/jovyan/.local/share/jupyter/kernels/python3

### Give Me Another Example Immediately

OK, and to clone a kernelspec, but give it a new name and display name too:

    $ clone-jupyter-kernel python3 --name=mykernel --display-name=mykernel

This will clone the kernelspec 'python3' from

    /usr/local/share/jupyter/kernels/python3

to

    /homes/jovyan/.local/share/jupyter/kernels/mykernel

and in the new `kernel.json` file `display_name` is set to "mykernel" too.

### Thanks

You're welcome!
