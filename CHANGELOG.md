# InMoose release changelog

## [0.2.1-dev]

- add a function to generate simulated RNA-Seq and scRNA-Seq data

## [0.2.0]

- `inmoose` now requires Python >= 3.8
- reorganize tests directory
- refactor module for batch effect correction. It is now named `pycombat`
  (instead of `batch`), and the function to correct batch effect on microarray
  data is now `pycombat_norm` (instead of `pycombat`).
- refactor design matrix computation, to share the code between `pycombat_norm`
  and `pycombat_seq`
- batch effect correction functions now accept both `numpy` arrays and `pandas`
  dataframes as input for the counts matrix
- improved logging: no more `print`s, better log formatting
- `inmoose` doc is now on `readthedocs.org`

## [0.1.1]

- upgrade to Cython 3.0.0b2
- fix C++ extension loading on Linux
- add CI/CD to build, test and publish distributions

## [0.1.0]

Initial release

