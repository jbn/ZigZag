.PHONY: build_for_testing
build_for_testing:
	python setup.py build_ext --inplace

.PHONY: clean
clean:
	rm -f zigzag/*.so
	rm -f zigzag/*.c
	rm -f zigzag/*.html

.PHONY: test
test:
	python setup.py nosetests

.PHONY: test_with_coverage
test_with_coverage:
	CYTHON_DEBUG=1 coverage run setup.py nosetests

.PHONY: coverage
coverage: clean test_with_coverage
	coverage html -i
	open htmlcov/index.html

.PHONY: profile
profile: clean test_with_coverage
	cython --annotate-coverage coverage.xml zigzag/*.pyx
	open zigzag

.PHONY: analyze
analyze: clean test_with_coverage
	coverage html -i
	cython --annotate-coverage coverage.xml zigzag/*.pyx
	open htmlcov/index.html
	open zigzag

.PHONY: docs
docs: build_for_testing
	cd docs && sphinx-apidoc -f -o source ../zigzag
	$(MAKE) -C docs html

.PHONY: gh-pages
gh-pages: ensure_clean docs
	git checkout gh-pages
	cp -r docs/build/html/* ./
	git add .
	@-git commit -m 'Update documentation'  # Don't fail if no changes.
	git checkout master

.PHONY: ensure_clean
ensure_clean:
ifeq ($(shell git status | grep "working directory clean"), )
	$(error Commit changes before generating docs)
endif
