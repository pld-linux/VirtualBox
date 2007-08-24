#
# TODO:
# - Home page says that some addons should be compiled, I don't see any except.
#   vboxaddon kernel module and {vboxmouse,vboxvideo)_drv.so. Are they required?
# - .desktop file
# - it seems that VBoxSVC should not be started by init script but I'm still 
#   testing this
# - /dev/vboxdrv should belong to vboxusers group and have rw rights to it
# - Devel stuff is not packaged yet.
# - Now its EA ix86 x8664, but looking into autogenerated env.sh suggests that
#   code may be compiled exclusively for i686.
# - use %kernel_build macros
#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	up		# without up packages
%bcond_without	smp		# without SMP kernel modules

%define		_rel		0.1

Summary:	VirtualBox
Summary(pl.UTF-8):	VirtualBox
Name:		VirtualBox
Version:	1.4.0
Release:	%{_rel}
License:	GPL v2
Group:		Applications/Emulators
Source0:	http://www.virtualbox.org/download/%{version}/VirtualBox-OSE-%{version}.tar.bz2
# Source0-md5:	8e89d32a67a3a39271f44039d0583a16
Source1:	virtualbox.init
Source2:	http://www.virtualbox.org/download/UserManual.pdf
# Source2-md5:	2e5458bd5b4b9acd18cc86866e8a7284
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
Requires:	kernel(vboxdrv) = %{version}-%{_rel}
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
%setup -q -n %{name}-OSE-%{version}
%patch0 -p0
%patch1 -p0

cat > VBox.sh <<'EOF'
#!/bin/sh

if [ ! -c /dev/vboxdrv ]; then
	echo "Special character device /dev/vboxdrv doesn't exists!"
	echo "Check your installation and if vboxdrv kernel module is loaded."
	exit 1
fi

if [ ! -w /dev/vboxdrv ]; then
	echo "You don't have write access to /dev/vboxdrv!"
	echo "Correct this situation or contact with your system administrator."
	exit 1
fi

BINFILE=$(basename "$0")
LD_LIBRARY_PATH=%{_libdir}/VirtualBox %{_libdir}/VirtualBox/$BINFILE ${1:+"$@"}
EOF

install %{SOURCE2} .

%build
KDIR="%{_builddir}/%{buildsubdir}/kernel"
mkdir -p $KDIR
cp -a %{_kernelsrcdir}/include $KDIR
%ifarch %{x8664}
ln -sf $KDIR/include/asm-x86_64 $KDIR/include/asm
%else
ln -sf $KDIR/include/asm-i386 $KDIR/include/asm
%endif
ln -sf $KDIR/include/linux/autoconf-up.h $KDIR/include/linux/autoconf.h

./configure \
	--with-gcc="%{__cc}" \
	--with-g++="%{__cxx}" \
	--with-linux="$KDIR"
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
	mv vboxdrv.ko ../../../../../vboxdrv-$cfg.ko
done

%install
rm -rf $RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_libdir}/VirtualBox \
	$RPM_BUILD_ROOT/etc/rc.d/init.d

for f in {VBox{BFE,Manage,SDL,SVC,XPCOMIPCD},VirtualBox}; do
	install out/linux.%{_outdir}/release/bin/$f $RPM_BUILD_ROOT%{_libdir}/VirtualBox/$f
	install VBox.sh $RPM_BUILD_ROOT%{_bindir}/$f
done

install out/linux.%{_outdir}/release/bin/VBox{C,DD,DD2,DDU,REM,REMImp,RT,SVCM,VMM,XML,XPCOM,XPCOMIPCC}.so \
	$RPM_BUILD_ROOT%{_libdir}/VirtualBox
install out/linux.%{_outdir}/release/bin/{VBox{DD,DD2}{GC.gc,R0.r0},VMM{GC.gc,R0.r0},*.xpt} \
	$RPM_BUILD_ROOT%{_libdir}/VirtualBox

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
install vboxdrv-up.ko $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/vboxdrv.ko
%if %{with smp} && %{with dist_kernel}
install vboxdrv-smp.ko $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/vboxdrv.ko
%endif

cp -a out/linux.%{_outdir}/release/bin/components $RPM_BUILD_ROOT%{_libdir}/VirtualBox
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/virtualbox

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add virtualbox
%service virtualbox restart "VBoxSVC daemon"

%preun 
if [ "$1" = "0" ]; then
	%service virtualbox stop
	/sbin/chkconfig --del virtualbox
fi

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
%doc UserManual.pdf
%dir %{_libdir}/VirtualBox
%dir %{_libdir}/VirtualBox/components
%attr(755,root,root) %{_bindir}/VBox*
%attr(755,root,root) %{_bindir}/VirtualBox
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxSVC
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxBFE
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxManage
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxSDL
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxXPCOMIPCD
%attr(755,root,root) %{_libdir}/VirtualBox/VirtualBox
%{_libdir}/VirtualBox/*.gc
%{_libdir}/VirtualBox/*.r0
%{_libdir}/VirtualBox/VBox*.so
%{_libdir}/VirtualBox/*.xpt
%{_libdir}/VirtualBox/components/*
%attr(754,root,root) /etc/rc.d/init.d/virtualbox

%if %{with up} || %{without dist_kernel}
%files	-n kernel%{_alt_kernel}-misc-vboxdrv
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vboxdrv.ko.gz
%endif

%if %{with smp} && %{with dist_kernel}
%files	-n kernel%{_alt_kernel}-smp-misc-vboxdrv
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/vboxdrv.ko.gz
%endif
