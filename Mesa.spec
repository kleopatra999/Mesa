#
# Conditional build:
%bcond_with	glide	# with GLIDE (broken now)
%bcond_with	xlibs	# use xlibs deps
#
Summary:	Free OpenGL implementation
Summary(pl):	Bezpłatna implementacja standardu OpenGL
Name:		Mesa
Version:	6.1
Release:	1
License:	MIT (core), LGPL (MesaGLU), SGI (GLU,libGLw) and others - see COPYRIGHT file
Group:		X11/Libraries
Source0:	http://dl.sourceforge.net/mesa3d/%{name}Lib-%{version}.tar.bz2
# Source0-md5:	5de1f53ec0709f60fc68fdfed57351f3
Source1:	http://dl.sourceforge.net/mesa3d/%{name}Demos-%{version}.tar.bz2
# Source1-md5:	89bfe0f6c69b39fd0ebd9fff481a4e9b
Patch0:		%{name}-opt.patch
URL:		http://www.mesa3d.org/
%ifarch %{ix86} alpha
%{?with_glide:BuildRequires:	Glide3-DRI-devel}
%{?with_glide:Requires:	Glide3-DRI}
%endif
%if %{with xlibs}
BuildRequires:	libXmu-devel
BuildRequires:	libXp-devel
%else
BuildRequires:	XFree86-devel
%endif
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool >= 2:1.4d
BuildRequires:	motif-devel
BuildRequires:	perl-devel
Provides:	OpenGL = 1.5
Provides:	OpenGL-GLU = 1.3
# reports version 1.3, but supports glXGetProcAddress() from 1.4
Provides:	OpenGL-GLX = 1.4
Obsoletes:	XFree86-OpenGL-libGL
Obsoletes:	XFree86-OpenGL-libs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# avoid XFree86-OpenGL* dependency
# Glide3 can be provided by Glide_V3-DRI or Glide_V5-DRI
%define		_noautoreqdep	libGL.so.1 libGLU.so.1 libOSMesa.so.4   libglide3.so.3

%define		_sysconfdir	/etc/X11

%description
Mesa is a 3-D graphics library with an API which is very similar to
that of OpenGL*. To the extent that Mesa utilizes the OpenGL command
syntax or state machine, it is being used with authorization from
Silicon Graphics, Inc. However, the author makes no claim that Mesa is
in any way a compatible replacement for OpenGL or associated with
Silicon Graphics, Inc. Those who want a licensed implementation of
OpenGL should contact a licensed vendor. This software is distributed
under the terms of the GNU Library General Public License, see the
LICENSE file for details.

- OpenGL(R) is a registered trademark of Silicon Graphics, Inc.

%description -l pl
Mesa jest biblioteką 3D będącą darmowym odpowiednikiem standardu
OpenGL(*).

- OpenGL jest zastrzeżonym znakiem towarowym firmy Silicon Graphics,
  Inc.

%package devel
Summary:	Development environment for Mesa
Summary(pl):	Środowisko programistyczne biblioteki Mesa
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%if %{with xlibs}
Requires:	libX11-devel
Requires:	libXp-devel
%else
Requires:	XFree86-devel
%endif
Provides:	OpenGL-devel = 1.5
Provides:	OpenGL-GLU-devel = 1.3
Provides:	OpenGL-GLX-devel = 1.4
Obsoletes:	XFree86-OpenGL-devel
Obsoletes:	XFree86-OpenGL-devel-base

%description devel
Header files and documentation needed for development.

%description devel -l pl
Pliki nagłówkowe i dokumentacja do Mesy.

%package static
Summary:	Mesa static libraries
Summary(pl):	Biblioteki statyczne Mesy
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	OpenGL-static = 1.5
Provides:	OpenGL-GLU-static = 1.3
Obsoletes:	XFree86-OpenGL-static

%description static
The static version of the Mesa libraries.

%description static -l pl
Biblioteki statyczne Mesy.

%package demos
Summary:	Mesa Demos
Summary(pl):	Demonstracje możliwości bibliotek Mesa
Group:		Development/Libraries
Requires:	OpenGL-devel

%description demos
Demonstration programs for the Mesa libraries.

%description demos -l pl
Programy demonstracyjne dla bibliotek Mesa.

%prep
%setup -q -n Mesa-%{version} -b 1
%patch0 -p1

# fix demos
%{__perl} -pi -e "s,\.\./images/,%{_examplesdir}/Mesa/images/,g" progs/demos/*

%build
%ifarch %{ix86}
targ=linux-x86
%else
targ=linux
%endif

%{__make} ${targ}-static \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	OPT="%{rpmcflags}" \
	XLIB_DIR=/usr/X11R6/%{_lib} \
	GLW_SOURCES="GLwDrawA.c GLwMDrawA.c"
mv -f lib lib-static
%{__make} clean
%{__make} ${targ} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	OPT="%{rpmcflags}" \
	XLIB_DIR=/usr/X11R6/%{_lib}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/GL,%{_mandir}/man3,%{_examplesdir}/Mesa}

cp -df lib-static/lib[GO]* $RPM_BUILD_ROOT%{_libdir}
cp -df lib/lib[GO]* $RPM_BUILD_ROOT%{_libdir}
cp -rf include/GL/{gl*,osmesa.h,xmesa*} src/glw/GLw*.h $RPM_BUILD_ROOT%{_includedir}/GL
rm -f $RPM_BUILD_ROOT%{_includedir}/GL/glut*

for l in demos redbook samples xdemos ; do
	%{__make} -C progs/$l clean
done
for l in demos redbook samples util xdemos images ; do
	cp -Rf progs/$l $RPM_BUILD_ROOT%{_examplesdir}/Mesa/$l
done
rm -rf $RPM_BUILD_ROOT%{_examplesdir}/Mesa/*/{.deps,CVS,Makefile.{BeOS*,win,cygnus,DJ,dja}}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc docs/{*.html,README.{3DFX,GGI,MITS,QUAKE,THREADS,X11},RELNOTES*,VERSIONS}
%attr(755,root,root) %{_libdir}/libGL.so.*.*
%attr(755,root,root) %{_libdir}/libGL.so
%attr(755,root,root) %{_libdir}/libGLU.so.*.*
%attr(755,root,root) %{_libdir}/libOSMesa.so.*.*

%files devel
%defattr(644,root,root,755)
%doc docs/*.spec
%attr(755,root,root) %{_libdir}/libGLU.so
%attr(755,root,root) %{_libdir}/libOSMesa.so
%{_libdir}/libGLw.a
%dir %{_includedir}/GL
%{_includedir}/GL/GLwDrawA.h
%{_includedir}/GL/GLwDrawAP.h
%{_includedir}/GL/GLwMDrawA.h
%{_includedir}/GL/GLwMDrawAP.h
%{_includedir}/GL/gl.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/gl_mangle.h
%{_includedir}/GL/glu.h
%{_includedir}/GL/glu_mangle.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glxext.h
%{_includedir}/GL/glx_mangle.h
%{_includedir}/GL/osmesa.h
%{_includedir}/GL/xmesa.h
%{_includedir}/GL/xmesa_x.h
%{_includedir}/GL/xmesa_xf86.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libGL.a
%{_libdir}/libGLU.a
%{_libdir}/libOSMesa.a

%files demos
%defattr(644,root,root,755)
%{_examplesdir}/Mesa
