SHELL := bash
PYTHON_NAME = rhasspyhermes
PACKAGE_NAME = rhasspy-hermes
PYTHON_FILES = $(SOURCE)/*.py tests/*.py setup.py
SHELL_FILES = bin/* debian/bin/*
PIP_INSTALL ?= install

.PHONY: reformat check dist venv test pyinstaller debian deploy

version := $(shell cat VERSION)
architecture := $(shell dpkg-architecture | grep DEB_BUILD_ARCH= | sed 's/[^=]\+=//')

debian_package := rhasspy-hermes_$(version)_$(architecture)
debian_dir := debian/$(debian_package)

# -----------------------------------------------------------------------------
# Python
# -----------------------------------------------------------------------------

reformat:
	scripts/format-code.sh $(PYTHON_FILES)

check:
	scripts/check-code.sh $(PYTHON_FILES)

venv:
	scripts/create-venv.sh


dist: sdist

sdist:
	python3 setup.py sdist

test:
	scripts/run-tests.sh $(PYTHON_NAME)

# -----------------------------------------------------------------------------
# Docker
# -----------------------------------------------------------------------------

docker: pyinstaller
	docker build . -t "rhasspy/$(PACKAGE_NAME):$(version)" -t "rhasspy/$(PACKAGE_NAME):latest"

deploy:
	echo "$$DOCKER_PASSWORD" | docker login -u "$$DOCKER_USERNAME" --password-stdin
	docker push "rhasspy/$(PACKAGE_NAME):$(version)"

# -----------------------------------------------------------------------------
# Debian
# -----------------------------------------------------------------------------

pyinstaller:
	mkdir -p dist
	pyinstaller -y --workpath pyinstaller/build --distpath pyinstaller/dist $(PYTHON_NAME).spec
	tar -C pyinstaller/dist -czf dist/$(PACKAGE_NAME)_$(version)_$(architecture).tar.gz $(PYTHON_NAME)/

debian: pyinstaller
	mkdir -p dist
	rm -rf "$(debian_dir)"
	mkdir -p "$(debian_dir)/DEBIAN" "$(debian_dir)/usr/bin" "$(debian_dir)/usr/lib"
	cat debian/DEBIAN/control | version=$(version) architecture=$(architecture) envsubst > "$(debian_dir)/DEBIAN/control"
	cp debian/bin/* "$(debian_dir)/usr/bin/"
	cp -R pyinstaller/dist/rhasspyhermes "$(debian_dir)/usr/lib/"
	cd debian/ && fakeroot dpkg --build "$(debian_package)"
	mv "debian/$(debian_package).deb" dist/
