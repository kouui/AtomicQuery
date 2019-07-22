# AtomicQuery
This is an experimental package for the sake of hashing atomic data by (configuration, term, J) level information instead of (idxI, idxJ), so that an Atom object is able to be created by given the information of necessary levels without editing the data file.

---

## Available Atomic model



| Atom & ionization stage | Available Terms | nLevel | Ref : Level & Aji | Ref: electron impact ECS | Ref: proton impact ECS |
|:-----------------------:|:----------------|:-----|:-----|:----------------|:-------------------------|
| C III | "1s2.2s2 1S" - "1s2.2p2 1S" | 10 | NIST | [Berrington et al. 1985](.ref/ECS/Berrington_et_al_1985.pdf) | not yet |
| O V | "1s2.2s2 1S" - "1s2.2p2 1S" | 10 | NIST | [Berrington et al. 1985](.ref/ECS/Berrington_et_al_1985.pdf) | not yet |
| Si III | "1s2.2s2.2p6.3s2 1S"- "1s2.2s2.2p6.3d.4d 1S" | 141 | [Kanti 2017](./ref/ECS/Kanti_2017.pdf) | [Kanti 2017](./ref/ECS/Kanti_2017.pdf) | not yet |


## Formatting files in database

### 1. Copy Level information and Einstein Aji coefficient from NIST database {: Developer}

For instance, we need the information of C^{2+}.

Level :

1. open https://physics.nist.gov/PhysRefData/ASD/levels_form.html
2. modified the corresponding parameters in red rectangular shown in Fig 1.
3. The query format looks like Fig 2.
4. copy the whole text to `./atom/NIST_ASCII/C_III/C_III.NistLevel`
5. check whether we need a `_prefix` for the inner shell configuration.
> for example, in Fig 2., the ground level configuration is '2s2' instead of the full configuration '1s2.2s2', then we need to specify `_prefix="1s2."`
6. modify the parameter in `./tools/prepare_level_from_nist.py` and then execute it. This will output a prototype config file called `./atom/config/C_III.Level` looks like Fig 3.
7. modify `stage` column and add general information into `./atom/config/C_III.Level` (Fig 4.). Lines start with '#' is comment line.

| ![img](./fig/nist_example1.png) |
|:---:|
| Fig 1. |

| ![img](./fig/nist_example2.png) |
|:---:|
| Fig 2. |

| ![img](./fig/output_example1.png) |
|:---:|
| Fig 3. |

| ![img](./fig/output_example2.png) |
|:---:|
| Fig 4. |

| ![img](./fig/nist_example3.png) |
|:---:|
| Fig 5. |

### 2. Formatting Level data (Config) {: Developer}


### 3. Formatting Aji and Wavelength data (Database) {: Developer}


### 4. Formatting Effective Collision Strength data for Collisional Excitation (database) {: Developer}


### 5. Construct `Atom()` instances (User interface) {: User}
