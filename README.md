# AtomicQuery
This is an experimental package for the sake of hashing atomic data by (configuration, term, J) level information instead of (idxI, idxJ), so that an Atom object is able to be created by given the information of necessary levels without editing the data file.

---

## Available Atomic model



| Atom & ionization stage | Available Terms | nLevel | Ref : Level & Aji | Ref: electron impact ECS | Ref: proton impact ECS |
|:-----------------------:|:----------------|:-----|:-----|:----------------|:-------------------------|
| C III | "1s2.2s2 1S" - "1s2.2p2 1S" | 10 | NIST | [Berrington et al. 1985](./ref/ECS/Berrington_et_al_1985.pdf) | not yet |
| O V | "1s2.2s2 1S" - "1s2.2p2 1S" | 10 | NIST | [Berrington et al. 1985](./ref/ECS/Berrington_et_al_1985.pdf) | not yet |
| Si III | "1s2.2s2.2p6.3s2 1S"- "1s2.2s2.2p6.3d.4d 1S" | 141 | [Kanti 2017](./ref/ECS/Kanti_2017.pdf) | [Kanti 2017](./ref/ECS/Kanti_2017.pdf) | not yet |


## Formatting files in database

For instance, we need the information of C^{2+}.

### 1. Copy Level information and Einstein Aji coefficient from NIST database {: Developer}

Level :

1. open https://physics.nist.gov/PhysRefData/ASD/levels_form.html
2. modified the corresponding parameters in red rectangular shown in Fig 1.
3. The query format looks like Fig 2.
4. copy the whole text to `./atom/NIST_ASCII/C_III/C_III.NistLevel`

| ![img](./fig/nist_example1.png) |
|:---:|
| Fig 1. |

| ![img](./fig/nist_example2.png) |
|:---:|
| Fig 2. |

Einstein Aji :

1. open https://physics.nist.gov/PhysRefData/ASD/lines_form.html
2. modified the corresponding parameters in red rectangular shown in Fig 3.
3. The query format looks like Fig 4.
4. copy the whole text to `./atom/NIST_ASCII/C_III/C_III.NistLine`

| ![img](./fig/nist_example3.png) |
|:---:|
| Fig 3. |

| ![img](./fig/nist_example4.png) |
|:---:|
| Fig 4. |

### 2. Format Level data (Config) {: Developer}

in this case, information such as Aji is taken from NIST.

1. check whether we need a `_prefix` for the inner shell configuration.
> for example, in Fig 2., the ground level configuration is '2s2' instead of the full configuration '1s2.2s2', then we need to specify `_prefix="1s2."`
2. modify the parameter in `./tools/prepare_level_from_nist.py` and then execute it. This will output a prototype config file called `./atom/config/C_III.Level` looks like Fig 5.
3. modify `stage` column and add general information into `./atom/config/C_III.Level` (Fig 6.). Lines start with '#' is comment line.

| ![img](./fig/output_example1.png) |
|:---:|
| Fig 5. |

| ![img](./fig/output_example2.png) |
|:---:|
| Fig 6. |


### 3. Format Aji and Wavelength data (Database) {: Developer}

in this case, information such as Aji is taken from NIST.

1. check whether we need a `_prefix` for the inner shell configuration.
> for example, in Fig 2., the ground level configuration is '2s2' instead of the full configuration '1s2.2s2', then we need to specify `_prefix="1s2."`
2. modify the parameter in `./tools/prepare_Aji_from_nist.py` and then execute it. This will output a prototype config file called `./atom/C_III/Einstein_A/Nist.Aji` looks like Fig 7.
3. add more general information into `./atom/config/C_III.Level` as comment line such as "reference" and so on.

| ![img](./fig/output_example3.png) |
|:---:|
| Fig 7. |


### 4. Format Effective Collision Strength data for Collisional Excitation (database) {: Developer}

Since for different atom with different ionization stage the data comes from different paper/database/website, there is no definite script to format ECS (Effective Collision Strength) data.

However, like Aji, Effective Collision Strength table should also follow (configuration, term, J) indexing (ctj indexing), like Fig 8.

| ![img](./fig/output_example4.png) |
|:---:|
| Fig 8. |

### 5. Construct `Atom()` instances (User interface) {: User}

An `AtomCls.Atom()`` instance can be constructed by
```
import sys
sys.path.append("..")

from src.Structure import AtomCls
file = "../atom/config/C_III.Level"
file_Aji = "../atom/C_III/Einstein_A/Nist.Aji"                                    # optional
file_CEe = "../atom/C_III/Collisional_Excitation/Berrington_et_al_1985.Electron"  # optional
atom = AtomCls.Atom(file, _file_Aji=file_Aji, _file_CEe=file_CEe)
```

furthermore, `Aji` and `CE` data could be read without resetting *.Level config file, like
```
atom.read_Aji(_file_Aji=file_Aji)
atom.read_CE(_file_CEe=file_CEe)
```

the available properties of this Class contains
> `atom.Title`, `atom.Z`, `atom.Element`, `atom.nLevel`, `atom.nLine`, `atom.Level`, `atom.Level_info`, `atom.Level_info_table`, `atom.Line_idx_table`, `atom.Line_ctj_table`, `atom.Line`, `atom.CE_Te_table`, `atom.CE_table`, `atom.CE_coe`, `atom.CE_type`


### 6. Generate Grotrian diagram {: User}
