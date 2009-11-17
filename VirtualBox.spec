#
# TODO:
# - Find how to compile with PLD CFLAGS/CXXFLAGS/LDFLAGS.
# - Package SDK.
# - Package utils (and write initscripts ?) for Guest OS.
# - Check License of VBoxGuestAdditions_*.iso, it's propably not GPL v2.
#   If so check if it is distributable.
#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel module
%bcond_without	userspace	# don't build userspace package
%bcond_with	verbose

%if %{without kernel}
%undefine	with_dist_kernel
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif
%if %{without userspace}
# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0
%endif

%define		rel		1
%define		pname	VirtualBox
Summary:	VirtualBox OSE - x86 hardware virtualizer
Summary(pl.UTF-8):	VirtualBox OSE - wirtualizator sprzętu x86
Name:		%{pname}%{_alt_kernel}
Version:	3.0.12
Release:	%{rel}
License:	GPL v2
Group:		Applications/Emulators
Source0:	http://download.virtualbox.org/virtualbox/%{version}/%{pname}-%{version}-OSE.tar.bz2
# Source0-md5:	4cdf4a829db73fb502b8269676c8db30
Source1:	http://download.virtualbox.org/virtualbox/%{version}/UserManual.pdf
# Source1-md5:	ac742f57893b46bb9324ae008b716059
Source2:	http://download.virtualbox.org/virtualbox/%{version}/VBoxGuestAdditions_%{version}.iso
# Source2-md5:	bc756ed1b3f7874b098675970572206f
Source3:	%{pname}-vboxdrv.init
Source4:	%{pname}-vboxadd.init
Source5:	%{pname}-vboxnetflt.init
Source6:	%{pname}-vboxvfs.init
Source7:	%{pname}.desktop
Source8:	%{pname}.sh
Source9:	mount.vdi
Patch0:		%{pname}-configure.patch
Patch1:		%{pname}-configure-spaces.patch
Patch2:		%{pname}-export_modules.patch
Patch3:		%{pname}-VBoxSysInfo.patch
URL:		http://www.virtualbox.org/
BuildRequires:	rpmbuild(macros) >= 1.379
%if %{with userspace}
%ifarch %{x8664}
BuildRequires:	gcc-multilib
BuildRequires:	glibc-devel(i686)
BuildRequires:	libstdc++-multilib-devel
BuildRequires:	libstdc++-multilib-static
%endif
%if "%{pld_release}" == "ac"
BuildRequires:	XFree86-devel
%else
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXmu-devel
%endif
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-devel
BuildRequires:	QtGui-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	SDL-devel >= 1.2.7
BuildRequires:	acpica
BuildRequires:	alsa-lib-devel >= 1.0.6
BuildRequires:	bash
BuildRequires:	bcc
BuildRequires:	bin86
BuildRequires:	curl-devel
BuildRequires:	gcc >= 5:3.2.3
BuildRequires:	libIDL-devel
BuildRequires:	libcap-static
BuildRequires:	libpng-devel >= 1.2.5
BuildRequires:	libstdc++-devel >= 5:3.2.3
BuildRequires:	libstdc++-static >= 5:3.2.3
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-devel >= 2.6.26
BuildRequires:	libxslt-devel >= 1.1.17
BuildRequires:	libxslt-progs >= 1.1.17
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel >= 0.9.0
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	qt4-build >= 4.2.0
BuildRequires:	qt4-linguist
BuildRequires:	sed >= 4.0
BuildRequires:	which
BuildRequires:	xalan-c-devel >= 1.10.0
BuildRequires:	xerces-c-devel >= 2.6.0
BuildRequires:	zlib-devel >= 1.2.1
%endif
%if %{with dist_kernel}
BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20
%endif
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Suggests:	gxmessage
Provides:	group(vbox)
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{x8664}
%define		outdir	amd64
%else
%define		outdir	x86
%endif
%define		_sbindir	/sbin

