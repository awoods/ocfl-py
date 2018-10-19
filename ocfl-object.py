#!/usr/bin/env python
"""OCFL Object and Inventory Builder."""
import argparse
import logging
import ocfl

parser = argparse.ArgumentParser(description='Build an OCFL inventory.',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--srcdir', '--src',
                    help='source directory path')
parser.add_argument('--digest', default='sha512',
                    help='digest type to use')
parser.add_argument('--fixity', action='append',
                    help='add fixity type to add')
parser.add_argument('--id', default=None,
                    help='identifier of object')

commands = parser.add_mutually_exclusive_group(required=True)
commands.add_argument('--create', action='store_true',
                      help='Create an new object with version 1 from objdir')
commands.add_argument('--build', action='store_true',
                      help='Build an new object from version directories in objdir')
commands.add_argument('--show', action='store_true',
                      help='Show versions and files in an OCFL object')
commands.add_argument('--validate', action='store_true',
                      help='Validate an OCFL object')

# Version metadata settings
ocfl.add_version_metadata_args(parser)

parser.add_argument('--skip', action='append', default=['README.md', '.DS_Store'],
                    help='directories and files to ignore')

# Versioning strategy settings
parser.add_argument('--no-forward-delta', action='store_true',
                    help='do not use forward deltas')
parser.add_argument('--no-dedupe', '--no-dedup', action='store_true',
                    help='do not use deduplicate files within a version')

parser.add_argument('--objdir', '--obj',
                    help='read from or write to OCFL object directory objdir')
parser.add_argument('--ocfl-version', default='draft',
                    help='OCFL specification version')
parser.add_argument('--verbose', '-v', action='store_true',
                    help="be more verbose")
args = parser.parse_args()
metadata = ocfl.VersionMetadata(args)

logging.basicConfig(level=logging.INFO if args.verbose else logging.WARN)

obj = ocfl.Object(identifier=args.id,
                  digest_algorithm=args.digest,
                  skips=args.skip,
                  forward_delta=not args.no_forward_delta,
                  dedupe=not args.no_dedupe,
                  ocfl_version=args.ocfl_version,
                  fixity=args.fixity)
if args.create:
    obj.create(srcdir=args.srcdir,
               metadata=metadata,
               objdir=args.objdir)
elif args.build:
    obj.write(srcdir=args.srcdir,
              metadata=metadata,
              objdir=args.objdir)
elif args.show:
    obj.show(path=args.objdir)
elif args.validate:
    obj.validate(path=args.objdir)
else:
    raise Exception("Command argument not supported!")
