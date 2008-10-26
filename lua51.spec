#
# Conditional build:
%bcond_with	luastatic        # build dietlibc-based static lua version (broken)
#
Summary:	A simple lightweight powerful embeddable programming language
Summary(pl.UTF-8):	Prosty, lekki ale potężny, osadzalny język programowania
Name:		lua51
Version:	5.1.3
Release:	3
License:	MIT
Group:		Development/Languages
Source0:	http://www.lua.org/ftp/lua-%{version}.tar.gz
# Source0-md5:	a70a8dfaa150e047866dc01a46272599
Patch0:		%{name}-link.patch
URL:		http://www.lua.org/
%{?with_luastatic:BuildRequires:       dietlibc-devel}
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
Group:		Development/Languages

%description libs
lua 5.1.x libraries.

%description libs -l pl.UTF-8
Biblioteki lua 5.1.x.

%package devel
Summary:	Header files for Lua
Summary(pl.UTF-8):	Pliki nagłówkowe dla Lua
Group:		Development/Languages
Requires:	%{name}-libs = %{version}-%{release}
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
sed -r -i 's|(#define LUA_ROOT.*)%{_prefix}/local/|\1%{_prefix}/|g' src/luaconf.h
sed -r -i 's|(#define LUA_CDIR.*)lib/|\1%{_lib}/|g' src/luaconf.h

%build
%if %{with luastatic}
%{__make} all \
	PLAT=posix \
	CC="%{_target_cpu}-dietlibc-gcc" \
	CFLAGS="%{rpmcflags} -Wall -fPIC -DPIC -D_GNU_SOURCE -DLUA_USE_POSIX"
mv src/lua lua.static
mv src/luac luac.static
%{__make} clean
%endif

%{__make} -j1 all \
	PLAT=linux \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall -fPIC -DPIC -D_GNU_SOURCE -DLUA_USE_LINUX"

#rm -f test/{lua,luac}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/lua}

%{__make} install \
	INSTALL_TOP=$RPM_BUILD_ROOT%{_prefix} \
	INSTALL_INC=$RPM_BUILD_ROOT%{_includedir}/lua51 \
	INSTALL_LIB=$RPM_BUILD_ROOT%{_libdir} \
	INSTALL_MAN=$RPM_BUILD_ROOT%{_mandir}/man1 \
	INSTALL_CMOD=$RPM_BUILD_ROOT%{_libdir}/lua/5.1

# change name from lua to lua51
for i in $RPM_BUILD_ROOT%{_bindir}/* ; do mv ${i}{,51} ; done
mv $RPM_BUILD_ROOT%{_mandir}/man1/lua{,51}.1
mv $RPM_BUILD_ROOT%{_mandir}/man1/luac{,51}.1
mv $RPM_BUILD_ROOT%{_libdir}/liblua{,51}.a

install src/liblua.so.5.1 $RPM_BUILD_ROOT%{_libdir}
ln -s liblua.so.5.1 $RPM_BUILD_ROOT%{_libdir}/liblua51.so

%if %{with luastatic}
install lua.static $RPM_BUILD_ROOT%{_bindir}/lua51.static
install luac.static $RPM_BUILD_ROOT%{_bindir}/luac51.static
%endif

# create pkgconfig file
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
cat > $RPM_BUILD_ROOT%{_pkgconfigdir}/lua51.pc <<'EOF'
prefix=%{_prefix}
exec_prefix=%{_exec_prefix}
includedir=%{_includedir}/%{name}
libdir=%{_libdir}
interpreter=%{_bindir}/lua51
compiler=%{_bindir}/luac51

Name: Lua
Description: An extension programming language
Version: %{version}
Cflags: -I%{_includedir}/%{name}
Libs: -L%{_libdir} -llua51 -ldl -lm
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lua51
%attr(755,root,root) %{_bindir}/luac51
%{_mandir}/man1/lua51.1*
%{_mandir}/man1/luac51.1*

%files libs
%defattr(644,root,root,755)
%doc COPYRIGHT HISTORY README
%attr(755,root,root) %{_libdir}/liblua.so.*.*
%dir %{_libdir}/lua
%{_libdir}/lua/5.1
%dir %{_datadir}/lua
%{_datadir}/lua/5.1

%files devel
%defattr(644,root,root,755)
%doc doc/*.{html,css,gif} test
%attr(755,root,root) %{_libdir}/liblua51.so
%{_includedir}/lua51
%{_pkgconfigdir}/lua51.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/liblua51.a

%if %{with luastatic}
%files luastatic
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*.static
%endif
