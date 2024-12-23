{
  pkgs ? import <nixpkgs> { },
}:

with pkgs;
mkShell {
  name = "pyrime";
  buildInputs = [
    librime

    stdenv.cc
    pkg-config
    meson
    ninja

    (python3.withPackages (
      p: with p; [
        build
        pytest

        cython
        autopxd2
      ]
    ))
  ];
}
