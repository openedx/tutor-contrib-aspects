# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v0.18.4 - 2023-07-27

### [0.18.4](https://github.com/openedx/tutor-contrib-aspects/compare/v0.18.3...v0.18.4) (2023-07-27)

### Bug Fixes

- specify insertion order in migration 0012 ([9c779c0](https://github.com/openedx/tutor-contrib-aspects/commit/9c779c053b10a802cc7ee265d97ccb130bbff212))

## v0.18.3 - 2023-07-27

### [0.18.3](https://github.com/openedx/tutor-contrib-aspects/compare/v0.18.2...v0.18.3) (2023-07-27)

### Bug Fixes

- oauth token refresh solution ([8e2b965](https://github.com/openedx/tutor-contrib-aspects/commit/8e2b965844c27ab64c4e05b5c612c26cd8970521))

## v0.18.2 - 2023-07-27

### [0.18.2](https://github.com/openedx/tutor-contrib-aspects/compare/v0.18.1...v0.18.2) (2023-07-27)

### Bug Fixes

- use DateTime instead of DateTime64 for datasets ([458b973](https://github.com/openedx/tutor-contrib-aspects/commit/458b973ae7fa43749fcf3a371aec9df676cdd27c))

## v0.18.1 - 2023-07-27

### [0.18.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.18.0...v0.18.1) (2023-07-27)

### Bug Fixes

- correct regex for xapi_tracking parser ([86b1a5b](https://github.com/openedx/tutor-contrib-aspects/commit/86b1a5b6746091941795cda37c2cdc974dd1974a))
- include lms and cms workers for kubernetes logs ([7c1c63c](https://github.com/openedx/tutor-contrib-aspects/commit/7c1c63cfe18a4ddfb52b7178f3c39877f6d45128))
- remove security context for vector daemonset ([25761ac](https://github.com/openedx/tutor-contrib-aspects/commit/25761ac54291d2a09b8fb6481585e9d2c6d2f795))

## v0.18.0 - 2023-07-27

### [0.18.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.17.1...v0.18.0) (2023-07-27)

#### Features

- Add a "tutor do" command to transform tracking logs ([5e0f970](https://github.com/openedx/tutor-contrib-aspects/commit/5e0f970d4fef3c33739426fb8e7ee22a84fb8d78))
- Change engine type of materialized view tables to ReplacingMergeTree ([1eaa9a5](https://github.com/openedx/tutor-contrib-aspects/commit/1eaa9a5e72d36d08aa0ae5d70bc6b6bb9763bd07))

#### Bug Fixes

- Wrap SQL "in" lists in parens ([a064287](https://github.com/openedx/tutor-contrib-aspects/commit/a064287bc15f12ed950bf2bd03e6ad3e89517ad1))

#### Documentation

- Small fix and cleanup ([8b932ff](https://github.com/openedx/tutor-contrib-aspects/commit/8b932ffc41fb51ef24c14d42b2c43033dea1b300))

## v0.17.1 - 2023-07-27

### [0.17.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.17.0...v0.17.1) (2023-07-27)

### Bug Fixes

- add compatibility with k8s for aspects and vector ([b4b5682](https://github.com/openedx/tutor-contrib-aspects/commit/b4b5682c10962b81c2a80103e854aeec1f16b604))

### Build Systems

- add ci job to test a k8s env ([f44c9ee](https://github.com/openedx/tutor-contrib-aspects/commit/f44c9eef2ccfe560f56c14f211a0544bbb94c64c))

## v0.17.0 - 2023-07-26

### [0.17.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.16.3...v0.17.0) (2023-07-26)

#### Features

- Add course and block names to in memory dictionaries ([8b6cc28](https://github.com/openedx/tutor-contrib-aspects/commit/8b6cc28637eb4b775f7d0b6150c3cef50bd3eb8b))

## v0.16.3 - 2023-07-26

### [0.16.3](https://github.com/openedx/tutor-contrib-aspects/compare/v0.16.2...v0.16.3) (2023-07-26)

### Bug Fixes

- block only students ([355eab9](https://github.com/openedx/tutor-contrib-aspects/commit/355eab9dce8bd9e9161a3f2468da8293f1560575))
- remove instructor permissions ([8b88cff](https://github.com/openedx/tutor-contrib-aspects/commit/8b88cff7691f3284471615aca2e06444ba3520c5))

## v0.16.2 - 2023-07-26

### [0.16.2](https://github.com/openedx/tutor-contrib-aspects/compare/v0.16.1...v0.16.2) (2023-07-26)

### Bug Fixes

- remove hardcoded xapi ([7ce4b4a](https://github.com/openedx/tutor-contrib-aspects/commit/7ce4b4a60279bded6331c11eb7854843efae9871))

### Documentation

- Instructions to Sink Historical event data to ClickHouse ([7493d95](https://github.com/openedx/tutor-contrib-aspects/commit/7493d957e7c214f5a3a9e3e310970b41b56ca9f4))
- Sink Historical event data to ClickHouse instructions for non-default settings ([cff61fe](https://github.com/openedx/tutor-contrib-aspects/commit/cff61fe5b998e4c0aed78e1c672ca81b6c2cd199))

## v0.16.1 - 2023-07-25

### [0.16.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.16.0...v0.16.1) (2023-07-25)

### ⚠ BREAKING CHANGES

- parse course key in MV queries (FC-0024) (#193)

### Bug Fixes

- Make migration replace the old table ([79076ed](https://github.com/openedx/tutor-contrib-aspects/commit/79076edae05666c330e156dce3487fc4dfd3ae7c))

### Code Refactoring

- parse course key in MV queries (FC-0024) ([#193](https://github.com/openedx/tutor-contrib-aspects/issues/193)) ([ab066a5](https://github.com/openedx/tutor-contrib-aspects/commit/ab066a53b2c4f6d34a9c841ac0bb2907af9d42dc))

## v0.16.0 - 2023-07-17

### [0.16.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.15.0...v0.16.0) (2023-07-17)

#### Features

- import superset extra roles ([825af56](https://github.com/openedx/tutor-contrib-aspects/commit/825af56bb7ba4884e69e325082793687ff7e296e))

#### Build Systems

- change default title for release PR ([e319e67](https://github.com/openedx/tutor-contrib-aspects/commit/e319e679cb61b339601fa00f836a49c594f00da1))
- push openedx-dev cache to registry ([accbca8](https://github.com/openedx/tutor-contrib-aspects/commit/accbca812476031e1229ec2a9ec41fc9d0bbe628))

## v0.15.0 - 2023-07-17

### [0.15.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.14.1...v0.15.0) (2023-07-17)

#### Features

- backfill course data at start up ([9f75ac4](https://github.com/openedx/tutor-contrib-aspects/commit/9f75ac4c855de1c47dd4adffbe30946a4b24be31))

#### Build Systems

- trigger build jobs after release ([3ffadf3](https://github.com/openedx/tutor-contrib-aspects/commit/3ffadf3ebf7fd9b2a7c9ab3c6acdc3d82e151308))
- **deps:** bump docker/login-action from 2.1.0 to 2.2.0 ([766dbae](https://github.com/openedx/tutor-contrib-aspects/commit/766dbae9a93c3f48385253d4f8fbf163c2e3508a))

## v0.14.1 - 2023-07-12

### [0.14.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.14.0...v0.14.1) (2023-07-12)

### Bug Fixes

- SQL error in video segments chart ([3a62f7e](https://github.com/openedx/tutor-contrib-aspects/commit/3a62f7ee17b87235256825efc35f6ba886391d53))

### Build Systems

- build docker images on release created ([dce132f](https://github.com/openedx/tutor-contrib-aspects/commit/dce132f32c4cda87be742f1746bae245562b0047))

## v0.14.0 - 2023-07-10

### [0.14.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.13.0...v0.14.0) (2023-07-10)

#### Features

- add operator dashboard ([0b8796d](https://github.com/openedx/tutor-contrib-aspects/commit/0b8796dc8b8aca4565d392db15d92b929b40f590))

#### Bug Fixes

- allow to configure when to block students ([f14c6ee](https://github.com/openedx/tutor-contrib-aspects/commit/f14c6ee968d3d1a4093db27e785f15a5f79d0f39))
- block non-instructor access to superset ([3b83efd](https://github.com/openedx/tutor-contrib-aspects/commit/3b83efd7b4cd1e15563c0b5cbdbde5e05f3ba8d7))
- publish dashboards at import time ([0910419](https://github.com/openedx/tutor-contrib-aspects/commit/0910419aea5f2c6d2828c8bef408401fc621bac9))

#### Build Systems

- add ci workflow to build and push docker images ([b8b2b35](https://github.com/openedx/tutor-contrib-aspects/commit/b8b2b35dd2f4ae6e8f410d45ca67dbdea64e60e6))

#### Code Refactoring

- create superset role mapping ([a3352be](https://github.com/openedx/tutor-contrib-aspects/commit/a3352be757386dfe2425b9c60f7c128a12ab6c30))
- remove assets zip ([339ed92](https://github.com/openedx/tutor-contrib-aspects/commit/339ed92ba99648cff6696ab9d66d4c58d5d60468))

## v0.13.0 - 2023-07-07

### [0.13.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.12.0...v0.13.0) (2023-07-07)

#### Features

- add support for extra rlsf ([892cba8](https://github.com/openedx/tutor-contrib-aspects/commit/892cba8366f3a6b66675a361633450b07449a67c))

## v0.12.0 - 2023-07-07

### [0.12.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.11.0...v0.12.0) (2023-07-07)

#### Features

- add video timeline chart ([1c2f2ac](https://github.com/openedx/tutor-contrib-aspects/commit/1c2f2ac9891e033665415f19199d2bec0beed0e3))

#### Code Refactoring

- use jinja variables for video segment table name ([13726ea](https://github.com/openedx/tutor-contrib-aspects/commit/13726eab2ab97c94868c17fb63abe08365a0f57d))

## v0.11.0 - 2023-07-07

### [0.11.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.10.0...v0.11.0) (2023-07-07)

#### Features

- allow to run extra clickhouse sql ([30bfd1d](https://github.com/openedx/tutor-contrib-aspects/commit/30bfd1d522b1997400c07c78cbeafbb3fdf1caec))

## v0.10.0 - 2023-07-07

### [0.10.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.9.1...v0.10.0) (2023-07-07)

#### Features

- add problem interaction charts to superset ([27d8492](https://github.com/openedx/tutor-contrib-aspects/commit/27d8492ca8ab2f11e7bc0c33dd71579dfb8d1fed))

#### Tests

- correct tutor test workflow ([a5f74a8](https://github.com/openedx/tutor-contrib-aspects/commit/a5f74a85e7a266873a15639568e91b427ea4bbc0))

## v0.9.1 - 2023-07-07

### [0.9.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.9.0...v0.9.1) (2023-07-07)

### Bug Fixes

- remove buildkit ([d769cff](https://github.com/openedx/tutor-contrib-aspects/commit/d769cff81ccae3e4be00321bfe2c4493a472cd48))

### Build Systems

- run tutor test on open pr ([d4c0e7e](https://github.com/openedx/tutor-contrib-aspects/commit/d4c0e7eadec3dd18a037db884d77201305e94737))
- use custom docker image ([9a0fbb5](https://github.com/openedx/tutor-contrib-aspects/commit/9a0fbb5cde9ac2710c248f20e4bd0983e2afe2ad))

### Tests

- add tests for tutor local env ([882db95](https://github.com/openedx/tutor-contrib-aspects/commit/882db954363fbca66809b1498185c7a513880b90))

### Code Refactoring

- move assets outside volumes ([51c2f16](https://github.com/openedx/tutor-contrib-aspects/commit/51c2f163a1110a2b401ca6c8ea15ae64ae008d39))

## v0.9.0 - 2023-07-06

### [0.9.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.8.0...v0.9.0) (2023-07-06)

#### Features

- backward compatibility with tutor14 ([869abe8](https://github.com/openedx/tutor-contrib-aspects/commit/869abe879630cdcc3d125d7adab1414b1349cdc0))

## v0.8.0 - 2023-07-06

### [0.8.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.7.0...v0.8.0) (2023-07-06)

#### Features

- add chart for active enrollments per day ([dedf916](https://github.com/openedx/tutor-contrib-aspects/commit/dedf9167714a1acd3e6debcbd7ae99d78186788a))
- use trendline chart for enrollments ([769e460](https://github.com/openedx/tutor-contrib-aspects/commit/769e46052d670218de22e63fa8c8782c66bf74fe))

#### Documentation

- include README section for virtual datasets ([a76b374](https://github.com/openedx/tutor-contrib-aspects/commit/a76b3744ec59f3130ee00b79947d14a288d68d17))

## v0.7.0 - 2023-07-05

### [0.7.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.6.0...v0.7.0) (2023-07-05)

#### Features

- add alembic migrations for clickhouse ([273a031](https://github.com/openedx/tutor-contrib-aspects/commit/273a031fbb7273817ce9f343b883172168383d8c))

## v0.6.0 - 2023-07-05

### [0.6.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.5.0...v0.6.0) (2023-07-05)

#### Features

- add "run" filter to instructor dashboard ([52df4d1](https://github.com/openedx/tutor-contrib-aspects/commit/52df4d1eb4b3f640b541c76fc1566043c5040478))
- use display names for entities instead of ID ([b37e57f](https://github.com/openedx/tutor-contrib-aspects/commit/b37e57f963b7885d245eeaf8db254e5be1030f08))

#### Bug Fixes

- use jinja to reuse virtual dataset queries ([07a74f4](https://github.com/openedx/tutor-contrib-aspects/commit/07a74f4a79196f520a84fa7150967ae5032323d1))

## v0.5.0 - 2023-07-05

### [0.5.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.4.0...v0.5.0) (2023-07-05)

#### Features

- allow to install extra dbt packages ([4eb28c4](https://github.com/openedx/tutor-contrib-aspects/commit/4eb28c4ad62ad48a7aa311d69c8602c77526eac8))

#### Build Systems

- **deps:** bump actions/setup-python from 2 to 4 ([e10e0b8](https://github.com/openedx/tutor-contrib-aspects/commit/e10e0b8a2ae13f2a1612ceb1f656ab5d459a45e1))
- **deps:** bump mathieudutour/github-tag-action from 6.0 to 6.1 ([15f2a9b](https://github.com/openedx/tutor-contrib-aspects/commit/15f2a9b9187150d9fcf03e4a957798456559426b))
- **deps:** bump stefanzweifel/changelog-updater-action ([84fc6f1](https://github.com/openedx/tutor-contrib-aspects/commit/84fc6f1474545c2c537b43815c3721ef73e246b5))

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
