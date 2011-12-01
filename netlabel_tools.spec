Summary: Tools to manage the Linux NetLabel subsystem
Name: netlabel_tools
Version: 0.19
Release: 6%{?dist}
License: GPLv2
Group: System Environment/Daemons
URL: http://netlabel.sf.net/
Source0: http://downloads.sourceforge.net/netlabel/%{name}-%{version}.tar.gz
Source1: netlabel
Source2: netlabel.rules
Patch1: netlabel_tools-0.17-new-hdrs.patch
Patch2: netlabel_tools-0.19-return_codes.patch
BuildRoot: %{_tmppath}/%{name}-%{version}
BuildRequires: kernel-headers >= 2.6.18
BuildRequires: libnl-devel
Requires(post): chkconfig
Requires(preun): chkconfig initscripts


%description
NetLabel is a kernel subsystem which implements explicit packet labeling
protocols such as CIPSO and RIPSO for Linux.  Packet labeling is used in
secure networks to mark packets with the security attributes of the data they
contain.  This package provides the necessary user space tools to query and
configure the kernel subsystem.

%prep 
%setup -q -n %{name}-%{version}

# Build fixes.
%patch1 -p1 -b .new-hdrs
%patch2 -p1 -b .rc

%build
# Don't use _smp_mflags, it's small and a hand crafted Makefile
make

%install
rm -rf $RPM_BUILD_ROOT
make INSTALL_PREFIX=${RPM_BUILD_ROOT} \
     INSTALL_MAN_DIR=${RPM_BUILD_ROOT}/usr/share/man \
     install
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d/
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/
install -m 0640 %{SOURCE2} $RPM_BUILD_ROOT/etc/

%post
/sbin/chkconfig --add netlabel

%preun
if [ $1 = 0 ]; then
    /sbin/service netlabel stop >/dev/null 2>&1
    /sbin/chkconfig --del netlabel
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc docs/*.txt
%attr(0755,root,root) /sbin/*
%attr(0755,root,root) /etc/rc.d/init.d/netlabel
%config(noreplace) %attr(640,root,root) /etc/netlabel.rules
%attr(0644,root,root) %{_mandir}/man8/*

%changelog
* Wed Jun 16 2010 Peter Vrabec <pvrabec@redhat.com> - 0.19-6
- make initscript LSB compliant
- show version of netlabelctl and libnetlabel in help
- fixing return codes
  Resolves: #537053 #602577 #602291


* Fri Jan 29 2010 Peter Vrabec <pvrabec@redhat.com> - 0.19-5
- Do chkconfig calls in post/preun
- Add chkconfig/service as a dep
  Resolves: #555835

* Wed Jan 13 2010 Peter Vrabec <pvrabec@redhat.com> - 0.19-4
- fix license tag
- make initscript LSB compliant 
  Resolves: #537053

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.19-3.1
- Rebuilt for RHEL 6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 08 2009 Peter Vrabec <pvrabec@redhat.com> - 0.19-1
- upgrade (#478903)

* Mon Oct 27 2008 Peter Vrabec <pvrabec@redhat.com> - 0.18-1
- upgrade (#439833)

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.17-8
- fix license tag

* Mon Feb  11 2008 Steve Conklin <sconklin@redhat.com> - 0.17-7
- New patch for bz#431766 to resolve conflicts

* Thu Feb  7 2008 Steve Conklin <sconklin@redhat.com> - 0.17-6
- Various fixes to follow upstream
- Resolves bz#431765 The example configuration file is invalid
- Resolves bz#431766 The netlabelctl command fails to run due to newer libnl package
- Resolves bz#431767 The url listed in the netlabel_tools package is wrong

* Mon Oct 16 2006 James Antill <james@and.org> - 0.17-3
- Add upstream patch.
- s/p1/p0/ for upstream patch.

* Sat Oct 14 2006 Steve Grubb <sgrubb@redhat.com> - 0.17-3
- Add init scripts and default rules

* Sun Oct  1 2006 James Antill <james@and.org> - 0.17-2
- Upgrade to latest upstream.

* Tue Aug 29 2006 James Antill <james@and.org> - 0.16-5
- Fix install calls for mock.

* Tue Aug 29 2006 James Antill <james@and.org> - 0.16-4
- Fix more reviewing problems, building on newer kernel-headers.
- Add URL tag.

* Fri Aug 18 2006 James Antill <james@and.org> - 0.16-3
- Fix minor review problems.
- Added BuildRequires for kernel headers (netlink).

* Fri Aug 18 2006 James Antill <james@and.org> - 0.16-2
- Use root as owner.
- Contribute to fedora extras.

* Thu Aug  3 2006 Paul Moore <paul.moore@hp.com> 0.16-1
- Bumped version number.

* Thu Jul  6 2006 Paul Moore <paul.moore@hp.com> 0.15-1
- Bumped version number.

* Mon Jun 26 2006 Paul Moore <paul.moore@hp.com> 0.14-1
- Bumped version number.
- Changes related to including the version number in the path name.
- Changed the netlabelctl perms from 0750 to 0755.
- Removed the patch. (included in the base with edits)
- Updated the description.

* Fri Jun 23 2006 Steve Grubb <sgrubb@redhat.com> 0.13-1
- Initial build.

