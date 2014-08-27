#
# Conditional build:
%bcond_with	luastatic        # build dietlibc-based static lua version (broken)

Summary:	A simple lightweight powerful embeddable programming language
Summary(pl.UTF-8):	Prosty, lekki ale potężny, osadzalny język programowania
Name:		lua51
Version:	5.1.5
Release:	2
License:	MIT
Group:		Development/Languages
Source0:	http://www.lua.org/ftp/lua-%{version}.tar.gz
# Source0-md5:	2e115fe26e435e33b0d5c022e4490567
Source1:	lua.pc.in
Source2:	lua-c++.pc.in
Patch0:		%{name}-link.patch
Patch1:		debian_make.patch
URL:		http://www.lua.org/
%{?with_luastatic:BuildRequires:       dietlibc-static}
BuildRequires:	readline-devel
BuildRequires:	sed >= 4.0
Requires:	%{name}-libs = %{version}-%{release}
Provides:	lua = %{version}
Obsoletes:	lua < 4.0.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lua is a powerful, light-weight programming language designed for
extending applications. It is also frequently used as a
general-purpose, stand-alone language. It combines simple procedural
syntax (similar to Pascal) with powerful data description constructs
based on associative arrays and extensible semantics. Lua is
dynamically typed, interpreted from bytecodes, and has automatic
memory management with garbage collection, making it ideal for
configuration, scripting, and rapid prototyping.

This version has compiled in support for dynamic libraries in baselib.

%description -l pl.UTF-8
Lua to język programowania o dużych możliwościach ale lekki,
przeznaczony do rozszerzania aplikacji. Jest też często używany jako
samodzielny język ogólnego przeznaczenia. Łączy prostą proceduralną
składnię (podobną do Pascala) z potężnymi konstrukcjami opisu danych
bazującymi na tablicach asocjacyjnych i rozszerzalnej składni. Lua ma
dynamiczny system typów, interpretowany z bytecodu i automatyczne
zarządzanie pamięcią z odśmiecaczem, co czyni go idealnym do
konfiguracji, skryptów i szybkich prototypów.

Ta wersja ma wkompilowaną obsługę ładowania dynamicznych bibliotek.

%package libs
Summary:	lua 5.1.x libraries
Summary(pl.UTF-8):	Biblioteki lua 5.1.x
Group:		Libraries
# Provide old SONAME to avoid rebuilds
%ifarch %{x8664}
Provides:	liblua.so.5.1()(64bit)
%else
Provides:	liblua.so.5.1
%endif

%description libs
lua 5.1.x libraries.

%description libs -l pl.UTF-8
Biblioteki lua 5.1.x.

%package libs-c++
Summary:	lua 5.1.x libraries
Summary(pl.UTF-8):	Biblioteki lua 5.1.x
Group:		Libraries

%description libs-c++
lua 5.1.x C++ libraries.

%description libs-c++ -l pl.UTF-8
Biblioteki lua 5.1.x C++.

%package devel
Summary:	Header files for Lua
Summary(pl.UTF-8):	Pliki nagłówkowe dla Lua
Group:		Development/Languages
Requires:	%{name}-libs = %{version}-%{release}
Requires:	%{name}-libs-c++ = %{version}-%{release}
Provides:	lua-devel = %{version}

%description devel
Header files needed to embed Lua in C/C++ programs and docs for the
language.

%description devel -l pl.UTF-8
Pliki nagłówkowe potrzebne do włączenia Lua do programów w C/C++ oraz
dokumentacja samego języka.

%package static
Summary:	Static Lua libraries
Summary(pl.UTF-8):	Biblioteki statyczne Lua
Group:		Development/Languages
Requires:	%{name}-devel = %{version}-%{release}
Provides:	lua-static = %{version}

%description static
Static Lua libraries.

%description static -l pl.UTF-8
Biblioteki statyczne Lua.

%package luastatic
Summary:	Static Lua interpreter
Summary(pl.UTF-8):	Statycznie skonsolidowany interpreter lua
Group:		Development/Languages

%description luastatic
Static lua interpreter.

%description luastatic -l pl.UTF-8
Statycznie skonsolidowany interpreter lua.

%prep
%setup -q -n lua-%{version}
%patch0 -p1
%patch1 -p1
sed -r -i 's|(#define LUA_ROOT.*)%{_prefix}/local/|\1%{_prefix}/|g' src/luaconf.h
sed -r -i 's|(#define LUA_CDIR.*)lib/|\1%{_lib}/|g' src/luaconf.h

cp -p %{SOURCE1} %{SOURCE2} .

%build
%if %{with luastatic}
%{__make} all \
	PLAT=posix \
	CC="diet %{__cc}" \
	CFLAGS="%{rpmcflags} -Wall -fPIC -Os -DPIC -D_GNU_SOURCE -DLUA_USE_POSIX"
