%define debug_package %{nil}
%define __jar_repack %{nil}

Name:       incubator-impala
Version:    2.7.0
Release:    1%{?dist}
Summary:    massively parallel processing query engine
Group:      Applications/Internet
License:    Apache 2.0
URL:        http://impala.apache.org/
Source:     %{name}-%{version}.tar.gz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Packager:   Alexander Hurd <hurdad@gmail.com>
BuildRequires: java-1.7.0-openjdk-devel
BuildRequires: maven
BuildRequires: redhat-lsb
BuildRequires: gcc-c++
BuildRequires: python-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: openssl-devel
BuildRequires: vim-common
Requires: bigtop-utils >= 0.7

AutoReqProv: no

%description
Impala is an open source massively parallel processing query engine on top of clustered systems like Apache Hadoop

%package        shell
Summary:        impala shell files
Group:          Applications/Internet
Requires: python

%description    shell
impala shell files

%package        catalog
Summary:        impala catalog daemon script
Group:          Applications/Internet

%description    catalog
impala catalog daemon script

%package        server
Summary:        impala server daemon script
Group:          Applications/Internet

%description    server
impala server daemon script

%package        state-store
Summary:        impala state-store daemon script
Group:          Applications/Internet

%description    state-store
impala state-store daemon script

%prep
%setup -q

%build
./buildall.sh -notests -release

%install
%{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}
%{__install} -d %{buildroot}/etc/impala/conf
%{__install} -d %{buildroot}/usr/bin
%{__install} -d %{buildroot}/usr/lib/impala
%{__install} -d %{buildroot}/var/lib/impala
%{__install} -d %{buildroot}/var/log/impala
%{__install} -d %{buildroot}/var/run/impala

%{__install} -d %{buildroot}/usr/lib/impala/lib
%{__cp} -rp fe/target/dependency/* %{buildroot}/usr/lib/impala/lib/
%{__cp} -p fe/target/impala-frontend-0.1-SNAPSHOT.jar %{buildroot}/usr/lib/impala/lib/
%{__cp} -rp www %{buildroot}/usr/lib/impala/

%{__install} -d %{buildroot}/usr/lib/impala/toolchain
%{__cp} -rp toolchain/gcc-4.9.2 %{buildroot}/usr/lib/impala/toolchain
%{__cp} -rp toolchain/kudu-0.8.0-RC1 %{buildroot}/usr/lib/impala/toolchain

%{__install} -d %{buildroot}/usr/lib/impala-shell
%{__cp} -rp shell/build/impala-shell-%{version}/ext-py %{buildroot}/usr/lib/impala-shell
%{__cp} -rp shell/build/impala-shell-%{version}/gen-py %{buildroot}/usr/lib/impala-shell
%{__cp} -rp shell/build/impala-shell-%{version}/lib %{buildroot}/usr/lib/impala-shell
%{__cp} -r shell/build/impala-shell-%{version}/impala_shell.py %{buildroot}/usr/lib/impala-shell
%{__cp} -r shell/build/impala-shell-%{version}/impala-shell %{buildroot}/usr/bin/
sed -i -e 's/SCRIPT_DIR=.*$/SCRIPT_DIR=\/usr\/lib\/impala-shell/g' %{buildroot}/usr/bin/impala-shell

%{__install} -d %{buildroot}/etc/security/limits.d
%{__cp} -rp %{_topdir}/limits.d/impala.conf %{buildroot}/etc/security/limits.d/

%{__install} -d %{buildroot}/etc/default
%{__cp} -p %{_topdir}/default/impala %{buildroot}/etc/default/

%{__install} -d %{buildroot}/etc/rc.d/init.d/
%{__cp} -rp %{_topdir}/init.d/* %{buildroot}/etc/rc.d/init.d/
%{__chmod} +755 %{buildroot}/etc/rc.d/init.d/*

systemctl daemon-reload

%{__cp} -p be/build/latest/service/impalad %{buildroot}/usr/bin
cd %{buildroot}/usr/bin/ && ln -s impalad catalogd
cd %{buildroot}/usr/bin/ && ln -s impalad statestored

%pre
if ! /usr/bin/id impala &>/dev/null; then
    /usr/sbin/useradd -r -d /var/lib/impala -s /bin/sh -c "impala" impala || \
        %logmsg "Unexpected error adding user \"impala\". Aborting installation."
fi

%post
systemctl daemon-reload

%preun

%postun
systemctl daemon-reload
if [ $1 -eq 0 ]; then
    /usr/sbin/userdel impala || %logmsg "User \"impala\" could not be deleted."
fi

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
/etc/security/limits.d/impala.conf
/etc/default/impala
/etc/impala/conf
/usr/bin/catalogd
/usr/bin/impalad
/usr/bin/statestored
/usr/lib/impala

%defattr(-,impala,impala,-)
/var/lib/impala
/var/log/impala
/var/run/impala

%files shell
%defattr(-,root,root,-)
/usr/bin/impala-shell
/usr/lib/impala-shell

%files catalog
%defattr(-,root,root,-)
/etc/rc.d/init.d/impala-catalog

%files server
%defattr(-,root,root,-)
/etc/rc.d/init.d/impala-server

%files state-store
%defattr(-,root,root,-)
/etc/rc.d/init.d/impala-state-store

%changelog
* Sat Dec 3 2016 Alexander Hurd <hurdad@gmail.com> 1.0.1-1
- Initial specfile writeup.