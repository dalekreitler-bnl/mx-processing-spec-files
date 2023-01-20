Name:		crystfel		           
Version:        0.10.1
Release:        1%{?dist}
Summary:        XFEL processing software suite

License:        GNU General Public
URL:            https://www.desy.de/~twhite/crystfel
Source0:        crystfel-0.10.1.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  bison
BuildRequires:  meson
BuildRequires:  ninja-build
Requires:       hdf5-devel
Requires:       gsl-devel
Requires:       gtk3-devel
Requires:       cairo-devel
Requires:       pango-devel
Requires:       fftw-devel
Requires:       zeromq-devel
Requires:       msgpack-devel
Requires:       flex

%description
Data processing software for XFEL data

%prep
%autosetup -c

%build
%meson
%meson_build

%install
%meson_install


rm -rf $RPM_BUILD_ROOT

%files
%{_libdir}/lib%{name}.so.*
#%license add-license-file-here
#%doc add-docs-here

%changelog
* Fri Jan 20 2023 Kreitler, Dale <dkreitler@bnl.gov>
- 