%description
InnoTek VirtualBox OSE is a general-purpose full virtualizer for x86
hardware. Targeted at server, desktop and embedded use, it is now the
only professional-quality virtualization solution that is also Open
Source Software.

Some of the features of VirtualBox OSE are:

Modularity: VirtualBox OSE has an extremely modular design with
well-defined internal programming interfaces and a client/server
design. This makes it easy to control it from several interfaces at
once: for example, you can start a virtual machine in a typical
virtual machine GUI and then control that machine from the command
line. VirtualBox OSE also comes with a full Software Development Kit:
even though it is Open Source Software, you don't have to hack the
source to write a new interface for VirtualBox OSE.

Virtual machine descriptions in XML: the configuration settings of
virtual machines are stored entirely in XML and are independent of the
local machines. Virtual machine definitions can therefore easily be
ported to other computers.

%description -l pl.UTF-8
InnoTek VirtualBox OSE jest emulatorem sprzętu x86. Kierowany do
zastosowań serwerowych, desktopowych oraz wbudowanych jest obecnie
jedynym wysokiej jakości rozwiązaniem wirtualizacyjnym dostępnym
również jako Otwarte Oprogramowanie.

Przykładowe cechy VirtualBoksa:

Modularność: VirtualBox OSE jest wysoce zmodularyzowanym produktem z
dobrze zaprojektowanym wewnętrznym interfejsem programowym typu
klient/serwer. Dzięki temu można łatwo kontrolować go za pomocą
różnych interfejsów. Można na przykład uruchomić maszynę wirtualną z
poziomu interfejsu graficznego, a później kontrolować ją z linii
poleceń. VirtualBox OSE dostarcza również pełny pakiet deweloperski,
co pozwala stworzyć dowolny inny interfejs zarządzania maszyną
wirtualną.

Opisy maszyn wirtualnych w XML-u: konfiguracje poszczególnych maszyn
wirtualnych są w całości przechowywane w XML-u i są niezależne od
lokalnej maszyny. Dzięki temu można szybko i łatwo przenieść
konfigurację maszyny wirtualnej na inny komputer.

%package udev
Summary:	udev rules for VirtualBox OSE kernel modules
Summary(pl.UTF-8):	Reguły udev dla modułów jądra Linuksa dla VirtualBoksa
Release:	%{rel}
Group:		Base/Kernel
Requires:	udev-core

%description udev
udev rules for VirtualBox OSE kernel modules.

%description udev -l pl.UTF-8
Reguły udev dla modułów jądra Linuksa dla VirtualBoksa.

%package -n kernel%{_alt_kernel}-misc-vboxadd
Summary:	VirtualBox OSE Guest Additions for Linux Module
Summary(pl.UTF-8):	Moduł jądra Linuksa dla VirtualBoksa OSE
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(vboxadd) = %{version}-%{rel}

%description -n kernel%{_alt_kernel}-misc-vboxadd
VirtualBox OSE Guest Additions for Linux Module.

%description -n kernel%{_alt_kernel}-misc-vboxadd -l pl.UTF-8
Moduł jądra Linuksa vboxadd dla VirtualBoksa OSE - dodatki dla systemu
gościa.

%package -n kernel%{_alt_kernel}-misc-vboxdrv
Summary:	VirtualBox OSE Support Driver
Summary(pl.UTF-8):	Moduł jądra Linuksa dla VirtualBoksa OSE
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(vboxdrv) = %{version}-%{rel}

%description -n kernel%{_alt_kernel}-misc-vboxdrv
VirtualBox OSE Support Driver.

%description -n kernel%{_alt_kernel}-misc-vboxdrv -l pl.UTF-8
Moduł jądra Linuksa dla VirtualBoksa OSE - sterownik wsparcia dla
systemu głównego.

