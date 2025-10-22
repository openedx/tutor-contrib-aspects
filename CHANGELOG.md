# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v2.5.0 - 2025-10-22

### [2.5.0](https://github.com/openedx/tutor-contrib-aspects/compare/v2.4.0...v2.5.0) (2025-10-22)

#### Features

* bump dbt ([31c0887](https://github.com/openedx/tutor-contrib-aspects/commit/31c08872770ee74f584484eb7c9e7ac29e2a39de))
* Upgrade ClickHouse to 25.8 LTS ([c3b84cf](https://github.com/openedx/tutor-contrib-aspects/commit/c3b84cf1998dfb66a0ea76cbe269b84fe476fb2f))
* Use new dbt models, various cleanup ([d9d171f](https://github.com/openedx/tutor-contrib-aspects/commit/d9d171f6f7eb93788901759a5261460280c7b1ee))
* use new dbt mvs ([840cfe5](https://github.com/openedx/tutor-contrib-aspects/commit/840cfe53a6a04516e6a7a7f5821035f845f372fa))

#### Bug Fixes

* assign value of ENABLE_PROXY_FIX to value of SUPERSET_ENABLE_PROXY_FIX to support tutor config guidelines ([5d91f55](https://github.com/openedx/tutor-contrib-aspects/commit/5d91f550e33efb802d42b170979cf4d51551e5cb))
* dbt version bump ([66ff7fd](https://github.com/openedx/tutor-contrib-aspects/commit/66ff7fdbb14bfe14f48fb7f55d5f164f977fce7c))
* pin stable click version ([58cce22](https://github.com/openedx/tutor-contrib-aspects/commit/58cce22cc77d2599561e608fe61d598c16d28232))
* put back last_visited ([630896e](https://github.com/openedx/tutor-contrib-aspects/commit/630896ebdb9677c8215ad3c60aea709affc27daa))

## v2.4.0 - 2025-09-03

### [2.4.0](https://github.com/openedx/tutor-contrib-aspects/compare/v2.3.1...v2.4.0) (2025-09-03)

#### Features

* Add REDIS_USERNAME environment variable support ([ef678e3](https://github.com/openedx/tutor-contrib-aspects/commit/ef678e35137402fcc1b4b6cd71ef0042924c6ef6))
* Updates to video queries ([f72196c](https://github.com/openedx/tutor-contrib-aspects/commit/f72196c5a1c7231496406fd94775fbca4f482269))

#### Bug Fixes

* CeleryConfig supports REDIS_USERNAME and REDIS_PASSWORD in broker URLs ([7a29371](https://github.com/openedx/tutor-contrib-aspects/commit/7a29371a604629bb0bdca8fb9819ab44d529d384))
* Don't try to use PLUGIN_SLOTS on Redwood ([0dca080](https://github.com/openedx/tutor-contrib-aspects/commit/0dca080724092bfb802fc150b3463a122fb90099))
* Lower the tutor-mfe pin to >= 18 from >=19 ([5f56060](https://github.com/openedx/tutor-contrib-aspects/commit/5f5606087f189061c924f2bc5b914ab3fbfb1adf))
* open github links in new tab ([edc19da](https://github.com/openedx/tutor-contrib-aspects/commit/edc19daaa9153ec3768e904056cceab0f5cd4000))
* open github links in new tab ([6608a9c](https://github.com/openedx/tutor-contrib-aspects/commit/6608a9cffa31ed828e38bfcf62e61325ea8d5ee2))
* Propagate ASPECTS_ENABLE_STUDIO_IN_CONTEXT_METRICS to LMS/CMS ([dc00123](https://github.com/openedx/tutor-contrib-aspects/commit/dc00123a072b9cd6d610d3a9baa2714536e7a709))
* Removes legacy peer dependency flag to make the install flexible ([a85231e](https://github.com/openedx/tutor-contrib-aspects/commit/a85231eeab8ae4f9baa7b7abbce3cc3d09f7d102))
* Superset Celery issues with healthcheck and pid ([926e2cd](https://github.com/openedx/tutor-contrib-aspects/commit/926e2cd883890a26b6e1ddc0e254a826f2d9080c))
* trigger github checks ([8dbe3e8](https://github.com/openedx/tutor-contrib-aspects/commit/8dbe3e89c8447745dd58cbbcd7aac2cb1d340cc3))
* Update platform-plugin-aspects to 1.1.1 ([e69753c](https://github.com/openedx/tutor-contrib-aspects/commit/e69753c367504c5882aff7c43353f8c298060590))
* Updates the link in the readme ([e736032](https://github.com/openedx/tutor-contrib-aspects/commit/e7360327489af194c0da330d276ece4b9c6aba4f))

#### Code Refactoring

* Simplify CeleryConfig class definition ([889af28](https://github.com/openedx/tutor-contrib-aspects/commit/889af28236cb4e027125ad2e418cd217ce046ef0))

#### Styles

* Format files ([9f669fa](https://github.com/openedx/tutor-contrib-aspects/commit/9f669fa4f0cf97bd4ef1bd66a263f9c1f2c2261d))

#### Documentation

* in-context metrics in key features ([b415607](https://github.com/openedx/tutor-contrib-aspects/commit/b415607f74d2a7458a4dbb5a393ea0a361ee5c45))
* in-context metrics installation instructions ([552347d](https://github.com/openedx/tutor-contrib-aspects/commit/552347d8cce17ca894141510ef106ee334f352e0))
* Update README to clarify compatibility ([777038b](https://github.com/openedx/tutor-contrib-aspects/commit/777038bd0666dd82ae950f5aa1208403d13ff557))

## v2.3.1 - 2025-05-16

### [2.3.1](https://github.com/openedx/tutor-contrib-aspects/compare/v2.3.0...v2.3.1) (2025-05-16)

### Bug Fixes

* lint ([40aaae8](https://github.com/openedx/tutor-contrib-aspects/commit/40aaae80fa2310d134b76a67a7d2e9e32cc597c9))
* uprgade dbt ([75b3208](https://github.com/openedx/tutor-contrib-aspects/commit/75b32088e06d3898b1681924a206de55754ab3ab))
* use name and location on xaxis, new dbt models ([9d1adae](https://github.com/openedx/tutor-contrib-aspects/commit/9d1adaea06357f3d3dc327c27b90eb1eba21b4a4))

## v2.3.0 - 2025-05-07

### [2.3.0](https://github.com/openedx/tutor-contrib-aspects/compare/v2.2.1...v2.3.0) (2025-05-07)

#### Features

* Upgrade ClickHouse to 25.3 ([6bf38d2](https://github.com/openedx/tutor-contrib-aspects/commit/6bf38d20ac03117cb8b8d259a5c51f7b16c09a18))

#### Bug Fixes

* bump dbt ([bb333e7](https://github.com/openedx/tutor-contrib-aspects/commit/bb333e7a62bd9a3a97a397b68415c83cb3fcc861))
* formatting ([204e8fe](https://github.com/openedx/tutor-contrib-aspects/commit/204e8fe176c1656e688f9d92d1b4843ad2863bb8))
* restart clickhouse and ralph automatically ([839bbba](https://github.com/openedx/tutor-contrib-aspects/commit/839bbba9dca6266e800c47f8a68b214b5c80503e))
* use end of block id ([74e1c5a](https://github.com/openedx/tutor-contrib-aspects/commit/74e1c5a9d1575dc37fad57ff739f3016324d520c))

## v2.2.1 - 2025-04-25

### [2.2.1](https://github.com/openedx/tutor-contrib-aspects/compare/v2.2.0...v2.2.1) (2025-04-25)

### Bug Fixes

* updates ([3c3f250](https://github.com/openedx/tutor-contrib-aspects/commit/3c3f2504c67955f9b758cf22def6c6d9962ac7c5))
* use problem instead of subsection ([22385be](https://github.com/openedx/tutor-contrib-aspects/commit/22385be6c6ba37ec2bd40d17ae4c05c6bfc053a3))

## v2.2.0 - 2025-04-24

### [2.2.0](https://github.com/openedx/tutor-contrib-aspects/compare/v2.1.0...v2.2.0) (2025-04-24)

#### Features

* add mfe plugin config for authoring metrics ([e22b34a](https://github.com/openedx/tutor-contrib-aspects/commit/e22b34ad0e7060af0c1d662f5009ba848318fc00))
* in-context analytics dashboards ([d95e6ab](https://github.com/openedx/tutor-contrib-aspects/commit/d95e6abcb9718bc5889e13fadaa31452317b84d9))
* In-Context metrics dashboard ([f95c351](https://github.com/openedx/tutor-contrib-aspects/commit/f95c351fde35d85f6de3cc5a046f90b68bcba01f))
* remove padding in embedded dashboards ([bd48763](https://github.com/openedx/tutor-contrib-aspects/commit/bd487639d14b153b1d44b0e7852b1433d82d509e))

## v2.1.0 - 2025-04-09

### [2.1.0](https://github.com/openedx/tutor-contrib-aspects/compare/v2.0.0...v2.1.0) (2025-04-09)

#### Features

* add custom color scheme for data charts ([8cbe697](https://github.com/openedx/tutor-contrib-aspects/commit/8cbe6971d7955d94bcba83efb268a769d8835e80))

## v2.0.0 - 2025-03-24

### [2.0.0](https://github.com/openedx/tutor-contrib-aspects/compare/v1.3.2...v2.0.0) (2025-03-24)

#### ⚠ BREAKING CHANGES

* Remove python < 3.11 references and Tutor < 18
* use new dbt models and rename datasets to adhere to dim/fact convention

#### Features

* add course name and org ([d3c40f6](https://github.com/openedx/tutor-contrib-aspects/commit/d3c40f6f2009cf11b8e25e6c28a2651e82667526))
* add course name to run charts ([491569a](https://github.com/openedx/tutor-contrib-aspects/commit/491569a91cf94d07c4aecbc1b3d4bcd0532b8f1d))
* enable tagging of charts and dashboards ([28817e4](https://github.com/openedx/tutor-contrib-aspects/commit/28817e4ddecdff8e2d231bfd275d4f0df3c96fbb))
* set the session locale from the Open edX preferred language ([#1017](https://github.com/openedx/tutor-contrib-aspects/issues/1017)) ([df9518c](https://github.com/openedx/tutor-contrib-aspects/commit/df9518c63299cf76c6c2db36c1c2378f8e506bb6))
* upgrade to superset v4.1.0 ([0286448](https://github.com/openedx/tutor-contrib-aspects/commit/0286448470367f238e974b3458424d635b90c821))
* upgrade to superset v4.1.1 ([e5a7d53](https://github.com/openedx/tutor-contrib-aspects/commit/e5a7d53f0760c09b373949116a747daf4915643a))
* use new dbt models and rename datasets to adhere to dim/fact convention ([fc48835](https://github.com/openedx/tutor-contrib-aspects/commit/fc48835e3f5ed8fbe482421691669cb392c4f1bb))

#### Bug Fixes

* correctly mount pythonpath module ([807646d](https://github.com/openedx/tutor-contrib-aspects/commit/807646d17ea0de41425d9c8a6990ece0c6d337a5))
* force major version bump ([2798101](https://github.com/openedx/tutor-contrib-aspects/commit/2798101afc4e196d71968900a1acdaad63bebef2))
* format ([7295cc2](https://github.com/openedx/tutor-contrib-aspects/commit/7295cc2874e34a9b432cd859577904c59bc47794))
* formatting ([e2dcd2b](https://github.com/openedx/tutor-contrib-aspects/commit/e2dcd2ba4fc6b2f3b509456517629acc6d67529c))
* load template processor for lineage data ([d48f89e](https://github.com/openedx/tutor-contrib-aspects/commit/d48f89ee45fcd6949f87329f92912de3e9d65865))
* manually install mysql client ([9f090b0](https://github.com/openedx/tutor-contrib-aspects/commit/9f090b01b54a33025609e554a5976f7fbeada2d7))
* new dbt version ([d069756](https://github.com/openedx/tutor-contrib-aspects/commit/d0697560243b5630edae5cffc7320b953b08205f))
* reset xapi ([d299a23](https://github.com/openedx/tutor-contrib-aspects/commit/d299a23e570b6a0a6f37c354e11d03896ae6a120))
* update sqlfmt version ([5839eac](https://github.com/openedx/tutor-contrib-aspects/commit/5839eacff353120295609a89aba3bfe85234cbd1))
* upgrade dbt ([2b2557f](https://github.com/openedx/tutor-contrib-aspects/commit/2b2557f560b7be4562054b3073fdf050463987bd))
* upgrade requirements ([35312f6](https://github.com/openedx/tutor-contrib-aspects/commit/35312f64e42ab9620b56a24ff34eb33804205de8))
* use pip to install ([c721dc1](https://github.com/openedx/tutor-contrib-aspects/commit/c721dc10217efdd0502aba35237076f98b795bcb))

#### Documentation

* Add note about version change ([4592526](https://github.com/openedx/tutor-contrib-aspects/commit/4592526855b4e723b77d2f5a2f5d246beca3c4c6))

#### chore

* Remove python < 3.11 references and Tutor < 18 ([4bad282](https://github.com/openedx/tutor-contrib-aspects/commit/4bad28282483d7fcfc2c479dfaaec51b012ce5ca))

## v1.3.0 - 2024-11-26

### [1.3.0](https://github.com/openedx/tutor-contrib-aspects/compare/v1.2.0...v1.3.0) (2024-11-26)

#### Features

* add autoscaling values for ralph and superset ([ac1a9be](https://github.com/openedx/tutor-contrib-aspects/commit/ac1a9bea7ea8d18f91a7494290626ec08bc97d26))
* add bind and compose mount settings for superset ([c9d0c9e](https://github.com/openedx/tutor-contrib-aspects/commit/c9d0c9e91fc5bd8090d4d3cd63e323250c57d2e9))
* allow to block instructor access ([b90e22b](https://github.com/openedx/tutor-contrib-aspects/commit/b90e22baa6beaecfdffbdacdc6d53c14f0c150ca))
* update dbt and use new param view ([4f466ea](https://github.com/openedx/tutor-contrib-aspects/commit/4f466ea699643fd9dae5d97f3df5dfc51dac2970))

#### Bug Fixes

* add configurable help tab for at-risk and comparison dashboard ([205acd9](https://github.com/openedx/tutor-contrib-aspects/commit/205acd9566714232e971643ab4b56b4a2b8761ed))
* add username to user_profile ([7e6e607](https://github.com/openedx/tutor-contrib-aspects/commit/7e6e607d8d457736d9801f484879b3a2a505a996))
* add username to user_profile serializer ([ed71f06](https://github.com/openedx/tutor-contrib-aspects/commit/ed71f0615c6e26903d575aac96474c7c671359c7))
* dbt version ([8fd7fee](https://github.com/openedx/tutor-contrib-aspects/commit/8fd7feeaac18dbb58d7b4010834d89fb3c3cc07a))
* dbt version ([5a84ec7](https://github.com/openedx/tutor-contrib-aspects/commit/5a84ec726664dc009a90cd5033cf77c1d860643f))
* formatting ([8a1e2f6](https://github.com/openedx/tutor-contrib-aspects/commit/8a1e2f627fb8a4d17a5762a83b7c75a0805fb3f0))
* parse external_id to string instead of actor_id to uuid ([6b792d1](https://github.com/openedx/tutor-contrib-aspects/commit/6b792d16e646461a1c83863dfd090d6c27ec173b))
* parse external_id to string instead of actor_id to uuid ([bdf4058](https://github.com/openedx/tutor-contrib-aspects/commit/bdf4058c49fd3427b1a6adfd517258a009777c38))
* video engagement updates ([7839b65](https://github.com/openedx/tutor-contrib-aspects/commit/7839b65a44e5198b7ca9ce8e4c72cc95c1be44b1))

## v1.2.0 - 2024-10-23

### [1.2.0](https://github.com/openedx/tutor-contrib-aspects/compare/v1.1.0...v1.2.0) (2024-10-23)

#### Features

* add course dashboard link to course info chart ([7fcb1d5](https://github.com/openedx/tutor-contrib-aspects/commit/7fcb1d548bc6e67cbfa6edd4e1ef7f2c635a414d))
* add jinja filter to render a link to a dashboard ([a2f0c44](https://github.com/openedx/tutor-contrib-aspects/commit/a2f0c4466e1f9c762ff0587c9aa1bf0663cb8311))
* add tag related tables ([fd333c5](https://github.com/openedx/tutor-contrib-aspects/commit/fd333c55fe0b91a08eb53040633446671f2c6a75))
* Delete unused assets owned by Aspects on imports ([97b4e11](https://github.com/openedx/tutor-contrib-aspects/commit/97b4e118823b1e56d5532bd3a9a930fd76e36eba))
* fix enrollment count, fix tag filter, misc updates ([b914ac2](https://github.com/openedx/tutor-contrib-aspects/commit/b914ac28519e44446d414ea568f4e96ef1bcb066))
* import dasboard changes for UI de-clutter ([f331026](https://github.com/openedx/tutor-contrib-aspects/commit/f3310262429ed14cf75256883124a8fbc5d02cf7))
* new course comparison dashboard ([0466fdb](https://github.com/openedx/tutor-contrib-aspects/commit/0466fdb34d117a05d5fee53f09d1a87e607acf46))
* Upgrade ClickHouse to 24.8 ([4afdbc8](https://github.com/openedx/tutor-contrib-aspects/commit/4afdbc83b874281ddc09d739e37cdb9c82d0c2cb))
* upgrade dbt to v3.11.0 ([3e8c2a8](https://github.com/openedx/tutor-contrib-aspects/commit/3e8c2a8e9b08118fbb2fde50acf2d983305ecdf9))
* upgrade platform-plugin-aspects to v0.11.0 ([90679f1](https://github.com/openedx/tutor-contrib-aspects/commit/90679f1495bb85165a0455b97e3a2e3362650e37))
* **assets:** format sql templates fore import ([98f7544](https://github.com/openedx/tutor-contrib-aspects/commit/98f75440d41aa0c7d5abfc826a2a3a4136a57849))
* **load:** bump xapi-db-load to v1.4 ([1bc3bf9](https://github.com/openedx/tutor-contrib-aspects/commit/1bc3bf95b10013f83c13d6ebae413b151164a314))
* **metrics:** add organization filter option ([f5a7533](https://github.com/openedx/tutor-contrib-aspects/commit/f5a7533e7fdaefa7ee5ddad51205a55a0a27320b))
* **metrics:** sort metrics by clickhouse query time ([2777db2](https://github.com/openedx/tutor-contrib-aspects/commit/2777db22fb1cba9a0bdd9f4fba82c62f74c65016))

#### Bug Fixes

* add missing query context for last_visit dataset ([a3da2d5](https://github.com/openedx/tutor-contrib-aspects/commit/a3da2d555a1c22c36abeee52f2f4a6cc468453a4))
* add sqlfmt as a base dependency ([f22849a](https://github.com/openedx/tutor-contrib-aspects/commit/f22849a528cc3ac8f0700e860f1afd5a92719b24))
* add sqlfmt as a base dependency ([3728514](https://github.com/openedx/tutor-contrib-aspects/commit/3728514d8bd80947f9f0ac3e74d2f6b36a485d23))
* add video_link to fact_video_watches dataset ([3032313](https://github.com/openedx/tutor-contrib-aspects/commit/3032313c82048d90f8a8b57f36c965f12ee1a53e))
* clone dbt repo if branch or repo has changed ([34e7077](https://github.com/openedx/tutor-contrib-aspects/commit/34e70779925a69fe31a89f96dcafc3b0370bae5d))
* disable check_table_dependencies clickhouse setting for dbt ([d071f96](https://github.com/openedx/tutor-contrib-aspects/commit/d071f96c87fd4f52f0bd0ecc2b5ffb1473d2c7aa))
* drop dependent dictionaries before dropping tables ([1f64b89](https://github.com/openedx/tutor-contrib-aspects/commit/1f64b89144030b8e0697b1e1ac80b3c60dfacd63))
* enable course_enrollment sink ([7100cdc](https://github.com/openedx/tutor-contrib-aspects/commit/7100cdc79cbe3cf23e5d68c3fce48bc56cd60516))
* get query context ([534583c](https://github.com/openedx/tutor-contrib-aspects/commit/534583cade79cc38b884e0b73409154938435434))
* open chart descriptions ([7265658](https://github.com/openedx/tutor-contrib-aspects/commit/72656583c9417fe25e36a9ea1c404541717c0207))
* remove trailing whitespace for include statements ([b171222](https://github.com/openedx/tutor-contrib-aspects/commit/b171222e28640f6e779148aa18c48c54e55eb852))
* remove trailing whitespace for include statements ([6fea9a1](https://github.com/openedx/tutor-contrib-aspects/commit/6fea9a1060b15fd844e907cf34a10c781e674391))
* split datasets and their sql ([36dca8b](https://github.com/openedx/tutor-contrib-aspects/commit/36dca8b553c0e272f888d7311b8ed80aaec413ed))
* update database ([1091f8c](https://github.com/openedx/tutor-contrib-aspects/commit/1091f8cc47d00a6282a2426662a6ef9695e17af9))
* updates ([09dc281](https://github.com/openedx/tutor-contrib-aspects/commit/09dc28116bd40f55e17ff90ae6c4c87cbc4aa045))
* upgrade platform-plugin-aspects to v0.11.1 ([a45b981](https://github.com/openedx/tutor-contrib-aspects/commit/a45b981e1c4af6c12941c0704c1e8a7cf3c5eb2d))
* upgrade superset ([ab59aad](https://github.com/openedx/tutor-contrib-aspects/commit/ab59aad4bab7fa5863862517669edc58011c8cee))
* upgrade superset and change legend location ([7867629](https://github.com/openedx/tutor-contrib-aspects/commit/7867629fad5341b8cd9efb5476cdcba515e335ce))
* **assets:** make filters work again ([c2e03c7](https://github.com/openedx/tutor-contrib-aspects/commit/c2e03c736a61c329d86bdfe5a51557682746b9ce))
* **assets:** move enrolles before tags ([973af96](https://github.com/openedx/tutor-contrib-aspects/commit/973af9602827ee71d94d977ff3bb2d1e2e121d53))
* **assets:** update description of learner performance charts ([29b5126](https://github.com/openedx/tutor-contrib-aspects/commit/29b5126afc4e645a02508a24088fa7b5c05d97cf))
* **assets:** update description of number of views chart ([47a685b](https://github.com/openedx/tutor-contrib-aspects/commit/47a685bbd9742ae58613778faae3c94e4ce785ac))
* **assets:** update description of number of views chart ([0304804](https://github.com/openedx/tutor-contrib-aspects/commit/0304804dd0a9501de667299deedfb723c1840628))
* **assets:** update metadata for dataset fact_watched_video_segments ([ad50b30](https://github.com/openedx/tutor-contrib-aspects/commit/ad50b30ba078be96d5899bd5aadcfc2527811979))
* **assets:** use dataset uuid instead of dataset id ([a7e2d61](https://github.com/openedx/tutor-contrib-aspects/commit/a7e2d6124bfd83ec4b3ca0e948b9e72813e3cac5))
* **dev:** sql parse dataset SQL statement ([52fee94](https://github.com/openedx/tutor-contrib-aspects/commit/52fee9424b99121388593a84f45b9210014723b2))
* use filter id ([7671ecd](https://github.com/openedx/tutor-contrib-aspects/commit/7671ecdab4fa567eaf2f72aceec71e333dc0be61))
* **embedded:** remove course-comparison dashboard from embeddable dashboards ([2866b3e](https://github.com/openedx/tutor-contrib-aspects/commit/2866b3e5e6bd2c171a801b3f108da177446d679b))
* **metrics:** restore extra filter per query ([4cb45ad](https://github.com/openedx/tutor-contrib-aspects/commit/4cb45adf3f3a623c6e6ff20d3f2f3f800ff6dccd))
* **metrics:** set global form data to allow prewhere filters ([a428882](https://github.com/openedx/tutor-contrib-aspects/commit/a42888262cc121e9fb55eab3d147163a15d042d6))
* **metrics:** use course name filter ([c71a90e](https://github.com/openedx/tutor-contrib-aspects/commit/c71a90e390b92c6c57ce63f0f59c2fdf53ff09ec))
* **sql:** add object_id to watched video segments ([3827252](https://github.com/openedx/tutor-contrib-aspects/commit/3827252edbcaf88c915907bab39178d28f35873f))
* **sql:** add where 1=1 for int_problem_results ([715c55f](https://github.com/openedx/tutor-contrib-aspects/commit/715c55ff3cfa5e4f021e35da15009302364e4689))
* **sql:** coursewide attempts grouped by problem_id ([fb6231c](https://github.com/openedx/tutor-contrib-aspects/commit/fb6231cbe5a189f77521633b7d74b4573443f899))
* **sql:** join at risk dataset with problem_coursewide_avg ([d0a1ea8](https://github.com/openedx/tutor-contrib-aspects/commit/d0a1ea8661e2df21013fb7bba77152586d9d7932))
* **sql:** remove duplicated comma ([f1f2f65](https://github.com/openedx/tutor-contrib-aspects/commit/f1f2f65bdf3a6f3127aab33d8d5c82456ccb6636))
* **sql:** use 0 instead of null ([7fd5c15](https://github.com/openedx/tutor-contrib-aspects/commit/7fd5c15cb6a703bc9858843aa3e991feff8e8310))
* add instructor role to operators too ([#970](https://github.com/openedx/tutor-contrib-aspects/issues/970)) ([3ffdbb9](https://github.com/openedx/tutor-contrib-aspects/commit/3ffdbb9d067adbc7f7776f48fcc7fa069c87c649))
* at risk ([563327b](https://github.com/openedx/tutor-contrib-aspects/commit/563327b44b4ff5aa8fe044a6b66bf53625b90b88))
* Bump platform-plugin-aspects to v0.11.3 ([97eda17](https://github.com/openedx/tutor-contrib-aspects/commit/97eda17e4bbd7af15b0b31a8cc6b9e7be25f1b2f))
* cleanup ([ab20125](https://github.com/openedx/tutor-contrib-aspects/commit/ab201253e66cdda1875eaf9235435bfc48d055c5))
* course ([9a84d66](https://github.com/openedx/tutor-contrib-aspects/commit/9a84d66994b81562ce5838e1e52dba27f3b28972))
* course compare ([a56258d](https://github.com/openedx/tutor-contrib-aspects/commit/a56258dceade6038a2dfd1491e5fffb684979ce0))
* format ([129c165](https://github.com/openedx/tutor-contrib-aspects/commit/129c1656a4d922d62014b8b333b0eb8a19816547))
* individual learner ([f5e17d1](https://github.com/openedx/tutor-contrib-aspects/commit/f5e17d10ef7938525f5a99c2abca1db06cedfa04))
* merge conflicts ([75d749b](https://github.com/openedx/tutor-contrib-aspects/commit/75d749bcb046675709a73fa0539e8f871ace6ca7))
* merge main ([fe08281](https://github.com/openedx/tutor-contrib-aspects/commit/fe0828107be871ea7a18b3e6ebb6ce05fa56cc43))
* pass translated uuids directly to method ([ca60ad7](https://github.com/openedx/tutor-contrib-aspects/commit/ca60ad79a4af824a4a323417f9c8dfabd6c0fcd6))
* point aspects docs to the right service ([18cd2f8](https://github.com/openedx/tutor-contrib-aspects/commit/18cd2f8deed7c6356909d2280b6a276d6244dbf8))
* pr comments ([fce4fe3](https://github.com/openedx/tutor-contrib-aspects/commit/fce4fe3d4ff7d3c9c4928de2986b433f02a89dfe))
* pr comments ([4351953](https://github.com/openedx/tutor-contrib-aspects/commit/4351953b3f749bcbe7f561c94216d3cc46a04817))
* real list of unused charts ([1412de7](https://github.com/openedx/tutor-contrib-aspects/commit/1412de70e6be5a2eb3ffc19884773aea4ecb97d7))
* reformat ([c3b8639](https://github.com/openedx/tutor-contrib-aspects/commit/c3b86397be9800979cd8d18a714cfd29a0bdc68e))
* reformat ([3e7a872](https://github.com/openedx/tutor-contrib-aspects/commit/3e7a872d3d2baa0ca8d787d23695d15260ac31e4))
* remove pagination ([117fe68](https://github.com/openedx/tutor-contrib-aspects/commit/117fe68b41734be74113a70cfddf6edf94ea0b80))
* reset assets ([7992108](https://github.com/openedx/tutor-contrib-aspects/commit/799210806efec041609c40fea1cfb5775d7d56b5))
* reset assets ([16185fb](https://github.com/openedx/tutor-contrib-aspects/commit/16185fb61561887492a671df479da9119262d9a4))
* supress formatting logs ([ecdd0da](https://github.com/openedx/tutor-contrib-aspects/commit/ecdd0da95680d21a4be1d192e5b7ad0f76fc645d))
* update readme ([fff47c1](https://github.com/openedx/tutor-contrib-aspects/commit/fff47c1635b2315748b7c0fdf02e35de36a7d762))
* update video count chart ([7b21854](https://github.com/openedx/tutor-contrib-aspects/commit/7b218543d63ab95e407e45c8abb837312330a132))
* update y axis type and video count ([a651f45](https://github.com/openedx/tutor-contrib-aspects/commit/a651f4563a56c5ad4ff55427907f500aef22232a))
* updates ([a5dd979](https://github.com/openedx/tutor-contrib-aspects/commit/a5dd979b013de0de5b956c0a1e931bae0b6e4c0c))
* updates ([1990460](https://github.com/openedx/tutor-contrib-aspects/commit/199046064cc13c734487943c63484505aa8e1062))
* video count ([f6497d1](https://github.com/openedx/tutor-contrib-aspects/commit/f6497d1d793d2f90f2e64a1c86c1858df102c235))
* video watch fix ([69f386e](https://github.com/openedx/tutor-contrib-aspects/commit/69f386e899fd14e0f022d221ea5dbfd04facc88e))

#### Performance Improvements

* improve init lms tasks time by using settings instead of waffle flags ([69b4bea](https://github.com/openedx/tutor-contrib-aspects/commit/69b4bea486113ce02c52c64d3fe6791671dfcbac))
* **sql:** bring int_problem_resuts from dbt to superset ([d718052](https://github.com/openedx/tutor-contrib-aspects/commit/d7180521a35b8a61e55d347ca9a3d83c9ddb7a07))
* **sql:** use last_course_visit mv for learner summary query ([68c4d12](https://github.com/openedx/tutor-contrib-aspects/commit/68c4d12e2529baaf544889b8bc1be7d8413f1ca1))
* **sql:** use org and course_key filters to use primary key indexes ([4e531d4](https://github.com/openedx/tutor-contrib-aspects/commit/4e531d482df45a440dfc51a5ef2b8456649e0b86))

#### Tests

* install dev requirements for CI ([6409f39](https://github.com/openedx/tutor-contrib-aspects/commit/6409f3949475493087b38c580ffa6b108ae18ae9))

#### Documentation

* correct the transform-tracking-logs do command name ([5ce0633](https://github.com/openedx/tutor-contrib-aspects/commit/5ce063339ae9dfbb76b39b373c9a3015afd36830))

#### Styles

* Remove unused import ([94695eb](https://github.com/openedx/tutor-contrib-aspects/commit/94695ebe34ae278ccef68912cab70eca3fbc2b82))

#### Build Systems

* Move translations pull to Docker build time ([fd6cc2c](https://github.com/openedx/tutor-contrib-aspects/commit/fd6cc2c2b512d59af410274e687ae2209a5115bc))
* Remove pull translations action and make target ([0b0dad1](https://github.com/openedx/tutor-contrib-aspects/commit/0b0dad135f7d7cfe4dd9adcf17db381b108879d9))
* **deps:** bump cryptography from 43.0.0 to 43.0.1 in /requirements ([b5789d5](https://github.com/openedx/tutor-contrib-aspects/commit/b5789d508747828e745f560acf3d7fc52e61dff5))
* **deps:** bump peter-evans/create-pull-request from 6 to 7 ([6629e96](https://github.com/openedx/tutor-contrib-aspects/commit/6629e962ba44205623e5d5331068a1260506eade))

## v1.1.0 - 2024-08-20

### [1.1.0](https://github.com/openedx/tutor-contrib-aspects/compare/v1.0.3...v1.1.0) (2024-08-20)

#### Features

* add course enrollment sink table ([2dbe789](https://github.com/openedx/tutor-contrib-aspects/commit/2dbe789c93eaa043f31e322c1679c118384ae408))
* allow to host dbt docs on cluster ([#892](https://github.com/openedx/tutor-contrib-aspects/issues/892)) ([87f8100](https://github.com/openedx/tutor-contrib-aspects/commit/87f81000310450e1e855b3b998249b721cdd0738))

#### Bug Fixes

* fix hardcoded db names ([5c8cd2f](https://github.com/openedx/tutor-contrib-aspects/commit/5c8cd2fc6bde58153fc68f443f5015ebd390494e))
* flask debug replaced flask env ([#896](https://github.com/openedx/tutor-contrib-aspects/issues/896)) ([115ed05](https://github.com/openedx/tutor-contrib-aspects/commit/115ed05e4faf34d19a2059e87f2f8c79f33564e4))
* master branch sunset ([#900](https://github.com/openedx/tutor-contrib-aspects/issues/900)) ([16c9b0f](https://github.com/openedx/tutor-contrib-aspects/commit/16c9b0fe6de5e5855487b93afb2a1eaab9d5cd0b))
* Upgrade aspects_dbt to v3.30.0 ([#919](https://github.com/openedx/tutor-contrib-aspects/issues/919)) ([b9727df](https://github.com/openedx/tutor-contrib-aspects/commit/b9727df1882895f9b59a8c56063c60d2567be0e7))
* Upgrade aspects-dbt to 3.29.1 ([#898](https://github.com/openedx/tutor-contrib-aspects/issues/898)) ([03395f6](https://github.com/openedx/tutor-contrib-aspects/commit/03395f6ab8bc319ee2405267e1fb5f4d7f7d6563))

#### Code Refactoring

* Upgrade aspects-dbt for performance changes ([#907](https://github.com/openedx/tutor-contrib-aspects/issues/907)) ([1da3d9d](https://github.com/openedx/tutor-contrib-aspects/commit/1da3d9d875307d2671bb7bf0677d86e032b34b16))

#### Documentation

* Update readme to include the Superset image ([#904](https://github.com/openedx/tutor-contrib-aspects/issues/904)) ([8d4e542](https://github.com/openedx/tutor-contrib-aspects/commit/8d4e5424bd11633c218e7a7ac498959d806e0c55))

#### Build Systems

* Updating workflow `add-remove-label-on-comment.yml`. ([#899](https://github.com/openedx/tutor-contrib-aspects/issues/899)) ([84d9f03](https://github.com/openedx/tutor-contrib-aspects/commit/84d9f03c8b33308f96ef574509ef86862b232c7d))
* **deps:** bump docker/login-action from 3.2.0 to 3.3.0 ([#903](https://github.com/openedx/tutor-contrib-aspects/issues/903)) ([895f6e5](https://github.com/openedx/tutor-contrib-aspects/commit/895f6e5d2ba0574c79ab5223c007f70a3979c9d2))

## v1.0.3 - 2024-07-03

### [1.0.3](https://github.com/openedx/tutor-contrib-aspects/compare/v1.0.2...v1.0.3) (2024-07-03)

### Bug Fixes

* Import of custom Superset assets ([d5f7daf](https://github.com/openedx/tutor-contrib-aspects/commit/d5f7daf816a636a32ca80d1669b3c38b9bbe30b0))
* replace deprecated github actions ([92a503e](https://github.com/openedx/tutor-contrib-aspects/commit/92a503e461dfa21ba0141f86f611a030e7ceedbd))
* replace deprecated github actions ([f1aeefa](https://github.com/openedx/tutor-contrib-aspects/commit/f1aeefa5bede1ba03045eed042849924ede26cd1))
* Serialize Superset zip exports to extensions ([fd44ff4](https://github.com/openedx/tutor-contrib-aspects/commit/fd44ff49e873668f19f7625f1ba01211dc36f5e0))

## v1.0.2 - 2024-06-20

### [1.0.2](https://github.com/openedx/tutor-contrib-aspects/compare/v1.0.1...v1.0.2) (2024-06-20)

### Bug Fixes

* add fallback for public hosts ([#876](https://github.com/openedx/tutor-contrib-aspects/issues/876)) ([7bbebb1](https://github.com/openedx/tutor-contrib-aspects/commit/7bbebb1fe70b4c5df5d32ec9fff65ac748e37166))
* At-risk chart text rotation ([fdd15f9](https://github.com/openedx/tutor-contrib-aspects/commit/fdd15f9958423cc2e96e41bd1887d57b22b95242))
* Course dash problem responses/results without PII ([1621790](https://github.com/openedx/tutor-contrib-aspects/commit/162179093174e0c3cbfd38b68d6cf4a26512133e))
* Individual learner dash translations ([de4faff](https://github.com/openedx/tutor-contrib-aspects/commit/de4faffb1a7644f3e3ab94ea6e85b4a69ba287b6))

### Build Systems

* **deps:** bump urllib3 from 2.2.1 to 2.2.2 in /requirements ([#865](https://github.com/openedx/tutor-contrib-aspects/issues/865)) ([1df1e6c](https://github.com/openedx/tutor-contrib-aspects/commit/1df1e6c47ec0f07987e4f3405b8b6a95f0ea0de9))
* build images on releases merges ([#875](https://github.com/openedx/tutor-contrib-aspects/issues/875)) ([4c5ec22](https://github.com/openedx/tutor-contrib-aspects/commit/4c5ec229fe4b861b17edb646eb424448e5a297a3))

## v1.0.1 - 2024-06-18

### [1.0.1](https://github.com/openedx/tutor-contrib-aspects/compare/v1.0.0...v1.0.1) (2024-06-18)

#### Features

* Update performance_metrics to take optional dashboard and slice ([#801](https://github.com/openedx/tutor-contrib-aspects/issues/801)) ([02e0a50](https://github.com/openedx/tutor-contrib-aspects/commit/02e0a50df23ea4a02919f2c1bd98b78e57ea6ad2))
* use jinja for watched video segments query ([#804](https://github.com/openedx/tutor-contrib-aspects/issues/804)) ([cb8c40c](https://github.com/openedx/tutor-contrib-aspects/commit/cb8c40c3560360a7bb959e359fa96835ba83f1fc))
* **perf:** improve time of running dbt by pre installing requirements ([ccb2c4b](https://github.com/openedx/tutor-contrib-aspects/commit/ccb2c4b8bd355fd32c96a5e78bd907521ccd589e))
* Add command to generate a dbt exposures file ([#851](https://github.com/openedx/tutor-contrib-aspects/issues/851)) ([859cb4c](https://github.com/openedx/tutor-contrib-aspects/commit/859cb4c699d55aae7bde47a7bdd01957c3ad2647))
* add init clickhouse job ([#815](https://github.com/openedx/tutor-contrib-aspects/issues/815)) ([a2fa0ff](https://github.com/openedx/tutor-contrib-aspects/commit/a2fa0ff7775aca9968b8ae846d65e2415ed315e8))
* Add real version of aspects-dbt to include new model ([f68fea3](https://github.com/openedx/tutor-contrib-aspects/commit/f68fea3ad64c3c5336c5ccf00ca03c39d4d686d7))
* add uuid to chart filenames ([01ec69a](https://github.com/openedx/tutor-contrib-aspects/commit/01ec69a81df80d0a6e735d172e1aed148e9d744a))
* adds superset to the list of URLs printed by tutor after launch ([f3e085b](https://github.com/openedx/tutor-contrib-aspects/commit/f3e085b5214080e5e064c8a7cea3456376258727))
* bring back int_problem_results CTEs ([8864c4b](https://github.com/openedx/tutor-contrib-aspects/commit/8864c4bd5ff14d5099b41d0b70bd1ecd4fb19018))
* changes from edunext for individual learner dashboard ([#860](https://github.com/openedx/tutor-contrib-aspects/issues/860)) ([9d17c82](https://github.com/openedx/tutor-contrib-aspects/commit/9d17c8299e9c20ccd9ad6fe66e8788a709ddd7a2))
* move page engagement to an mv ([5c2792f](https://github.com/openedx/tutor-contrib-aspects/commit/5c2792f02009db65b15316f041d16ebf2cbb8816))
* serialize query_context as json for redability ([ca06d3a](https://github.com/openedx/tutor-contrib-aspects/commit/ca06d3a15016d073e49d159a9a899399c49c2699))
* Turn on event-routing-backends batching by default ([#844](https://github.com/openedx/tutor-contrib-aspects/issues/844)) ([deabdd5](https://github.com/openedx/tutor-contrib-aspects/commit/deabdd5ff928aadcfb5814739fca5fe80b02c2c5))
* ui changes from edunext sandbox ([#858](https://github.com/openedx/tutor-contrib-aspects/issues/858)) ([4bcc491](https://github.com/openedx/tutor-contrib-aspects/commit/4bcc491728832bc6d0858884d82685608e78740c))
* upgrade aspects-dbt to pages ([546e304](https://github.com/openedx/tutor-contrib-aspects/commit/546e30407307df2fba55ff93b46d0ca2db6c1b89))
* upgrade aspects-dbt to v3.26.0 ([07a5ca2](https://github.com/openedx/tutor-contrib-aspects/commit/07a5ca272a30fe1999bb798241f46fcb8ea5052d))
* upgrade aspects-dbt to v3.27.0 ([eddd610](https://github.com/openedx/tutor-contrib-aspects/commit/eddd61006b5e1ea17d3bfcbfaa1806d4c9fb1462))
* use video engagement from MV ([f23bdce](https://github.com/openedx/tutor-contrib-aspects/commit/f23bdce630eb2d6c4aa6f769b20fe73d13d95a26))

#### Bug Fixes

* Add help text to the individual learner dash ([01941b8](https://github.com/openedx/tutor-contrib-aspects/commit/01941b831ca452f3ece7ad33963385786106f5c0))
* add key for memoized_func ([d3fabff](https://github.com/openedx/tutor-contrib-aspects/commit/d3fabff4966d8b511929d28cdcc219397fbdd842))
* add missing aspects instructor help markdown ([6d36aa5](https://github.com/openedx/tutor-contrib-aspects/commit/6d36aa5ee61592b5ecf3ba57fe297b51734b2a1f))
* Add verbose names to fact_problem_engagement fields ([9cb979c](https://github.com/openedx/tutor-contrib-aspects/commit/9cb979ceb45b264bebe05f3268ade5bf2446c314))
* Bump aspects-dbt to v3.29.0 to get associated changes ([27e412f](https://github.com/openedx/tutor-contrib-aspects/commit/27e412fe6ec71f26851438415902dd79832e5e26))
* Bump event-routing-backends to v9.2.1 ([#850](https://github.com/openedx/tutor-contrib-aspects/issues/850)) ([8651843](https://github.com/openedx/tutor-contrib-aspects/commit/8651843e217537be29c7b29c7808250342d268d8))
* Bump platform-plugin-aspects to 0.9.7 ([3441da7](https://github.com/openedx/tutor-contrib-aspects/commit/3441da7944a707154b489371a8eda4220cd2c90b))
* Course Dash limit label lengths, require course key ([03e7d1f](https://github.com/openedx/tutor-contrib-aspects/commit/03e7d1f87f8c3de42899e3ef25dcefcae334a20e))
* Display issues with "problems attempted by section/subsection" ([5fd4f26](https://github.com/openedx/tutor-contrib-aspects/commit/5fd4f267c8c706c39ca6e9bbd1dbaefae23658e8))
* Enrollment pii fix, use 2 dbt threads by default ([b307164](https://github.com/openedx/tutor-contrib-aspects/commit/b307164876e3f59e5b26c7ec780e418d319ebed4))
* Fix KeyError in compile_translations ([#807](https://github.com/openedx/tutor-contrib-aspects/issues/807)) ([d4a02db](https://github.com/openedx/tutor-contrib-aspects/commit/d4a02dbe12c1691af2afb006d0df5e741975da75))
* increase gunicorn keep alive to 5 ([477497b](https://github.com/openedx/tutor-contrib-aspects/commit/477497ba3fee0ff3e5b75fe75e696d200bc93bd3))
* linting ([46ea56d](https://github.com/openedx/tutor-contrib-aspects/commit/46ea56d4a7a59c2b7b811265231fd1c4ba4dd8ed))
* load query context as json at import ([714e660](https://github.com/openedx/tutor-contrib-aspects/commit/714e66025624ce880f7cc182dd788bd655231416))
* new strings for translation ([#842](https://github.com/openedx/tutor-contrib-aspects/issues/842)) ([8c0c4bb](https://github.com/openedx/tutor-contrib-aspects/commit/8c0c4bbc0b8593d812d9a5fdcdc8bde646d567e6))
* Operator dash user counts, performance ([0cc17dc](https://github.com/openedx/tutor-contrib-aspects/commit/0cc17dcb4ba886432a07673aa57336fcd9781f46))
* override pre-generated database connection ([fc80352](https://github.com/openedx/tutor-contrib-aspects/commit/fc8035244edaf16fa1bded370648384860d4b77f))
* Performance enhancements for at-risk dashboards ([22bf042](https://github.com/openedx/tutor-contrib-aspects/commit/22bf0421c8222173e1720f0459958a16351a2138))
* Performance enhancements for at-risk dashboards ([ee191a3](https://github.com/openedx/tutor-contrib-aspects/commit/ee191a37e4d571029eec4631ddfbae166d89006f))
* Performance fixes for learner summary, fix grade % ([4fc17cc](https://github.com/openedx/tutor-contrib-aspects/commit/4fc17cc0f38cafe2e8aa8ab5e8657f00b59d6b03))
* Performance fixes, more dataset strings, new help text ([1aa24cd](https://github.com/openedx/tutor-contrib-aspects/commit/1aa24cd6371b3e706ab0514835dd370eb384bd4c))
* Problem results correct/incorrect to percentages ([d44b650](https://github.com/openedx/tutor-contrib-aspects/commit/d44b650c2417d97dbf4951c1de38a8eb62b0de88))
* Re-add jinja filters for performance ([c8200e3](https://github.com/openedx/tutor-contrib-aspects/commit/c8200e37eff63821597a252450f66d8c0c2ea405))
* re-serialize assets for query context ([bb2a553](https://github.com/openedx/tutor-contrib-aspects/commit/bb2a5531a3db8cd8ae76c3b5c37b19a8b120a19d))
* re-serialize partial views assets ([c58daae](https://github.com/openedx/tutor-contrib-aspects/commit/c58daae4f47c188aba32bae03a9c9a48a7c744bc))
* Remove all references to JSON column and setting ([#806](https://github.com/openedx/tutor-contrib-aspects/issues/806)) ([2ca930f](https://github.com/openedx/tutor-contrib-aspects/commit/2ca930f92a32125dc2955d639d185949021eca6d))
* remove leftUT8 references ([f85a328](https://github.com/openedx/tutor-contrib-aspects/commit/f85a32835c2ab38c3b5514aeb3e58978d8c78d93))
* remove leftUT8 references ([91c597f](https://github.com/openedx/tutor-contrib-aspects/commit/91c597f7d1118da2f2175a8c7368407fd799c9f3))
* serialize query performance asset ([557d2eb](https://github.com/openedx/tutor-contrib-aspects/commit/557d2eb6f50d6d4e84c9753a9cff30d59525cf67))
* show correct value on watched segments x-axis ([ade8379](https://github.com/openedx/tutor-contrib-aspects/commit/ade837938cb6bfd2e838ca410775636149592cfe))
* Translate "graded" data strings in Course Dash ([0fb0aa0](https://github.com/openedx/tutor-contrib-aspects/commit/0fb0aa0d637133bb221c23c1ed2ddeb6a09e4709))
* Use correct schema, coerce actor_id, move include ([aab080b](https://github.com/openedx/tutor-contrib-aspects/commit/aab080b3a26457d53ddce1bd68cac8dabcb0337a))
* Use enrolled date if last visited is not set ([0b4ea8a](https://github.com/openedx/tutor-contrib-aspects/commit/0b4ea8a69cec1e5a461c1a649a0c04e5828d991a))
* Use new column name for fact_learner_last_course_visit ([416299b](https://github.com/openedx/tutor-contrib-aspects/commit/416299b7ffccc0070fb12043ce03b691e70dbd4f))
* verify event bus producer config is defined ([ed4b4f4](https://github.com/openedx/tutor-contrib-aspects/commit/ed4b4f46bf4b843a9e7fc6398cca4f4a33375c13))

#### Styles

* formatting ([a0731b7](https://github.com/openedx/tutor-contrib-aspects/commit/a0731b79c0a69ad4c606dcb50f5fb3bb60ff52f3))
* only check new filename ([d386b45](https://github.com/openedx/tutor-contrib-aspects/commit/d386b45d9385faa37a72a4e9e2e7b38ee032c12a))
* Sqlfmt fix ([230ed54](https://github.com/openedx/tutor-contrib-aspects/commit/230ed54c897d05e86e50b6cfc7b6497dc5dadb2b))

#### Build Systems

* **deps:** bump stefanzweifel/changelog-updater-action ([#819](https://github.com/openedx/tutor-contrib-aspects/issues/819)) ([f0bb4dd](https://github.com/openedx/tutor-contrib-aspects/commit/f0bb4dde6f54a7bfc236cb651f4aa7eb91bf971b))
* don't tag this in Open edX releases ([#810](https://github.com/openedx/tutor-contrib-aspects/issues/810)) ([839460a](https://github.com/openedx/tutor-contrib-aspects/commit/839460a6969d471a50bc2eccadc181eef8bf218d))
* fail on error on every environment ([8cda924](https://github.com/openedx/tutor-contrib-aspects/commit/8cda924fcf713cc550353ec3ee1febe7129c495f))
* **deps:** bump docker/login-action from 3.1.0 to 3.2.0 ([#847](https://github.com/openedx/tutor-contrib-aspects/issues/847)) ([1b963c7](https://github.com/openedx/tutor-contrib-aspects/commit/1b963c7e24c27fbc0d22e75c91d7d84d156a57b7))
* Make CI force course_overviews dump ([#856](https://github.com/openedx/tutor-contrib-aspects/issues/856)) ([03b45d1](https://github.com/openedx/tutor-contrib-aspects/commit/03b45d1f3e3d3721365bb183bb96657a9b2e1deb))
* Speed up CI by limiting languages ([307c60a](https://github.com/openedx/tutor-contrib-aspects/commit/307c60a3b6fd129fd80176b8c823241b0d998023))

## v1.0.0 - 2024-05-09

### Release 1.0!

## v0.107.3 - 2024-05-09

### [0.107.3](https://github.com/openedx/tutor-contrib-aspects/compare/v0.107.2...v0.107.3) (2024-05-09)

### Bug Fixes

* use proper dataset columns ([#785](https://github.com/openedx/tutor-contrib-aspects/issues/785)) ([1113805](https://github.com/openedx/tutor-contrib-aspects/commit/11138050e71fefef26400ed9e84cbbb7bff0c39a)), closes [#786](https://github.com/openedx/tutor-contrib-aspects/issues/786)

## v0.107.2 - 2024-05-08

### [0.107.2](https://github.com/openedx/tutor-contrib-aspects/compare/v0.107.1...v0.107.2) (2024-05-08)

### Bug Fixes

* automatically add verbose name for dataset columns ([8d37a19](https://github.com/openedx/tutor-contrib-aspects/commit/8d37a192a69572a6afd50d5b3cf0e2b9618b3fa4))
* automatically add verbose name for metrics ([66d7117](https://github.com/openedx/tutor-contrib-aspects/commit/66d711714e24baa77943165ebbdea810cbad09a4))
* move chart metrics to datasets ([0db0f57](https://github.com/openedx/tutor-contrib-aspects/commit/0db0f5785d7a3dc38658db5e1a2f57474531a97c))
* update charts owners if configured ([73b8954](https://github.com/openedx/tutor-contrib-aspects/commit/73b89545571f40c24565e9b5e0e09722e8782efe))
* update conditional format for new metrics ([fb55119](https://github.com/openedx/tutor-contrib-aspects/commit/fb551191e2b8674a87d9f6c366d0ba91ae6b25ed))

## v0.107.1 - 2024-05-08

### [0.107.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.107.0...v0.107.1) (2024-05-08)

### Bug Fixes

* Use base.in for install_requires ([#779](https://github.com/openedx/tutor-contrib-aspects/issues/779)) ([77ba855](https://github.com/openedx/tutor-contrib-aspects/commit/77ba855f72a4d6402487f45acc94900d3ac5c129))

## v0.107.0 - 2024-05-08

### [0.107.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.106.0...v0.107.0) (2024-05-08)

#### Features

* add materials for at-risk learner group (FC-0051) ([#765](https://github.com/openedx/tutor-contrib-aspects/issues/765)) ([e0bbc4f](https://github.com/openedx/tutor-contrib-aspects/commit/e0bbc4f276d140ccdc1d0044e1472dc05435eb8c))

## v0.106.0 - 2024-05-07

### [0.106.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.105.4...v0.106.0) (2024-05-07)

#### Features

* import latest version of course dashboard ([a61ee7b](https://github.com/openedx/tutor-contrib-aspects/commit/a61ee7ba39937238665056205614541b62905f77))

#### Bug Fixes

* update course dashboard slug ([b1fc366](https://github.com/openedx/tutor-contrib-aspects/commit/b1fc366db687b31dcfa80072461d1fc8e8e8d37b))

#### Code Refactoring

* use watched video segments from dbt ([788ef17](https://github.com/openedx/tutor-contrib-aspects/commit/788ef17d6d5f117cdc3f84f708b284893b554c0e))

## v0.105.4 - 2024-05-07

### [0.105.4](https://github.com/openedx/tutor-contrib-aspects/compare/v0.105.3...v0.105.4) (2024-05-07)

### Bug Fixes

* Import on openedx-translations ([#773](https://github.com/openedx/tutor-contrib-aspects/issues/773)) ([b6a78c2](https://github.com/openedx/tutor-contrib-aspects/commit/b6a78c2ebfdbb6ca1d3512deee4e1826000d9c8f))

## v0.105.3 - 2024-05-01

### [0.105.3](https://github.com/openedx/tutor-contrib-aspects/compare/v0.105.2...v0.105.3) (2024-05-01)

### Bug Fixes

* Normalize localized asset UUIDs ([94915a2](https://github.com/openedx/tutor-contrib-aspects/commit/94915a2bc9c328ebdbc46f53c103df8bb9c129c6))

## v0.105.2 - 2024-04-29

### [0.105.2](https://github.com/openedx/tutor-contrib-aspects/compare/v0.105.1...v0.105.2) (2024-04-29)

### Bug Fixes

* Distribution of current course grades chart errors in perf metrics ([27e9a62](https://github.com/openedx/tutor-contrib-aspects/commit/27e9a626d061f1c75c800943239c27bbe2598919))
* Fail Tutor command on performance_metrics failure ([9a6f065](https://github.com/openedx/tutor-contrib-aspects/commit/9a6f0652240d7037afea27ddc21eb89a05b8e780))
* Fix course_key option in performance_metrics ([b77ea4d](https://github.com/openedx/tutor-contrib-aspects/commit/b77ea4d2bf2c8464da4addc8827ffd382b24f5b3))
* Learners with passing grade filter to only passing ([7946df4](https://github.com/openedx/tutor-contrib-aspects/commit/7946df4d7cd50326aa3bc7006ab10a2ae7416a8c))

## v0.105.1 - 2024-04-29

### [0.105.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.105.0...v0.105.1) (2024-04-29)

### Bug Fixes

* use correct casing for Int32 ([d196151](https://github.com/openedx/tutor-contrib-aspects/commit/d196151f01549237d27490f485dc1748a398efcf))
* use proper casing for splitByString ([85800f2](https://github.com/openedx/tutor-contrib-aspects/commit/85800f243bc12ec45e82af2de996580a9f21d063))

### Build Systems

* **deps:** bump helm/kind-action from 1.9.0 to 1.10.0 ([1326aeb](https://github.com/openedx/tutor-contrib-aspects/commit/1326aeb2d2f531b0b04ef2fe7931da08beeb1694))

## v0.105.0 - 2024-04-29

### [0.105.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.104.3...v0.105.0) (2024-04-29)

#### Features

* Add check for orphaned assets ([3e70836](https://github.com/openedx/tutor-contrib-aspects/commit/3e70836948fc1b5c0a2e47bb3074b4b66041bbe6))
* Update operator dash to scale better ([470caba](https://github.com/openedx/tutor-contrib-aspects/commit/470cabaed8d66384d7d87180c23c0d6d17253592))

#### Bug Fixes

* Account for values being nulled on changed import yaml ([aaf8d0c](https://github.com/openedx/tutor-contrib-aspects/commit/aaf8d0c18d18c0ee5d1c073babc3fb3a436c7e72))
* Don't overwrite Superset configurations if they already exist ([321b2c4](https://github.com/openedx/tutor-contrib-aspects/commit/321b2c498ce8c26ee5f198cccc2c230903f565a0))
* Fail tasks when subcommands fail ([4a16044](https://github.com/openedx/tutor-contrib-aspects/commit/4a16044d411fa8ac1cd9867f14b58e76269f14ff))
* Fixes for orphan detection ([3067963](https://github.com/openedx/tutor-contrib-aspects/commit/306796394fe8283dfc92cd17d48e6d844203eda9))
* Prefer dbt over other queries for memory usage ([26eafcc](https://github.com/openedx/tutor-contrib-aspects/commit/26eafccd9f6849bde7d4aa5a77b799ff52c577a6))
* Reduce CH memory usage by using uniqCombinedMerge ([ae355dd](https://github.com/openedx/tutor-contrib-aspects/commit/ae355dd419cf121d5abfa3868db2e97f55ddbfb5))

#### Styles

* Fix linting issues ([10b4de1](https://github.com/openedx/tutor-contrib-aspects/commit/10b4de129adbcecd20b7075a01f4d181ad952bbc))

#### Code Refactoring

* Clean up logging ([645ed38](https://github.com/openedx/tutor-contrib-aspects/commit/645ed3862cb780345a64b2bb6e938f61f9465dce))
* Fix column names for next aspects-dbt release ([5716e38](https://github.com/openedx/tutor-contrib-aspects/commit/5716e38fc899398600495ed0ec5cc1ad42237682))
* Operator dash performance / usability refactor ([a47caa3](https://github.com/openedx/tutor-contrib-aspects/commit/a47caa3c58685dadd64b9024c95d2e13e7d248b0))
* Remove unused assets ([ffb1e40](https://github.com/openedx/tutor-contrib-aspects/commit/ffb1e4069d1136e67f6d9dfc3e32a8043a63a242))
* Use asset import instead of example import ([0fbee3f](https://github.com/openedx/tutor-contrib-aspects/commit/0fbee3f256d72a761feb5c9d4f6a04153d21dc31))
* Use real asset import instead of example ([e5997cf](https://github.com/openedx/tutor-contrib-aspects/commit/e5997cf8b73d9174666447dc132f481a4dcb38a0))

## v0.104.3 - 2024-04-23

### [0.104.3](https://github.com/openedx/tutor-contrib-aspects/compare/v0.104.2...v0.104.3) (2024-04-23)

### Bug Fixes

* upgrade platform-plugin-aspects on production image ([cf61a96](https://github.com/openedx/tutor-contrib-aspects/commit/cf61a96db3ea95c0616b595f2eab93f000d5ce6b))

## v0.104.2 - 2024-04-23

### [0.104.2](https://github.com/openedx/tutor-contrib-aspects/compare/v0.104.1...v0.104.2) (2024-04-23)

### Bug Fixes

* apply filters to course dashboard datasets ([29a26b3](https://github.com/openedx/tutor-contrib-aspects/commit/29a26b3dd16ce708158eaf94f4f610deed4a9473))

## v0.104.1 - 2024-04-22

### [0.104.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.104.0...v0.104.1) (2024-04-22)

### Bug Fixes

* Add logger we're trying to use ([3a05929](https://github.com/openedx/tutor-contrib-aspects/commit/3a059297456d064bd2fc0d961f7b73042a20cfb9))
* Add missing import ([6e6e917](https://github.com/openedx/tutor-contrib-aspects/commit/6e6e917239368c5d4ae49885a4682c1c3c182273))
* Broken logging statement ([ca4ee49](https://github.com/openedx/tutor-contrib-aspects/commit/ca4ee49479e0833e92ce2a9f20c09f06fca234a4))
* Remove query context after asset import ([992f0cc](https://github.com/openedx/tutor-contrib-aspects/commit/992f0ccc7e8dde4e27c26fa216c794ddbdbeef83))

## v0.104.0 - 2024-04-22

### [0.104.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.103.0...v0.104.0) (2024-04-22)

#### Features

* add video plays table to course dashboard ([21b2b0c](https://github.com/openedx/tutor-contrib-aspects/commit/21b2b0c180ab008d37b508adf564bd753d3c9e63))

## v0.103.0 - 2024-04-22

### [0.103.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.102.1...v0.103.0) (2024-04-22)

#### Features

* Add an option to print the SQL, bug fix ([f3fa9f1](https://github.com/openedx/tutor-contrib-aspects/commit/f3fa9f10e490eaa36b89c62528b834e6057d3d7f))
* allow to filter course id for performance metrics ([0ec681e](https://github.com/openedx/tutor-contrib-aspects/commit/0ec681ea900993f436406afbcc5294340ad767e8))
* allow to filter course id for performance metrics ([659804b](https://github.com/openedx/tutor-contrib-aspects/commit/659804bc4297e7fcd2ad0cea9aae30e9b37111be))

#### Styles

* Fix lint error ([6e65a7a](https://github.com/openedx/tutor-contrib-aspects/commit/6e65a7aa7de6d22c2fd0ec2f2b247d9821805752))
* Fix lint error ([c124082](https://github.com/openedx/tutor-contrib-aspects/commit/c124082b81aa4e025863ec624ea475038646b100))

## v0.102.1 - 2024-04-19

### [0.102.1](https://github.com/openedx/tutor-contrib-aspects/compare/v0.102.0...v0.102.1) (2024-04-19)

### Bug Fixes

* use correct datasets for engagement charts ([07ebbdb](https://github.com/openedx/tutor-contrib-aspects/commit/07ebbdb97034a3b406fd938ef072ce6013ba75e4))

## v0.102.0 - 2024-04-18

### [0.102.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.101.0...v0.102.0) (2024-04-18)

#### Features

* update enrollment datasets ([d5b229f](https://github.com/openedx/tutor-contrib-aspects/commit/d5b229f563a1e08257da2e72b5830c027b6974c5))

## v0.101.0 - 2024-04-17

### [0.101.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.100.0...v0.101.0) (2024-04-17)

#### Features

* install platform plugin aspects v0.7.0 ([5dcb82e](https://github.com/openedx/tutor-contrib-aspects/commit/5dcb82eac0ee52c19c90d9ad698ee7adb198647f))

#### Bug Fixes

* do not check for main schema when translating datasets ([5561793](https://github.com/openedx/tutor-contrib-aspects/commit/5561793116947fe199dcf32d3823a8c55841fae7))
* link filters to the course_name dataset ([b3a0ba9](https://github.com/openedx/tutor-contrib-aspects/commit/b3a0ba9136785be9de266e469c2ae7a53202e4d5))
* use virtual datasets ([78e2a23](https://github.com/openedx/tutor-contrib-aspects/commit/78e2a239ed0623a1c1c892cdf9d3236035658833))

## v0.100.0 - 2024-04-16

### [0.100.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.99.0...v0.100.0) (2024-04-16)

#### Features

* add configurable TTL ([5078750](https://github.com/openedx/tutor-contrib-aspects/commit/507875076dba7cb3ac7152722025403322a344a8))
* migrate aspects dictionaries to dbt ([89acf63](https://github.com/openedx/tutor-contrib-aspects/commit/89acf63e51acb9b41cb7a8566778cad4472dde12))

#### Bug Fixes

* install only dbt requirements ([e3d5768](https://github.com/openedx/tutor-contrib-aspects/commit/e3d5768473bf8a152a879563b7070ce345dd28b7))
* restore installation of aspects-dbt requirements ([b0a711d](https://github.com/openedx/tutor-contrib-aspects/commit/b0a711d5568d63a3bf04a742bae0057bd09d4e43))

## v0.99.0 - 2024-04-14

### [0.99.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.98.0...v0.99.0) (2024-04-14)

#### Features

* remove unnecessary settings ([7e170ce](https://github.com/openedx/tutor-contrib-aspects/commit/7e170ce2485864fe589bede3ab4488e12686797e))

## v0.98.0 - 2024-04-14

### [0.98.0](https://github.com/openedx/tutor-contrib-aspects/compare/v0.97.1...v0.98.0) (2024-04-14)

#### Features

* remove instructor dashboard and related assets ([30722b5](https://github.com/openedx/tutor-contrib-aspects/commit/30722b555b32ac6b6973a0c661c5a79d95eb07ba))

#### Build Systems

* **deps:** bump idna from 3.6 to 3.7 in /requirements ([d07b0b6](https://github.com/openedx/tutor-contrib-aspects/commit/d07b0b6a40b2501a07f0a24e535a748a5c135728))

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
