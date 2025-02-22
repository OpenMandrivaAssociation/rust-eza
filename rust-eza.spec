# Rust packages always list license files and docs
# inside the crate as well as the containing directory
%undefine _duplicate_files_terminate_build
%bcond_without check

# prevent library files from being installed
%global __cargo_is_lib() 0

%global crate eza

Name:           rust-eza
Version:        0.20.22
Release:        1
Summary:        Modern replacement for ls
Group:          Development/Rust

License:        EUPL-1.2
URL:            https://crates.io/crates/eza
Source0:        %{crates_source}
Source1:        %{name}-%{version}-vendor.tar.xz
# Automatically generated patch to strip dependencies and normalize metadata
Patch:          eza-fix-metadata-auto.diff

ExclusiveArch:  %{rust_arches}

BuildRequires:  cargo
BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
A modern replacement for ls.}

%description %{_description}

%files
%license LICENSE.txt
%license LICENSES/CC-BY-4.0.txt
%license LICENSE.dependencies
%license cargo-vendor.txt
%doc CHANGELOG.md
%doc CODE_OF_CONDUCT.md
%doc CONTRIBUTING.md
%doc INSTALL.md
%doc README.md
%doc SECURITY.md
%doc TESTING.md
%{_bindir}/eza
%{_datadir}/bash-completion/completions/eza
%{_datadir}/fish/completions/eza.fish
%{_datadir}/zsh/site-functions/_eza

%prep
%autosetup -n %{crate}-%{version} -p1 -a1
%cargo_prep -v vendor

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%{cargo_vendor_manifest}
rm -fr %{buildroot}/usr/src/debug
rm -fr %{buildroot}/usr/lib/debug
rm -fr %{buildroot}/usr/share/cargo

%install
%cargo_install
# install shell completions
install -Dpm 0644 completions/bash/eza -t %{buildroot}/%{_datadir}/bash-completion/completions/
install -Dpm 0644 completions/fish/eza.fish -t %{buildroot}/%{_datadir}/fish/completions/
install -Dpm 0644 completions/zsh/_eza -t %{buildroot}/%{_datadir}/zsh/site-functions/
rm -fr %{buildroot}/usr/share/cargo

