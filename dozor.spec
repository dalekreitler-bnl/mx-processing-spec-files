Name:           dozor 
Version:        2020_08_10
Release:        1%{?dist}
Summary:        Fortran binaries for fast MX spot finding and filtering
License:        closed
URL:            https://code.nsls2.bnl.gov/mx-processing-software/dozor-10Aug2020
Source0:        dozor-2020_08_10.tar.gz
BuildRequires:  gcc-gfortran
Requires:       glibc

%description
Fast, parallel MX spotfinding application developed by Gleb Bourenkov (EMBL)\
and Sasha Popov (ESRF). Kindly provided to NSLS-II MX staff by Gleb via\
private email. Reads hdf5 files directly and reliably filters ice and small\
molecule lattices from results. Requires a configuration that contains\
separate detector parameters.

%define debug_package %{nil}

%prep
%setup -q -n %{name}-%{version}

%build
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}/%{_bindir}
cp %{_topdir}/BUILD/%{name}-%{version}/%{name} %{buildroot}/%{_bindir}

%files
%{_bindir}/dozor
#%license add-license-file-here
#%doc add-docs-here

%clean
rm -rf %{_topdir}/BUILD/%{name}-%{version}
%changelog
* Sun Aug  8 2021 dkreitler
- 
