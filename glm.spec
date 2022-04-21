# The library consists of headers only
%global debug_package %{nil}

Name:           glm
Version:        0.9.9.8
Release:        1
Summary:        C++ mathematics library for graphics programming

License:        MIT
URL:            http://glm.g-truc.net/
Source0:        https://github.com/g-truc/glm/releases/download/%{version}/%{name}-%{version}.tar.gz
Patch0:         fix-tests-big-endian-and-installation.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake >= 3.14

%description
GLM is a C++ library for doing mathematics operations
required in many OpenGL based applications. Its interface
has been designed to resemble the built-in matrix and vector
types of the OpenGL shading language.

%package        devel
Summary:        C++ mathematics library for graphics programming
BuildArch:      noarch

Provides:       %{name}-static = %{version}-%{release}

%description    devel
GLM is a C++ library for doing mathematics operations
required in many OpenGL based applications. Its interface
has been designed to resemble the built-in matrix and vector
types of the OpenGL shading language.

%{name}-devel is only required for building software that uses
the GLM library. Because GLM currently is a header-only library,
there is no matching run time package.

%package        doc
Summary:        Documentation for %{name}-devel
BuildArch:      noarch

%description    doc
The %{name}-doc package contains reference documentation and
a programming manual for the %{name}-devel package.

%prep
%autosetup -p1

%build
%cmake \
  -DCMAKE_CXX_FLAGS="%{optflags} -fPIC -fno-strict-aliasing" \
  -DGLM_TEST_ENABLE=ON

%check
ctest --output-on-failure -E '(test-core_func_common|test-gtc_packing)'

%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name CMakeLists.txt -exec rm -f {} ';'

mkdir -pv $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_libdir}/cmake $RPM_BUILD_ROOT%{_datadir}/cmake
mv $RPM_BUILD_ROOT%{_libdir}/pkgconfig $RPM_BUILD_ROOT%{_datadir}/pkgconfig
rmdir $RPM_BUILD_ROOT%{_libdir}

%files devel
%doc readme.md
%{_includedir}/%{name}
%{_datadir}/cmake
%{_datadir}/pkgconfig/

%files doc
%license readme.md
%doc doc/api
%doc manual.md readme.md
%doc doc/manual.pdf

%changelog
* Thu Apr 21 2022 <misaka00251@misakanet.cn> - 0.9.9.8-1
- Init package (Spec file by fedora team, patch by Max Ree & Krzysztof Kurek)