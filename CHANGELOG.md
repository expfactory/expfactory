# CHANGELOG

This is a manually generated log to track changes to the repository for each release. 
Each section should include general headers such as **Implemented enhancements** 
and **Merged pull requests**. All closed issued and bug fixes should be 
represented. The versions to the right of the description correspond with pypi releases.
Critical items to know are:

 - renamed commands
 - deprecated / removed commands
 - changed defaults
 - backward incompatible changes (recipe file format? image file format?)
 - migration guidance (how to convert images?)
 - changed behaviour (recipe sections work differently)


## [v3.x](https://github.com/expfactory/expfactory/tree/master) (master)
 - Add codespell config and github workflow + fixed some typos
 - Add support for loading existing data (3.2.15)
 - fixing bug with Dockerfile generation (3.2.14)
 - updating sqlalchemy (3.2.13)
 - updating flask to 1.1.4 (3.2.12)
 - updating yaml to use safe_load (3.2.11)
 - adding support for receiving a token in the url and updating docs template (3.2.0)
 - setting csrf token expire time to 3 hours (3.19)
 - update of base images to ubuntu 20.04 (3.18)
 - removing unneeded import of secure_filename (3.17)
 - adding black lint formatting (3.16)
 - pinning flask version to known working (3.15)
 - set psycopg2==2.7.5, removing python 2 support (3.14)
 - added option to print version, and https configuration (3.13)
 - documentation for labjs integration, and re-organization of integrations
 - increasing body size of nginx conf server block to 20M (3.12)
 - addition of participant variables to be set at runtime (3.11)
**contributions**
 - a [contributing](.github/CONTRIBUTING.md) file was added to guide users to contribute.
 - a [code of conduct](.github/CODE_OF_CONDUCT.md) was added.
 - a [pull request](.github/PULL_REQUEST_TEMPLATE.md) and [issues template](.github/ISSUE_TEMPLATE.md) was added.
**additions**
 - this changelog was added
 - a development image `vanessa/expfactory-builder.dev` was added for others to test new changes before integration into master repo.
 - addition of tests for builder (and databases)
**changed defaults**
 - the interactive portal study identifier used to be an incrementing number. To be consistent with the ability to generate a token, the identifier is now an automatically generated 34 character string.
**features**
 - `--headless` has been added as an option for start, meaning that the portal is closed off and tokens must be entered to participate. The experiments order is either preset with `--experiments` and `--no-randomize`, randomized (default) or filtered to a limited subset (`--experiments` without `--no-randomize`),
 - `expfactory logs` can be used inside the container to print out application logs. With `--tail` they are left open for viewing updates.

## [v3.0](https://github.com/expfactory/expfactory/releases/tag/v3.0) (v3.0)

 - databases are added for filesystem, sqlite, postgres, and mysql. See [release notes](https://vsoch.github.io/2017/expfactory-beta/). Note that the 2.0 is equivalent to 3.0, minus the addition of the paper folder.

