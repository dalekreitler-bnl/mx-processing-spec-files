Name:           eiger2cbf 
Version:        2020.10.14 
Release:        1%{?dist}
Summary:        Library and executables for fast hdf5 array decompression
Packager:       Dale Kreitler (dkreitler@bnl.gov)
License:        BSD 
URL:            https://github.com/dalekreitler-bnl/eiger2cbf
Source0:        https://github.com/dalekreitler-bnl/eiger2cbf

BuildRequires:  cbflib
BuildRequires:  zlib-devel
BuildRequires:  hdf5-devel
Requires:       hdf5-devel
Requires:       cbflib

%description
eiger2cbf uses bitshuffle lz4 decompression to convert hdf5 arrays that\
correspond to individual 2D diffraction images into crystallographic binary\
format (CBF), eiger2cbf uses libcbf.so in addition to C headers provided by
cbflib, which is a prerequisite for building and running. 

%setup -q -n %{name}

%prep
cd %{_topdir}/BUILD
rm -rf %{name}
cp -rf %{_topdir}/SOURCES/%{name} .

%build
cd %{name}
make

%install
mkdir -p %{buildroot}%{_libdir}
cp %{_topdir}/BUILD/%{name}/lib/eiger2cbf.so %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_bindir}
cp %{_topdir}/BUILD/%{name}/bin/eiger2cbf %{buildroot}%{_bindir}
cp %{_topdir}/BUILD/%{name}/bin/eiger2cbf_4t %{buildroot}%{_bindir}
cp %{_topdir}/BUILD/%{name}/bin/eiger2params %{buildroot}%{_bindir}
cp %{_topdir}/BUILD/%{name}/bin/eiger2cbf-so-worker %{buildroot}%{_bindir}

%files
%{_libdir}/eiger2cbf.so
%{_bindir}/eiger2cbf
%{_bindir}/eiger2cbf_4t
%{_bindir}/eiger2params
%{_bindir}/eiger2cbf-so-worker

#%license add-license-file-here
#%doc add-docs-here

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Aug 18 2021 Dale Kreitler <dkreitler@bnl.gov>
-initial commit
