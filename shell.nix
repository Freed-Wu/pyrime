{
  pkgs ? import <nixpkgs> { },
}:

with pkgs;
mkShell {
  name = "pyrime";
  buildInputs = [
    meson
    ninja
    pkg-config
    librime
    stdenv.cc
    (python3.withPackages (
      p: with p; [
        cython
        build
      ]
    ))
  ];
}
