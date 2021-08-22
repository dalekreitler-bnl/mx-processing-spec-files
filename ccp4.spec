Name:           ccp4
Version:        7.1
Release:        1%{?dist}
Summary:        Computational Crystallography Project 4 (CCP4) for MX
Packager:       Dale Kreitler (dkreitler@bnl.gov)
License:        Academic
URL:            https://www.ccp4.ac.uk
Source0:        ccp4-7.1.tar.gz

AutoReq:        no

%description
Full computational crystallography stack for macromolecular crystallography\
data reduction, data processing, model phasing, and refinement. Building from\
source seems to require a version control package (bazaar) that is not readily\
available for RHEL8. So, opted for packing pre-built Linux-x86_64 binaries.\
The required packages are required by the molecular graphics visualization\
program Coot. Downstream NSLS-II MX data processing packages that use CCP4\
programs rely on small, static subset of CCP4 capabilities. Updates to this\
package should be infrequent. Package made by Dale Kreitler (dkreitler@bnl.gov).\
Made a small modification to the BINARY.setup script to automatically accept\
license agreement so that it will automatically run as post install script.

%define __arch_install_post %{nil}
%define __os_install_post %{nil}
%prep
%setup -q -n %{name}-%{version}

%install
OPT_CCP4=%{buildroot}/opt/%{name}
mkdir -p $OPT_CCP4
cp -rfa %{_topdir}/BUILD/%{name}-%{version}/examples $OPT_CCP4
cp -rfa %{_topdir}/BUILD/%{name}-%{version}/html $OPT_CCP4
cp -rfa %{_topdir}/BUILD/%{name}-%{version}/images $OPT_CCP4
cp -rfa %{_topdir}/BUILD/%{name}-%{version}/include $OPT_CCP4
cp -rfa %{_topdir}/BUILD/%{name}-%{version}/lib $OPT_CCP4
cp -rfa %{_topdir}/BUILD/%{name}-%{version}/libexec $OPT_CCP4
cp -rfa %{_topdir}/BUILD/%{name}-%{version}/Licenses $OPT_CCP4
cp -rfa %{_topdir}/BUILD/%{name}-%{version}/bin $OPT_CCP4
cp -rfa %{_topdir}/BUILD/%{name}-%{version}/etc $OPT_CCP4
cp -rfa %{_topdir}/BUILD/%{name}-%{version}/share $OPT_CCP4
cp -rfa %{_topdir}/BUILD/%{name}-%{version}/restore $OPT_CCP4
cp -a %{_topdir}/BUILD/%{name}-%{version}/start $OPT_CCP4
cp -a %{_topdir}/BUILD/%{name}-%{version}/academic* $OPT_CCP4
cp -a %{_topdir}/BUILD/%{name}-%{version}/CHANGES $OPT_CCP4
cp -a %{_topdir}/BUILD/%{name}-%{version}/README $OPT_CCP4
cp -a %{_topdir}/BUILD/%{name}-%{version}/BINARY.setup $OPT_CCP4

%files
%dir /opt/%{name}
/opt/%{name}/*

%post
/opt/%{name}/BINARY.setup
cp /opt/%{name}/bin/ccp4.setup-sh /etc/profile.d/ccp4.sh

echo '
********************************************
CCP4 start up script added to /etc/profile.d
--------------------------------------------
Changes will only take effect when new shell
instance is started.
********************************************'

%postun
rm /etc/profile.d/ccp4.sh

%clean
rm -rf %{_topdir}/BUILD/*

#%license
#%doc add-docs-here

%changelog
* Sun Aug  8 2021 dkreitler
* Sat Aug 28 2021 dkreitler
-full stack, using pre-built binaries
-add startup script that sets ccp4 env vars to /etc/profile.d
