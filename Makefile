.PHONY: build-deb build-win build-mac build-all clean bump-major bump-minor bump-patch release

build-deb: bump-patch
	dpkg-buildpackage -b -uc -us
	mkdir -p dist
	mv ../anyfile-to-markdown_*.deb ../anyfile-to-markdown_*.buildinfo ../anyfile-to-markdown_*.changes dist/ 2>/dev/null || true

build-win:
	pyinstaller build-windows.spec
	makensis installer/anyfile-to-markdown.nsi
	mv AnyFileToMarkdown-Setup.exe dist/

build-mac:
	./installer/build-macos.sh
	mv *.dmg dist/

build-all: build-deb build-win build-mac

clean:
	rm -f ../anyfile-to-markdown_* 2>/dev/null || true
	rm -rf dist/ .pybuild/ *.egg-info/ build/ __pycache__/ 2>/dev/null || true
	rm -rf debian/anyfile-to-markdown/ 2>/dev/null || true
	rm -rf debian/.debhelper/ 2>/dev/null || true

bump-patch:
	./debian/bump-version.sh patch

bump-minor:
	./debian/bump-version.sh minor

bump-major:
	./debian/bump-version.sh major

release: build-all
