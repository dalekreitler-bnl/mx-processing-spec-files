Name:           ccp4
Version:        7.1
Release:        1%{?dist}
Summary:        Computational Crystallography Project 4 (CCP4) for MX
Packager:       Dale Kreitler (dkreitler@bnl.gov)
License:        Academic
URL:            https://www.ccp4.ac.uk
Source0:        ccp4-7.1.tar.gz

AutoReq:        no

Requires:       compat-libgfortran-48
Requires:       lapack

%description
Minimal computational crystallography stack for macromolecular crystallography\
data reduction, data processing, model phasing, and refinement. Building from\
source seems to require a version control package (bazaar) that is not readily\
available for RHEL8 (as rpm). So, opted for packing pre-built Linux-x86_64 binaries.\
Downstream NSLS-II MX data processing packages that use CCP4\
programs rely on small, static subset of CCP4 capabilities. Updates to this\
package should be infrequent.\
Some CCP4 programs use environment variables as shell script, pertinent variables\
were extracted and placed as startup script in /etc/profile.d

%define __arch_install_post %{nil}
%define __os_install_post %{nil}
%prep
%setup -q -n %{name}-%{version}

%install
#setup buildroot dirs
BINDIR=%{buildroot}%{_bindir}
LIBDIR=%{buildroot}%{_libdir}/%{name}
SHAREDIR=%{buildroot}%{_datadir}/%{name}
OPTBINDIR=%{buildroot}%{_prefix}/opt/bin
mkdir -p $BINDIR
mkdir -p $LIBDIR
mkdir -p $SHAREDIR
mkdir -p $OPTBINDIR

CCP4BUILD=%{_topdir}/BUILD/%{name}-%{version}
#licences
mkdir -p $SHAREDIR/licenses
cp $CCP4BUILD/academic_software_licence* $SHAREDIR/licenses

#fast_dp binaries
cp $CCP4BUILD/bin/pointless $BINDIR
cp $CCP4BUILD/bin/aimless $BINDIR

#dimple binaries
cp $CCP4BUILD/bin/phaser $BINDIR
cp $CCP4BUILD/bin/refmac5 $BINDIR
cp $CCP4BUILD/bin/truncate $OPTBINDIR/truncate
cp $CCP4BUILD/bin/unique $BINDIR
cp $CCP4BUILD/bin/cad $BINDIR
cp $CCP4BUILD/bin/reindex $BINDIR
cp $CCP4BUILD/bin/freerflag $BINDIR
cp $CCP4BUILD/bin/rwcontents $BINDIR
cp $CCP4BUILD/bin/pdbset $BINDIR
cp $CCP4BUILD/bin/mtzdump $BINDIR
cp $CCP4BUILD/bin/find-blobs $BINDIR

#shared ccp4 libraries
cp $CCP4BUILD/lib/libcctbx* $LIBDIR
cp $CCP4BUILD/lib/libccp4* $LIBDIR
cp $CCP4BUILD/lib/libclipper* $LIBDIR
cp $CCP4BUILD/lib/libmmdb2.so $LIBDIR
cp $CCP4BUILD/lib/libiotbx* $LIBDIR
cp $CCP4BUILD/lib/libmmtbx* $LIBDIR
cp $CCP4BUILD/lib/libboost* $LIBDIR
cp $CCP4BUILD/lib/libccif* $LIBDIR
cp $CCP4BUILD/lib/libomptbx* $LIBDIR
cp $CCP4BUILD/lib/libtcl8* $LIBDIR
cp $CCP4BUILD/lib/lib*fftw* $LIBDIR

