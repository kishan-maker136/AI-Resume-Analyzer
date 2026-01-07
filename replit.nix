{ pkgs }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python311
    pkgs.python311Packages.pip
  ];

  shellHook = ''
    pip install --upgrade pip
    pip install flask fla resume-parser
  '';
}
