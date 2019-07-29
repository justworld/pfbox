# coding: utf-8
"""
zip相关
"""
import os
import zipfile


def create_zip_file(source_dir, outfile):
    """
    Create a zip file from a source input directory.

    This function is intended to be an equivalent to
    `zip -r`.  You give it a source directory, `source_dir`,
    and it will recursively zip up the files into a zipfile
    specified by the `outfile` argument.

    from chalice
    """
    with zipfile.ZipFile(outfile, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for root, _, filenames in os.walk(source_dir):
            for filename in filenames:
                full_name = os.path.join(root, filename)
                archive_name = os.path.relpath(full_name, source_dir)
                z.write(full_name, archive_name)
