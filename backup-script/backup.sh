#!/bin/sh
# Create a dated gzip-compressed tar archive of one directory.
set -u

usage() {
  printf 'Usage: %s SOURCE_DIRECTORY BACKUP_DIRECTORY\n' "$0" >&2
  exit 2
}

[ "$#" -eq 2 ] || usage
source_arg=$1
backup_arg=$2

case "$source_arg" in
  -*) source_arg=./$source_arg ;;
esac
case "$backup_arg" in
  -*) backup_arg=./$backup_arg ;;
esac

if [ ! -d "$source_arg" ]; then
  printf 'Error: source directory does not exist: %s\n' "$source_arg" >&2
  exit 1
fi

source_real=$(CDPATH= cd "$source_arg" 2>/dev/null && pwd -P) || {
  printf 'Error: cannot access source directory: %s\n' "$source_arg" >&2
  exit 1
}
[ "$source_real" != / ] || {
  printf 'Error: refusing to archive the filesystem root.\n' >&2
  exit 1
}

if ! mkdir -p "$backup_arg"; then
  printf 'Error: cannot create backup directory: %s\n' "$backup_arg" >&2
  exit 1
fi
backup_real=$(CDPATH= cd "$backup_arg" 2>/dev/null && pwd -P) || {
  printf 'Error: cannot access backup directory: %s\n' "$backup_arg" >&2
  exit 1
}

case "$backup_real/" in
  "$source_real/"*)
    printf 'Error: backup directory must be outside the source directory.\n' >&2
    exit 1
    ;;
esac

source_name=$(basename "$source_real")
parent_dir=$(dirname "$source_real")
timestamp=$(date '+%Y%m%d_%H%M%S')
archive="$backup_real/${source_name}_${timestamp}.tar.gz"
suffix=1
while [ -e "$archive" ]; do
  archive="$backup_real/${source_name}_${timestamp}_${suffix}.tar.gz"
  suffix=$((suffix + 1))
done

if tar -czf "$archive" -C "$parent_dir" "$source_name"; then
  printf 'Backup created: %s\n' "$archive"
  printf 'Archive size: '
  ls -lh "$archive" | awk '{print $5}'
else
  rm -f "$archive"
  printf 'Error: tar could not create the backup.\n' >&2
  exit 1
fi
