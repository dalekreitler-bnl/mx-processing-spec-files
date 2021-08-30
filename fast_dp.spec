# Created by pyp2rpm-3.3.7
%global pypi_name fast_dp
%global pypi_version 1.6.2

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        Fast DP: Fast Data Processsing with XDS
Packager:       Dale Kreitler (dkreitler@bnl.gov)
License:        Apache-2.0
URL:            https://github.com/DiamondLightSource/fast_dp
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  ccp4
Requires:       ccp4
Requires:       xdsstat
Requires:       neggia
Requires:       XDS

Prefix:         /opt/ccp4

%define _prefix /opt/ccp4

%description
 Fast DP: Fast Data Processsing with XDS .. image::

%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
 Fast DP: Fast Data Processsing with XDS .. image::

%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{_prefix}/libexec/python2.7 setup.py build

%install
rm -rf %{buildroot}/%{pypi_name}-%{pypi_version}
mkdir -p %{buildroot}%{_prefix}/lib/python2.7/site-packages
export PYTHONPATH=%{buildroot}%{_prefix}/lib/python2.7/site-packages
%{_prefix}/libexec/python2.7 setup.py install --prefix %{buildroot}%{_prefix}

%check
#disabled, unable to install required python packages
#%{__python2} setup.py test

%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{_prefix}/bin/fast_dp
%{_prefix}/bin/fast_rdp
%{_prefix}/lib/python2.7/site-packages/*

%changelog
* Sun Aug 29 2021 Dale Kreitler <dkreitler@bnl.gov> - 1.6.2-1
- Initial package.