mv src/lua lua.static
mv src/luac luac.static
%{__make} clean
%endif

%{__make} debian_linux \
	RPATH=%{_libdir} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} -Wall -fPIC -DPIC -D_GNU_SOURCE -DLUA_USE_LINUX" \
	CXXFLAGS="%{rpmcxxflags} -Wall -fPIC -DPIC -D_GNU_SOURCE -DLUA_USE_LINUX"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/lua/5.1,%{_datadir}/lua/5.1,%{_pkgconfigdir}}

%{__make} debian_install \
	INSTALL_TOP=$RPM_BUILD_ROOT%{_prefix} \
	INSTALL_INC=$RPM_BUILD_ROOT%{_includedir}/lua51 \
	INSTALL_LIB=$RPM_BUILD_ROOT%{_libdir} \
	INSTALL_MAN=$RPM_BUILD_ROOT%{_mandir}/man1 \
	INSTALL_CMOD=$RPM_BUILD_ROOT%{_libdir}/lua/5.1

# generate autodeps
chmod +x $RPM_BUILD_ROOT%{_libdir}/lib*.so*

%if %{with luastatic}
install -p lua.static $RPM_BUILD_ROOT%{_bindir}/lua51.static
install -p luac.static $RPM_BUILD_ROOT%{_bindir}/luac51.static
%endif

# alias to old pld names
ln -s liblua5.1.so $RPM_BUILD_ROOT%{_libdir}/liblua51.so
ln -s liblua5.1.a $RPM_BUILD_ROOT%{_libdir}/liblua51.a
ln -s lua5.1.pc $RPM_BUILD_ROOT%{_pkgconfigdir}/lua51.pc
ln -s liblua5.1.so.0 $RPM_BUILD_ROOT%{_libdir}/liblua.so.5.1

# we have pkgconfig files, rm .la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/liblua5.1.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/liblua5.1-c++.la

# create pkgconfig files
cat > $RPM_BUILD_ROOT%{_pkgconfigdir}/lua5.1.pc <<'EOF'
major_version=5.1
version=%{version}
lib_name_include=lua5.1

prefix=%{_prefix}
exec_prefix=%{_exec_prefix}
libdir=%{_libdir}
interpreter=%{_bindir}/lua5.1
compiler=%{_bindir}/luac5.1

$(cat lua.pc.in)
EOF

cat > $RPM_BUILD_ROOT%{_pkgconfigdir}/lua5.1-c++.pc <<'EOF'
major_version=5.1
version=%{version}
lib_name_include=lua5.1

prefix=%{_prefix}
exec_prefix=%{_exec_prefix}
libdir=%{_libdir}
interpreter=%{_bindir}/lua5.1
compiler=%{_bindir}/luac5.1

$(cat lua-c++.pc.in)
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post   libs-c++ -p /sbin/ldconfig
%postun libs-c++ -p /sbin/ldconfig

%triggerpostun libs -- %{name}-libs < 5.1.5-1.2
# restore symlink which ldconfig removed (it was ghost of old package)
ln -s liblua5.1.so.0 %{_libdir}/liblua.so.5.1 || :

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lua5.1
%attr(755,root,root) %{_bindir}/luac5.1
%{_mandir}/man1/lua5.1.1*
%{_mandir}/man1/luac5.1.1*

%files libs
%defattr(644,root,root,755)
%doc COPYRIGHT HISTORY README
%attr(755,root,root) %{_libdir}/liblua.so.5.1
%attr(755,root,root) %{_libdir}/liblua5.1.so.*.*.*
%ghost %{_libdir}/liblua5.1.so.0
%dir %{_libdir}/lua
%{_libdir}/lua/5.1
%dir %{_datadir}/lua
%{_datadir}/lua/5.1

%files libs-c++
%defattr(644,root,root,755)
%doc COPYRIGHT HISTORY README
%attr(755,root,root) %{_libdir}/liblua5.1-c++.so.*.*.*
%ghost %{_libdir}/liblua5.1-c++.so.0

%files devel
%defattr(644,root,root,755)
%doc doc/*.{html,css,gif} test
%{_libdir}/liblua5.1.so
%{_libdir}/liblua5.1-c++.so
%{_libdir}/liblua51.so
%{_includedir}/lua51
%{_pkgconfigdir}/lua5.1-c++.pc
%{_pkgconfigdir}/lua5.1.pc
%{_pkgconfigdir}/lua51.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/liblua5.1.a
%{_libdir}/liblua51.a
%{_libdir}/liblua5.1-c++.a

%if %{with luastatic}
%files luastatic
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*.static
%endif
