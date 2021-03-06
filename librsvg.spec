Summary:	SVG Rendering Library
Name:		librsvg
Version:	2.40.9
Release:	1
Epoch:		1
License:	GPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/librsvg/2.40/%{name}-%{version}.tar.xz
# Source0-md5:	31df15e3beaa8fbbf538ca3c52b400d2
URL:		http://live.gnome.org/LibRsvg
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gdk-pixbuf-devel >= 2.30.0
BuildRequires:	gtk-doc
BuildRequires:	libcroco-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	popt-devel
BuildRequires:	pkg-config
BuildRequires:	rpm-pythonprov
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
librsvg is a library to render SVG files using cairo.

%package devel
Summary:	Include files for developing with librsvg
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
This package provides the necessary development libraries and include
files to allow you to develop with librsvg.

%package apidocs
Summary:	librsvg API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
librsvg API documentation.

%package -n rsvg-convert
Summary:	Converting tool
Group:		Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n rsvg-convert
Turns SVG files into raster images.

%package -n gdk-pixbuf-rsvg
Summary:	Gtk+ rsvg pixbuffer loader
Group:		Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires(post,postun):	gdk-pixbuf

%description -n gdk-pixbuf-rsvg
Gtk+ rsvg pixbuffer loader.

%prep
%setup -q

# Makefile.am:255: ENABLE_VAPIGEN does not appear in AM_CONDITIONAL
echo 'AC_DEFUN([VAPIGEN_CHECK],[AM_CONDITIONAL([ENABLE_VAPIGEN], [false])])' >> acinclude.m4

%build
%{__libtoolize}
%{__gtkdocize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-gtk-theme	\
	--disable-silent-rules	\
	--disable-static	\
	--with-html-dir=%{_gtkdocdir}/%{name}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/{,*/*/*/}*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%post -n gdk-pixbuf-rsvg
umask 022
gdk-pixbuf-query-loaders --update-cache || :

%postun -n gdk-pixbuf-rsvg
if [ "$1" != "0" ]; then
	umask 022
	gdk-pixbuf-query-loaders --update-cache || :
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog AUTHORS NEWS
%attr(755,root,root) %ghost %{_libdir}/lib*.so.?
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_libdir}/girepository-1.0/Rsvg-2.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_datadir}/gir-1.0/Rsvg-2.0.gir
%{_pkgconfigdir}/*.pc
%{_includedir}/librsvg-2.0

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{name}

%files -n rsvg-convert
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rsvg-convert
%{_mandir}/man1/rsvg-convert.1*

%files -n gdk-pixbuf-rsvg
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gdk-pixbuf-2.0/2.*.*/loaders/libpixbufloader-svg.so

