# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v0.97.1 - 2024-04-11

### [0.97.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.97.0...v0.97.1) (2024-04-11)

### Bug Fixes

* Add allow_translations to instructor dash settings ([#715](https://github.com/openedx/tutor-contrib-aspects/issues/715)) ([23b14fc](https://github.com/openedx/tutor-contrib-aspects/commit/23b14fc5185e0ff484789e2919f0608684902b54))

## v0.97.0 - 2024-04-10

### [0.97.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.96.4...v0.97.0) (2024-04-10)

#### Features

* import course dashboard v1 ([#710](https://github.com/openedx/tutor-contrib-aspects/issues/710)) ([5a322a5](https://github.com/openedx/tutor-contrib-aspects/commit/5a322a53303fcbe3968dc6320551039a95186b33))

## v0.96.4 - 2024-04-09

### [0.96.4](https://github.com/openedx/tutor-contrib-aspects/compare/v0.96.3...v0.96.4) (2024-04-09)

### Bug Fixes

* automatically add RLSF to all tables ([43731da](https://github.com/openedx/tutor-contrib-aspects/commit/43731daf394b1a6edadc255f460bb4d182511c9f))

## v0.96.3 - 2024-04-09

### [0.96.3](https://github.com/openedx/tutor-contrib-aspects/compare/v0.96.2...v0.96.3) (2024-04-09)

### Bug Fixes

* set dashboard color_schema to supersetColors ([99e4aed](https://github.com/openedx/tutor-contrib-aspects/commit/99e4aed88f07fce6d21f7698077a973669547b81))

## v0.96.2 - 2024-04-09

### [0.96.2](https://github.com/openedx/tutor-contrib-aspects/compare/v0.96.1...v0.96.2) (2024-04-09)

### Bug Fixes

* set correct schema for all datasets ([94cf24f](https://github.com/openedx/tutor-contrib-aspects/commit/94cf24f5297ff0e0c7f126ecdae5d339338440cb))

## v0.96.1 - 2024-04-09

### [0.96.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.96.0...v0.96.1) (2024-04-09)

### Bug Fixes

* allow to embed translated dashboards ([62e1056](https://github.com/openedx/tutor-contrib-aspects/commit/62e1056a3581ae10f15d0dc9eb818a95d09f10d8))

## v0.96.0 - 2024-04-09

### [0.96.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.95.0...v0.96.0) (2024-04-09)

#### Features

* upgrade superset to 3.1.2 ([32510b6](https://github.com/openedx/tutor-contrib-aspects/commit/32510b653b12e41b896caa8cd96fb8a158f58582))

#### Bug Fixes

* add * for select video plays ([fe9c7eb](https://github.com/openedx/tutor-contrib-aspects/commit/fe9c7ebcea54e7b19f486bdcb2e29704015bfa13))
* refresh datasets that are not empty ([2bd5fd7](https://github.com/openedx/tutor-contrib-aspects/commit/2bd5fd7864af8b38567d973f1a3244ccb656d923))
* use dataset fetch_metadata method ([7fd2fba](https://github.com/openedx/tutor-contrib-aspects/commit/7fd2fba1b76d452f353271c54a8541ecae936056))
* use dataset fetch_metadata method ([9f5d2bd](https://github.com/openedx/tutor-contrib-aspects/commit/9f5d2bd804403a7c7bb7bc723f4d4fc550e19155))

## v0.95.0 - 2024-04-09

### [0.95.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.94.0...v0.95.0) (2024-04-09)

#### Features

* add chart for full and partial video views ([17f6437](https://github.com/openedx/tutor-contrib-aspects/commit/17f6437dd2d2497c1ae24c9eb11a038d2d56cbc0))

## v0.94.0 - 2024-04-08

### [0.94.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.93.0...v0.94.0) (2024-04-08)

#### Features

* add problem engagement dropoff chart to instructor dashboard ([d6796ce](https://github.com/openedx/tutor-contrib-aspects/commit/d6796ce5d80226e4930c74d5d2cb1df6ef77732c))

#### Bug Fixes

* bump aspects-dbt version ([791e372](https://github.com/openedx/tutor-contrib-aspects/commit/791e37291e5d315c76ae18a1cb2b64949738f70d))

## v0.93.0 - 2024-04-04

### [0.93.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.92.0...v0.93.0) (2024-04-04)

#### Features

* add dataset and chart for video engagement dropoff ([bdd20bb](https://github.com/openedx/tutor-contrib-aspects/commit/bdd20bb773b390e8003035ef1c6e66407601518f))
* bump aspects-dbt version to include video engagement model ([0b6dd28](https://github.com/openedx/tutor-contrib-aspects/commit/0b6dd28aee9954887089859e963cf69ebd07779d))

#### Bug Fixes

* update chart aggregation to count video views ([9216579](https://github.com/openedx/tutor-contrib-aspects/commit/921657938cf8806a6d12731158634e463d788c9a))

## v0.92.0 - 2024-04-03

### [0.92.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.91.0...v0.92.0) (2024-04-03)

#### Features

* create aspects-consumer deployment ([e17ae39](https://github.com/openedx/tutor-contrib-aspects/commit/e17ae3979a12857f8c04d4a6923bd2d2460eb514))
* use new ERB settings model ([9a42807](https://github.com/openedx/tutor-contrib-aspects/commit/9a42807e4e420d6379dfec017149cb4833503ecc))

#### Bug Fixes

* install plugins after dev requirements ([1601f8f](https://github.com/openedx/tutor-contrib-aspects/commit/1601f8f134bb5854186e0dda2ec4fe9a45dec1f6))

## v0.91.0 - 2024-04-02

### [0.91.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.90.0...v0.91.0) (2024-04-02)

#### Features

* upgrade to clickhouse 24.3 LTS ([2542a5a](https://github.com/openedx/tutor-contrib-aspects/commit/2542a5af132314c40224c1fd3012a8a70086792b))

## v0.90.0 - 2024-04-02

### [0.90.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.89.2...v0.90.0) (2024-04-02)

#### Features

* Add support for data pipeline load testing ([a5906fe](https://github.com/openedx/tutor-contrib-aspects/commit/a5906feb41f62e2703b7f9f0cfb0fba66aefc201))

#### Code Refactoring

* Remove ERB batching settings ([f6f5235](https://github.com/openedx/tutor-contrib-aspects/commit/f6f5235fe8dabf6c95ad0023f2351f853b38b0db))

## v0.89.2 - 2024-04-02

### [0.89.2](https://github.com/openedx/tutor-contrib-aspects/compare/v0.89.1...v0.89.2) (2024-04-02)

### Bug Fixes

* Make the locale.yaml file utf-8 for sane diffs ([8bf196d](https://github.com/openedx/tutor-contrib-aspects/commit/8bf196d5adbb302fcee65455ef38c5ec4dc227cd))

## v0.89.1 - 2024-04-01

### [0.89.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.89.0...v0.89.1) (2024-04-01)

### Bug Fixes

* install aspects-dbt package requirements before running dbt ([7904516](https://github.com/openedx/tutor-contrib-aspects/commit/790451661be9e90bc660e66381a0357830353460))

## v0.89.0 - 2024-03-25

### [0.89.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.88.0...v0.89.0) (2024-03-25)

#### Features

* add dataset for pageview engagement charts ([f62ecb9](https://github.com/openedx/tutor-contrib-aspects/commit/f62ecb99df238e71c1d99615cae0ea6ae2b67d90))

#### Build Systems

* only push cache on latest ([acba540](https://github.com/openedx/tutor-contrib-aspects/commit/acba540a58fa741ce6f65c0067a16d1e67458014))
* skip login to docker hub and push step on error ([2726e4a](https://github.com/openedx/tutor-contrib-aspects/commit/2726e4abaa911d260f6bbdf010cb79ae1e5cb16f))

## v0.88.0 - 2024-03-20

### [0.88.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.87.1...v0.88.0) (2024-03-20)

#### Features

* create new dashboards ([ae0a990](https://github.com/openedx/tutor-contrib-aspects/commit/ae0a99028096a669d6111c22ee49468ea1a057c7))

#### Code Refactoring

* moves the openedx pip requirements into a patch ([df65fd6](https://github.com/openedx/tutor-contrib-aspects/commit/df65fd6cf576f33bf5d632ae2e2f9bfdd8116c69))
* split requirements into separate lines ([e84ff53](https://github.com/openedx/tutor-contrib-aspects/commit/e84ff531046ba3b13f6043e0c2412b01fca671a0))

#### Build Systems

* build images on bot PRs ([1ea9b0a](https://github.com/openedx/tutor-contrib-aspects/commit/1ea9b0aa5d6c2423b59eaaaaebc5d9307334f1a0))
* push latest image on CI ([04f4929](https://github.com/openedx/tutor-contrib-aspects/commit/04f4929b2408267da91aa831ce3444630a089dbf))

## v0.87.1 - 2024-03-18

### [0.87.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.87.0...v0.87.1) (2024-03-18)

### Bug Fixes

* send event as str from vector to the 'event' field ([7a9d7e8](https://github.com/openedx/tutor-contrib-aspects/commit/7a9d7e8f5ef565d66579b5006e8735b718db3ece))

### Build Systems

* do not build images on bot PRs ([7b0cb69](https://github.com/openedx/tutor-contrib-aspects/commit/7b0cb699ea3f82ea7dccafc035ea8e8f47c54e63))
* **deps:** bump dbt-core ([77bfd93](https://github.com/openedx/tutor-contrib-aspects/commit/77bfd93a7d5e0a06e4dab99ff08d97fef3cbf117))
* **deps:** bump docker/login-action from 3.0.0 to 3.1.0 ([e507e93](https://github.com/openedx/tutor-contrib-aspects/commit/e507e93fd5cefdf1b133f607f2a2e6d5719feba6))

## v0.87.0 - 2024-03-18

### [0.87.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.86.2...v0.87.0) (2024-03-18)

#### Features

* add performance metrics commands ([#657](https://github.com/openedx/tutor-contrib-aspects/issues/657)) ([59139d6](https://github.com/openedx/tutor-contrib-aspects/commit/59139d6f11f903fb6e5658a4df0cb5b4a7526998))

## v0.86.2 - 2024-03-15

### [0.86.2](https://github.com/openedx/tutor-contrib-aspects/compare/v0.86.1...v0.86.2) (2024-03-15)

### Bug Fixes

* remove internal_service_url from production settings ([554f562](https://github.com/openedx/tutor-contrib-aspects/commit/554f562ac9614d2e764a458f26176d4c3ea5a351))

## v0.86.1 - 2024-03-14

### [0.86.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.86.0...v0.86.1) (2024-03-14)

### Bug Fixes

* enable clickhouse console logging ([daa7698](https://github.com/openedx/tutor-contrib-aspects/commit/daa7698ff7956e524dc25ac8d3fe0a18501f7674))

## v0.86.0 - 2024-03-13

### [0.86.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.85.0...v0.86.0) (2024-03-13)

#### Features

* adds ASPECTS_ENABLE_INSTRUCTOR_DASHBOARD_PLUGIN ([082a6c4](https://github.com/openedx/tutor-contrib-aspects/commit/082a6c4d8137fc731559c57d864eb687aa93911f))
* uses platform-plugin-aspects 0.3.0 ([eed3f66](https://github.com/openedx/tutor-contrib-aspects/commit/eed3f667ffbde6b5ed16cd49725dc943ee1a008d))

#### Bug Fixes

* ASPECTS_ENABLE_INSTRUCTOR_DASHBOARD_PLUGIN config ([1d8bec1](https://github.com/openedx/tutor-contrib-aspects/commit/1d8bec16f9c8a6ed2cfc5edb83fd2479bb641720))
* quality ([7648807](https://github.com/openedx/tutor-contrib-aspects/commit/7648807c7f5112efa368cb10137d54a42ff605a0))

#### Build Systems

* don't cache PR images to registry ([8bf4076](https://github.com/openedx/tutor-contrib-aspects/commit/8bf4076db7cfee7dfb124609381f9f9cdaa91891))

## v0.85.0 - 2024-03-13

### [0.85.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.84.0...v0.85.0) (2024-03-13)

#### Features

* turn datasets into virtual ([d4432b5](https://github.com/openedx/tutor-contrib-aspects/commit/d4432b5ee27ba8b324b5e9ba5b40de34464e3188))

## v0.84.0 - 2024-03-13

### [0.84.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.83.0...v0.84.0) (2024-03-13)

#### Features

* allow to translate dataset text on chart ([#648](https://github.com/openedx/tutor-contrib-aspects/issues/648)) ([59ce454](https://github.com/openedx/tutor-contrib-aspects/commit/59ce45476d179a0d6ea039d619a80636bc0e276e))

## v0.83.0 - 2024-03-11

### [0.83.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.82.0...v0.83.0) (2024-03-11)

#### Features

* add metrics and column translation support ([a81e552](https://github.com/openedx/tutor-contrib-aspects/commit/a81e55226e05595b24777196cf68c9bf4b98fc26))
* allow to translate dashboard description ([c147697](https://github.com/openedx/tutor-contrib-aspects/commit/c147697dd1dfd73f03286110355d7380a9d0d119))

#### Bug Fixes

* slowest clickhouse queries sql ([6b56b91](https://github.com/openedx/tutor-contrib-aspects/commit/6b56b91bfb8363fd7fc2ce3a9c18b9cff6d2ab41))

#### Build Systems

* Fix translation pull action ([3ab9874](https://github.com/openedx/tutor-contrib-aspects/commit/3ab9874a0c6780742ce069ea41a94e78dce449da))
* Fix translation pull action ([05be246](https://github.com/openedx/tutor-contrib-aspects/commit/05be246566da738151f49a220512f3526fe722c0))

## v0.82.0 - 2024-03-06

### [0.82.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.81.0...v0.82.0) (2024-03-06)

#### Features

* upgrade dbt to v3.9.0 ([3904283](https://github.com/openedx/tutor-contrib-aspects/commit/39042830b43eea55db60ee8f06cd9875ba3d761d))

## v0.81.0 - 2024-03-06

### [0.81.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.80.0...v0.81.0) (2024-03-06)

#### Features

* install platform plugin aspects ([eaa732b](https://github.com/openedx/tutor-contrib-aspects/commit/eaa732b30614b21061a2d4ab0d6787d9b92d1386))

## v0.80.0 - 2024-03-05

### [0.80.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.79.0...v0.80.0) (2024-03-05)

#### Features

* translations bundled in into Superset image ([c4147d3](https://github.com/openedx/tutor-contrib-aspects/commit/c4147d36c871bee6caa8a3d64587a2cabaaa1d5a))

## v0.79.0 - 2024-02-29

### [0.79.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.78.1...v0.79.0) (2024-02-29)

#### Features

* Use dbt state to avoid large table rebuilds ([e034246](https://github.com/openedx/tutor-contrib-aspects/commit/e034246952c35a5846caece37caccfc099d739bd))

## v0.78.1 - 2024-02-29

### [0.78.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.78.0...v0.78.1) (2024-02-29)

### Bug Fixes

* Some dashboard assets do not have a name to localize ([a8310d7](https://github.com/openedx/tutor-contrib-aspects/commit/a8310d7324686cb74e9a66f832a76630e9d0fb6f))

## v0.78.0 - 2024-02-28

### [0.78.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.77.1...v0.78.0) (2024-02-28)

#### Features

* improve operator dashboard and asset contribution workflow ([#617](https://github.com/openedx/tutor-contrib-aspects/issues/617)) ([81cc1a8](https://github.com/openedx/tutor-contrib-aspects/commit/81cc1a8b1f6e31de7b01c3b3f1d15d23a554bb1d))

## v0.77.1 - 2024-02-26

### [0.77.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.77.0...v0.77.1) (2024-02-26)

### Bug Fixes

* Add importlib-resources to base requirements ([ad2c195](https://github.com/openedx/tutor-contrib-aspects/commit/ad2c1951d87aafc24a617a43c2123470bec0b3e4))

### Build Systems

* Replace old github token for creating PRs ([6806e13](https://github.com/openedx/tutor-contrib-aspects/commit/6806e137f8de7d0b1a0e90f6f76449d6b142f6cd))

## v0.77.0 - 2024-02-23

### [0.77.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.76.0...v0.77.0) (2024-02-23)

#### Features

* upgrade requirements to support CCX courses ([c5fd94e](https://github.com/openedx/tutor-contrib-aspects/commit/c5fd94ed080f28afb188402bf7d26958231b12fc))

## v0.76.0 - 2024-02-21

### [0.76.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.75.0...v0.76.0) (2024-02-21)

#### Features

* Upgrade Ralph to version 4.1.0 ([c85c96d](https://github.com/openedx/tutor-contrib-aspects/commit/c85c96d0e8eb0617a661994c19d18fd2cb74c612))

## v0.75.0 - 2024-02-21

### [0.75.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.74.0...v0.75.0) (2024-02-21)

#### Features

* grant permissions to embed dashboard to Public role ([239ad7f](https://github.com/openedx/tutor-contrib-aspects/commit/239ad7fe30cc940d4d67b03e0818415c94f9dace))

## v0.74.0 - 2024-02-20

### [0.74.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.73.2...v0.74.0) (2024-02-20)

#### Features

* add get_org_from_ccx_course_url function ([45b5e99](https://github.com/openedx/tutor-contrib-aspects/commit/45b5e99428edb8857af6061cf331d8e237eb752c))

## v0.73.2 - 2024-02-16

### [0.73.2](https://github.com/openedx/tutor-contrib-aspects/compare/v0.73.1...v0.73.2) (2024-02-16)

### Bug Fixes

* Fix Python 3.12 support, image building ([dc4d792](https://github.com/openedx/tutor-contrib-aspects/commit/dc4d792b9349c5aac502053d16cfc37652cc50db))

### Code Refactoring

* removes duplicated code in favour of using script files ([6337ef0](https://github.com/openedx/tutor-contrib-aspects/commit/6337ef001194aaebe1e297613aa30605d4276c4d))
* removes the DBT_REPOSITORY_PATH variable ([7ed7362](https://github.com/openedx/tutor-contrib-aspects/commit/7ed7362e03e776ebe66fa60ca14b96e79629be03))

## v0.73.1 - 2024-02-15

### [0.73.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.73.0...v0.73.1) (2024-02-15)

### Bug Fixes

* Upgrade dbt-clickhouse to 1.7.2 ([4d63f79](https://github.com/openedx/tutor-contrib-aspects/commit/4d63f79e0f6fbfc5ad2a19042205284e9eb088c9))

## v0.73.0 - 2024-02-12

### [0.73.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.72.0...v0.73.0) (2024-02-12)

#### Features

* add command to dump data to clickhouse ([019218f](https://github.com/openedx/tutor-contrib-aspects/commit/019218f9e5814013f5e03a80d0acf4fd63f34f74))
* upgrade event-sink-clickhouse to v1.1.0 ([447e052](https://github.com/openedx/tutor-contrib-aspects/commit/447e052f9c2e64a9d9b01d947b64dcb743a42d55))

## v0.72.0 - 2024-02-08

### [0.72.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.71.0...v0.72.0) (2024-02-08)

#### Features

* deploy ralph with uvicorn ([f1e005c](https://github.com/openedx/tutor-contrib-aspects/commit/f1e005c45ba70426be859f4b0febc6144555dee6))

## v0.71.0 - 2024-02-07

### [0.71.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.70.2...v0.71.0) (2024-02-07)

#### Features

* patition xapi_events_all table ([bce56de](https://github.com/openedx/tutor-contrib-aspects/commit/bce56de9554cc6985ae734836dd118ea6db173cf))

## v0.70.2 - 2024-02-07

### [0.70.2](https://github.com/openedx/tutor-contrib-aspects/compare/v0.70.1...v0.70.2) (2024-02-07)

### Bug Fixes

* allow to setup private dbt repository ([947c98d](https://github.com/openedx/tutor-contrib-aspects/commit/947c98d442722212db824f32e44619ba79cd63bc))

## v0.70.1 - 2024-02-02

### [0.70.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.70.0...v0.70.1) (2024-02-02)

### Bug Fixes

* Bump aspects-dbt to 3.4.1 ([e07a4ab](https://github.com/openedx/tutor-contrib-aspects/commit/e07a4aba6db7556365a65857723e9519374a361b))

### Documentation

* Update opencraft URLs to openedx ([22ae778](https://github.com/openedx/tutor-contrib-aspects/commit/22ae778d73429da7d1578bd8a393b03473379cd2))

### Code Refactoring

* Remove refs to ClickHouse allow_experimental_object_type ([56f6d96](https://github.com/openedx/tutor-contrib-aspects/commit/56f6d96cbf745702ab1d89fa5706a5b479153980))

## v0.70.0 - 2024-01-30

### [0.70.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.69.1...v0.70.0) (2024-01-30)

#### Features

* Upgrade event-sink-clickhouse to 1.0.0 ([81b2f8b](https://github.com/openedx/tutor-contrib-aspects/commit/81b2f8b18529bd71a1188b0d24330cd844b78aee))
* Upgrade xapi-db-load to 1.2 for related schema changes ([d5d3a26](https://github.com/openedx/tutor-contrib-aspects/commit/d5d3a2625775f2b154aac8afcaaab197fdd567ee))

## v0.69.1 - 2024-01-30

### [0.69.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.69.0...v0.69.1) (2024-01-30)

### Bug Fixes

* import databases from settings ([be5d76d](https://github.com/openedx/tutor-contrib-aspects/commit/be5d76d39d512c775f0722ad21536b28e360f2d6))

### Documentation

* add superset build information ([a971529](https://github.com/openedx/tutor-contrib-aspects/commit/a971529e2a28ca9128cc411877593be37867f406))

## v0.69.0 - 2024-01-29

### [0.69.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.68.2...v0.69.0) (2024-01-29)

#### ⚠ BREAKING CHANGES

* Upgrade to Ralph 4.0

#### Features

* Upgrade xapi-db-load to 1.1 ([8a81a3b](https://github.com/openedx/tutor-contrib-aspects/commit/8a81a3bef4b5a3485d73ee2b5a76ad18603c42a8))
* Use official versions of Ralph 4 and aspects-dbt ([fded401](https://github.com/openedx/tutor-contrib-aspects/commit/fded40145d6a20ea5040d900a96bb3ad895e0aaa))

#### Bug Fixes

* Use new Ralph config vars in k8s ([30816c5](https://github.com/openedx/tutor-contrib-aspects/commit/30816c582ae0f7746765cdb19839737df97033a0))

#### Code Refactoring

* Upgrade to Ralph 4.0 ([885c33f](https://github.com/openedx/tutor-contrib-aspects/commit/885c33f56b710b74a4548b4ff4bdbdb8babcc107))

#### Documentation

* Update readme to include building Superset image ([dbe1736](https://github.com/openedx/tutor-contrib-aspects/commit/dbe17366eb13329d9bb1c3a74fd19be58656ae43))

## v0.68.2 - 2024-01-29

### [0.68.2](https://github.com/openedx/tutor-contrib-aspects/compare/v0.68.1...v0.68.2) (2024-01-29)

### Bug Fixes

* mount clickhouse settings by individual files ([1b572a5](https://github.com/openedx/tutor-contrib-aspects/commit/1b572a51471ea34c2fcd688022fca975bad54684))

### Styles

* Update style for black v24 ([9f0a4b9](https://github.com/openedx/tutor-contrib-aspects/commit/9f0a4b965c546be2240bffd052d2a3170a20ef6b))

### Documentation

* annotates the PII tables in Aspects ([b5138dc](https://github.com/openedx/tutor-contrib-aspects/commit/b5138dc2bd3efbf9933c22a5d9a396ae55222382))

### Code Refactoring

* Make config file a patch ([f9b0e01](https://github.com/openedx/tutor-contrib-aspects/commit/f9b0e01364fe327ff37a078a746440c8fe32bd76))
* use patch for clickhouse settings ([a1069db](https://github.com/openedx/tutor-contrib-aspects/commit/a1069db985846f2edb22e8038037bdd5cdeb4588))

## v0.68.1 - 2024-01-18

### [0.68.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.68.0...v0.68.1) (2024-01-18)

### Bug Fixes

* change jobs PVC by emptyDir volume ([2ff1a44](https://github.com/openedx/tutor-contrib-aspects/commit/2ff1a442ae87ddf90fe64376de598dc2ce8d9d3b))

### Code Refactoring

* moves the LMS init script under its own dir ([44e8a2f](https://github.com/openedx/tutor-contrib-aspects/commit/44e8a2f0596a5942bc40661c4da9ace18bbda2e5))

## v0.68.0 - 2024-01-12

### [0.68.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.67.2...v0.68.0) (2024-01-12)

#### Features

* prefer course_names in operator dashboard ([ff2e3fc](https://github.com/openedx/tutor-contrib-aspects/commit/ff2e3fc503c5472d971f0d0239c9d8360043b6bd))

## v0.67.2 - 2024-01-12

### [0.67.2](https://github.com/openedx/tutor-contrib-aspects/compare/v0.67.1...v0.67.2) (2024-01-12)

### Bug Fixes

* write MVs to xapi schema ([be279d7](https://github.com/openedx/tutor-contrib-aspects/commit/be279d7d30cfb49cd9f17cd37b0cb7508510959e))

## v0.67.1 - 2024-01-11

### [0.67.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.67.0...v0.67.1) (2024-01-11)

### Bug Fixes

* enable user retirement sink ([5e39b03](https://github.com/openedx/tutor-contrib-aspects/commit/5e39b03ba5c633dcbbfd5e7e4430b0423ee689a3))

### Code Refactoring

* separate event sink models from PII models ([4332e05](https://github.com/openedx/tutor-contrib-aspects/commit/4332e05ec3c7c1e12fdeea17fca54909acd5d5ee))

## v0.67.0 - 2024-01-10

### [0.67.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.66.1...v0.67.0) (2024-01-10)

#### Features

* course_names for operator dashboard filters ([306c504](https://github.com/openedx/tutor-contrib-aspects/commit/306c50479ee4ce91a33ee9bf297a407740de0708))

## v0.66.1 - 2023-12-20

### [0.66.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.66.0...v0.66.1) (2023-12-20)

### ⚠ BREAKING CHANGES

* Move materialized views to dbt

### Bug Fixes

* Upgrade aspects-dbt to 3.1.1 to get bug fixes ([cb990e3](https://github.com/openedx/tutor-contrib-aspects/commit/cb990e3dba68f9ca7a834babe002d146bd078321))

### Code Refactoring

* Move materialized views to dbt ([d2d9b88](https://github.com/openedx/tutor-contrib-aspects/commit/d2d9b88c5d9f9f6f9bc38fc14505735e83b7d8b4))

## v0.66.0 - 2023-12-11

### [0.66.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.65.1...v0.66.0) (2023-12-11)

#### Features

* add external id table ([bcd308f](https://github.com/openedx/tutor-contrib-aspects/commit/bcd308fa41073a62a4c68ac237fa3db8d396b604))
* adds event_sink.user_pii table ([7ced3f7](https://github.com/openedx/tutor-contrib-aspects/commit/7ced3f703073bc8e1ecadacfe0e204a0bf358f5a))
* adds user_pii dataset ([9ceb57b](https://github.com/openedx/tutor-contrib-aspects/commit/9ceb57b7840a6712786768097be146d224e602d1))
* partition the event_sink.external_id table by user_id % 100 ([c45aefe](https://github.com/openedx/tutor-contrib-aspects/commit/c45aefe74c435debc2fde438757f983af31b41a2))
* partition the event_sink.user_profile table by user_id % 100 ([24db8d1](https://github.com/openedx/tutor-contrib-aspects/commit/24db8d115c55e1c5b4d8a0b3809109324d49ff0a))
* pass EVENT_SINK_CLICKHOUSE_PII_MODELS to the openedx settings ([defb3f1](https://github.com/openedx/tutor-contrib-aspects/commit/defb3f19cd06a790ab5c837bc34aa87cdc0e54a4))

#### Bug Fixes

* grant DELETE access to the CMS Clickhouse user on the event_sink db ([b97a690](https://github.com/openedx/tutor-contrib-aspects/commit/b97a6909a1790eaadbe171fb908711ce5e0004e5))
* user_pii uses external_id_type=xapi ([57a4f56](https://github.com/openedx/tutor-contrib-aspects/commit/57a4f563abf38c446b01417a2e3fc10b36aa63a5))

## v0.65.1 - 2023-12-06

### [0.65.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.65.0...v0.65.1) (2023-12-06)

### Bug Fixes

* Add more informational error message. ([703e969](https://github.com/openedx/tutor-contrib-aspects/commit/703e969e8cca77cb44fcb095fc7edd9033c7f000))
* Bump ERB to 7.2.0 ([f6ef21f](https://github.com/openedx/tutor-contrib-aspects/commit/f6ef21f51dd1baf5a07bbbcf2115082289ff70b1))

## v0.65.0 - 2023-11-29

### [0.65.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.64.0...v0.65.0) (2023-11-29)

#### Features

* add external id table ([3c50bd7](https://github.com/openedx/tutor-contrib-aspects/commit/3c50bd76b49da8379349fc5e52398af81e4e8089))

## v0.64.0 - 2023-11-29

### [0.64.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.63.1...v0.64.0) (2023-11-29)

#### Features

* Adds course_key_short computed field ([93e07da](https://github.com/openedx/tutor-contrib-aspects/commit/93e07da18364eb45abfd57af5159d91cd5753b2a))

#### Bug Fixes

* re-adds the "Events per course" pie chart to the Operator > Courses tab ([20fc7b5](https://github.com/openedx/tutor-contrib-aspects/commit/20fc7b59efb7188d4a19dec56ff366fa6cf89ce4))

## v0.63.1 - 2023-11-23

### [0.63.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.63.0...v0.63.1) (2023-11-23)

### Bug Fixes

- containerPort values must be numeric ([332e79b](https://github.com/openedx/tutor-contrib-aspects/commit/332e79b4d7b7ae8e11ed7845dad4676bc8c040a4))
- use tutor variables to expose clickhouse container ports in k8s ([8c1720f](https://github.com/openedx/tutor-contrib-aspects/commit/8c1720fd35209d062fee8dad6b0b99cc1c764ea7))

## v0.63.0 - 2023-11-09

### [0.63.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.62.4...v0.63.0) (2023-11-09)

#### Features

- Adds Help tab to Instructor Dashboard ([2d931f8](https://github.com/openedx/tutor-contrib-aspects/commit/2d931f83fe8a5c649a53eb2ad1e2a787a025115b))
- Adds Help tab to Operator Dashboard ([a11a0e0](https://github.com/openedx/tutor-contrib-aspects/commit/a11a0e0729f54e1370efe9d5e9947830729cd361))

#### Bug Fixes

- link to Aspects References page ([1d17283](https://github.com/openedx/tutor-contrib-aspects/commit/1d172832492d038e2f8e30ea39d8591df8785a23))
- lint ([b92c80c](https://github.com/openedx/tutor-contrib-aspects/commit/b92c80c53b529833f65da1308cd99b643730f253))

#### Code Refactoring

- replaces dashboard tab docs with link to openedx-aspects docs ([994d8a0](https://github.com/openedx/tutor-contrib-aspects/commit/994d8a0d04f08d873ab1da74ed6689d9b3d4a79b))

## v0.62.4 - 2023-11-09

### [0.62.4](https://github.com/openedx/tutor-contrib-aspects/compare/v0.62.3...v0.62.4) (2023-11-09)

### Bug Fixes

- Bump ERB to 7.0.1 for problem result fixes ([9b98699](https://github.com/openedx/tutor-contrib-aspects/commit/9b9869908bbb7a6b1203a77b4cf5ade1a0d76f74))
- Remove split on requirements in versions chart ([24dc754](https://github.com/openedx/tutor-contrib-aspects/commit/24dc7547e7ab1770cb20ad61cc37d4ad11d0c9e5))

## v0.62.3 - 2023-11-03

### [0.62.3](https://github.com/openedx/tutor-contrib-aspects/compare/v0.62.2...v0.62.3) (2023-11-03)

### Bug Fixes

- Quote new templated values in assets ([e3c1476](https://github.com/openedx/tutor-contrib-aspects/commit/e3c1476cc0481146cd849c5f1394ed628712c6ce))

## v0.62.2 - 2023-11-02

### [0.62.2](https://github.com/openedx/tutor-contrib-aspects/compare/v0.62.1...v0.62.2) (2023-11-02)

### Bug Fixes

- Change translations source path ([e045b10](https://github.com/openedx/tutor-contrib-aspects/commit/e045b106c7239263c020c568ae744fd5efc7d255))

## v0.62.1 - 2023-11-02

### [0.62.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.62.0...v0.62.1) (2023-11-02)

### Bug Fixes

- Don't save intermediate translations files, fix parse error ([d26e6e9](https://github.com/openedx/tutor-contrib-aspects/commit/d26e6e9924127f89f95482ac3470e45f593501df))

### Code Refactoring

- Remove language tag from untranslated strings ([934c627](https://github.com/openedx/tutor-contrib-aspects/commit/934c6275b96bbf76967d379603ec19cc9eafb0aa))

## v0.62.0 - 2023-11-02

### [0.62.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.61.0...v0.62.0) (2023-11-02)

#### Features

- adds "Most-used Charts" to Superset Usage dashboard ([cc86114](https://github.com/openedx/tutor-contrib-aspects/commit/cc8611454688e7baeac66d577956edc24ad68fe7))
- adds description field to Superset Usage charts ([f0db289](https://github.com/openedx/tutor-contrib-aspects/commit/f0db2893f6c53e48056190c62907a786eab972bc))
- adds Superset Metadata ([0586ee6](https://github.com/openedx/tutor-contrib-aspects/commit/0586ee6bc774bc75fde8ec8503940b9e5b31d533))

#### Bug Fixes

- grant SELECT access to a subset of superset metadata tables ([60d0f37](https://github.com/openedx/tutor-contrib-aspects/commit/60d0f37a981090333e852c0a32d71493506e45f5))
- nulls unneeded query_context field in charts ([8d71dfc](https://github.com/openedx/tutor-contrib-aspects/commit/8d71dfc9b9ad2cdf3968310af6ac2b4427e06563))

#### Code Refactoring

- moves Superset Metadata dashboard into a tab on the Operator dashboard ([9ad42bf](https://github.com/openedx/tutor-contrib-aspects/commit/9ad42bf8759d0ebd7eda9985d938d4e87f607d1c))
- splits mysql init into two steps ([ba89145](https://github.com/openedx/tutor-contrib-aspects/commit/ba891451499de2a37698fe822c1ac7a5b240614f))

## v0.61.0 - 2023-11-01

### [0.61.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.60.0...v0.61.0) (2023-11-01)

#### Features

- load default assets from image instead of a larger assets file ([5fc6de2](https://github.com/openedx/tutor-contrib-aspects/commit/5fc6de2a4746b547e079a12ffa40005dfad6997f))

#### Bug Fixes

- address suggestions ([532c9d5](https://github.com/openedx/tutor-contrib-aspects/commit/532c9d583d0af80967b3724ecf6eda06d21c4451))

#### Documentation

- add rebuild step to docs ([62939d4](https://github.com/openedx/tutor-contrib-aspects/commit/62939d4db417e2f0b4917be3ca5a855a978e4bc7))

## v0.60.0 - 2023-11-01

### [0.60.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.59.0...v0.60.0) (2023-11-01)

#### Features

- adds Clickhouse metrics to Operator / Clickhouse tab ([5af67af](https://github.com/openedx/tutor-contrib-aspects/commit/5af67af8f0820cb25471c42910c2bf573b47b015))

## v0.59.0 - 2023-10-26

### [0.59.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.58.0...v0.59.0) (2023-10-26)

#### Features

- replace double quotes in problem responses ([c56a9d6](https://github.com/openedx/tutor-contrib-aspects/commit/c56a9d696e543b310e9d44c02fa5e961bac2f933))

#### Bug Fixes

- properly escape characters in migration ([e9a6157](https://github.com/openedx/tutor-contrib-aspects/commit/e9a6157ec0173b62b83bf9b2e7accd2e1c1c8da8))

## v0.58.0 - 2023-10-25

### [0.58.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.57.3...v0.58.0) (2023-10-25)

#### Features

- Upgrade Superset to 3.0.1 ([549e015](https://github.com/openedx/tutor-contrib-aspects/commit/549e0157b11592c7c04f26399f2774b1d4f96d2c))

#### Documentation

- Fix duplicate https in doc links ([323cc21](https://github.com/openedx/tutor-contrib-aspects/commit/323cc21055f17262875fdb448a3e414c6e044c03))

## v0.57.3 - 2023-10-25

### [0.57.3](https://github.com/openedx/tutor-contrib-aspects/compare/v0.57.2...v0.57.3) (2023-10-25)

### Bug Fixes

- Pull filter names as translatable strings ([50be682](https://github.com/openedx/tutor-contrib-aspects/commit/50be682d99ad44528af2964b0cd7135390ab9ef8))

## v0.57.2 - 2023-10-24

### [0.57.2](https://github.com/openedx/tutor-contrib-aspects/compare/v0.57.1...v0.57.2) (2023-10-24)

### Bug Fixes

- Allow Jinja in templates again ([22f8d80](https://github.com/openedx/tutor-contrib-aspects/commit/22f8d807b31bc380752c3d1c77b77b6b5b2b80bb))
- Correctly cache user permissions ([4d793e3](https://github.com/openedx/tutor-contrib-aspects/commit/4d793e3376521a9e14ba5627b0b46f22a9288ba0))

## v0.57.1 - 2023-10-19

### [0.57.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.57.0...v0.57.1) (2023-10-19)

### Bug Fixes

- Lint issue ([36ba791](https://github.com/openedx/tutor-contrib-aspects/commit/36ba791020b2ada47df7e2eea28de1e47f814068))

### Code Refactoring

- Use new Transifex / Atlas pipeline to pull loc ([bf45e35](https://github.com/openedx/tutor-contrib-aspects/commit/bf45e35f977107a94c303916c26a67dc9b212fe4))

## v0.57.0 - 2023-10-19

### [0.57.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.56.1...v0.57.0) (2023-10-19)

#### Features

- display multiple-choice answers separately ([4ea65d6](https://github.com/openedx/tutor-contrib-aspects/commit/4ea65d69307b53e5da96cedb46296c785fe3a259))

#### Code Refactoring

- use extended block names in dashboard ([d2145f0](https://github.com/openedx/tutor-contrib-aspects/commit/d2145f02c6679b101b0ed18ac953321c598b750b))

## v0.56.1 - 2023-10-16

### [0.56.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.56.0...v0.56.1) (2023-10-16)

### Bug Fixes

- consistently apply datetime filter on problem engagement tab ([83dd43e](https://github.com/openedx/tutor-contrib-aspects/commit/83dd43e49feb6e12259f6853a358ac9eb68bf372))

## v0.56.0 - 2023-10-16

### [0.56.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.55.0...v0.56.0) (2023-10-16)

#### Features

- add location to block display names ([6b634ba](https://github.com/openedx/tutor-contrib-aspects/commit/6b634baa0ab59c4c44b30569d9a7fd91c55d107e))

## v0.55.0 - 2023-10-13

### [0.55.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.54.0...v0.55.0) (2023-10-13)

#### Features

- create embeddable UUID ([d272077](https://github.com/openedx/tutor-contrib-aspects/commit/d2720772fc146982785281c124bc65ced2bee8e0))
- create Superset LMS admin user ([cef50fd](https://github.com/openedx/tutor-contrib-aspects/commit/cef50fd5efa1bea5879fc0531a7d7b03a6a2371e))
- inject superset dashboards settings in LMS ([30cce25](https://github.com/openedx/tutor-contrib-aspects/commit/30cce25b23a41e42891f7c457341bbfe2edb0a78))

#### Code Refactoring

- define SUPERSET_EMBEDDABLE_DASHBOARDS setting ([6c8cb82](https://github.com/openedx/tutor-contrib-aspects/commit/6c8cb829ecafbdbf4f2e09292eaeedbbf35634a2))

## v0.54.0 - 2023-10-13

### [0.54.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.53.0...v0.54.0) (2023-10-13)

#### Features

- add tutor patches for superset config ([b05a198](https://github.com/openedx/tutor-contrib-aspects/commit/b05a198dbd7b2503fec6a7bff7e0d9cdc5d641b6))

#### Bug Fixes

- Remove Jinja from localized files ([6249248](https://github.com/openedx/tutor-contrib-aspects/commit/6249248ae1ce84483d5b2230eb543f486b30ced9))

#### Build Systems

- Add free disk space to dev and local tests ([3d8eb9f](https://github.com/openedx/tutor-contrib-aspects/commit/3d8eb9f3970cd23623dd7ae79395d4d21da2d16c))
- Update workflows for new translations ([43a967c](https://github.com/openedx/tutor-contrib-aspects/commit/43a967c1cb2d700302156790c9a3ff97a20d05a1))

#### Code Refactoring

- Change where transifex input generates ([f2216b1](https://github.com/openedx/tutor-contrib-aspects/commit/f2216b105697b3ee5860d45fffe0a2d65f5176fc))
- Move translations to the openedx Transifex project ([c12fdcf](https://github.com/openedx/tutor-contrib-aspects/commit/c12fdcf810980799583ab09ee0746ee9a1f291c5))

## v0.53.1 - 2023-10-13

### [0.53.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.53.0...v0.53.1) (2023-10-13)

### Bug Fixes

- Remove Jinja from localized files ([6249248](https://github.com/openedx/tutor-contrib-aspects/commit/6249248ae1ce84483d5b2230eb543f486b30ced9))

### Build Systems

- Add free disk space to dev and local tests ([3d8eb9f](https://github.com/openedx/tutor-contrib-aspects/commit/3d8eb9f3970cd23623dd7ae79395d4d21da2d16c))
- Update workflows for new translations ([43a967c](https://github.com/openedx/tutor-contrib-aspects/commit/43a967c1cb2d700302156790c9a3ff97a20d05a1))

### Code Refactoring

- Change where transifex input generates ([f2216b1](https://github.com/openedx/tutor-contrib-aspects/commit/f2216b105697b3ee5860d45fffe0a2d65f5176fc))
- Move translations to the openedx Transifex project ([c12fdcf](https://github.com/openedx/tutor-contrib-aspects/commit/c12fdcf810980799583ab09ee0746ee9a1f291c5))

## v0.53.0 - 2023-10-11

### [0.53.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.52.2...v0.53.0) (2023-10-11)

#### Features

- add forum interaction tab ([e923a30](https://github.com/openedx/tutor-contrib-aspects/commit/e923a304c652843f137d3e7d1887da6f09bdf00d))

#### Code Refactoring

- remove unnecessary query_context from forum charts ([48cd3da](https://github.com/openedx/tutor-contrib-aspects/commit/48cd3dae28d5765da235c4a035d5971636d3cdfb))

## v0.52.2 - 2023-10-11

### [0.52.2](https://github.com/openedx/tutor-contrib-aspects/compare/v0.52.1...v0.52.2) (2023-10-11)

### Bug Fixes

- Make the Superset MySQL database utf8mb4 ([4e2f9e0](https://github.com/openedx/tutor-contrib-aspects/commit/4e2f9e035970cba2bb7e0c7ab9031013e6e064ae))

## v0.52.1 - 2023-10-11

### [0.52.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.52.0...v0.52.1) (2023-10-11)

### Bug Fixes

- Incorrect path for assets introduced in the loc refactor ([d6858fe](https://github.com/openedx/tutor-contrib-aspects/commit/d6858fe19d7e8b8f7d4d1a692650ea564b576477))

### Build Systems

- Move locale.yaml to new mount location ([e93a095](https://github.com/openedx/tutor-contrib-aspects/commit/e93a0951adbafb283e7bfad05f655ba98b631554))

### Code Refactoring

- Tidy up Operator Dashboard ([6c9f957](https://github.com/openedx/tutor-contrib-aspects/commit/6c9f957290a2ffde73a8acacd496d1fe185f4451))

## v0.52.0 - 2023-10-10

### [0.52.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.51.1...v0.52.0) (2023-10-10)

#### Features

- enable embedded superset and charts ([b20c2dc](https://github.com/openedx/tutor-contrib-aspects/commit/b20c2dc4ebd55fc8ece3310300aa657a13c8921e))

## v0.51.1 - 2023-10-03

### [0.51.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.51.0...v0.51.1) (2023-10-03)

### Bug Fixes

- remove cache for get_courses ([ff5c9c5](https://github.com/openedx/tutor-contrib-aspects/commit/ff5c9c5651e5d0f7abd4aace0809d8344d433ffa))

## v0.51.0 - 2023-10-03

### [0.51.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.50.0...v0.51.0) (2023-10-03)

#### Features

- Bump event-sink-clickhouse to 0.4.0 ([269aa1e](https://github.com/openedx/tutor-contrib-aspects/commit/269aa1e063ac3df2ecc34515d6365f83aabd2209))

## v0.50.0 - 2023-09-26

### [0.50.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.49.0...v0.50.0) (2023-09-26)

#### Features

- Upgrade event-routing-backends to v7.0.0 ([9b3770a](https://github.com/openedx/tutor-contrib-aspects/commit/9b3770a34186f28a1406c9091cdb660c990b96ef))

## v0.49.0 - 2023-09-26

### [0.49.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.48.0...v0.49.0) (2023-09-26)

#### Features

- upgrade aspects-dbt to v2.5 ([518e9c7](https://github.com/openedx/tutor-contrib-aspects/commit/518e9c7d683141ee5961b812406d97dcde4d841a))

## v0.48.0 - 2023-09-25

### [0.48.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.47.0...v0.48.0) (2023-09-25)

#### Features

- add version card to operator dashboard ([4c659b5](https://github.com/openedx/tutor-contrib-aspects/commit/4c659b50b9efa57087f1f9c348d69a130c2055dd))

## v0.47.0 - 2023-09-25

### [0.47.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.46.2...v0.47.0) (2023-09-25)

#### Features

- add views for completion events ([e0b1daa](https://github.com/openedx/tutor-contrib-aspects/commit/e0b1daafc7d8d7763982b1e40c3cd441106f6c61))

## v0.46.2 - 2023-09-25

### [0.46.2](https://github.com/openedx/tutor-contrib-aspects/compare/v0.46.1...v0.46.2) (2023-09-25)

### Bug Fixes

- implement a enable PII flag ([ef0d7ef](https://github.com/openedx/tutor-contrib-aspects/commit/ef0d7efe00ac140725c189f17d6222ec1cac8fd2))

## v0.46.1 - 2023-09-25

### [0.46.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.46.0...v0.46.1) (2023-09-25)

### Bug Fixes

- do not override openedx docker image ([57fa9a2](https://github.com/openedx/tutor-contrib-aspects/commit/57fa9a26d6e6a1c29d678d4a41acc1948edf53ac))

### Tests

- update docker image in CI ([1bd8f5d](https://github.com/openedx/tutor-contrib-aspects/commit/1bd8f5df92232faff6d508e7499f4b9984e522de))

## v0.46.0 - 2023-09-25

### [0.46.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.45.0...v0.46.0) (2023-09-25)

#### Features

- upgrade event-routing-backends to 6.2.0 ([bc8d8a7](https://github.com/openedx/tutor-contrib-aspects/commit/bc8d8a7d6b6af954bed4d11e88d97fad7a258fb3))

## v0.45.0 - 2023-09-22

### [0.45.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.44.4...v0.45.0) (2023-09-22)

#### Features

- upgrade superset to 3.0.0 ([ba6aa1f](https://github.com/openedx/tutor-contrib-aspects/commit/ba6aa1fc5eac507c1527b1b003db9feb14be2338))

## v0.44.4 - 2023-09-22

### [0.44.4](https://github.com/openedx/tutor-contrib-aspects/compare/v0.44.3...v0.44.4) (2023-09-22)

### Bug Fixes

- remove unused PVC for vector ([06572a9](https://github.com/openedx/tutor-contrib-aspects/commit/06572a9c8b86cc64884d7038329e5b54f9a6e3fa))
- use local volume instead of emtpy dir for vector data ([9fd3ad3](https://github.com/openedx/tutor-contrib-aspects/commit/9fd3ad35796262b181a5971f9b9fec3be4976384))

## v0.44.3 - 2023-09-22

### [0.44.3](https://github.com/openedx/tutor-contrib-aspects/compare/v0.44.2...v0.44.3) (2023-09-22)

### Bug Fixes

- update ralph clickhouse database name ([e8a39cf](https://github.com/openedx/tutor-contrib-aspects/commit/e8a39cf0c02d35359035afb099fd15a7b239a569))

### Tests

- add test for custom commands in CI ([836a203](https://github.com/openedx/tutor-contrib-aspects/commit/836a2037e8b06e632ca64834a1e100a2efab0fd5))

## v0.44.2 - 2023-09-21

### [0.44.2](https://github.com/openedx/tutor-contrib-aspects/compare/v0.44.1...v0.44.2) (2023-09-21)

### Bug Fixes

- update the get org from url function to include other chars ([3711db3](https://github.com/openedx/tutor-contrib-aspects/commit/3711db36522abc3342862fbcfd500e8dd880a076))

## v0.44.1 - 2023-09-21

### [0.44.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.44.0...v0.44.1) (2023-09-21)

### Bug Fixes

- upgrade openedx-event-sink-clickhouse to 0.2.2 ([9fbd1f5](https://github.com/openedx/tutor-contrib-aspects/commit/9fbd1f5fb719e2be354e869f41da8bdffc7612d1))

### Tests

- add test for dump-courses command ([6ff7280](https://github.com/openedx/tutor-contrib-aspects/commit/6ff72806c21c013b7646baf60b5cb526ea337df3))
- load the openedx image instead of openedx-dev ([29709ba](https://github.com/openedx/tutor-contrib-aspects/commit/29709ba737711e4bfea2739868604c9635534922))

## v0.44.0 - 2023-09-19

### [0.44.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.43.0...v0.44.0) (2023-09-19)

#### Features

- Add support ClickHouse clusters ([72b7ae8](https://github.com/openedx/tutor-contrib-aspects/commit/72b7ae820ff9bbca91023d7e554258aad0455bf7))

## v0.43.0 - 2023-09-19

### [0.43.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.42.2...v0.43.0) (2023-09-19)

#### Features

- add materialized view for forum events ([65e7785](https://github.com/openedx/tutor-contrib-aspects/commit/65e7785b4e9f6af0102e8e263585d3fb58d16f23))

#### Code Refactoring

- use more accurate filter for forum event MV ([4a9bbef](https://github.com/openedx/tutor-contrib-aspects/commit/4a9bbefcdd2239cb93d983cf0363ac19c6b41a85))

## v0.42.2 - 2023-09-19

### [0.42.2](https://github.com/openedx/tutor-contrib-aspects/compare/v0.42.1...v0.42.2) (2023-09-19)

### Bug Fixes

- Enable Superset proxy fix when Caddy is on ([39e4b53](https://github.com/openedx/tutor-contrib-aspects/commit/39e4b53bab73f258a957f319f0636b50c4c82dfb))

## v0.42.1 - 2023-09-18

### [0.42.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.42.0...v0.42.1) (2023-09-18)

### Bug Fixes

- add security context for k8s-job ([0709612](https://github.com/openedx/tutor-contrib-aspects/commit/07096121b317f565599624c9111dcd700ac6a302))
- delete folder ([52b1bb8](https://github.com/openedx/tutor-contrib-aspects/commit/52b1bb8cdaf34d41850fbb09f84fa15a31b58c09))

## v0.42.0 - 2023-09-14

### [0.42.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.41.0...v0.42.0) (2023-09-14)

#### Features

- Add new localization fields, update locale ([7f5c23f](https://github.com/openedx/tutor-contrib-aspects/commit/7f5c23f58ba1b50561cfeaf3779fbc8d4a10e848))
- Usability updates to Instructor Dashboard ([0b45e16](https://github.com/openedx/tutor-contrib-aspects/commit/0b45e16b2a30293a541f7c3c7f1f7742f58f9566))

#### Bug Fixes

- Org filter, weird colors, Responses Per Problem chart ([1245981](https://github.com/openedx/tutor-contrib-aspects/commit/1245981f55d6793b4e3eeb21668f82c90eea75c0)), closes [#377](https://github.com/openedx/tutor-contrib-aspects/issues/377)
- Remove Help tab and FAQ ([d230469](https://github.com/openedx/tutor-contrib-aspects/commit/d2304690bc8c97e7ac23893dbf8141a10853e0be))
- Remove query_context to try to reduce assets.yml size ([a5abd78](https://github.com/openedx/tutor-contrib-aspects/commit/a5abd7868f230435abedab31774340a9844ce398))
- Update help text to match what users need to do ([df133cd](https://github.com/openedx/tutor-contrib-aspects/commit/df133cd9055c3a695b1ea26eaafcf3ccf6224c99)), closes [#377](https://github.com/openedx/tutor-contrib-aspects/issues/377)

#### Build Systems

- Move namespace setup above init in k8s tests ([74c636d](https://github.com/openedx/tutor-contrib-aspects/commit/74c636d85b5d79ef7ac91b6737d7a9e769b5843b))

## v0.41.0 - 2023-09-13

### [0.41.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.40.2...v0.41.0) (2023-09-13)

#### Features

- limit data returned by learner summary query ([0f7e904](https://github.com/openedx/tutor-contrib-aspects/commit/0f7e9041b96529c0ce2faa705e0f982e67a8d205))
- limit data returned when filters are absent ([7a71daf](https://github.com/openedx/tutor-contrib-aspects/commit/7a71daf64a526b73c6243e818f3a51b508281e7b))

#### Bug Fixes

- ensure datasets follow filter guidelines ([d5270ce](https://github.com/openedx/tutor-contrib-aspects/commit/d5270cef60536cdfb7d7b0ea72a1bb2d8f61186e))

## v0.40.2 - 2023-09-13

### [0.40.2](https://github.com/openedx/tutor-contrib-aspects/compare/v0.40.1...v0.40.2) (2023-09-13)

### Bug Fixes

- rename clickhouse config to avoid conflict ([badd23f](https://github.com/openedx/tutor-contrib-aspects/commit/badd23ffa88744c8ea641c58838bd863f841c761))
- revert value for ClickHouse HTTP settings ([791eac6](https://github.com/openedx/tutor-contrib-aspects/commit/791eac679ece26d2ec09fcdac5f3eff494c739c1))

## v0.40.1 - 2023-09-12

### [0.40.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.40.0...v0.40.1) (2023-09-12)

### Bug Fixes

- Event sink config with SSL ClickHouse ([1660a5e](https://github.com/openedx/tutor-contrib-aspects/commit/1660a5e47607dfce97879fcb691f49d9c63df98d))
- Fix ClickHouse port names, allow overrides ([d541ebd](https://github.com/openedx/tutor-contrib-aspects/commit/d541ebdbe39d32cda08143fccc6ceba7b0e51583))

### Styles

- Fix linting errors ([5c2d79d](https://github.com/openedx/tutor-contrib-aspects/commit/5c2d79d6d523dc670fa388b776e15fc9044fcab9))

## v0.40.0 - 2023-09-12

### [0.40.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.39.0...v0.40.0) (2023-09-12)

#### Features

- add charts for course and problem grades ([95180d1](https://github.com/openedx/tutor-contrib-aspects/commit/95180d147a7865d75dd04905b9d6b1d4a71921cf))

#### Code Refactoring

- rename grade distribution chart files ([a9bd0d2](https://github.com/openedx/tutor-contrib-aspects/commit/a9bd0d2abbb1e3dbbb3a1dcb6bc277cf7356ef66))

## v0.39.0 - 2023-09-11

### [0.39.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.38.0...v0.39.0) (2023-09-11)

#### Features

- add graded boolean to course_block_names ([44aa74b](https://github.com/openedx/tutor-contrib-aspects/commit/44aa74bbba2ec11b71b13c9a1d49b3ca8cf5ddf9))
- add top-level MV for grading events ([06d30b8](https://github.com/openedx/tutor-contrib-aspects/commit/06d30b8c6334d841330011041c3651ba6e2c056d))

#### Bug Fixes

- align downgrade schema with previous version ([6a39394](https://github.com/openedx/tutor-contrib-aspects/commit/6a39394889898544f1cc95d0e8275aea929ac69f))

#### Documentation

- Update readme install instructions ([4ca46dd](https://github.com/openedx/tutor-contrib-aspects/commit/4ca46dd69625b83a1608a13ee8ce225d626784b5))

#### Code Refactoring

- move graded into separate migration ([cfe2a86](https://github.com/openedx/tutor-contrib-aspects/commit/cfe2a86318714c7748d75ec2b19a317124a216e3))

## v0.38.0 - 2023-09-07

### [0.38.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.37.0...v0.38.0) (2023-09-07)

#### Features

- Upgrade ClickHouse to 23.8 LTS ([44ccd13](https://github.com/openedx/tutor-contrib-aspects/commit/44ccd1304653eae7ba6b0252cb6475a4e55f5376))

#### Bug Fixes

- update course run filter to correct column name ([a2068cf](https://github.com/openedx/tutor-contrib-aspects/commit/a2068cfc7dfa3ae2f230b34e34e7f0a62b522de5))

## v0.37.0 - 2023-09-07

### [0.37.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.36.0...v0.37.0) (2023-09-07)

#### Features

- enable model sink by default ([5f4b2c8](https://github.com/openedx/tutor-contrib-aspects/commit/5f4b2c837dd55a52e9efe16a3d1882481abe99ee))
- upgrade openedx-event-sink-clickhouse to 0.2.0 ([0519906](https://github.com/openedx/tutor-contrib-aspects/commit/0519906eeeb9063331d8618d2d197ef2edcedb57))

#### Bug Fixes

- correct event sink profile migration ([9aedc16](https://github.com/openedx/tutor-contrib-aspects/commit/9aedc16d6602c24818e8adb57dab687154109095))

#### Tests

- start tutor services before initialization ([1a1853a](https://github.com/openedx/tutor-contrib-aspects/commit/1a1853a89342ae930a5dcb7b950c8aeddaf01654))

#### Code Refactoring

- use dim_course_blocks for metadata joins ([dde2864](https://github.com/openedx/tutor-contrib-aspects/commit/dde2864fa03e78a8088fd75ff6b25d5039341b50))

## v0.36.0 - 2023-09-06

### [0.36.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.35.0...v0.36.0) (2023-09-06)

#### Features

- enable alerts and reports ([66bf961](https://github.com/openedx/tutor-contrib-aspects/commit/66bf9611d7357841f796f01d22caf761cf660892))

#### Bug Fixes

- setup.py update using script ([5b1a142](https://github.com/openedx/tutor-contrib-aspects/commit/5b1a14239d024a69c89b94182bb88c15aed10e9f))

## v0.35.0 - 2023-09-05

### [0.35.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.34.0...v0.35.0) (2023-09-05)

#### Features

- add `course_key` to block dictionary ([2895d6f](https://github.com/openedx/tutor-contrib-aspects/commit/2895d6ffcffd3c18bfc8d94168c1cfa01351ef3b))

## v0.34.0 - 2023-08-29

### [0.34.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.33.0...v0.34.0) (2023-08-29)

#### Features

- upgrade dbt-aspects to v2.2 ([e732e5b](https://github.com/openedx/tutor-contrib-aspects/commit/e732e5b7c0ee7cbf2e69759f486ab505280074d9))
- upgrade superset to 2.1.0 ([8fd4396](https://github.com/openedx/tutor-contrib-aspects/commit/8fd439637eca7a82359e8fd5391b0ddc6515a13a))

#### Bug Fixes

- add missing permission for activity log ([4dfa26a](https://github.com/openedx/tutor-contrib-aspects/commit/4dfa26a420d8774bc189864a925b5e240b60a97b))
- add name for superset RLSF ([8ff5a5d](https://github.com/openedx/tutor-contrib-aspects/commit/8ff5a5d224e4f30a822d68c773efd3745bea8d37))

## v0.33.0 - 2023-08-29

### [0.33.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.32.0...v0.33.0) (2023-08-29)

#### Features

- feat: include language code in translated asset name (FC-0033) ([f5b8c51](https://github.com/openedx/tutor-contrib-aspects/commit/f5b8c519483ef111dafef4e39c5e3d760997e7fd))

## v0.32.0 - 2023-08-29

### [0.32.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.31.3...v0.32.0) (2023-08-29)

#### Features

- upgrade event-routing-backends to 5.6.0 ([bb344cb](https://github.com/openedx/tutor-contrib-aspects/commit/bb344cb88455b2bd56b6c0c0d96c486afba6238b))

## v0.31.3 - 2023-08-29

### [0.31.3](https://github.com/openedx/tutor-contrib-aspects/compare/v0.31.2...v0.31.3) (2023-08-29)

### Bug Fixes

- remove unused dbt overrides ([e7cf50e](https://github.com/openedx/tutor-contrib-aspects/commit/e7cf50e1fa88897aa442a81554f524bf9c96876b))

## v0.31.2 - 2023-08-28

### [0.31.2](https://github.com/openedx/tutor-contrib-aspects/compare/v0.31.1...v0.31.2) (2023-08-28)

### Bug Fixes

- add option to deduplicate tables after backfill ([26f6cf2](https://github.com/openedx/tutor-contrib-aspects/commit/26f6cf2fd1936caa4b25956ce0baef8d8ff4ba43))
- print packages and project dbt correctly ([4490848](https://github.com/openedx/tutor-contrib-aspects/commit/44908482d6f5e8696d3ef2fd86e75836a06a2237))
- print packages and project dbt correctly ([84d0a72](https://github.com/openedx/tutor-contrib-aspects/commit/84d0a72ba072b89ff8c1193962391a659cf615e3))

## v0.31.1 - 2023-08-25

### [0.31.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.31.0...v0.31.1) (2023-08-25)

### Bug Fixes

- add cache wrapper for can_view_courses filter ([a3cda98](https://github.com/openedx/tutor-contrib-aspects/commit/a3cda989ef1d0ae5b02383892ddcd98abbfd62b0))

## v0.31.0 - 2023-08-25

### [0.31.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.30.0...v0.31.0) (2023-08-25)

#### Features

- add RLS filters for dbt models ([f63fd4f](https://github.com/openedx/tutor-contrib-aspects/commit/f63fd4f06c745e74a362574528a59a0524e095c6))
- add RLS filters for event_sink tables ([5f27772](https://github.com/openedx/tutor-contrib-aspects/commit/5f277721e7a42a5d770362fcbedae5b149a56bf6))

## v0.30.0 - 2023-08-25

### [0.30.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.29.0...v0.30.0) (2023-08-25)

#### Features

- defining student rol ([e678c51](https://github.com/openedx/tutor-contrib-aspects/commit/e678c51a649c7f06bfc4b225491935272b8d225d))

## v0.29.0 - 2023-08-24

### [0.29.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.28.1...v0.29.0) (2023-08-24)

#### Features

- ensure course_key is in each dataset ([01f7d28](https://github.com/openedx/tutor-contrib-aspects/commit/01f7d2887ba80eaa9d4820748a8733abd472d9b7))

#### Bug Fixes

- filter out unsuccessful responses in chart ([4ea1824](https://github.com/openedx/tutor-contrib-aspects/commit/4ea1824b21c68aa5cc4d34d9f6d5985c0f718f08))

#### Code Refactoring

- rewrite query to avoid memory limits ([87ce848](https://github.com/openedx/tutor-contrib-aspects/commit/87ce848271a8d27865ed7aebaa36b2c719145585))
- use `course_run` instead of `run_name` ([66e493a](https://github.com/openedx/tutor-contrib-aspects/commit/66e493af956c7e0dad0eb04fb09ab9117cf7f0ea))
- use course_key index in dashboard queries ([4516386](https://github.com/openedx/tutor-contrib-aspects/commit/4516386c90f583e6944b6ef8dae08dfa80528aca))

## v0.28.1 - 2023-08-21

### [0.28.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.28.0...v0.28.1) (2023-08-21)

### Bug Fixes

- Changes needed to run in CH Cloud ([8648fa0](https://github.com/openedx/tutor-contrib-aspects/commit/8648fa0d44543b3cf64f5396f1e06b19e520da49))

## v0.28.0 - 2023-08-17

### [0.28.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.27.0...v0.28.0) (2023-08-17)

#### Features

- create component-specific tabs ([f42e24d](https://github.com/openedx/tutor-contrib-aspects/commit/f42e24d595ec3b4b98adcd7ac3eb465451c40879))

#### Tests

- load images built in kind ([ae4d4e7](https://github.com/openedx/tutor-contrib-aspects/commit/ae4d4e7efacf2cade57dece732dd2a40018b679e))

## v0.27.0 - 2023-08-16

### [0.27.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.26.1...v0.27.0) (2023-08-16)

#### Features

- add fields to event_sink.course_names ([9ee5fe5](https://github.com/openedx/tutor-contrib-aspects/commit/9ee5fe54fc27b32e1625808588d4c17dfcc7354f))

#### Bug Fixes

- use drop and create for increased stability ([6ccdaf4](https://github.com/openedx/tutor-contrib-aspects/commit/6ccdaf4f08a8b7ed373be4dc7f33a35ceb121a22))

#### Code Refactoring

- templatize db name in migration ([82828a6](https://github.com/openedx/tutor-contrib-aspects/commit/82828a634ae733642f3e0328af29cd7e0c324b5f))

## v0.26.1 - 2023-08-16

### [0.26.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.26.0...v0.26.1) (2023-08-16)

### Bug Fixes

- Environment variable contain whitespace issue ([9d20dd1](https://github.com/openedx/tutor-contrib-aspects/commit/9d20dd12211363495d39103eab6599a2352e00a6))
- Update env ([882db11](https://github.com/openedx/tutor-contrib-aspects/commit/882db116ad0e061776a61f21f19754b81e027a6a))

## v0.26.0 - 2023-08-15

### [0.26.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.25.1...v0.26.0) (2023-08-15)

#### Features

- Update Operator Dashboard ([3659f90](https://github.com/openedx/tutor-contrib-aspects/commit/3659f904768e9233c4ed95f9a676dff486f3270d))

#### Bug Fixes

- Re-add roles to dashboards, update docs, update import script to force roles ([bcab2a0](https://github.com/openedx/tutor-contrib-aspects/commit/bcab2a01a40094f77ae9bd41a5ed3e57765c3561))
- Remove unnecessary date filter from unique actors chart ([598b794](https://github.com/openedx/tutor-contrib-aspects/commit/598b794332221b35055d1a36a4d9309ac0c35b00))

#### Documentation

- Update asset contribution readme section ([12fb7bf](https://github.com/openedx/tutor-contrib-aspects/commit/12fb7bfead8fec3c1772248fd6ab107789bddafe))

#### Build Systems

- Pin disk space cleaner, try to fix build error ([5b1fef2](https://github.com/openedx/tutor-contrib-aspects/commit/5b1fef207900332f516237657f585516bec3fbe0))

## v0.25.1 - 2023-08-14

### [0.25.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.25.0...v0.25.1) (2023-08-14)

### Bug Fixes

- Adapted transform_tracking_logs command for enhanced CLI integration. ([dfcf820](https://github.com/openedx/tutor-contrib-aspects/commit/dfcf8208ce181150575899123a51d54aa3ed7bac))
- add configurable clickhouse volume size ([e513d02](https://github.com/openedx/tutor-contrib-aspects/commit/e513d02648b314fd7ed1ced934609d2e4c0f260d))

## v0.25.0 - 2023-08-08

### [0.25.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.24.0...v0.25.0) (2023-08-08)

#### Features

- use dbt models for problem datasets ([b5e9ee5](https://github.com/openedx/tutor-contrib-aspects/commit/b5e9ee53ab9235d7e3efcc6179f8f68bd3e3c892))

#### Build Systems

- **deps:** bump stefanzweifel/changelog-updater-action ([26ff876](https://github.com/openedx/tutor-contrib-aspects/commit/26ff876e96ff8758f11a6d0797e074db4b15c365))

## v0.24.0 - 2023-08-04

### [0.24.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.23.2...v0.24.0) (2023-08-04)

#### Features

- add superset owners configurable variable ([870a9d9](https://github.com/openedx/tutor-contrib-aspects/commit/870a9d9dd03e7ef1f0715b459d7d6150342ef117))
- allow to translate markdown elements ([ceaf898](https://github.com/openedx/tutor-contrib-aspects/commit/ceaf89893f8ebe0c4e1296fdd4566d5b21808654))

## v0.23.2 - 2023-08-04

### [0.23.2](https://github.com/openedx/tutor-contrib-aspects/compare/v0.23.1...v0.23.2) (2023-08-04)

### Bug Fixes

- remove loading locale file before processing ([3401796](https://github.com/openedx/tutor-contrib-aspects/commit/3401796061b62e39f2c9cc6414b59a78565c5f80))

## v0.23.1 - 2023-08-04

### [0.23.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.23.0...v0.23.1) (2023-08-04)

### Bug Fixes

- use yaml delimiter to separate translations ([a95706d](https://github.com/openedx/tutor-contrib-aspects/commit/a95706d048f69762b03572498fd5c748020d931e))

## v0.23.0 - 2023-08-03

### [0.23.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.22.0...v0.23.0) (2023-08-03)

#### Features

- include current day in instructor dashboard ([19b7b47](https://github.com/openedx/tutor-contrib-aspects/commit/19b7b472dad2dc09c3f1900a3fc25055b92e879c)), closes [#246](https://github.com/openedx/tutor-contrib-aspects/issues/246)

#### Bug Fixes

- allow to translate dashboard headers ([12bc030](https://github.com/openedx/tutor-contrib-aspects/commit/12bc03018d1e82621562f531027e92c6ba8f313a))
- remove extra parens from org filters ([dfef41c](https://github.com/openedx/tutor-contrib-aspects/commit/dfef41cbe6020b444a4701303c7e1c2d9b55927c)), closes [#258](https://github.com/openedx/tutor-contrib-aspects/issues/258)
- upgrade event-routing-backends to 5.5.4 ([454063c](https://github.com/openedx/tutor-contrib-aspects/commit/454063c226860f7477d24020b38e27b0b811bbc8))

## v0.22.0 - 2023-08-02

### [0.22.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.21.0...v0.22.0) (2023-08-02)

#### Features

- add transifex automatic translations ([7f1d756](https://github.com/openedx/tutor-contrib-aspects/commit/7f1d756554790d251aa257d67cc97bd42e5f6289))

#### Code Refactoring

- use dbt models for video datasets ([d03c641](https://github.com/openedx/tutor-contrib-aspects/commit/d03c641bacafb2bc08aeec32c88b311b4962a56c))

## v0.21.0 - 2023-08-02

### [0.21.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.20.0...v0.21.0) (2023-08-02)

#### Features

- add filter to initial enrollments query ([d032f95](https://github.com/openedx/tutor-contrib-aspects/commit/d032f9590a60e6426578d4d33eebb82b08f035e6))
- use `fact_enrollments` dbt model ([d83ed3a](https://github.com/openedx/tutor-contrib-aspects/commit/d83ed3afe7fb29b0b67d1c673dbcf7c24d3140fb))

#### Documentation

- update virtual dataset links in README ([189f3cd](https://github.com/openedx/tutor-contrib-aspects/commit/189f3cdfdbc6daa0e172d7caa348ca8b61738781))

## v0.20.0 - 2023-08-01

### [0.20.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.19.0...v0.20.0) (2023-08-01)

#### Features

- use new dictionary-backed lookup tables ([ec89692](https://github.com/openedx/tutor-contrib-aspects/commit/ec89692d7803b40e9c293d113db1ae2828b446b1))

## v0.19.0 - 2023-08-01

### [0.19.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.18.5...v0.19.0) (2023-08-01)

#### Features

- patch for extra asset translations ([493275f](https://github.com/openedx/tutor-contrib-aspects/commit/493275f9ac8a7d3b8eee5c7319ae89b26981159c))
- support for asset translation ([7735d28](https://github.com/openedx/tutor-contrib-aspects/commit/7735d28ee5ceef7b9dd9f9bbd29d34270e1e9610))

#### Build Systems

- **deps:** bump helm/kind-action from 1.5.0 to 1.8.0 ([6036e89](https://github.com/openedx/tutor-contrib-aspects/commit/6036e8951ac7e85046f07c4d6e648a7bcddd4f02))
- k8s ci refactored to fail earlier ([abad1d9](https://github.com/openedx/tutor-contrib-aspects/commit/abad1d9c4c0e23cff3e493203d868d008d8adee1))

## v0.18.5 - 2023-07-28

### [0.18.5](https://github.com/openedx/tutor-contrib-aspects/compare/v0.18.4...v0.18.5) (2023-07-28)

### ⚠ BREAKING CHANGES

- reorder MVs and change data types

### Features

- reorder MVs and change data types ([c9cf476](https://github.com/openedx/tutor-contrib-aspects/commit/c9cf47670e91205ca354c540a5ac0ee9e7001790))

### Bug Fixes

- deduplicate video timeline events ([e575b76](https://github.com/openedx/tutor-contrib-aspects/commit/e575b76ddb4994a6b8d56ea6e8c440c604a9ce3c))
- update timestamp type in enrollment_by_day ([3a73907](https://github.com/openedx/tutor-contrib-aspects/commit/3a73907837dc64d78b6073044d1d2df14e88ed12))

### Code Refactoring

- reorder top-level materialized views ([14a21d8](https://github.com/openedx/tutor-contrib-aspects/commit/14a21d8662d90908f96a83c72b4a7cf8f2710ecf))

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
