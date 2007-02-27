#
# TODO:
# - Doesn't compile without /usr/src/linux/include/linux/autoconf.h so one must
#   symlink it before building package. This is because during compilation kernel
#   module is being build. Since we are building kernel modules later
#   sources/makefiles probably needs some hacking to drop this requirement.
# - Home page says that some addons should be compiled, I don't see any except.
#   vboxaddon kernel module and {vboxmouse,vboxvideo)_drv.so. Are they required?
# - BR list was a quickie so it may be incomplete or too big.
# - R list probably required.
# - .desktop file, some wrapper to launch VirtualBox (LD_LIBRARY_PATH must include
#   %{_libdir}/VirtualBox), maybe some init script to launch VBoxSVC.
# - Devel stuff is not packaged yet.
# - Now its EA ix86 x8664, but looking into autogenerated env.sh suggests that
#   code may be compiled exclusively for i686.
# - use %kernel_build macros
#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	smp		# without SMP kernel modules
#
Summary:	VirtualBox
Summary(pl.UTF-8):	VirtualBox
Name:		VirtualBox
Version:	1.3.6
Release:	0.1
License:	GPL v2
Group:		Applications/Emulators
Source0:	http://www.virtualbox.org/download/%{version}/VirtualBox-OSE-%{version}.tar.bz2
# Source0-md5:	70c24ccee8b5778efd8d22f9996fbec9
Patch0:		%{name}-configure.patch
Patch1:		%{name}-qt-paths.patch
URL:		http://www.virtualbox.org/
BuildRequires:	SDL-devel
BuildRequires:	bash
BuildRequires:	bcc
BuildRequires:	bin86
BuildRequires:	gcc >= 5:3.2.3
BuildRequires:	iasl
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.7}
BuildRequires:	libIDL-devel
BuildRequires:	libuuid-devel
BuildRequires:	libxslt-progs
BuildRequires:	qt-devel >= 6:3.3.6
BuildRequires:	rpmbuild(macros) >= 1.329
BuildRequires:	xalan-c-devel >= 1.10.0
#BuildRequires:	xcursor-devel
BuildRequires:	xerces-c-devel >= 2.6.0
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	zlib-devel >= 1.2.1
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{x8664}
%define		_outdir	amd64
%else
%define		_outdir	x86
%endif

%description
InnoTek VirtualBox is a general-purpose full virtualizer for x86
hardware. Targeted at server, desktop and embedded use, it is now the
only professional-quality virtualization solution that is also Open
Source Software.

Some of the features of VirtualBox are:

Modularity: VirtualBox has an extremely modular design with
well-defined internal programming interfaces and a client/server
design. This makes it easy to control it from several interfaces at
once: for example, you can start a virtual machine in a typical
virtual machine GUI and then control that machine from the command
line. VirtualBox also comes with a full Software Development Kit: even
though it is Open Source Software, you don't have to hack the source
to write a new interface for VirtualBox.

Virtual machine descriptions in XML: the configuration settings of
virtual machines are stored entirely in XML and are independent of the
local machines. Virtual machine definitions can therefore easily be
ported to other computers.

%description -l pl.UTF-8
InnoTek VirtualBox jest emulatorem sprzętu x86. Kierowany do
zastosowań serwerowych, desktopowych oraz wbudowanych jest obecnie
jedynym wysokiej jakości rozwiązaniem wirtualizacyjnym dostępnym
również jako Otwarte Oprogramowanie.

Przykładowe cechy VirtualBoksa:

Modularność: VirtualBox jest wysoce zmodularyzowanym produktem z
dobrze zaprojektowanym wewnętrznym interfejsem programowym typu
klient/serwer. Dzięki temu można łatwo kontrolować go za pomocą
różnych interfejsów. Można na przykład uruchomić maszynę wirtualną z
poziomu interfejsu graficznego, a później kontrolować ją z linii
poleceń. VirtualBox dostarcza również pełny pakiet deweloperski, co
pozwala stworzyć dowolny inny interfejs zarządzania maszyną wirtualną.

