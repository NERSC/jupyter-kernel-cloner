
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import json
import os
import sys
from textwrap import dedent

from jupyter_client.kernelspec import (
    _list_kernels_in, jupyter_data_dir, KernelSpecManager
)

def main():
    path = os.path.join(sys.prefix, "share/jupyter/kernels")
    source_kernelspecs = get_source_kernelspecs(path)
    args = parse_arguments(source_kernelspecs)
    source_dir = source_kernelspecs[args.kernel_name]
    copy_kernelspec(args, source_dir)

def copy_kernelspec(args, source_dir):

    km = KernelSpecManager()
    name = args.name or args.kernel_name
    user = True

    if not args.yes:
        destination = km._get_destination_dir(name, user)
        print(f"Copying\n  '{source_dir}'\nto\n  '{destination}'")
        confirm = input(f"ARE YOU SURE [y/N]? ")
        if not confirm.lower().startswith("y"):
            print("OK, not copying then!")
            sys.exit(0)

    destination = km.install_kernel_spec(source_dir, name, user)

    if args.display_name:
        # Don't use KernelSpec, it adds fields, may change other things and we
        # have to write the revised kernelspec as JSON directly anyway
        kernel_json = os.path.join(destination, "kernel.json")
        with open(kernel_json, "r") as f:
            k = json.load(f)
        k["display_name"] = args.display_name
        with open(kernel_json, "w") as f:
            json.dump(k, f, indent=1)

def get_source_kernelspecs(path):
    source_kernelspecs = _list_kernels_in(path)
    assert source_kernelspecs, f"No kernelspecs, searched {path}"
    return source_kernelspecs

def parse_arguments(source_kernelspecs):

    description = dedent("""\
    Copy a sys.prefix kernel resource directory to a user kernel resource
    directory by name.  Any existing user resource directory by that name
    will be removed and replaced.
    """)

    parser = ArgumentParser(
        description=description,
        epilog=format_source_kernelspecs(source_kernelspecs),
        formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "kernel_name",
        help="Name of the kernel-spec you want to clone, list below.",
        choices=source_kernelspecs.keys(),
        metavar="{kernel-name}"
    )
    parser.add_argument(
        "--display-name", "-d",
        help="Optional new display name for the cloned kernel-spec."
    )
    parser.add_argument(
        "--name", "-n",
        help="Optional new name for the cloned kernel-spec."
    )
    parser.add_argument(
        "--yes", "-y",
        action="store_true",
        help="Prevent the 'are you sure' confirmation prompt.",
    )
    return parser.parse_args()

def format_source_kernelspecs(source_kernelspecs):
    kernel_name_label = "kernel-name:"
    resource_dir_label = "resource-dir:"

    len_kernel_name_label = len(kernel_name_label)
    len_resource_dir_label = len(resource_dir_label)

    width = len_kernel_name_label
    for name in source_kernelspecs:
        if (len_name := len(name)) > width:
            width = len_name

    text = "kernel-name (and source directory) choices:\n"
    for name in sorted(source_kernelspecs):
        text += f"  {name:<{width}} ({source_kernelspecs[name]})\n"

    text += "\nsimply clone a kernelspec:\n\n"
    text += f"    $ clone-jupyter-kernel {name}\n\n"
    text += f"  This will clone the kernelspec '{name}' from\n"
    text += f"    {source_kernelspecs[name]}\n"
    text += f"  to\n"
    text += f"    {jupyter_data_dir()}/{name}\n\n"

    text += "\nclone kernelspec, but give it a new name and display name:\n\n"
    text += f"    $ clone-jupyter-kernel {name} \\\n"
    text += f"        --name=mykernel --display-name=mykernel\n\n"
    text += f"  This will clone the kernelspec '{name}' from\n"
    text += f"    {source_kernelspecs[name]}\n"
    text += f"  to\n"
    text += f"    {jupyter_data_dir()}/mykernel\n"
    text += f"  and set 'display_name' to 'mykernel' in the new kernelspec\n"

    return text
