{
  description = "A utility to fetch stock prices from the ING website";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-24.05";
    flake-utils = {
      url = "github:numtide/flake-utils";
    };
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      rec {
        packages = {
          default = pkgs.python3Packages.buildPythonApplication {
            name = "fetch_ing_price";
            version = "2024-07-21";

            src = ./.;

            buildInputs = [
              pkgs.python3Packages.requests
            ];

            meta = {
              homepage = "https://github.com/matthiasbeyer/fetch-ing-prices";
              description = "Fetch Stock prices from the ING website";
              license = pkgs.lib.licenses.mit;
              maintainers = [ pkgs.lib.maintainers.matthiasbeyer ];
              platforms = pkgs.lib.platforms.all;
              mainProgram = "fetch_ing_price";
            };
          };
        };

        apps.default = flake-utils.lib.mkApp {
          name = "fetch_ing_price";
          drv = packages.default;
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [
            pkgs.python3
            pkgs.python3Packages.requests
          ];
        };
      }
    );
}