Opisy maszyn wirtualnych w XML-u: konfiguracje poszczególnych maszyn
wirtualnych są w całości przechowywane w XML-u i są niezależne od
lokalnej maszyny. Dzięki temu można szybko i łatwo przenieść
konfigurację maszyny wirtualnej na inny komputer.

%package -n kernel%{_alt_kernel}-misc-vboxdrv
Summary:	Linux kernel module for VirtualBox
Summary(pl.UTF-8):	Moduł jądra Linuksa dla VirtualBoksa
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
Provides:	kernel(vboxdrv) = %{version}-%{_rel}

%description -n kernel%{_alt_kernel}-misc-vboxdrv
Linux kernel module vboxdrv for VirtualBox.

%description -n kernel%{_alt_kernel}-misc-vboxdrv -l pl.UTF-8
Moduł jądra Linuksa vboxdrv dla VirtualBoksa.

%package -n kernel%{_alt_kernel}-smp-misc-vboxdrv
Summary:	Linux SMP kernel module for VirtualBox
Summary(pl.UTF-8):	Moduł jądra Linuksa SMP dla VirtualBoksa
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif
Provides:	kernel(vboxdrv) = %{version}-%{_rel}

%description -n kernel%{_alt_kernel}-smp-misc-vboxdrv
Linux SMP kernel module vboxdrv for VirtualBox.

%description -n kernel%{_alt_kernel}-smp-misc-vboxdrv -l pl.UTF-8
Moduł jądra Linuksa SMP vboxdrv dla VirtualBoksa.

%prep
%setup -q -n vbox
%patch0 -p0
%patch1 -p0

%build
./configure \
	--with-gcc="%{__cc}" \
	--with-g++="%{__cxx}"
. ./env.sh
kmk

cd out/linux.%{_outdir}/release/bin/src
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf o
	install -d o/include/linux
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
%if %{with dist_kernel}
	%{__make} -j1 -C %{_kernelsrcdir} O=$PWD/o prepare scripts
%else
	touch o/include/config/MARKER
	ln -sf %{_kernelsrcdir}/scripts o/scripts
%endif
	ln -sf ../../include/VBox o/include/VBox
	ln -sf ../../include/iprt o/include/iprt
	%{__make} -C %{_kernelsrcdir} clean \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	mv vboxdrv.ko vboxdrv-$cfg.ko
done

%install
rm -rf $RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_libdir}/VirtualBox

install out/linux.%{_outdir}/release/bin/{VBox{BFE,Manage,SDL,SVC,XPCOMIPCD},VirtualBox} \
	$RPM_BUILD_ROOT%{_bindir}
install out/linux.%{_outdir}/release/bin/VBox{DD,DD2,REM,REMImp,RT,VMM,XML,XPCOM,XPCOMIPCC}.so \
	$RPM_BUILD_ROOT%{_libdir}/VirtualBox
install out/linux.%{_outdir}/release/bin/{VBox{DD,DD2}{GC.gc,R0.r0},VMM{GC.gc,R0.r0}} \
	$RPM_BUILD_ROOT%{_libdir}/VirtualBox

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
%if %{with smp} && %{with dist_kernel}
install out/linux.%{_outdir}/release/bin/src/vboxdrv-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/vboxdrv.ko
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-misc-vboxdrv
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-misc-vboxdrv
%depmod %{_kernel_ver}

%if %{with smp} && %{with dist_kernel}
%post	-n kernel%{_alt_kernel}-smp-misc-vboxdrv
%depmod %{_kernel_ver}smp

%postun	-n kernel%{_alt_kernel}-smp-misc-vboxdrv
%depmod %{_kernel_ver}smp
%endif

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/VBox*
%attr(755,root,root) %{_bindir}/VirtualBox
%{_libdir}/VirtualBox

%files	-n kernel%{_alt_kernel}-misc-vboxdrv
%defattr(644,root,root,755)

%if %{with smp} && %{with dist_kernel}
%files	-n kernel%{_alt_kernel}-smp-misc-vboxdrv
%defattr(644,root,root,755)
%endif
