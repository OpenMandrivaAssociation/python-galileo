%define	oname	galileo

Name:		python-%{oname}
Version:	0.5
%define	dev	dev
Release:	%{?dev:0.%{dev}.}1
Summary:	Utility to securely synchronize a Fitbit tracker with the Fitbit server
Source0:	http://pypi.python.org/packages/source/g/%{oname}/%{oname}-%{version}%{?dev}.tar.xz
License:	LGPLv3+
Group:		Development/Python
Url:		https://bitbucket.org/benallard/galileo
BuildArch:	noarch
BuildRequires:	pythonegg(setuptools)
Requires(pre,postun):rpm-helper

%description
Galileo is a Python utility to securely synchronize a Fitbit device with the
Fitbit web service. It allows you to browse your data on their website, and
compatible applications.

All Bluetooth-based trackers are supported. Those are:

- Fitbit One
- Fitbit Zip
- Fitbit Flex
- Fitbit Force
- Fitbit Charge

.. note:: The Fitbit Ultra tracker is **not supported** as it communicates
	  using the ANT protocol. To synchronize it, please use libfitbit_.

This utility is mainly targeted at Linux because Fitbit does not
provide any Linux-compatible software, but as Python is
cross-platform and the libraries used are available on a broad variety
of platforms, it should not be too difficult to port it to other
platforms.

%prep
%setup -q -n %{oname}-%{version}%{?dev}

%build
python setup.py build

%install
python setup.py install --root=%{buildroot}
install -m644 99-fitbit.rules -D %{buildroot}%{_udevrulesdir}/99-fitbit.rules
install -m644 contrib/galileo.service -D %{buildroot}%{_unitdir}/galileo.service
install -m644 doc/galileo.1 -D %{buildroot}%{_mandir}/man1/galileo.1
install -m644 doc/galileorc.5 -D %{buildroot}%{_mandir}/man5/galileorc.5
install -m644 galileorc.sample -D %{buildroot}%{_sysconfdir}/galileorc
install -d %{buildroot}%{_localstatedir}/lib/galileo

%pre
%_pre_useradd galileo %{_localstatedir}/lib/galileo /sbin/nologin

%postun
%_postun_userdel galileo

%check
#python setup.py test

%files
%doc README.txt CHANGES
%{_bindir}/galileo 
%attr(755,galileo,galileo) %dir %{_localstatedir}/lib/galileo
%{_mandir}/man1/galileo.1*
%{_mandir}/man5/galileorc.5*
%{py_puresitedir}/galileo/*.py*
%{py_puresitedir}/galileo*.egg-info
%config(noreplace) %{_sysconfdir}/galileorc
%{_udevrulesdir}/99-fitbit.rules
%{_unitdir}/galileo.service

%changelog
* Thu Dec  4 2014 Per Øyvind Karlsen <proyvind@moondrake.org> 0.5-0.dev.1
- Initial release