%package -n kernel%{_alt_kernel}-misc-vboxnetflt
Summary:	VirtualBox OSE Guest Additions for Linux Module
Summary(pl.UTF-8):	Moduł jądra Linuksa dla VirtualBoksa OSE
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
Requires:	kernel%{_alt_kernel}-misc-vboxdrv
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(vboxnetflt) = %{version}-%{rel}

%description -n kernel%{_alt_kernel}-misc-vboxnetflt
VirtualBox OSE Network Filter Driver.

%description -n kernel%{_alt_kernel}-misc-vboxnetflt -l pl.UTF-8
Moduł jądra Linuksa dla VirtualBoksa OSE - sterownik filtrowania sieci
dla systemu głównego.

%package -n kernel%{_alt_kernel}-misc-vboxvfs
Summary:	Host file system access VFS for VirtualBox OSE
Summary(pl.UTF-8):	Moduł jądra Linuksa dla VirtualBoksa OSE
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
Requires:	kernel%{_alt_kernel}-misc-vboxadd
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(vboxvfs) = %{version}-%{rel}

%description -n kernel%{_alt_kernel}-misc-vboxvfs
Host file system access VFS for VirtualBox OSE.

%description -n kernel%{_alt_kernel}-misc-vboxvfs -l pl.UTF-8
Moduł jądra Linuksa dla VirtualBoksa OSE - dostęp do plików systemu
głównego z poziomu systemu gościa.

%package -n kernel%{_alt_kernel}-misc-vboxvideo
Summary:	DRM support for VirtualBox OSE
Summary(pl.UTF-8):	Moduł jądra Linuksa dla VirtualBoksa OSE
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(vboxvideo) = %{version}-%{rel}

%description -n kernel%{_alt_kernel}-misc-vboxvideo
DRM support for VirtualBox OSE.

%description -n kernel%{_alt_kernel}-misc-vboxvideo -l pl.UTF-8
Moduł jądra Linuksa dla VirtualBoksa OSE - sterownik obsługi DRM.

%package -n xorg-driver-input-vboxmouse
Summary:	X.org mouse driver for VirtualBox OSE guest OS
Summary(pl.UTF-8):	Sterownik myszy dla systemu gościa w VirtualBoksie OSE
Release:	%{rel}
Group:		X11/Applications
Requires:	xorg-xserver-server >= 1.0.99.901
Requires:	xorg-xserver-server(xinput-abi) < 5.0
Requires:	xorg-xserver-server(xinput-abi) >= 4.0

%description -n xorg-driver-input-vboxmouse
X.org mouse driver for VirtualBox OSE guest OS.

%description -n xorg-driver-input-vboxmouse  -l pl.UTF-8
Sterownik myszy dla systemu gościa w VirtualBoksie.

%package -n xorg-driver-video-vboxvideo
Summary:	X.org video driver for VirtualBox OSE guest OS
Summary(pl.UTF-8):	Sterownik grafiki dla systemu gościa w VirtualBoksie OSE
Release:	%{rel}
Group:		X11/Applications
Requires:	xorg-xserver-server >= 1.0.99.901
Requires:	xorg-xserver-server(videodrv-abi) < 6.0
Requires:	xorg-xserver-server(videodrv-abi) >= 2.0

%description -n xorg-driver-video-vboxvideo
X.org video driver for VirtualBox OSE guest OS.

%description -n xorg-driver-video-vboxvideo -l pl.UTF-8
Sterownik grafiki dla systemu gościa w VirtualBoksie OSE.

%prep
%setup -q -n %{pname}-%{version}_OSE
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

cat <<'EOF' > udev.conf
KERNEL=="vboxdrv", NAME="%k", GROUP="vbox", MODE="0660"
KERNEL=="vboxadd", NAME="%k", GROUP="vbox", MODE="0660"
EOF

install %{SOURCE1} .
sed 's#@LIBDIR@#%{_libdir}#' < %{SOURCE8} > VirtualBox-wrapper.sh

