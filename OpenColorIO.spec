# Filter provides from Python libraries
%{?filter_setup:
%filter_provides_in %{python_sitearch}.*\.so$
%filter_setup
}

Name:           OpenColorIO
Version:        1.0.9
Release:        11%{?dist}
Summary:        Enables color transforms and image display across graphics apps

License:        BSD
URL:            http://opencolorio.org/
# Github archive was generated on the fly using the following URL:
# https://github.com/imageworks/OpenColorIO/tarball/v1.0.9
Source0:        %{name}-%{version}.tar.gz
Patch0:         OpenColorIO-yaml_cpp3.patch

# Utilities
BuildRequires:  cmake
BuildRequires:  help2man
BuildRequires:  python-markupsafe

# WARNING: OpenColorIO and OpenImageIO are cross dependent.
# If an ABI incompatible update is done in one, the other also needs to be
# rebuilt.
BuildRequires:  OpenImageIO-devel

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
BuildRequires:  yaml-cpp03-devel >= 0.3.0

# The following bundled projects are only used for document generation.
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


%package tools
Summary:        Command line tools for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tools
Command line tools for %{name}.


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
%setup -q
%patch0 -p1 -b .yaml3

# Remove what bundled libraries
rm -f ext/lcms*
rm -f ext/tinyxml*
rm -f ext/yaml*


%build
rm -rf build && mkdir build && pushd build
%cmake -DOCIO_BUILD_STATIC=OFF \
       -DOCIO_BUILD_DOCS=ON \
       -DOCIO_BUILD_TESTS=ON \
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
%make_install

# Generate man pages
mkdir -p %{buildroot}%{_mandir}/man1
help2man -N -s 1 %{?fedora:--version-string=%{version}} \
         -o %{buildroot}%{_mandir}/man1/ociocheck.1 \
         src/apps/ociocheck/ociocheck
help2man -N -s 1 %{?fedora:--version-string=%{version}} \
         -o %{buildroot}%{_mandir}/man1/ociobakelut.1 \
         src/apps/ociobakelut/ociobakelut

# Move installed documentation back so it doesn't conflict with the main package
popd
mkdir _tmpdoc
mv %{buildroot}%{_docdir}/%{name}/* _tmpdoc/


%check
# Testing passes locally in mock but fails on the fedora build servers.
#pushd build && make test


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc ChangeLog LICENSE README
%{_libdir}/*.so.*
%dir %{_datadir}/ocio
%{_datadir}/ocio/setup_ocio.sh
%{python_sitearch}/*.so

%files tools
%{_bindir}/*
%{_mandir}/man1/*

%files doc
%doc _tmpdoc/*

%files devel
%{_includedir}/OpenColorIO/
%{_includedir}/PyOpenColorIO/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Richard Shaw <hobbes1069@gmail.com> - 1.0.9-10
- Rebuild for OpenImageIO 1.6.9.

* Thu Jan 14 2016 Adam Jackson <ajax@redhat.com> - 1.0.9-9
- Rebuild for glew 1.13

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.0.9-7
- Rebuilt for GCC 5 C++11 ABI change

* Wed Jan 28 2015 Richard Shaw <hobbes1069@gmail.com> - 1.0.9-6
- Rebuild for OpenImageIO 1.5.11.

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Richard Shaw <hobbes1069@gmail.com> - 1.0.9-3
- Rebuild for updated OpenImageIO 1.4.7.

* Mon Jan 13 2014 Richard Shaw <hobbes1069@gmail.com> - 1.0.9-2
- Add OpenImageIO as build requirement to build additional command line tools.
  Fixes BZ#1038860.

* Wed Nov  6 2013 Richard Shaw <hobbes1069@gmail.com> - 1.0.9-1
- Update to latest upstream release.

* Mon Sep 23 2013 Richard Shaw <hobbes1069@gmail.com> - 1.0.8-6
- Rebuild against yaml-cpp03 compatibility package.

* Mon Aug 26 2013 Richard Shaw <hobbes1069@gmail.com> - 1.0.8-5
- Fix for new F20 feature, unversion doc dir. Fixes BZ#1001264

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 11 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.8-1
- Update to latest upstream release.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

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
