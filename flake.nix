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
            name = "fetch-ing-prices";
            version = "2024-07-21";

            src = pkgs.fetchFromGitHub {
              owner = "matthiasbeyer";
              repo = "fetch-ing-prices";
              rev = "a3c75253f7e1fc24eb4e269cdf43cc810b0aea0f";
              sha256 = "sha256-oc+cl8XtPgDNummh9FQIF3yLdeNo3p4ijBCzdmnqzl4=";
            };

            buildInputs = [
              pkgs.python3Packages.requests
            ];

            installPhase = ''
              mkdir $out/bin -p
              cp -v fetch-ing-prices.py $out/bin/fetch-ing-prices
            '';

            meta = {
              homepage = "https://github.com/matthiasbeyer/fetch-ing-prices";
              description = "Fetch Stock prices from the ING website";
              license = pkgs.lib.licenses.mit;
              maintainers = [ pkgs.lib.maintainers.matthiasbeyer ];
              platforms = pkgs.lib.platforms.all;
              mainProgram = "fetch-ing-prices";
            };
          };
        };

        apps.default = flake-utils.lib.mkApp {
          name = "fetch-ing-prices";
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
