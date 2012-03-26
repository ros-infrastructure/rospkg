.PHONY: all setup clean_dist distro clean install dsc source_deb upload

NAME='rospkg'
VERSION=`./setup.py --version`

OUTPUT_DIR='deb_dist'


all:
	echo "noop for debbuild"

setup:
	echo "building version ${VERSION}"

clean_dist:
	-rm -f MANIFEST
	-rm -rf dist
	-rm -rf deb_dist

distro: setup clean_dist
	python setup.py sdist

push: distro
	python setup.py sdist register upload
	scp dist/${NAME}-${VERSION}.tar.gz ipr:/var/www/pr.willowgarage.com/html/downloads/${NAME}

clean: clean_dist
	echo "clean"

install: distro
	sudo checkinstall python setup.py install

binary_deb: dsc
	# need to convert unstable to each distro and repeat
	python setup.py --command-packages=stdeb.command bdist_deb 


upload: binary_deb 
	dput -u -c dput.cf lucid ${OUTPUT_DIR}/${NAME}_${VERSION}-1_amd64.changes 

testsetup:
	echo "running rospkg tests"

test: testsetup
	cd test && nosetests
