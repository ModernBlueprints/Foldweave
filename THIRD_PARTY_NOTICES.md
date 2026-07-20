# Third-party notices

Foldweave packages selected static assets and compiled JavaScript from
[Palantir Blueprint](https://github.com/palantir/blueprint), React, ReactDOM,
and the production dependency closure listed below. The bundled JavaScript
runs locally in Foldweave's review surface and ChatGPT widget. Node.js is a
build-time dependency only and is not required to run the packaged application
or the browser fallback.

## Bundled JavaScript production dependency closure

The production bundles are tree-shaken, but this notice conservatively covers
the complete `npm ls --omit=dev --all` dependency closure used to build them.

| License | Packages and exact versions |
|---|---|
| Apache-2.0 | `@blueprintjs/colors` 5.1.16; `@blueprintjs/core` 6.17.2; `@blueprintjs/icons` 6.13.0 |
| MIT | `@babel/runtime` 7.29.7; `@floating-ui/core` 1.8.0; `@floating-ui/dom` 1.8.0; `@floating-ui/react` 0.27.20; `@floating-ui/react-dom` 2.1.9; `@floating-ui/utils` 0.2.12; `@popperjs/core` 2.11.8; `@types/prop-types` 15.7.15; `@types/react` 18.3.31; `camel-case` 4.1.2; `capital-case` 1.0.4; `change-case` 4.1.2; `classnames` 2.5.1; `constant-case` 3.0.4; `csstype` 3.2.3; `dom-helpers` 5.2.1; `dot-case` 3.0.4; `header-case` 2.0.4; `js-tokens` 4.0.0; `loose-envify` 1.4.0; `lower-case` 2.0.2; `no-case` 3.0.4; `normalize.css` 8.0.1; `object-assign` 4.1.1; `param-case` 3.0.4; `pascal-case` 3.1.2; `path-case` 3.0.4; `prop-types` 15.8.1; `react` 18.3.1; `react-dom` 18.3.1; `react-fast-compare` 3.2.2; `react-is` 16.13.1; `react-popper` 2.3.0; `scheduler` 0.23.2; `sentence-case` 3.0.4; `snake-case` 3.0.4; `tabbable` 6.5.0; `upper-case` 2.0.2; `upper-case-first` 2.0.2; `warning` 4.0.3 |
| BSD-3-Clause | `react-transition-group` 4.4.5 |
| 0BSD | `tslib` 2.6.3 |

### Copyright notices for the MIT-licensed dependency group

- Babel runtime: Copyright (c) 2014-present Sebastian McKenzie and other contributors.
- Floating UI packages: Copyright (c) 2021-present Floating UI contributors.
- Popper: Copyright (c) 2019 Federico Zivolo.
- DefinitelyTyped React declarations: Copyright (c) Microsoft Corporation.
- Change Case packages: Copyright (c) 2014 Blake Embrey.
- classnames: Copyright (c) 2018 Jed Watson.
- CSSType: Copyright (c) 2017-2018 Fredrik Nicol.
- dom-helpers: Copyright (c) 2015 Jason Quense.
- js-tokens: Copyright (c) 2014-2018 Simon Lydell.
- loose-envify: Copyright (c) 2015 Andres Suarez.
- normalize.css: Copyright Nicolas Gallagher and Jonathan Neal.
- object-assign: Copyright Sindre Sorhus.
- React, ReactDOM, React Is, and Scheduler: Copyright (c) Facebook, Inc. and its affiliates.
- react-fast-compare: Copyright (c) 2018 Formidable Labs and Copyright (c) 2017 Evgeny Poberezkin.
- React Popper: Copyright (c) 2018 React Popper authors.
- tabbable: Copyright (c) 2015 David Clark.

The MIT-licensed packages above are distributed under this permission notice:

> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions: The above copyright
> notice and this permission notice shall be included in all copies or
> substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS",
> WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
> THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
> NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
> FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
> TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
> THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### `react-transition-group` 4.4.5 — BSD-3-Clause

Copyright (c) 2018, React Community. Forked from React; Copyright 2013-present,
Facebook, Inc.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

### `tslib` 2.6.3 — 0BSD

Copyright (c) Microsoft Corporation.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted. THE SOFTWARE IS PROVIDED "AS IS"
AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING
ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR
ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN
AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

## `@blueprintjs/core` 6.17.2

- License declared by the package: Apache-2.0
- Registry metadata:
  <https://registry.npmjs.org/@blueprintjs%2fcore/6.17.2>
- Exact npm tarball:
  <https://registry.npmjs.org/@blueprintjs/core/-/core-6.17.2.tgz>
- Registry SHA-1: `12b1d6c1a3966faf2def2e31e491de2bfa276774`
- Registry SRI:
  `sha512-mY7gmb31iN80/0wJvLvVpp0RPlYrSX7VNh657cGUDVohUsZ+Nxtj62GgJlNmJhkoura9J2lK3rbvHnBqZcMIIA==`
- Downloaded tarball SHA-256:
  `df7649577a2b7c5548c07538fec57cded14c856b42db0ddeca2d36f315e74180`
- Vendored upstream member: `package/lib/css/blueprint.css`
- Local path: `src/name_atlas/static/vendor/blueprint/blueprint.css`
- Exact local/upstream member SHA-256:
  `04c4dc66a0753f7256194af14f5f96f15a1a149e125898349b26c26c92ba377e`

The compiled stylesheet is copied byte-for-byte. Its `url(...)` declarations
are embedded `data:image/svg+xml` values; it has no CDN or other network asset
dependency.

## `@blueprintjs/icons` 6.13.0

- License declared by the package: Apache-2.0
- Registry metadata:
  <https://registry.npmjs.org/@blueprintjs%2ficons/6.13.0>
- Exact npm tarball:
  <https://registry.npmjs.org/@blueprintjs/icons/-/icons-6.13.0.tgz>
- Registry SHA-1: `7481070b55d0a88f6cc7a4059379ce9723610318`
- Registry SRI:
  `sha512-wEQgADFPwufKiKeF/L5K21bKgouuIbIdYPvMPFv2tt7reSuCEftX0dZpga+21JY4KvEJIz+xtVJoqMmXBesiwQ==`
- Downloaded tarball SHA-256:
  `6344d90154a1d47d62989a90ca9e87d3055963fcd7ce9cd942843eb178b9837d`
- Upstream member pattern:
  `package/lib/esm/generated/20px/paths/{icon}.js`
- Local path pattern:
  `src/name_atlas/static/vendor/blueprint/icons/{icon}.svg`

Only the frozen icon vocabulary is packaged. Each SVG copies the Blueprint
20-pixel path geometry verbatim and adds only an inert SVG wrapper with
`viewBox="0 0 20 20"`, `fill="currentColor"`, `focusable="false"`, and
`aria-hidden="true"`. The icons must accompany visible text in the application.

| Icon | Upstream path-module SHA-256 | Local SVG SHA-256 |
|---|---|---|
| `chevron-right` | `f06ca353d3a2264f8a2260fc5a8b41197f56b1f8254faa55e29440021cfbc198` | `a8767948728333c16fead870a7bb1722c90b7a5c3216fe43319de8c94eb28493` |
| `clipboard` | `40a20491ad645d3c1e1525083270951e7c389b5e987eb5fc9e0c2b2dda4c9fdd` | `8303d5fee96cb8e943043df3ae8fd2cd9183860b55ccf5f5dd1394c8ad06530e` |
| `database` | `c655673b6384af8f67a2be09b0f463dfab441877e377cb42105ee1a290efa101` | `2922db1a1380e56ef312016ea34c256f9faf6afe0bf8a7e489ea5df92ee7e812` |
| `diagram-tree` | `c3312eca12caebab60a2522493a59f7bf9875ab66059227a9ec0bdd68d4b0caa` | `5a1f27fd94f5731aec2e22fe57dedd6cd6a8d686ddf3a9dc7bcfab008b6576a9` |
| `export` | `ef69c5451f2e2131cf094c9401ef4e6532e7fead916b52026abd8df83ab467d0` | `271fcbc30849bca5ebcfd5f92ea33afeefc5398f965cb625b9ab644c14331012` |
| `help` | `8e8562c006b16c08f3e50566bcf90e8a77c8acfefdf2951365d477f6e0a4c68b` | `8ca7d60d8a1031ebd2a03a9d18934c6683fe195c5729f7b5b06c7954bbe58039` |
| `history` | `6422532b1c4607e9152c2ceb3f15e6a8e1f64339a6b4480a575602c345c474cb` | `edfdb3955b3d0ca04f3edff84629e7273e74387b728816dbe4dd0fa1b8e5eb37` |
| `tick-circle` | `3e5534a83c0989cadc285fc4f748a2aecbd33fc29039d90da591c9b0b2681fc9` | `99dfcea0b90e42742afd60f174fc28a18ce94ed5d1ced3ce90568c9e8121166d` |
| `warning-sign` | `d8e4ae34fc1f08e22d56264e5680085e30a7284f97100bfa7e7fb1188d841c66` | `617429b93029fd5411b968df8f836553bdda5ee79649181ebdb2dfa6e17c9f9d` |

## License text

Both exact npm packages contain the same Apache License 2.0 text, SHA-256
`a6cba85bc92e0cff7a450b1d873c0eaa2e9fc96bf472df0247a26bec77bf3ff9`.
One byte-identical copy is distributed at
`src/name_atlas/static/vendor/blueprint/LICENSE` and in the Python wheel.
The license applies to the Blueprint assets described above, not to replace the
repository's own MIT license.

## `@cloudflare/workers-oauth-provider` 0.8.2

The checked-in Foldweave public-gateway build depends on
[`@cloudflare/workers-oauth-provider`](https://github.com/cloudflare/workers-oauth-provider)
version 0.8.2. This dependency is MIT licensed. Its presence in the source and
lockfile is not evidence that the gateway has been deployed or publicly listed.

Copyright (c) 2025 Cloudflare, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

The installed `LICENSE.txt` used for this notice has SHA-256
`5514f48637fa1d8fed2256d12d322009a75962e6111370755fc5b20773db67ad`.

## Packaged Python runtime

The native macOS application packages the following Python runtime
distributions. Their exact installed metadata and license files are copied into
the application under their respective `*.dist-info` directories. Those files
are distributed application resources, not merely build records.

| Distribution | Version | Declared or conservatively applied license |
|---|---:|---|
| `annotated-doc` | 0.0.4 | MIT |
| `annotated-types` | 0.7.0 | MIT |
| `anyio` | 4.14.2 | MIT |
| `attrs` | 26.1.0 | MIT |
| `bagit` | 1.9.0 | Public Domain |
| `bottle` | 0.13.4 | MIT |
| `certifi` | 2026.6.17 | MPL-2.0 |
| `cffi` | 2.1.0 | MIT-0 |
| `click` | 8.4.2 | BSD-3-Clause |
| `cryptography` | 49.0.0 | Apache-2.0 OR BSD-3-Clause |
| `distro` | 1.9.0 | Apache-2.0 |
| `fastapi` | 0.139.2 | MIT |
| `h11` | 0.16.0 | MIT |
| `httpcore` | 1.0.9 | BSD-3-Clause |
| `httpx` | 0.28.1 | BSD-3-Clause |
| `httpx-sse` | 0.4.3 | MIT |
| `idna` | 3.18 | BSD-3-Clause |
| `Jinja2` | 3.1.6 | BSD-3-Clause |
| `jiter` | 0.16.0 | MIT |
| `jsonschema` | 4.26.0 | MIT |
| `jsonschema-specifications` | 2025.9.1 | MIT |
| `MarkupSafe` | 3.0.3 | BSD-3-Clause |
| `mcp` | 1.28.1 | MIT |
| `openai` | 2.46.0 | Apache-2.0 |
| `proxy_tools` | 0.1.0 | MIT metadata; BSD source-header terms also retained |
| `pydantic` | 2.13.4 | MIT |
| `pydantic_core` | 2.46.4 | MIT |
| `pydantic-settings` | 2.14.2 | MIT |
| `pycparser` | 3.0 | BSD-3-Clause |
| `PyJWT` | 2.13.0 | MIT |
| `pyobjc-core` | 12.2.1 | MIT |
| `pyobjc-framework-Cocoa` | 12.2.1 | MIT |
| `pyobjc-framework-Quartz` | 12.2.1 | MIT |
| `pyobjc-framework-Security` | 12.2.1 | MIT |
| `pyobjc-framework-UniformTypeIdentifiers` | 12.2.1 | MIT |
| `pyobjc-framework-WebKit` | 12.2.1 | MIT |
| `python-dotenv` | 1.2.2 | BSD-3-Clause |
| `python-multipart` | 0.0.32 | Apache-2.0 |
| `pywebview` | 6.2.1 | BSD-3-Clause |
| `referencing` | 0.37.0 | MIT |
| `rpds-py` | 2026.6.3 | MIT |
| `sniffio` | 1.3.1 | MIT OR Apache-2.0 |
| `sse-starlette` | 3.4.5 | BSD-3-Clause |
| `starlette` | 1.3.1 | BSD-3-Clause |
| `tqdm` | 4.68.4 | MPL-2.0 AND MIT |
| `typing-inspection` | 0.4.2 | MIT |
| `typing_extensions` | 4.16.0 | PSF-2.0 |
| `uvicorn` | 0.51.0 | BSD-3-Clause |
| `websockets` | 15.0.1 | BSD-3-Clause |

The bundled metadata contains the complete applicable license texts and
copyright notices. In particular, it preserves the Apache/BSD alternatives for
`cryptography`, the MPL-2.0 terms for the `certifi` certificate bundle, and the
PSF terms associated with `typing_extensions`.

### `proxy_tools` 0.1.0

The installed wheel metadata declares MIT. The installed source header says
BSD and attributes the original proxy code to Armin Ronacher, adapted by
Jonathan Tushman in 2014. Foldweave therefore preserves both MIT and
BSD-3-Clause terms conservatively rather than resolving this upstream metadata
disagreement in its own favor.

## CPython and incorporated libraries

The packaged application contains the following interpreter and native-library
runtime. Foldweave distributes the exact CPython license and the complete
CPython 3.11 licensing appendix as application resources under `licenses/`.

| Component | Exact version | License or terms |
|---|---:|---|
| CPython | 3.11.9 | Python Software Foundation License Version 2 and historical Python licenses |
| OpenSSL | 3.0.13 | Apache License 2.0 |
| ncurses | 5.9.20120616 | ncurses permissive license |
| XZ/liblzma | 5.2.3 | Public-domain and permissive terms described in the CPython licensing appendix |

The packaged CPython `LICENSE.txt` has SHA-256
`3b2f81fe21d181c499c59a256c8e1968455d6689d269aa85373bfb6af41da3bf`.
The complete local CPython licensing appendix, including the OpenSSL 3 terms,
has SHA-256
`2b734ec5975b21b29ae8b9756a00fc3dfe701abe51687cec4c98a21c51005bca`.

## Packaging runtime

Foldweave's native executable is produced with PyInstaller 6.21.0 and the
PyInstaller community hooks package 2026.6. The application bundle retains the
exact installed metadata and licensing material for both.

PyInstaller is distributed under GPL-2.0-or-later with its special exception
permitting use of its bootloader to produce and distribute executables under
the license chosen for the bundled application, provided that modifications to
the bootloader itself remain covered by the GNU General Public License. The
exact installed PyInstaller `COPYING.txt`, including that exception, has
SHA-256
`dcf75fdb959db1e3b41c0f8505069d2ece781b5ec6b3d0a4d30975cfc6580245`.

The PyInstaller community hooks package is Apache-2.0 licensed. Its runtime
cryptography hook is included in the executable, and its exact installed
license has SHA-256
`91d0baaff00773038e72c0a1fc9d5d2d38706b7a2b9c04f34296608f931b9cd0`.

PyInstaller, its Python build package, pytest, setuptools, Pygments, altgraph,
macholib, and packaging are build-time tools and must not appear as importable
application modules in the final Foldweave runtime. Their metadata may be
included solely where required to preserve the packaging-runtime license
notices described above.

## Native-extension provenance

The application retains the CycloneDX software-bill-of-materials files shipped
by native-extension distributions. Acceptance verifies these exact hashes:

| Packaged SBOM | SHA-256 |
|---|---|
| `cryptography-rust.cyclonedx.json` | `e88b4427a6b70097b9fead6aab292456b29a40049567c4c501a25be506a370d7` |
| `cryptography` `sbom.json` | `95022207ef86610c13d768fac68a21fbf2edd8dcefc0a143154e84c5359b7c9c` |
| `jiter-python.cyclonedx.json` | `796c92c45da906a58f452cd49c458145028487f83297bafafb07669b0bcecc0f` |
| `pydantic-core.cyclonedx.json` | `7d6726d9debc3c715f2860114b4ceccde59fa7e7b4d696953b3fc3cd3bb8a846` |

The SBOMs describe the corresponding upstream native artifacts; they do not
replace the license texts distributed with each package.
