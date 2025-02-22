#!/bin/bash
set -e

if [ ! $(which cargo) ]; then
	echo "cargo not found!" >&2
	echo "You need to install the cargo package before running this script." >&2
	exit 1
fi

if [ ! $(which rpmspec) ]; then
	echo "rpmspec not found!" >&2
	echo "You need to install the rpm-build package before running this script." >&2
	exit 1
fi


if [ $# -ne 1 ]; then
	echo "Usage: $0 <spec_file>" >&2
	exit 1
fi

SOURCE=$(rpmspec -P $1| grep -i '^Source0\s*:' | sed 's/^Source0\s*:\s*//')
NAME=$(rpmspec -P $1|grep -i '^Name\s*:'| sed 's/^Name\s*:\s*//')
VERSION=$(rpmspec -P $1|grep -i '^Version\s*:' | sed 's/^Version\s*:\s*//')

if [ -f ${NAME}-${VERSION}-vendor.tar.xz ]; then
	echo "${NAME}-${VERSION}-vendor.tar.xz already exists"
	exit 0
fi

if [ ! -f ${NAME}-${VERSION}-source.tar.gz ]; then
	curl -L ${SOURCE} -o ${NAME}-${VERSION}-source.tar.gz
fi

tar xfz ${NAME}-${VERSION}-source.tar.gz

dir=$(tar -tf ${NAME}-${VERSION}-source.tar.gz | head -1 | cut -f1 -d"/")

if [ -d "$dir" ]; then
    cd "$dir" || exit
    echo "Entered directory: $dir"
else
    echo "Could not determine the extracted directory."
    exit 1
fi

echo "Running cargo vendor for ${NAME}"
cargo vendor 3>&1 1> ../cargo-vendor.log 2>&1
tar cf ../${NAME}-${VERSION}-vendor.tar vendor
cd ..
echo "Compressing the ${NAME}-${VERSION}-vendor archive"
xz -e9 ${NAME}-${VERSION}-vendor.tar
rm -f ${NAME}-${VERSION}-vendor.tar
rm -rf ${dir}
echo "Done"
