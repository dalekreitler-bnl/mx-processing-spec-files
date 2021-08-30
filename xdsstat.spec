Name:           xdsstat
Version:        9.3.2019 
Release:        1%{?dist}
Summary:        A program that prints statistics from CORRECT/XSCALE HKL files
Packager:       Dale Kreitler (dkreitler@bnl.gov)

License:        Closed
URL:            https://strucbio.biologie.uni-konstanz.de/xdswiki/index.php/xdsstat
Source0:        https://strucbio.biologie.uni-constanz.de/pub/linux_bin/xdsstat

%description
A single binary executable that generates log files and tables of statistics\
from XDS_ASCII.HKL format reflection files produced by the XDS programs CORRECT\
and XSCALE.

%setup -n %{name}

%prep

%install
mkdir -p %{buildroot}%{_bindir}
cp %{_topdir}/SOURCES/%{name} %{buildroot}%{_bindir}

%files
%attr(755,-,-) %{_bindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

#%license add-license-file-here
#%doc add-docs-here

%changelog
* Sun Aug 29 2021 Dale Kreitler <dkreitler@bnl.gov>
- 