rm -rf PLD-MODULE-BUILD && mkdir PLD-MODULE-BUILD && cd PLD-MODULE-BUILD
../src/VBox/Additions/linux/export_modules modules.tar.gz
	tar -zxf modules.tar.gz && rm -f modules.tar.gz
../src/VBox/HostDrivers/linux/export_modules modules.tar.gz --without-hardening && \
	tar -zxf modules.tar.gz && rm -f modules.tar.gz
#./src/VBox/HostDrivers/Support/linux/Makefile:70:
#./PLD-MODULE-BUILD/vboxdrv/Makefile:70:


%build
%if %{with userspace}
./configure \
	--with-gcc="%{__cc}" \
	--with-g++="%{__cxx}" \
	--disable-hardening \
	--disable-kmods

. ./env.sh && \
kmk -j1 %{?with_verbose:KBUILD_VERBOSE=3} USER=$(id -un)
%endif

%if %{with kernel}
cd PLD-MODULE-BUILD
%build_kernel_modules -m vboxadd -C vboxadd
%build_kernel_modules -m vboxdrv -C vboxdrv
%build_kernel_modules -m vboxnetflt -C vboxnetflt
cp -a vboxadd/Module.symvers vboxvfs
%build_kernel_modules -m vboxvfs -C vboxvfs -c
%build_kernel_modules -m vboxvideo -C vboxvideo_drm
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d \
	$RPM_BUILD_ROOT{%{_bindir},%{_pixmapsdir},%{_desktopdir}} \
	$RPM_BUILD_ROOT%{_libdir}/VirtualBox \
	$RPM_BUILD_ROOT/sbin

install -p %{SOURCE9} $RPM_BUILD_ROOT/sbin/mount.vdi
install -p VirtualBox-wrapper.sh $RPM_BUILD_ROOT%{_libdir}/VirtualBox
for f in {VBox{BFE,Headless,Manage,SDL,SVC,Tunctl,XPCOMIPCD},VirtualBox}; do
	install -p out/linux.%{outdir}/release/bin/$f $RPM_BUILD_ROOT%{_libdir}/VirtualBox/$f
	ln -s %{_libdir}/VirtualBox/VirtualBox-wrapper.sh $RPM_BUILD_ROOT%{_bindir}/$f
done

install -p out/linux.%{outdir}/release/bin/VBox{TestOGL,NetAdpCtl,NetDHCP} \
	$RPM_BUILD_ROOT%{_libdir}/VirtualBox
install -p out/linux.%{outdir}/release/bin/VBox*.so \
	$RPM_BUILD_ROOT%{_libdir}/VirtualBox
install -p out/linux.%{outdir}/release/bin/{VBox{DD,DD2}{GC.gc,R0.r0},VMM{GC.gc,R0.r0}} \
	$RPM_BUILD_ROOT%{_libdir}/VirtualBox
install -p out/linux.%{outdir}/release/bin/VBoxSysInfo.sh \
	$RPM_BUILD_ROOT%{_libdir}/VirtualBox

install -d $RPM_BUILD_ROOT%{_libdir}/VirtualBox/additions
install -d $RPM_BUILD_ROOT%{_libdir}/VirtualBox/nls

cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_libdir}/VirtualBox/additions/VBoxGuestAdditions.iso
cp -a out/linux.%{outdir}/release/bin/components $RPM_BUILD_ROOT%{_libdir}/VirtualBox
cp -a out/linux.%{outdir}/release/bin/nls/* $RPM_BUILD_ROOT%{_libdir}/VirtualBox/nls

install -d $RPM_BUILD_ROOT%{_sbindir}
install -p out/linux.%{outdir}/release/bin/additions/mountvboxsf		\
	$RPM_BUILD_ROOT%{_sbindir}/mount.vboxsf

install -d $RPM_BUILD_ROOT%{_libdir}/xorg/modules/{drivers,input}

install -p out/linux.%{outdir}/release/bin/additions/vboxmouse_drv_16.so	\
	$RPM_BUILD_ROOT%{_libdir}/xorg/modules/input/vboxmouse_drv.so
install -p out/linux.%{outdir}/release/bin/additions/vboxvideo_drv_16.so	\
	$RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/vboxvideo_drv.so

install -p out/linux.%{outdir}/release/bin/VBox.png $RPM_BUILD_ROOT%{_pixmapsdir}/VBox.png
cp -a %{SOURCE7} $RPM_BUILD_ROOT%{_desktopdir}/%{pname}.desktop

install -d $RPM_BUILD_ROOT/etc/udev/rules.d
cp -a udev.conf $RPM_BUILD_ROOT/etc/udev/rules.d/virtualbox.rules
%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -p %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/vboxdrv
install -p %{SOURCE4} $RPM_BUILD_ROOT/etc/rc.d/init.d/vboxadd
install -p %{SOURCE5} $RPM_BUILD_ROOT/etc/rc.d/init.d/vboxnetflt
install -p %{SOURCE6} $RPM_BUILD_ROOT/etc/rc.d/init.d/vboxvfs
%install_kernel_modules -m PLD-MODULE-BUILD/vboxadd/vboxadd -d misc
%install_kernel_modules -m PLD-MODULE-BUILD/vboxdrv/vboxdrv -d misc
%install_kernel_modules -m PLD-MODULE-BUILD/vboxnetflt/vboxnetflt -d misc
%install_kernel_modules -m PLD-MODULE-BUILD/vboxvfs/vboxvfs -d misc
%install_kernel_modules -m PLD-MODULE-BUILD/vboxvideo_drm/vboxvideo -d misc

install -d $RPM_BUILD_ROOT/etc/modprobe.d
cat <<'EOF' > $RPM_BUILD_ROOT/etc/modprobe.d/vboxvfs.conf
# Somewhy filesystem is not called as same as kernel module.
alias vboxsf vboxvfs
EOF
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 221 -r -f vbox

%post
cat << 'EOF'
You must also install kernel module for this software to work:
    kernel-misc-vboxdrv-%{version}-%{rel}@%{_kernel_ver_str}

Additionally you might want to install:
    kernel-misc-vboxnetflt-%{version}-%{rel}@%{_kernel_ver_str}

On Guest Linux system you might want to install:
    kernel-misc-vboxadd-%{version}-%{rel}@%{_kernel_ver_str}
    kernel-misc-vboxvfs-%{version}-%{rel}@%{_kernel_ver_str}
    kernel-misc-vboxvideo-%{version}-%{rel}@%{_kernel_ver_str}

NOTE: for different kernel brands append after word kernel the brand, like:
    kernel-desktop-misc-vboxdrv-%{version}-%{rel}@%{_kernel_ver_str}
    kernel-laptop-misc-vboxdrv-%{version}-%{rel}@%{_kernel_ver_str}
    kernel-vanilla-misc-vboxdrv-%{version}-%{rel}@%{_kernel_ver_str}
    ...etc.

Depending on which kernel brand You use.

EOF

%postun
if [ "$1" = "0" ]; then
	%groupremove vbox
fi

%post	-n kernel%{_alt_kernel}-misc-vboxadd
%depmod %{_kernel_ver}
/sbin/chkconfig --add vboxadd
%service vboxadd restart "VirtualBox OSE Guest additions driver"

%postun	-n kernel%{_alt_kernel}-misc-vboxadd
%depmod %{_kernel_ver}

%preun -n kernel%{_alt_kernel}-misc-vboxadd
if [ "$1" = "0" ]; then
	%service vboxadd stop
	/sbin/chkconfig --del vboxadd
fi

%post	-n kernel%{_alt_kernel}-misc-vboxdrv
%depmod %{_kernel_ver}
/sbin/chkconfig --add vboxdrv
%service vboxdrv restart "VirtualBox USE Support Driver"

%postun	-n kernel%{_alt_kernel}-misc-vboxdrv
%depmod %{_kernel_ver}

%preun -n kernel%{_alt_kernel}-misc-vboxdrv
if [ "$1" = "0" ]; then
	%service vboxdrv stop
	/sbin/chkconfig --del vboxdrv
fi

%post	-n kernel%{_alt_kernel}-misc-vboxnetflt
%depmod %{_kernel_ver}
/sbin/chkconfig --add vboxnetflt
%service vboxnetflt restart "VirtualBox OSE Network Filter driver"

%postun	-n kernel%{_alt_kernel}-misc-vboxnetflt
%depmod %{_kernel_ver}

%preun -n kernel%{_alt_kernel}-misc-vboxnetflt
if [ "$1" = "0" ]; then
	%service vboxnetflt stop
	/sbin/chkconfig --del vboxnetflt
fi

%post	-n kernel%{_alt_kernel}-misc-vboxvfs
%depmod %{_kernel_ver}
/sbin/chkconfig --add vboxvfs
%service vboxvfs restart "VirtualBox OSE Host file system access VFS"

%postun	-n kernel%{_alt_kernel}-misc-vboxvfs
%depmod %{_kernel_ver}

%preun -n kernel%{_alt_kernel}-misc-vboxvfs
if [ "$1" = "0" ]; then
	%service vboxvfs stop
	/sbin/chkconfig --del vboxvfs
fi

%post	-n kernel%{_alt_kernel}-misc-vboxvideo
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-misc-vboxvideo
%depmod %{_kernel_ver}

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc UserManual.pdf
%dir %{_libdir}/VirtualBox
%dir %{_libdir}/VirtualBox/additions
%dir %{_libdir}/VirtualBox/components
%dir %{_libdir}/VirtualBox/nls
%attr(755,root,root) %{_bindir}/VBoxBFE
%attr(755,root,root) %{_bindir}/VBoxHeadless
%attr(755,root,root) %{_bindir}/VBoxManage
%attr(755,root,root) %{_bindir}/VBoxSDL
%attr(755,root,root) %{_bindir}/VBoxSVC
%attr(755,root,root) %{_bindir}/VBoxTunctl
%attr(755,root,root) %{_bindir}/VBoxXPCOMIPCD
%attr(755,root,root) %{_bindir}/VirtualBox
%attr(755,root,root) /sbin/mount.vdi
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxSVC
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxBFE
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxHeadless
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxManage
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxSDL
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxTestOGL
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxTunctl
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxXPCOMIPCD
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxDD.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxDD2.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxDDU.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxGuestPropSvc.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxKeyboard.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxNetAdpCtl
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxNetDHCP
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxOGLhostcrutil.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxOGLhosterrorspu.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxOGLrenderspu.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxPython.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxPython2_6.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxREM.so
%ifarch %{ix86}
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxREM32.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxREM64.so
%endif
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxRT.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxSettings.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxSharedClipboard.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxSharedCrOpenGL.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxSharedFolders.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxVMM.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxXPCOM.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxXPCOMC.so
%attr(755,root,root) %{_libdir}/VirtualBox/VirtualBox
%attr(755,root,root) %{_libdir}/VirtualBox/VirtualBox-wrapper.sh
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxSysInfo.sh
%{_libdir}/VirtualBox/VBoxDD2GC.gc
%{_libdir}/VirtualBox/VBoxDDGC.gc
%{_libdir}/VirtualBox/VMMGC.gc
%{_libdir}/VirtualBox/VBoxDD2R0.r0
%{_libdir}/VirtualBox/VBoxDDR0.r0
%{_libdir}/VirtualBox/VMMR0.r0
%{_libdir}/VirtualBox/additions/VBoxGuestAdditions.iso
%{_libdir}/VirtualBox/components/VBoxC.so
%{_libdir}/VirtualBox/components/VBoxSVCM.so
%{_libdir}/VirtualBox/components/VBoxXPCOMBase.xpt
%{_libdir}/VirtualBox/components/VBoxXPCOMIPCC.so
%{_libdir}/VirtualBox/components/VirtualBox_XPCOM.xpt
%lang(ar) %{_libdir}/VirtualBox/nls/*_ar.qm
%lang(bg) %{_libdir}/VirtualBox/nls/*_bg.qm
%lang(ca) %{_libdir}/VirtualBox/nls/*_ca.qm
%lang(cs) %{_libdir}/VirtualBox/nls/*_cs.qm
%lang(de) %{_libdir}/VirtualBox/nls/*_de.qm
%lang(el) %{_libdir}/VirtualBox/nls/*_el.qm
%lang(es) %{_libdir}/VirtualBox/nls/*_es.qm
%lang(eu) %{_libdir}/VirtualBox/nls/*_eu.qm
%lang(fi) %{_libdir}/VirtualBox/nls/*_fi.qm
%lang(fr) %{_libdir}/VirtualBox/nls/*_fr.qm
%lang(hu) %{_libdir}/VirtualBox/nls/*_hu.qm
%lang(id) %{_libdir}/VirtualBox/nls/*_id.qm
%lang(it) %{_libdir}/VirtualBox/nls/*_it.qm
%lang(ja) %{_libdir}/VirtualBox/nls/*_ja.qm
%lang(km_KH) %{_libdir}/VirtualBox/nls/*_km_KH.qm
%lang(ko) %{_libdir}/VirtualBox/nls/*_ko.qm
%lang(nl) %{_libdir}/VirtualBox/nls/*_nl.qm
%lang(pl) %{_libdir}/VirtualBox/nls/*_pl.qm
%lang(pt) %{_libdir}/VirtualBox/nls/*_pt.qm
%lang(pt_BR) %{_libdir}/VirtualBox/nls/*_pt_BR.qm
%lang(ro) %{_libdir}/VirtualBox/nls/*_ro.qm
%lang(ru) %{_libdir}/VirtualBox/nls/*_ru.qm
%lang(sk) %{_libdir}/VirtualBox/nls/*_sk.qm
%lang(sr) %{_libdir}/VirtualBox/nls/*_sr.qm
%lang(sv) %{_libdir}/VirtualBox/nls/*_sv.qm
%lang(tr) %{_libdir}/VirtualBox/nls/*_tr.qm
%lang(uk) %{_libdir}/VirtualBox/nls/*_uk.qm
%lang(zh_CN) %{_libdir}/VirtualBox/nls/*_zh_CN.qm
%lang(zh_TW) %{_libdir}/VirtualBox/nls/*_zh_TW.qm
%{_pixmapsdir}/VBox.png
%{_desktopdir}/%{pname}.desktop

%files udev
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/virtualbox.rules

%files -n xorg-driver-input-vboxmouse
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/input/vboxmouse_drv.so

%files -n xorg-driver-video-vboxvideo
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/drivers/vboxvideo_drv.so
%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-misc-vboxadd
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/vboxadd
/lib/modules/%{_kernel_ver}/misc/vboxadd.ko*

%files -n kernel%{_alt_kernel}-misc-vboxdrv
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/vboxdrv
/lib/modules/%{_kernel_ver}/misc/vboxdrv.ko*

%files -n kernel%{_alt_kernel}-misc-vboxnetflt
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/vboxnetflt
/lib/modules/%{_kernel_ver}/misc/vboxnetflt.ko*

%files -n kernel%{_alt_kernel}-misc-vboxvfs
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/vboxvfs
%attr(755,root,root) %{_sbindir}/mount.vboxsf
/etc/modprobe.d/vboxvfs.conf
/lib/modules/%{_kernel_ver}/misc/vboxvfs.ko*

%files -n kernel%{_alt_kernel}-misc-vboxvideo
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vboxvideo.ko*
%endif
