{ pkgs ? import <nixpkgs> { }}:
pkgs.mkShell {
  nativeBuildInputs = with pkgs; [
    # (octave.withPackages (opkgs: with opkgs; [ symbolic ]))
    python312Packages.pip
    python312Packages.playwright
    python312Packages.jmespath
    playwright

    playwright-driver.browsers
  ];

  shellHook = ''
      export PLAYWRIGHT_BROWSERS_PATH=${pkgs.playwright-driver.browsers}
      export PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=true
    '';
}
