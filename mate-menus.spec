Summary:	Displays menus for MATE Desktop
Name:		mate-menus
Version:	1.5.0
Release:	1
License:	GPL v2+ and LGPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.5/%{name}-%{version}.tar.xz
# Source0-md5:	fc36e94245d8508cda14c2cd436aad5a
URL:		http://wiki.mate-desktop.org/mate-menus
BuildRequires:	gobject-introspection-devel
BuildRequires:	intltool >= 0.40.0
BuildRequires:	mate-common >= 1.5
BuildRequires:	python-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Displays menus for MATE Desktop.

%package libs
Summary:	Shared libraries for mate-menus
Group:		Libraries

%description libs
Shared libraries for mate-menus

%package devel
Summary:	Development files for mate-menus
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Development files for mate-menus

%prep
%setup -q

%build
NOCONFIGURE=1 ./autogen.sh
%configure \
	--disable-static \
	--enable-python \
	--enable-introspection=yes

# XXX: libtool it creates is broken. fix is to use libtool from system
# http://sprunge.us/fIIF
%{__make} -j1 \
	LIBTOOL=libtool \
	V=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmate-menu.{a,la}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/matemenu.{a,la}

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/gn
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/io

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING README
%{_sysconfdir}/xdg/menus/mate-applications.menu
%{_sysconfdir}/xdg/menus/mate-settings.menu
%{_datadir}/mate-menus
%{_datadir}/mate/desktop-directories

%files libs
%defattr(644,root,root,755)
%{_libdir}/girepository-1.0/MateMenu-2.0.typelib
%attr(755,root,root) %{_libdir}/libmate-menu.so.*.*.*
%ghost %{_libdir}/libmate-menu.so.2
%attr(755,root,root) %{py_sitedir}/matemenu.so

%files devel
%defattr(644,root,root,755)
%{_libdir}/libmate-menu.so
%{_datadir}/gir-1.0/MateMenu-2.0.gir
%{_includedir}/mate-menus
%{_pkgconfigdir}/libmate-menu.pc
