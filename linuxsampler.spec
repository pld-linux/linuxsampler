#
# Conditional build:
%bcond_with	tests		# build with tests
#
Summary:	LinuxSampler - free, streaming capable open source pure software audio sampler
Name:		linuxsampler
Version:	2.1.0
Release:	0.1
License:	GPL v2
Group:		Applications
Source0:	http://download.linuxsampler.org/packages/%{name}-%{version}.tar.bz2
# Source0-md5:	c57fbd1310e9189ee72acf81e63bf3d5
Patch0:		ladspa_dir.patch
Patch1:		lib_location.patch
URL:		https://www.linuxsampler.org/
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	libgig-devel >= 4.1.0
BuildRequires:	libsndfile-devel
BuildRequires:	libtool
BuildRequires:	lv2-devel
BuildRequires:	sqlite3-devel
%if %{with tests}
BuildRequires:	cppunit-devel
%endif
Requires:	%{name}-lib = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoprovfiles	%{_libdir}/(dssi|lv2|linuxsampler/plugins)

%description
The LinuxSampler project was founded in 2002 with the goal to produce
a free, streaming capable open source pure software audio sampler with
high stability, efficiency and very low latency, providing
professional grade features, comparable to both hardware and
commercial Windows/Mac software samplers and to introduce new features
not yet available by any other sampler in the world.

%package dssi
Summary:	LinuxSampler as a DSSI plugin
Group:		Applications/Sound
Requires:	%{name}-lib = %{version}-%{release}

%description dssi
The LinuxSampler project was founded in 2002 with the goal to produce
a free, streaming capable open source pure software audio sampler with
high stability, efficiency and very low latency, providing
professional grade features, comparable to both hardware and
commercial Windows/Mac software samplers and to introduce new features
not yet available by any other sampler in the world.

This package provides the sampler as a DSSI plugin.

%package lv2
Summary:	LinuxSampler as a DSSI plugin
Group:		Applications/Sound
Requires:	%{name}-lib = %{version}-%{release}

%description lv2
The LinuxSampler project was founded in 2002 with the goal to produce
a free, streaming capable open source pure software audio sampler with
high stability, efficiency and very low latency, providing
professional grade features, comparable to both hardware and
commercial Windows/Mac software samplers and to introduce new features
not yet available by any other sampler in the world.

This package provides the sampler as an LV2 plugin.

%package lib
Summary:	LinuxSampler library
Group:		Libraries

%description lib
Library for the LinuxSampler project.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name}-lib = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -q

%patch0 -p1
%patch1 -p1

sed -i -e's@/usr/lib/ladspa@%{_libdir}/ladspa@' ./Documentation/lscp.xml

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}

%configure \
	--disable-arts-driver \
	--disable-artstest \
	--disable-asio-driver \
	--disable-midishare-driver \
	--disable-coremidi-driver \
	--disable-coreaudio-driver \
	--disable-mmemidi-driver

%{__make}

%{?with_tests:%{__make} tests}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/dssi/*{.la,.a}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lv2/*/*{.la,.a}

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ -e /var/lib/%{name}/instruments.db ] || %{_bindir}/%{name} --create-instruments-db /var/lib/%{name}/instruments.db || :

%post	lib -p /sbin/ldconfig
%postun	lib -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README

%attr(755,root,root) %{_bindir}/linuxsampler
%attr(755,root,root) %{_bindir}/ls_instr_script
%attr(755,root,root) %{_bindir}/lscp

%{_mandir}/man1/linuxsampler.1*
%{_mandir}/man1/lscp.1*

%dir /var/lib/%{name}
%ghost /var/lib/%{name}/instruments.db

%files lib
%defattr(644,root,root,755)
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_libdir}/liblinuxsampler.so.5.*.*
%ghost %attr(755,root,root) %{_libdir}/liblinuxsampler.so.5

%files dssi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/dssi/linuxsampler.so

%files lv2
%defattr(644,root,root,755)
%dir %{_libdir}/lv2/linuxsampler.lv2
%{_libdir}/lv2/linuxsampler.lv2/*.ttl
%attr(755,root,root) %{_libdir}/lv2/linuxsampler.lv2/linuxsampler.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
%attr(755,root,root) %{_libdir}/liblinuxsampler.so
%{_pkgconfigdir}/%{name}.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/liblinuxsampler.a
