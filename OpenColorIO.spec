%if ! 0%{?bootstrap} || ! 0%{?rhel}
%global docs 1
%global tests 1
%endif

Name:           OpenColorIO
Version:        2.1.0
Release:        3%{?dist}
Summary:        Enables color transforms and image display across graphics apps

License:        BSD
URL:            http://opencolorio.org/
Source0:        https://github.com/AcademySoftwareFoundation/OpenColorIO/archive/v%{version}/%{name}-%{version}.tar.gz

# https://github.com/AcademySoftwareFoundation/OpenColorIO/issues/1296
Patch0:         ocio-install.patch

# For compatibility with OIIO 2.3.
Patch1:         https://patch-diff.githubusercontent.com/raw/AcademySoftwareFoundation/OpenColorIO/pull/1488.patch

# OIIO is only built for these arches due to Libraw
%if 0%{?rhel} >= 8
ExclusiveArch:  x86_64 ppc64le
%endif

# Utilities
BuildRequires:  cmake gcc-c++
BuildRequires:  help2man
BuildRequires:  python3
BuildRequires:  python3-markupsafe
BuildRequires:  python3-setuptools

# Libraries
BuildRequires:  OpenEXR-devel
BuildRequires:  boost-devel
BuildRequires:  expat-devel
BuildRequires:  freeglut-devel
BuildRequires:  glew-devel
BuildRequires:  libX11-devel libXmu-devel libXi-devel
BuildRequires:  mesa-libGL-devel mesa-libGLU-devel
BuildRequires:  opencv-devel
BuildRequires:  pybind11-devel
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  pystring-devel
BuildRequires:  zlib-devel

# WARNING: OpenColorIO and OpenImageIO are cross dependent.
# If an ABI incompatible update is done in one, the other also needs to be
# rebuilt.
BuildRequires:  OpenImageIO-devel
BuildRequires:  OpenImageIO-iv
BuildRequires:  OpenImageIO-utils

#######################
# Unbundled libraries #
#######################
BuildRequires:  lcms2-devel
BuildRequires:  yaml-cpp-devel >= 0.5.0

%if 0%{?docs}
BuildRequires:  doxygen
BuildRequires:  python3-breathe
BuildRequires:  python3-recommonmark
BuildRequires:  python3-sphinx-press-theme
BuildRequires:  python3-sphinx-tabs
BuildRequires:  python3-testresources
%endif

%if ! 0%{?docs}
# upgrade path for when/if docs are not included
Obsoletes: %{name}-doc < %{version}-%{release}
%endif


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
Requires:       %{name} = %{version}-%{release}

%description doc
API documentation for %{name}.


%package devel
Summary:        Development libraries and headers for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries and headers for %{name}.


%prep
%autosetup -p1 -n %{name}-%{version}%{?relcan:-rc%{relcan}}


%build
%cmake -DCMAKE_CXX_STANDARD=14 \
       -DOCIO_BUILD_DOCS=%{?docs:ON}%{?!docs:OFF} \
       -DOCIO_BUILD_TESTS=%{?tests:ON}%{?!tests:OFF} \
	   -DOCIO_USE_HEADLESS=ON \
	   -DOCIO_INSTALL_EXT_PACKAGES=NONE \
%ifnarch x86_64
       -DOCIO_USE_SSE=OFF \
%endif
       -DOpenGL_GL_PREFERENCE=GLVND

%cmake_build


%install
%cmake_install

# Remove static libs
find %{buildroot} -type f -name "*.a" -exec rm -f {} \;

# Generate man pages
pushd %{__cmake_builddir}/src/apps
mkdir -p %{buildroot}%{_mandir}/man1
for app in ociobakelut ociocheck ociochecklut ocioconvert ociolutimage ociomakeclf ocioperf ociowrite; do \
help2man -N -s 1 %{?fedora:--version-string=%{version}} \
         -o %{buildroot}%{_mandir}/man1/$app.1 \
         $app/$app
done
popd


%check
# Testing passes locally in mock but fails on the fedora build servers.
#pushd build && make test


%ldconfig_scriptlets


