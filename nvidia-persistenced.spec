Name:           nvidia-persistenced
Version:        340.98
Release:        1%{?dist}
Summary:        A daemon to maintain persistent software state in the NVIDIA driver
Epoch:          2
License:        GPLv2+
URL:            http://www.nvidia.com/object/unix.html
ExclusiveArch:  %{ix86} x86_64 armv7hl

Source0:        ftp://download.nvidia.com/XFree86/%{name}/%{name}-%{version}.tar.bz2
Source1:        %{name}.service
Source2:        %{name}.init

BuildRequires:      m4

%if 0%{?fedora} || 0%{?rhel} >= 7
BuildRequires:      systemd
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
%endif

%if 0%{?rhel} == 6
Requires(post):     /sbin/chkconfig
Requires(preun):    /sbin/chkconfig
Requires(preun):    /sbin/service
Requires(postun):   /sbin/service
%endif

Requires(pre):      shadow-utils
Requires:           nvidia-kmod-common = %{?epoch}:%{version}
Requires:           nvidia-driver-cuda = %{?epoch}:%{version}

%description
The %{name} utility is used to enable persistent software state in the NVIDIA
driver. When persistence mode is enabled, the daemon prevents the driver from
releasing device state when the device is not in use. This can improve the
startup time of new clients in this scenario.

%prep
%setup -q

%build
export CFLAGS=${RPM_OPT_FLAGS}
make %{?_smp_mflags} \
    NV_VERBOSE=1 \
    STRIP_CMD="true"

%install
make install DESTDIR=%{buildroot} INSTALL="install -p" PREFIX=%{_prefix}
mv %{buildroot}%{_bindir} %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

%if 0%{?fedora} || 0%{?rhel} >= 7

# Systemd unit files
install -p -m 644 -D %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%else

# Initscripts
install -p -m 755 -D %{SOURCE2} %{buildroot}%{_initrddir}/%{name}

%endif

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d /var/run/%{name} -s /sbin/nologin \
    -c "NVIDIA persistent software state" %{name}
exit 0

%if 0%{?fedora} || 0%{?rhel} >= 7

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%endif

%if 0%{?rhel} == 6

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 -eq 0 ]; then
    /sbin/service %{name} stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi

%endif

%files
%doc COPYING
%{_mandir}/man1/%{name}.1.*
%{_sbindir}/%{name}
%if 0%{?fedora} || 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif
%attr(750,%{name},%{name}) %{_sharedstatedir}/%{name}

%changelog
* Sun Oct 02 2016 Simone Caronni <negativo17@gmail.com> - 2:340.98-1
- Update to 340.98.

* Tue Nov 17 2015 Simone Caronni <negativo17@gmail.com> - 2:340.96-1
- Update to 340.96.

* Tue Sep 08 2015 Simone Caronni <negativo17@gmail.com> - 2:340.93-1
- Update to 340.93.

* Wed Jan 28 2015 Simone Caronni <negativo17@gmail.com> - 2:340.76-1
- Update to 340.76.

* Mon Dec 08 2014 Simone Caronni <negativo17@gmail.com> - 2:340.65-1
- Update to 340.65.

* Wed Nov 05 2014 Simone Caronni <negativo17@gmail.com> - 2:340.58-1
- Update to 340.58.

* Mon Nov 03 2014 Simone Caronni <negativo17@gmail.com> - 2:340.46-2
- Fix daemon command in systemd service file.

* Wed Oct 01 2014 Simone Caronni <negativo17@gmail.com> - 2:340.46-1
- Update to 340.46.
- Switched to GitHub sources.

* Sun Aug 17 2014 Simone Caronni <negativo17@gmail.com> - 2:340.32-1
- Update to 340.32.

* Mon Jul 14 2014 Simone Caronni <negativo17@gmail.com> - 2:340.24-2
- Add requirements on CUDA driver parts to operate.

* Tue Jul 08 2014 Simone Caronni <negativo17@gmail.com> - 2:340.24-1
- Update to 340.24.

* Mon Jun 09 2014 Simone Caronni <negativo17@gmail.com> - 2:340.17-1
- Update to 340.17.

* Mon Jun 02 2014 Simone Caronni <negativo17@gmail.com> - 2:337.25-1
- Update to 337.25.

* Tue May 06 2014 Simone Caronni <negativo17@gmail.com> - 2:337.19-1
- Update to 337.19.

* Tue Apr 08 2014 Simone Caronni <negativo17@gmail.com> - 2:337.12-1
- Update to 337.12.

* Tue Mar 04 2014 Simone Caronni <negativo17@gmail.com> - 2:334.21-1
- Update to 334.21.

* Wed Feb 19 2014 Simone Caronni <negativo17@gmail.com> - 2:331.49-1
- Update to 331.49.

* Tue Jan 14 2014 Simone Caronni <negativo17@gmail.com> - 2:331.38-1
- Update to 331.38.

* Mon Dec 23 2013 Simone Caronni <negativo17@gmail.com> - 2:331.20-2
- Do not strip binaries during build, let rpm generate debuginfo files.

* Thu Nov 07 2013 Simone Caronni <negativo17@gmail.com> - 2:331.20-1
- Update to 331.20.

* Wed Oct 23 2013 Simone Caronni <negativo17@gmail.com> - 2:331.17-1
- Updated to 331.17.

* Fri Oct 04 2013 Simone Caronni <negativo17@gmail.com> - 2:331.13-1
- Update to 331.13.

* Mon Sep 09 2013 Simone Caronni <negativo17@gmail.com> - 2:325.15-1
- Update to 325.15.

* Wed Aug 21 2013 Simone Caronni <negativo17@gmail.com> - 2:319.49-1
- Updated to 319.49.

* Mon Aug 05 2013 Simone Caronni <negativo17@gmail.com> - 2:319.32-3
- Fedora 17 has gone EOL.

* Wed Jul 03 2013 Simone Caronni <negativo17@gmail.com> - 2:319.32-2
- Add armv7hl support.

* Fri Jun 28 2013 Simone Caronni <negativo17@gmail.com> - 1:319.32-1
- Update to 319.32.

* Fri May 24 2013 Simone Caronni <negativo17@gmail.com> - 1:319.23-1
- Update to 319.23.

* Thu May 02 2013 Simone Caronni <negativo17@gmail.com> - 1:319.17-1
- First build.
