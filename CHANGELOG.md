# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v0.4.0 - 2023-07-03

### [0.4.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.3.0...v0.4.0) (2023-07-03)

#### Features

- allow to import dashboards roles ([2d796e8](https://github.com/openedx/tutor-contrib-aspects/commit/2d796e865835c566c89390557c9477f40b3fee71))

## v0.3.0 - 2023-06-30

### [0.3.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.2.2...v0.3.0) (2023-06-30)

#### Features

- add support for extra jinja filters ([d5f242c](https://github.com/openedx/tutor-contrib-aspects/commit/d5f242c3c22c15097b03ed939ef48878ddfb6d7d))

## v0.2.2 - 2023-06-29

### [0.2.2](https://github.com/openedx/tutor-contrib-aspects/compare/v0.2.1...v0.2.2) (2023-06-29)

### Bug Fixes

- appropriately bootstrap dbt database ([f798da3](https://github.com/openedx/tutor-contrib-aspects/commit/f798da38afd480940b8c568a48d357490cfce3d8))
- re-add select permission to xapi db for report user ([6a5f04b](https://github.com/openedx/tutor-contrib-aspects/commit/6a5f04b34d6e271f887322b1cec7430841543da4))
- update permissions on dbt database ([7be3bcd](https://github.com/openedx/tutor-contrib-aspects/commit/7be3bcdc4a8c72d7c6a4a40b23091dd5aa296b25))

### Build Systems

- fix condition for release workflow ([eb9387a](https://github.com/openedx/tutor-contrib-aspects/commit/eb9387aec8cdbc913c07317af8e0eb872afa4ab8))
- release on push to bot branch ([0e22c65](https://github.com/openedx/tutor-contrib-aspects/commit/0e22c651bbd1f62345fb8bcd870f985fc3a34258))

### Code Refactoring

- create a separate database for dbt ([a00ecfa](https://github.com/openedx/tutor-contrib-aspects/commit/a00ecfa823d7f768a707eded393528375fbbf309))

## v0.2.1 - 2023-06-29

### [0.2.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.2.0...v0.2.1) (2023-06-29)

### Bug Fixes

- Allow Vector to use remote ClickHouse ([a2397dd](https://github.com/openedx/tutor-contrib-aspects/commit/a2397ddc407fab361cf4310c21c00ef8ff0a6c3a))
- Duplicate statements in Vector ([0a2defb](https://github.com/openedx/tutor-contrib-aspects/commit/0a2defb10ee36a1e1c8a9c86f6bb0e0182279f9a))
- Use correct name for Ralph database override ([796f7dd](https://github.com/openedx/tutor-contrib-aspects/commit/796f7dd03049ac2dbd9b0d256030420a799369a1))

## v0.2.0 - 2023-06-29

### [0.2.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.1.1...v0.2.0) (2023-06-29)

#### Features

- create instructor dashboard with video data ([e2592e1](https://github.com/openedx/tutor-contrib-aspects/commit/e2592e1ad2a375ed20e64a27d27ef1856ed9f7d8))

#### Bug Fixes

- Give dbt permissions it needs ([a3ddbae](https://github.com/openedx/tutor-contrib-aspects/commit/a3ddbae20a64608a025d6c4ce49382c1a730f6d5))
- Pass down Aspects config to dbt ([9360bdc](https://github.com/openedx/tutor-contrib-aspects/commit/9360bdca5c17a829eaddb7171dede14ed6993eb7))

#### Code Refactoring

- align aspects folder structure ([90d5b6f](https://github.com/openedx/tutor-contrib-aspects/commit/90d5b6fdb58742b31c5a3900dfa71a8bef506251))
- Move env vars, de-dupe dbt commands ([2d649d1](https://github.com/openedx/tutor-contrib-aspects/commit/2d649d19fcac1784195e1993928481bf253cb526))
- simplify clickhouse port ([51f7000](https://github.com/openedx/tutor-contrib-aspects/commit/51f7000f1b0b49ab76ca7adb9e04e365c2fb75ee))

#### Build Systems

- back the release workflow ([785553a](https://github.com/openedx/tutor-contrib-aspects/commit/785553a74952de7bc3aaf17df0fa0d172a15e403))
- correct current version for release ([69924d9](https://github.com/openedx/tutor-contrib-aspects/commit/69924d965e0ce74425c2e3c2fb38e77fc76661c7))
- fix release workflow ([41b5041](https://github.com/openedx/tutor-contrib-aspects/commit/41b5041bc1d2783d3d730dd1ef72b4862799777f))
