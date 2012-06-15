%global githash1 g87da508
%global githash2 b3cb224

# Filter provides from Python libraries
%{?filter_setup:
%filter_provides_in %{python_sitearch}.*\.so$
%filter_setup
}

Name:           OpenColorIO
Version:        1.0.7
Release:        4%{?dist}
Summary:        Enables color transforms and image display across graphics apps

License:        BSD
URL:            http://opencolorio.org/
# Github archive was generated on the fly using the following URL:
# https://github.com/imageworks/OpenColorIO/tarball/v1.0.7
Source0:        imageworks-%{name}-v%{version}-0-%{githash1}.tar.gz

Patch0:         OpenColorIO-1.0.7-pylib_no_soname.patch
Patch1:         OpenColorIO-1.0.7-docfix.patch

# Utilities
BuildRequires:  cmake28
BuildRequires:  help2man

# Libraries
BuildRequires:  python-devel
BuildRequires:  mesa-libGL-devel mesa-libGLU-devel
BuildRequires:  libX11-devel libXmu-devel libXi-devel
BuildRequires:  freeglut-devel
BuildRequires:  glew-devel
BuildRequires:  zlib-devel

#######################
# Unbundled libraries #
#######################
BuildRequires:  tinyxml-devel
BuildRequires:  lcms2-devel
BuildRequires:  yaml-cpp-devel >= 0.3.0

# The following are only used for document generation.
#BuildRequires:  python-docutils
#BuildRequires:  python-jinja2
#BuildRequires:  python-pygments
#BuildRequires:  python-setuptools
#BuildRequires:  python-sphinx


%description
OCIO enables color transforms and image display to be handled in a consistent
manner across multiple graphics applications. Unlike other color management
solutions, OCIO is geared towards motion-picture post production, with an
emphasis on visual effects and animation color pipelines.


%package doc
BuildArch:      noarch
Summary:        API Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description doc
API documentation for %{name}.


%package devel
Summary:        Development libraries and headers for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries and headers for %{name}.


%prep
%setup -q -n imageworks-%{name}-%{githash2}
# Dot set soname for python modules.
%patch0 -p1 -b .pylib
# Exclude hidden files from being packaged.
%patch1 -p1 -b .docfix


# Remove what bundled libraries
rm -f ext/lcms*
rm -f ext/tinyxml*
rm -f ext/yaml*


%build
rm -rf build && mkdir build && pushd build
%cmake28 -DOCIO_BUILD_STATIC=OFF \
         -DPYTHON_INCLUDE_LIB_PREFIX=OFF \
%if 0%{?el6}
         -DCMAKE_SKIP_RPATH=OFF \
%endif
         -DOCIO_BUILD_TESTS=ON \
         -DOCIO_LINK_PYGLUE=ON \
         -DOCIO_PYGLUE_SONAME=OFF \
         -DUSE_EXTERNAL_YAML=TRUE \
         -DUSE_EXTERNAL_TINYXML=TRUE \
         -DUSE_EXTERNAL_LCMS=TRUE \
%ifnarch x86_64
         -DOCIO_USE_SSE=OFF \
%endif
         ../

make %{?_smp_mflags}


%install
pushd build
make install DESTDIR=%{buildroot}

# Generate man pages
mkdir -p %{buildroot}%{_mandir}/man1
help2man -N -s 1 %{?fedora:--version-string=%{version}} \
         -o %{buildroot}%{_mandir}/man1/ociocheck.1 \
         src/apps/ociocheck/ociocheck
help2man -N -s 1 %{?fedora:--version-string=%{version}} \
         -o %{buildroot}%{_mandir}/man1/ociobakelut.1 \
         src/apps/ociobakelut/ociobakelut


%check
# Testing passes locally in mock but fails on the fedora build servers.
#pushd build && make test


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc ChangeLog LICENSE README
%{_bindir}/*
%{_libdir}/*.so.*
%dir %{_datadir}/ocio
%{_datadir}/ocio/setup_ocio.sh
%{_mandir}/man1/*
%{python_sitearch}/*.so

%files doc
%doc %{_docdir}/%{name}/

%files devel
%{_includedir}/OpenColorIO/
%{_includedir}/PyOpenColorIO/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Thu Apr 26 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.7-4
- Only use SSE instructions on x86_64.

* Wed Apr 25 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.7-3
- Misc spec cleanup for packaging guidelines.
- Disable testing for now since it fails on the build servers.

* Wed Apr 18 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.7-1
- Latest upstream release.

* Thu Apr 05 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.6-1
- Latest upstream release.

* Wed Nov 16 2011 Richard Shaw <hobbes1069@gmail.com> - 1.0.2-1
- Initial release.