#platform independent libraries
cp $CCP4BUILD/lib/ccp4/cif_mmdic.lib $SHAREDIR
cp $CCP4BUILD/lib/data/syminfo.lib $SHAREDIR
cp $CCP4BUILD/lib/data/symop.lib $SHAREDIR
cp $CCP4BUILD/lib/data/atomsf.lib $SHAREDIR
cp $CCP4BUILD/lib/data/crossec.lib $SHAREDIR
cp $CCP4BUILD/share/ccif/cif_mm.dic $SHAREDIR
cp $CCP4BUILD/include/*.def $SHAREDIR
#cp $CCP4BUILD/lib/data $SHAREDIR
cp -ra $CCP4BUILD/lib/data/monomers $SHAREDIR

#add /usr/lib64/ccp4 to lookup
mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "%{_libdir}/%{name}" >> %{name}.conf
mv %{name}.conf %{buildroot}%{_sysconfdir}/ld.so.conf.d

#put CCP4 env vars into default startup sh
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
cat > %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh<<EOF
export CINCL=%{_datadir}/%{name}/
export CCP4_SCR=/tmp/
export CCP4_OPEN=UNKNOWN
export CLIBD_MON=%{_datadir}/%{name}/monomers/ #refmac5 bug requires / at end
export CLIBD=%{_datadir}/%{name}/
export MMCIFDIC=%{_datadir}/%{name}/
export PATH=/usr/opt/bin:\$PATH
EOF

#cctbx
cat > %{buildroot}%{_bindir}/ccp4-python<<EOF
#!/bin/sh
# ccp4-python can be used before the setup is sourced (e.g. during build)
OPTCCP4="/opt/ccp4"
export LIBTBX_BUILD=\$OPTCCP4/lib/py2/cctbx
export PYTHONPATH=\$OPTCCP4/lib/python2.7/site-packages
export PYTHONPATH=\$PYTHONPATH:\$OPTCCP4/lib/py2
export PYTHONPATH=\$PYTHONPATH:\$OPTCCP4/lib/py2/site-packages
export PYTHONPATH=\$PYTHONPATH:\$LIBTBX_BUILD/../site-packages
export PYTHONPATH=\$PYTHONPATH:\$LIBTBX_BUILD/../site-packages/cctbx_project
export PYTHONPATH=\$PYTHONPATH:\$LIBTBX_BUILD/../site-packages/cctbx_project/libtbx/pythonpath
export PYTHONPATH=\$PYTHONPATH:\$LIBTBX_BUILD/lib
export CCP4=/opt/%{name} #a necessary hack for dimple
exec \$OPTCCP4/libexec/python2.7 "\$@"
EOF

chmod 755 %{buildroot}%{_bindir}/ccp4-python

mkdir -p %{buildroot}/opt/%{name}/lib
OPTCCP4LIB=%{buildroot}/opt/%{name}/lib

#non MX python2 packages such as six, futures
cp -rf $CCP4BUILD/lib/python2.7 $OPTCCP4LIB

#non-standard MX python2 packages 
mkdir -p $OPTCCP4LIB/py2
cp -rf $CCP4BUILD/lib/py2/cctbx $OPTCCP4LIB/py2
cp -rf $CCP4BUILD/lib/py2/dimple $OPTCCP4LIB/py2

#MX python2 packages required for dimple, fast_dp
mkdir -p $OPTCCP4LIB/py2/site-packages
cp -rf $CCP4BUILD/lib/py2/site-packages/boost $OPTCCP4LIB/py2/site-packages
cp -rf $CCP4BUILD/lib/py2/site-packages/cctbx_project $OPTCCP4LIB/py2/site-packages
cp -rf $CCP4BUILD/lib/py2/site-packages/ccp4io $OPTCCP4LIB/py2/site-packages
cp -rf $CCP4BUILD/lib/py2/site-packages/dxtbx $OPTCCP4LIB/py2/site-packages

#for hashlib
cp $CCP4BUILD/lib/libssl* $OPTCCP4LIB
cp $CCP4BUILD/lib/libcrypto* $OPTCCP4LIB
#for cctbx
cp $CCP4BUILD/lib/libboost_system* $OPTCCP4LIB
cp $CCP4BUILD/lib/libboost_thread* $OPTCCP4LIB
cp $CCP4BUILD/lib/libboost_python* $OPTCCP4LIB
cp $CCP4BUILD/lib/libpython2.7.so* $OPTCCP4LIB
cp $CCP4BUILD/lib/libscitbx_slatec* $OPTCCP4LIB
cp $CCP4BUILD/lib/libscitbx_boost_python* $OPTCCP4LIB
cp $CCP4BUILD/lib/libasymmetric_map.so $OPTCCP4LIB
cp $CCP4BUILD/lib/libcctbx.so $OPTCCP4LIB
cp $CCP4BUILD/lib/libjpeg* $OPTCCP4LIB

mkdir -p %{buildroot}/opt/%{name}/libexec
cp -rf $CCP4BUILD/libexec/python2.7 %{buildroot}/opt/%{name}/libexec

#another hack for dimple, note relative links
mkdir -p %{buildroot}/opt/%{name}/bin
cd %{buildroot}/opt/%{name}/bin
cp -s ../../..%{_bindir}/pointless .
cp -s ../../..%{_bindir}/reindex .
cp -s ../../../usr/opt/bin/truncate .
cp -s ../../..%{_bindir}/phaser .
cp -s ../../..%{_bindir}/refmac5 .
cp -s ../../..%{_bindir}/unique .
cp -s ../../..%{_bindir}/pdbset .
cp -s ../../..%{_bindir}/freerflag .
cp -s ../../..%{_bindir}/rwcontents .
cp -s ../../..%{_bindir}/cad .
cp -s ../../..%{_bindir}/mtzdump .
cp -s ../../..%{_bindir}/find-blobs .

#ccp4 python2.7 comes with it's own library, need to update rpath
exec %{buildroot}/opt/%{name}/libexec/python2.7 -Wignore -m compileall %{buildroot}/opt/%{name}/lib/py2 %{buildroot}/opt/%{name}/python2.7

%files
%{_bindir}/pointless
%{_bindir}/aimless
%{_bindir}/phaser
%{_bindir}/refmac5
%{_bindir}/pdbset
%{_bindir}/rwcontents
%{_bindir}/freerflag
%{_bindir}/reindex
%{_bindir}/cad
%{_bindir}/unique
%{_bindir}/mtzdump
%{_bindir}/find-blobs
%{_prefix}/opt/bin/truncate
%{_libdir}/%{name}/lib*.so*
%{_datadir}/%{name}/*
%{_datadir}/%{name}/licenses/*
%{_sysconfdir}/ld.so.conf.d/%{name}.conf
%{_sysconfdir}/profile.d/%{name}.sh

#python
%{_bindir}/ccp4-python
/opt/%{name}/bin/*
/opt/%{name}/lib/*
/opt/%{name}/libexec/*

%post -p /sbin/ldconfig

%clean
rm -rf %{_topdir}/BUILD/*
rm -rf %{buildroot}/%{name}-%{version}

#%license
#%doc add-docs-here

%changelog
* Sun Aug  8 2021 dkreitler
-inital commit for pointless, aimless, truncate, refmac5, phaser 
