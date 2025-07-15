#
# Conditional build:
%bcond_without	crashreporter		# crashreporter support
# requires post recent qxt additions including qxtsslserver
%bcond_with	system_qxt		# use system libqxt package

%ifarch %{arm} aarch64
%undefine	with_crashreporter
%endif

%global libechonest_version %(pkg-config --modversion libechonest 2>/dev/null || echo 1.1.7)
%global phonon_version %(pkg-config --modversion phonon 2>/dev/null || echo 4.5.0)

Summary:	The Social Media Player
Name:		tomahawk
Version:	0.8.4
Release:	0.1
License:	GPL v2+
Group:		X11/Applications/Multimedia
Source0:	http://download.tomahawk-player.org/%{name}-%{version}.tar.bz2
# Source0-md5:	04832abe1786edcc55805875b5882445
Patch50:	%{name}-0.8.4-taglib_version.patch
Patch0:		%{name}-0.8.0-system_qxt.patch
URL:		http://tomahawk-player.org/
BuildRequires:	QtDBus-devel
BuildRequires:	QtGui-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	QtWebKit-devel
BuildRequires:	QtXmlPatterns-devel
BuildRequires:	attica-devel >= 0.4.0
BuildRequires:	boost-devel
BuildRequires:	clucene-core-devel >= 2.3
BuildRequires:	gnutls-devel
BuildRequires:	kde4-kdelibs-devel
BuildRequires:	libechonest-devel >= 2.2
BuildRequires:	liblastfm-devel >= 1.0
BuildRequires:	phonon-devel >= 4.5.0
BuildRequires:	pkgconfig(libjreen) >= 1.1.1
BuildRequires:	pkgconfig(liblucene++)
BuildRequires:	qca-devel
BuildRequires:	qjson-devel >= 0.8.1
BuildRequires:	qtkeychain-devel
BuildRequires:	qtweetlib-devel >= 0.4
BuildRequires:	quazip-qt4-devel
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	sparsehash-devel
BuildRequires:	taglib-devel
BuildRequires:	telepathy-qt4-devel
BuildRequires:	websocketpp-devel
%if %{with system_qxt}
BuildRequires:	libqxt-devel >= 0.7
%else
Provides:	bundled(libqxt) = 0.7
%endif
Requires:	%{name}-libs = %{version}-%{release}
Requires:	desktop-file-utils
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	libechonest >= %{libechonest_version}
Requires:	phonon >= %{phonon_version}
Requires:	qca-cyrus-sasl
Requires:	qca-ossl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Stop chasing your music across different machines, services and
websites. It's time to take the work out of "play". If the song you
want to listen to is in your local library, it just plays. If the song
is on a remote machine, it just plays. If the song is on the web, or
available from your subscription service, it just plays. By
abstracting a piece of content's metadata from its file location,
users can easily share playlists, listening history and more. It's
sort of like Wonka Vision, Tomahawk will reassemble it on the other
side. OK, maybe that's not a good analogy... but it's just as
delicious.

%package libs
Summary:	Runtime libraries for %{name}
Group:		Libraries

%description libs
Runtime libraries for %{name}

%package devel
Summary:	Development files for %{name}
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Development files for %{name}

%prep
%setup -q -n %{name}-%{version}%{?pre}

%if %{with system_qxt}
%patch -P0 -p1
rm -rv thirdparty/qxt
%endif

%patch -P50 -p1

%build
install -d build
cd build
%cmake \
	-DBUILD_RELEASE:BOOL=ON \
	-DBUILD_WITH_QT4:BOOL=ON \
	-DCMAKE_BUILD_TYPE:STRING="RelWithDebInfo" \
	-DBUILD_HATCHET:BOOL=ON \
	-DWITH_CRASHREPORTER:BOOL=%{?with_crashreporter:ON}%{!?with_crashreporter:OFF} \
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install/fast \
	DESTDIR=$RPM_BUILD_ROOT

# unpackaged files (fixme?)
rm -v $RPM_BUILD_ROOT%{_iconsdir}/hicolor/scalable/tomahawk.svg

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/tomahawk.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor

%postun
%update_desktop_database
%update_icon_cache hicolor

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE.txt
%attr(755,root,root) %{_bindir}/tomahawk
%{_libdir}/libtomahawk_*.so
%{_desktopdir}/tomahawk.desktop
%{_iconsdir}/hicolor/*/apps/tomahawk.*

%files libs
%defattr(644,root,root,755)
%{_libdir}/libtomahawk.so.%{version}
%{_libdir}/libtomahawk-playdarapi.so.%{version}
%{_libdir}/libtomahawk-widgets.so.%{version}

%files devel
%defattr(644,root,root,755)
%{_includedir}/libtomahawk/
%{_libdir}/libtomahawk.so
%{_libdir}/libtomahawk-playdarapi.so
%{_libdir}/libtomahawk-widgets.so
%{_libdir}/cmake/Tomahawk/
