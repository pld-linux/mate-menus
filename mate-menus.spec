Summary:	Displays menus for MATE Desktop
Name:		mate-menus
Version:	1.5.0
Release:	1
License:	GPLv2+ and LGPLv2+
Group:		X11/Applications
URL:		http://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/1.5/%{name}-%{version}.tar.xz
# Source0-md5:	fc36e94245d8508cda14c2cd436aad5a
BuildRequires:	gobject-introspection-devel
BuildRequires:	mate-common
BuildRequires:	python-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# we don't want to provide private python extension libs
#filter_provides_in %{python_sitearch}/.*\.so$

%description
Displays menus for MATE Desktop

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
NOCONFIGURE=1 ./autogen.sh

%build
%configure \
	--disable-static \
	--enable-python \
	--enable-introspection=yes

%{__make} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmate-menu.la
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/matemenu.la

rm -r $RPM_BUILD_ROOT%{_localedir}/gn
rm -r $RPM_BUILD_ROOT%{_localedir}/io

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
