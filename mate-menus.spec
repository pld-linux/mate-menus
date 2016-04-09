Summary:	Displays menus for MATE Desktop
Summary(pl.UTF-8):	Wyświetlanie menu w środowisku MATE Desktop
Name:		mate-menus
Version:	1.14.0
Release:	1
# only (unpackaged) python example is GPL
License:	LGPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.14/%{name}-%{version}.tar.xz
# Source0-md5:	0143cbc50fe69f9c9012c23cc007c91b
Patch0:		xdg-menu-prefix-compat.patch
URL:		http://wiki.mate-desktop.org/mate-menus
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.9
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.36.0
BuildRequires:	gobject-introspection-devel >= 0.6.7
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libtool >= 1:1.4.3
BuildRequires:	mate-common >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	rpm-pythonprov
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Displays menus for MATE Desktop.

%description -l pl.UTF-8
Wyświetlanie menu w środowisku MATE Desktop.

%package libs
Summary:	Shared libmate-menu library
Summary(pl.UTF-8):	Biblioteka współdzielona libmate-menu
Group:		Libraries
Requires:	glib2 >= 1:2.36.0

%description libs
Shared libmate-menu library.

%description libs -l pl.UTF-8
Biblioteka współdzielona libmate-menu.

%package devel
Summary:	Development files for libmate-menu library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libmate-menu
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.36.0

%description devel
Development files for libmate-menu library.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki libmate-menu.

%package -n python-matemenu
Summary:	Python binding for mate-menus library
Summary(pl.UTF-8):	Wiązanie Pythona do biblioteki mate-menus
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}

%description -n python-matemenu
Python binding for mate-menus library.

%description -n python-matemenu -l pl.UTF-8
Wiązanie Pythona do biblioteki mate-menus.

%prep
%setup -q
%patch0 -p1

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-introspection \
	--enable-python \
	--disable-silent-rules \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmate-menu.la
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/matemenu.la
# just example
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/mate-menus/examples
# empty dir
rmdir $RPM_BUILD_ROOT%{_datadir}/mate-menus
# not supported by glibc
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{frp,gn,io,jv,ku_IQ}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%{_sysconfdir}/xdg/menus/mate-applications.menu
%{_sysconfdir}/xdg/menus/mate-preferences-categories.menu
%{_sysconfdir}/xdg/menus/mate-settings.menu
%{_datadir}/mate/desktop-directories

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmate-menu.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmate-menu.so.2
%{_libdir}/girepository-1.0/MateMenu-2.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmate-menu.so
%{_datadir}/gir-1.0/MateMenu-2.0.gir
%{_includedir}/mate-menus
%{_pkgconfigdir}/libmate-menu.pc

%files -n python-matemenu
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/matemenu.so
