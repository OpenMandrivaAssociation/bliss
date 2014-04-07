Name:           bliss
Version:        0.72
Release:        7%{?dist}
Summary:        Compute automorphism groups and canonical labelings of graphs


License:        GPLv3
URL:            http://www.tcs.hut.fi/Software/bliss/
Source0:        http://www.tcs.hut.fi/Software/bliss/%{name}-%{version}.zip
# Man page written by Jerry James using text borrowed from the sources.
# The man page therefore has the same copyright and license as the sources.
Source1:        bliss.1
Source10:       %{name}.rpmlintrc
# Sent upstream 28 Oct 2011.  Don't call exit() in library code.
Patch0:         bliss-error.patch
# Patch from Thomas Rehn, also sent upstream.  Fix one bug and add one
# performance enhancement.
Patch1:         bliss-rehn.patch

BuildRequires:  doxygen
BuildRequires:  gmp-devel
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%global sover %(echo %{version} | cut -d. -f1)

%description
Bliss is an open source tool for computing automorphism groups and
canonical forms of graphs.  It has both a command line user interface as
well as C++ and C programming language APIs. 

%package devel
Summary:        Headers and library files for developing with bliss

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       gmp-devel%{?_isa}

%description devel
Headers and library files needed to develop applications that use the
bliss library.

%package libs
Summary:        Compute automorphism groups and canonical labelings of graphs


%description libs
A command-line bliss tool to access the functionality of the bliss
library.

%prep
%setup -q
%patch0

%build
# The Makefile creates a static library, so we roll our own shared library
# here instead.  Also, avoid an unused direct dependency on libm.
g++ $RPM_OPT_FLAGS -DBLISS_USE_GMP -fPIC -shared -o libbliss.so.%{version} \
  -Wl,-soname,libbliss.so.%{sover} defs.cc graph.cc partition.cc orbit.cc \
  uintseqhash.cc heap.cc timer.cc utils.cc bliss_C.cc -lgmp -Wl,--as-needed
ln -s libbliss.so.%{version} libbliss.so.%{sover}
ln -s libbliss.so.%{sover} libbliss.so

# The Makefile doesn't know how to link the binary against a shared library.
# Also, once again avoid an unused direct dependency on libm.
g++ $RPM_OPT_FLAGS -DBLISS_USE_GMP -o bliss bliss.cc -L. -lbliss -lgmp \
  -Wl,--as-needed

# Build the documentation
doxygen

%install
# The Makefile has no install target.

# Install the library
mkdir -p $RPM_BUILD_ROOT%{_libdir}
cp -a libbliss.* $RPM_BUILD_ROOT%{_libdir}

# Install the header files
mkdir -p $RPM_BUILD_ROOT%{_includedir}/bliss
cp -p *.h *.hh $RPM_BUILD_ROOT%{_includedir}/bliss

# Install the binary
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp -p bliss $RPM_BUILD_ROOT%{_bindir}

# Install the man page
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_mandir}/man1

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%{_bindir}/bliss
%{_mandir}/man1/bliss.1*

%files devel
%doc html
%{_includedir}/bliss
%{_libdir}/libbliss.so

%files libs
%doc COPYING.txt
%{_libdir}/libbliss.so.*

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.72-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.72-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.72-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 16 2012 Jerry James <loganjerry@gmail.com> - 0.72-4
- Apply bug fix and performance enhancement patch from Thomas Rehn

* Fri Jan  6 2012 Jerry James <loganjerry@gmail.com> - 0.72-3
- Rebuild for GCC 4.7.

* Tue Nov 15 2011 Jerry James <loganjerry@gmail.com> - 0.72-2
- Add patch to avoid calling exit() in the library

* Wed Jul 20 2011 Jerry James <loganjerry@gmail.com> - 0.72-1
- Initial RPM