%files
%license LICENSE
%doc CHANGELOG.md COMMITTERS.md CONTRIBUTING.md GOVERNANCE.md PROCESS.md
%doc README.md SECURITY.md THIRD-PARTY.md
%{_libdir}/*.so.*
%{python3_sitearch}/*.so

%files tools
%{_bindir}/*
%{_datadir}/ocio/
%{_mandir}/man1/*

%if 0%{?docs}
%files doc
%{_datadir}/doc/%{name}/html/
%endif

%files devel
%{_includedir}/OpenColorIO/
%{_libdir}/cmake/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Sun Oct 03 2021 Richard Shaw <hobbes1069@gmail.com> - 2.1.0-3
- Rebuild for OpenImageIO 2.3.

* Sat Oct 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.1.0-2
- Rebuild for OpenEXR/Imath 3.1

* Wed Sep 01 2021 Richard Shaw <hobbes1069@gmail.com> - 2.1.0-1
- Update to 2.1.0.

* Fri Aug 13 2021 Richard Shaw <hobbes1069@gmail.com> - 2.0.1-1
- Update to 2.0.1.

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct  9 2020 Orion Poplawski <orion@nwra.com> - 1.1.1-12
- Add BR python3-sphinx-latex

* Fri Sep 04 2020 Richard Shaw <hobbes1069@gmail.com> - 1.1.1-11
- Rebuild for OpenImageIO 2.2.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-10
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed May 20 2020 Tom Callaway <spot@fedoraproject.org> - 1.1.1-8
- update tex buildrequires

* Sat Mar 14 2020 Richard Shaw <hobbes1069@gmail.com> - 1.1.1-7
- Rebuild to fix bad timing with mass rebuild and OIIO 2.0.x -> 2.1.x.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 27 2020 Richard Shaw <hobbes1069@gmail.com> - 1.1.1-5
- Rebuild for OpenImageIO 2.1.10.1.

* Fri Oct 18 2019 Richard Shaw <hobbes1069@gmail.com> - 1.1.1-4
- Rebuild for yaml-cpp 0.6.3.

* Tue Sep 17 2019 Gwyn Ciesla <gwync@protonmail.com> - 1.1.1-3
- Rebuilt for new freeglut

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 03 2019 Richard Shaw <hobbes1069@gmail.com> - 1.1.1-1
- Update to 1.1.1.
- Removing python glue module as python 3 is not currently supported.

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 13 2018 Richard Shaw <hobbes1069@gmail.com> - 1.1.0-10
- Add patch for OIIO 2.0 and mesa glext.h header changes.

* Mon Sep 24 2018 Richard Shaw <hobbes1069@gmail.com> - 1.1.0-9
- Obsolete Python2 library and build Python3 library.

* Thu Aug 23 2018 Nicolas Chauvet <kwizart@gmail.com> - 1.1.0-8
- Rebuilt for glew 2.1.0

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 22 2018 Adam Williamson <awilliam@redhat.com> - 1.1.0-6
- Rebuild with bootstrap disabled, so we get docs again

* Thu Feb 22 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.0-5
- Rebuild

* Tue Feb 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.1.0-4
- support %%bootstrap (no docs, no tests)
- enable bootstrap mode on f28+ to workaround bug #1546964

* Mon Feb 19 2018 Adam Williamson <awilliam@redhat.com> - 1.1.0-3
- Fix build with yaml-cpp 0.6+ (patch out bogus hidden visibility)
- Fix build with GCC 8 (issues in Python bindings, upstream PR #518)
- Rebuild for yaml-cpp 0.6.1

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 12 2018 Richard Shaw <hobbes1069@gmail.com> - 1.1.0-1
- Update to latest upstream release.

* Sun Jan 07 2018 Richard Shaw <hobbes1069@gmail.com> - 1.0.9-20
- Rebuild for OpenImageIO 1.8.7.

* Wed Dec 06 2017 Richard Shaw <hobbes1069@gmail.com> - 1.0.9-19
- Fix ambiguous Python 2 dependency declarations
  https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.0.9-16
- Rebuild due to bug in RPM (RHBZ #1468476)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 10 2017 Orion Poplawski <orion@cora.nwra.com> - 1.0.9-14
- Rebuild for glew 2.0.0

* Mon Oct 03 2016 Richard Shaw <hobbes1069@gmail.com> - 1.0.9-13
- Rebuild for new OpenImageIO.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-12
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

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
