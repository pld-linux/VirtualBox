# TODO
# - java bindings
# - Package SDK.
# - Package utils (and write initscripts ?) for Guest OS.
# - Check License of VBoxGuestAdditions_*.iso, it's probably not GPL v2.
#   If so check if it is distributable.
# - resolve mess with subpackages?
#   - addtions: iso (containing additions/*.iso)
#   - guest: to be installed to guests (deps on x11 drivers)
# - enable VDE networking: --enable-vde
#
# Conditional build:
%bcond_without	doc		# don't build the documentation
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel module
%bcond_without	userspace	# don't build userspace package
%bcond_with	webservice	# webservice (soap) support
%bcond_without	verbose
%bcond_with	force_userspace # force userspace build (useful if alt_kernel is set)

%if %{without kernel}
%undefine	with_dist_kernel
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif
%if %{with force_userspace}
%define		with_userspace 1
%endif
%if %{without userspace}
# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0
%endif

%define		rel		8
%define		pname		VirtualBox
Summary:	VirtualBox - x86 hardware virtualizer
Summary(pl.UTF-8):	VirtualBox - wirtualizator sprzętu x86
Name:		%{pname}%{_alt_kernel}
Version:	4.2.6
Release:	%{rel}
License:	GPL v2
Group:		Applications/Emulators
Source0:	http://download.virtualbox.org/virtualbox/%{version}/%{pname}-%{version}.tar.bz2
# Source0-md5:	d680aeb3b4379b8281527aeb012b2df5
Source1:	http://download.virtualbox.org/virtualbox/%{version}/VBoxGuestAdditions_%{version}.iso
# Source1-md5:	53fc6c0e400e1e40d1896d35ba46a945
Source3:	%{pname}-vboxdrv.init
Source4:	%{pname}-vboxguest.init
Source5:	%{pname}-vboxnetflt.init
Source6:	%{pname}-vboxsf.init
Source7:	%{pname}-vboxnetadp.init
Source8:	%{pname}-vboxpci.init
Source9:	%{pname}.sh
Source10:	mount.vdi
Source11:	udev.rules
Source12:	%{pname}-vboxdrv-modules-load.conf
Source13:	%{pname}-vboxguest-modules-load.conf
Source14:	%{pname}-vboxnetflt-modules-load.conf
Source15:	%{pname}-vboxsf-modules-load.conf
Source16:	%{pname}-vboxnetadp-modules-load.conf
Source17:	%{pname}-vboxpci-modules-load.conf
Patch0:		%{pname}-configure-spaces.patch
Patch1:		%{pname}-VBoxSysInfo.patch
Patch2:		%{pname}-warning_workaround.patch
Patch3:		%{pname}-dri.patch
Patch4:		%{pname}-disable_build_NetBiosBin.patch
Patch5:		xserver-1.12.patch
# ubuntu patches
Patch10:	16-no-update.patch
Patch11:	18-system-xorg.patch
# /ubuntu patches
URL:		http://www.virtualbox.org/
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
BuildRequires:	xorg-lib-libXcomposite-devel
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-proto-glproto-devel
BuildRequires:	xorg-xserver-server-devel
%endif
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-devel
BuildRequires:	QtGui-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	QtOpenGL-devel
BuildRequires:	SDL-devel >= 1.2.7
BuildRequires:	acpica
BuildRequires:	alsa-lib-devel >= 1.0.6
BuildRequires:	bash
BuildRequires:	bcc
BuildRequires:	bin86
BuildRequires:	curl-devel
BuildRequires:	device-mapper-devel
%{?with_doc:BuildRequires:	docbook-dtd44-xml}
BuildRequires:	gcc >= 5:3.2.3
%{?with_webservice:BuildRequires:	gsoap-devel}
BuildRequires:	kBuild >= 0.1.9998-2
BuildRequires:	libIDL-devel
BuildRequires:	libcap-static
BuildRequires:	libdrm-devel
BuildRequires:	libpng-devel >= 1.2.5
BuildRequires:	libstdc++-devel >= 5:3.2.3
BuildRequires:	libstdc++-static >= 5:3.2.3
BuildRequires:	libuuid-devel
BuildRequires:	libvncserver-devel >= 0.9.9
BuildRequires:	libxml2-devel >= 2.6.26
BuildRequires:	libxslt-devel >= 1.1.17
BuildRequires:	libxslt-progs >= 1.1.17
BuildRequires:	makeself
BuildRequires:	mkisofs
BuildRequires:	pam-devel
BuildRequires:	pixman-devel
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel >= 0.9.0
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	qt4-build >= 4.2.0
BuildRequires:	qt4-linguist
BuildRequires:	rpmbuild(macros) >= 1.627
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	texlive-fonts-bitstream
BuildRequires:	texlive-fonts-other
BuildRequires:	texlive-fonts-type1-bitstream
BuildRequires:	texlive-format-pdflatex
BuildRequires:	texlive-latex-ucs
BuildRequires:	texlive-xetex
%endif
BuildRequires:	which
BuildRequires:	xalan-c-devel >= 1.10.0
BuildRequires:	xerces-c-devel >= 2.6.0
BuildRequires:	yasm
BuildRequires:	zlib-devel >= 1.2.1
%endif
%if %{with dist_kernel}
BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20
%endif
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires:	QtCore >= 4.7.0
Requires:	desktop-file-utils
Requires:	libvncserver >= 0.9.9
Suggests:	gxmessage
Provides:	group(vbox)
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{x8664}
%define		vbox_arch	amd64
%else
%define		vbox_arch	x86
%endif
%define		vbox_platform	linux.%{vbox_arch}
%define		outdir		out/%{vbox_platform}/release/bin
%define		_sbindir	/sbin

# workaround buggy 'file' results:
#
# EfiThunk:     \0
# qt_ro.qm:     \0 "<\270d\030\312\357\234\225\315!\034\277`\241\275\335B"
# VBoxEFI32.fd: \0
# VBoxEFI64.fd: \0
#
# which lead to 'Stripping ... ELF shared libraries... (...)/nls/qt_ro.qm: File format not recognized'
%define		_noautostrip	.*%{_libdir}/%{name}/.*

%description
Oracle VirtualBox is a general-purpose full virtualizer for x86
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

You should install this package in your Host OS.

%description -l pl.UTF-8
Oracle VirtualBox jest emulatorem sprzętu x86. Kierowany do zastosowań
serwerowych, desktopowych oraz wbudowanych jest obecnie jedynym
wysokiej jakości rozwiązaniem wirtualizacyjnym dostępnym również jako
Otwarte Oprogramowanie.

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

%package doc
Summary:	VirtualBox documentation
Group:		Documentation

%description doc
This package contains VirtualBox User Manual.

%package udev
Summary:	udev rules for VirtualBox kernel modules
Summary(pl.UTF-8):	Reguły udev dla modułów jądra Linuksa dla VirtualBoksa
Group:		Base/Kernel
Requires:	udev-core

%description udev
udev rules for VirtualBox kernel modules.

You should install this package in your Host OS and in Guest OS.

%description udev -l pl.UTF-8
Reguły udev dla modułów jądra Linuksa dla VirtualBoksa.

%package additions
Summary:	VirtualBox Guest Additions
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description additions
VirtualBox Guest Additions.

This package contains ISO9660 image with drivers for Guest OS.

You should install this package in your Host OS.

%package guest
Summary:	VirtualBox Guest Additions
Group:		Base
Requires:	xorg-driver-input-vboxmouse = %{version}-%{release}
Requires:	xorg-driver-video-vboxvideo = %{version}-%{release}
Suggests:	kernel%{_alt_kernel}-misc-vboxsf = %{version}-%{rel}@%{_kernel_ver_str}
Suggests:	kernel%{_alt_kernel}-misc-vboxvideo = %{version}-%{rel}@%{_kernel_ver_str}

%description guest
Tools that utilize kernel modules for supporting integration with the
Host, including file sharing and tracking of mouse pointer movement
and X.org X11 video and mouse driver.

You should install this package in your Guest OS.

%package -n pam-pam_vbox
Summary:	PAM module to perform automated guest logons
Group:		Base

%description  -n pam-pam_vbox
PAM module (Pluggable Authentication Module) which can be used to
perform automated guest logons.

%package -n xorg-driver-input-vboxmouse
Summary:	X.org mouse driver for VirtualBox guest OS
Summary(pl.UTF-8):	Sterownik myszy dla systemu gościa w VirtualBoksie
Group:		X11/Applications
Requires:	xorg-xserver-server >= 1.0.99.901
Requires:	xorg-xserver-server(xinput-abi) <= 18.0
Requires:	xorg-xserver-server(xinput-abi) >= 4.0

%description -n xorg-driver-input-vboxmouse
X.org mouse driver for VirtualBox guest OS.

%description -n xorg-driver-input-vboxmouse  -l pl.UTF-8
Sterownik myszy dla systemu gościa w VirtualBoksie.

%package -n xorg-driver-video-vboxvideo
Summary:	X.org video driver for VirtualBox guest OS
Summary(pl.UTF-8):	Sterownik grafiki dla systemu gościa w VirtualBoksie
Group:		X11/Applications
Requires:	Mesa-dri-driver-swrast
Requires:	xorg-xserver-libdri >= 1.7.4
Requires:	xorg-xserver-server >= 1.0.99.901
Requires:	xorg-xserver-server(videodrv-abi) <= 13.1
Requires:	xorg-xserver-server(videodrv-abi) >= 2.0

%description -n xorg-driver-video-vboxvideo
X.org video driver for VirtualBox guest OS.

%description -n xorg-driver-video-vboxvideo -l pl.UTF-8
Sterownik grafiki dla systemu gościa w VirtualBoksie.

%package kernel-init-host
Summary:	SysV initscripts for host kernel modules
Group:		Base/Kernel

%description kernel-init-host
SysV initscripts for host kernel modules.

%package kernel-init-guest
Summary:	SysV initscripts for guest kernel modules
Group:		Base/Kernel

%description kernel-init-guest
SysV initscripts for guest kernel modules.

# KERNEL PACKAGES

# KEEP ALL REGULAR SUBPACKAGES BEFORE KERNEL PACKAGES.

%package -n kernel%{_alt_kernel}-misc-vboxguest
Summary:	VirtualBox Guest Additions for Linux Module
Summary(pl.UTF-8):	Moduł jądra Linuksa dla VirtualBoksa
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires(post):	systemd-units >= 38
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Requires:	systemd-units >= 38
Suggests:	%{name}-kernel-init-guest >= %{version}-%{rel}
Provides:	kernel(vboxguest) = %{version}-%{rel}
Obsoletes:	kernel%{_alt_kernel}-misc-vboxadd
Conflicts:	kernel%{_alt_kernel}-misc-vboxdrv

%description -n kernel%{_alt_kernel}-misc-vboxguest
VirtualBox Guest Additions for Linux Module.

You should install this package in your Guest OS.

%description -n kernel%{_alt_kernel}-misc-vboxguest -l pl.UTF-8
Moduł jądra Linuksa vboxguest dla VirtualBoksa - dodatki dla systemu
gościa.

%package -n kernel%{_alt_kernel}-misc-vboxdrv
Summary:	VirtualBox Support Driver
Summary(pl.UTF-8):	Moduł jądra Linuksa dla VirtualBoksa
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires(post):	systemd-units >= 38
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Requires:	systemd-units >= 38
Suggests:	%{name}-kernel-init-host >= %{version}-%{rel}
Provides:	kernel(vboxdrv) = %{version}-%{rel}

%description -n kernel%{_alt_kernel}-misc-vboxdrv
VirtualBox Support Driver.

You should install this package in your Host OS.

%description -n kernel%{_alt_kernel}-misc-vboxdrv -l pl.UTF-8
Moduł jądra Linuksa dla VirtualBoksa - sterownik wsparcia dla systemu
głównego.

%package -n kernel%{_alt_kernel}-misc-vboxnetadp
Summary:	VirtualBox Network Adapter Driver
Summary(pl.UTF-8):	Moduł jądra Linuksa dla VirtualBoksa
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires(post):	systemd-units >= 38
Requires:	dev >= 2.9.0-7
Requires:	kernel%{_alt_kernel}-misc-vboxdrv
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Requires:	systemd-units >= 38
Suggests:	%{name}-kernel-init-host >= %{version}-%{rel}
Provides:	kernel(vboxnetflt) = %{version}-%{rel}

%description -n kernel%{_alt_kernel}-misc-vboxnetadp
VirtualBox Network Adapter Driver.

You should install this package in your Host OS.

%description -n kernel%{_alt_kernel}-misc-vboxnetadp -l pl.UTF-8
Moduł jądra Linuksa dla VirtualBoksa - sterownik witrualnej karty
sieciowej.

%package -n kernel%{_alt_kernel}-misc-vboxnetflt
Summary:	VirtualBox Network Filter Driver
Summary(pl.UTF-8):	Moduł jądra Linuksa dla VirtualBoksa
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires(post):	systemd-units >= 38
Requires:	dev >= 2.9.0-7
Requires:	kernel%{_alt_kernel}-misc-vboxdrv
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Requires:	systemd-units >= 38
Suggests:	%{name}-kernel-init-host >= %{version}-%{rel}
Provides:	kernel(vboxnetflt) = %{version}-%{rel}

%description -n kernel%{_alt_kernel}-misc-vboxnetflt
VirtualBox Network Filter Driver.

You should install this package in your Host OS.

%description -n kernel%{_alt_kernel}-misc-vboxnetflt -l pl.UTF-8
Moduł jądra Linuksa dla VirtualBoksa - sterownik filtrowania sieci dla
systemu głównego.

%package -n kernel%{_alt_kernel}-misc-vboxpci
Summary:	VirtualBox PCI card passthrough Driver
Summary(pl.UTF-8):	Moduł jądra Linuksa dla VirtualBoksa
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires(post):	systemd-units >= 38
Requires:	dev >= 2.9.0-7
Requires:	kernel%{_alt_kernel}-misc-vboxdrv
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Requires:	systemd-units >= 38
Suggests:	%{name}-kernel-init-host >= %{version}-%{rel}
Provides:	kernel(vboxpci) = %{version}-%{rel}

%description -n kernel%{_alt_kernel}-misc-vboxpci
VirtualBox PCI card passthrough driver that works as host proxy
between guest and PCI hardware.

You should install this package in your Host OS.

%description -n kernel%{_alt_kernel}-misc-vboxnetflt -l pl.UTF-8
Moduł jądra Linuksa dla VirtualBoksa - sterownik, ktory działa jako
proxy między gościem i gospodarzem sprzętu PCI.

%package -n kernel%{_alt_kernel}-misc-vboxsf
Summary:	Host file system access (Shared Folders) for VirtualBox
Summary(pl.UTF-8):	Moduł jądra Linuksa dla VirtualBoksa
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires(post):	systemd-units >= 38
Requires:	dev >= 2.9.0-7
Requires:	kernel%{_alt_kernel}-misc-vboxguest
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Requires:	systemd-units >= 38
Suggests:	%{name}-kernel-init-guest >= %{version}-%{rel}
Provides:	kernel(vboxsf) = %{version}-%{rel}
Obsoletes:	kernel%{_alt_kernel}-misc-vboxvfs

%description -n kernel%{_alt_kernel}-misc-vboxsf
Host file system access (Shared Folders) for VirtualBox.

You should install this package in your Guest OS.

%description -n kernel%{_alt_kernel}-misc-vboxsf -l pl.UTF-8
Moduł jądra Linuksa dla VirtualBoksa - dostęp do plików systemu
głównego z poziomu systemu gościa.

%package -n kernel%{_alt_kernel}-misc-vboxvideo
Summary:	DRM support for VirtualBox
Summary(pl.UTF-8):	Moduł jądra Linuksa dla VirtualBoksa
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
%requires_releq_kernel -n drm
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(vboxvideo) = %{version}-%{rel}

%description -n kernel%{_alt_kernel}-misc-vboxvideo
DRM support for VirtualBox.

You should install this package in your Guest OS.

%description -n kernel%{_alt_kernel}-misc-vboxvideo -l pl.UTF-8
Moduł jądra Linuksa dla VirtualBoksa - sterownik obsługi DRM.

%prep
%setup -q -n %{pname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%{__sed} -i -e 's,@VBOX_DOC_PATH@,%{_docdir}/%{name}-%{version},' \
	-e 's/Categories=.*/Categories=Utility;Emulator;/' src/VBox/Installer/common/virtualbox.desktop.in

# Respect LDFLAGS
%{__sed} -i -e "s@_LDFLAGS\.%{vbox_arch}*.*=@& %{rpmldflags}@g" \
	-i Config.kmk src/libs/xpcom18a4/Config.kmk

%{__sed} 's#@LIBDIR@#%{_libdir}#' < %{SOURCE9} > VirtualBox-wrapper.sh

install -d PLD-MODULE-BUILD/{GuestDrivers,HostDrivers}
cd PLD-MODULE-BUILD
../src/VBox/Additions/linux/export_modules guest-modules.tar.gz
tar -zxf guest-modules.tar.gz -C GuestDrivers

../src/VBox/HostDrivers/linux/export_modules host-modules.tar.gz --without-hardening
tar -zxf host-modules.tar.gz -C HostDrivers
cd -
%patch10 -p1
%patch11 -p1

# using system kBuild package
%{__rm} -r kBuild

%build
%if %{with userspace}
echo "VBOX_WITH_TESTCASES := " > LocalConfig.kmk
./configure \
	--with-gcc="%{__cc}" \
	--with-g++="%{__cxx}" \
	%{!?with_doc:--disable-docs} \
	--disable-java \
	--disable-hardening \
	--disable-kmods \
	--enable-vnc \
	%{__enable webservice} \
	%{nil}

XSERVER_VERSION=$(rpm -q --queryformat '%{VERSION}\n' xorg-xserver-server-devel | awk -F. ' { print $1 $2 } ' 2> /dev/null || echo ERROR)
kmk %{?_smp_mflags} \
	%{?with_verbose:KBUILD_VERBOSE=3} \
	USER=%(id -un) \
	VBOX_VERSION_STRING='$(VBOX_VERSION_MAJOR).$(VBOX_VERSION_MINOR).$(VBOX_VERSION_BUILD)'_PLD \
	XSERVER_VERSION="$XSERVER_VERSION" \
	TOOL_GCC3_CFLAGS="%{rpmcflags}" \
	TOOL_GCC3_CXXFLAGS="%{rpmcxxflags}" \
	VBOX_GCC_OPT="%{rpmcxxflags}" \
	%{nil}
%endif

%if %{with kernel}
export KERN_DIR=%{_kernelsrcdir}
cd PLD-MODULE-BUILD/HostDrivers
%build_kernel_modules -m vboxdrv -C vboxdrv
%build_kernel_modules -m vboxnetadp -C vboxnetadp
%build_kernel_modules -m vboxnetflt -C vboxnetflt
%build_kernel_modules -m vboxpci -C vboxpci

cd ../GuestDrivers
%build_kernel_modules -m vboxguest -C vboxguest
cp -a vboxguest/Module.symvers vboxsf
%build_kernel_modules -m vboxsf -C vboxsf -c
%build_kernel_modules -m vboxvideo -C vboxvideo
cd ../..
%{__cc} %{rpmcflags} %{rpmldflags} -Wall -Werror src/VBox/Additions/linux/sharedfolders/{mount.vboxsf.c,vbsfmount.c} -o mount.vboxsf
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}/%{pname}/ExtensionPacks} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}} \
	$RPM_BUILD_ROOT%{_libdir}/xorg/modules/{drivers,dri,input}

# test if we can hardlink -- %{_builddir} and $RPM_BUILD_ROOT on same partition
if cp -al VBox.png $RPM_BUILD_ROOT/Vbox.png 2>/dev/null; then
	l=l
	rm -f $RPM_BUILD_ROOT/VBox.png
fi

cp -a$l %{outdir}/* $RPM_BUILD_ROOT%{_libdir}/%{pname}

%if %{with doc}
ln -sf %{_docdir}/%{pname}-doc-%{version}/UserManual.pdf $RPM_BUILD_ROOT%{_libdir}/%{pname}/UserManual.pdf
ln -sf %{_docdir}/%{pname}-doc-%{version}/UserManual_fr_FR.pdf $RPM_BUILD_ROOT%{_libdir}/%{pname}/UserManual_fr_FR.pdf
%endif

install -d $RPM_BUILD_ROOT%{_libdir}/%{pname}/additions
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_libdir}/%{pname}/additions/VBoxGuestAdditions.iso
install -p %{SOURCE10} $RPM_BUILD_ROOT%{_sbindir}/mount.vdi
install -p VirtualBox-wrapper.sh $RPM_BUILD_ROOT%{_libdir}/%{pname}
for f in {VBox{BFE,Headless,Manage,SDL,SVC,Tunctl,XPCOMIPCD},VirtualBox}; do
	ln -s %{_libdir}/%{pname}/VirtualBox-wrapper.sh $RPM_BUILD_ROOT%{_bindir}/$f
done

mv $RPM_BUILD_ROOT{%{_libdir}/%{pname}/VBox.png,%{_pixmapsdir}/virtualbox.png}
mv $RPM_BUILD_ROOT{%{_libdir}/%{pname},%{_desktopdir}}/virtualbox.desktop

mv $RPM_BUILD_ROOT{%{_libdir}/%{pname}/vboxmouse_drv.so,%{_libdir}/xorg/modules/input/vboxmouse_drv.so}
mv $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions/vboxvideo_drv.so,%{_libdir}/xorg/modules/drivers/vboxvideo_drv.so}
mv $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions/VBoxOGL.so,%{_libdir}/xorg/modules/dri/vboxvideo_dri.so}
# xorg other driver versions
rm -vf $RPM_BUILD_ROOT%{_libdir}/%{pname}/vboxmouse_drv*.{o,so}
rm -vf $RPM_BUILD_ROOT%{_libdir}/%{pname}/vboxvideo_drv*.{o,so}

# XXX: where else to install them that vboxvideo_dri.so finds them? patch with rpath?
mv $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_libdir}}/VBoxOGLarrayspu.so
mv $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_libdir}}/VBoxOGLcrutil.so
mv $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_libdir}}/VBoxOGLerrorspu.so
mv $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_libdir}}/VBoxOGLfeedbackspu.so
mv $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_libdir}}/VBoxOGLpackspu.so
mv $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_libdir}}/VBoxOGLpassthroughspu.so

install -d $RPM_BUILD_ROOT/etc/udev/rules.d
cp -a %{SOURCE11} $RPM_BUILD_ROOT/etc/udev/rules.d/virtualbox.rules

install -d $RPM_BUILD_ROOT/%{_lib}/security
mv $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,/%{_lib}/security}/pam_vbox.so

# cleanup unpackaged
rm -r $RPM_BUILD_ROOT%{_libdir}/%{pname}/{src,sdk,testcase}
rm -r $RPM_BUILD_ROOT%{_libdir}/%{pname}/additions/src
rm $RPM_BUILD_ROOT%{_libdir}/%{pname}/vboxkeyboard.tar.bz2
rm $RPM_BUILD_ROOT%{_libdir}/%{pname}/tst*
rm $RPM_BUILD_ROOT%{_libdir}/%{pname}/ExtensionPacks/VNC/ExtPack-license.*

# Guest Only Tools
install -d $RPM_BUILD_ROOT/etc/{X11/xinit/xinitrc.d,xdg/autostart}
mv $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_bindir}}/VBoxService
mv $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_bindir}}/VBoxClient
mv $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_bindir}}/VBoxControl
install -p -D src/VBox/Additions/x11/Installer/98vboxadd-xclient \
	$RPM_BUILD_ROOT/etc/X11/xinit/xinitrc.d/98vboxadd-xclient.sh
cp -p src/VBox/Additions/x11/Installer/vboxclient.desktop \
	$RPM_BUILD_ROOT/etc/xdg/autostart/vboxclient.desktop

# unknown - checkme
%if 1
rm $RPM_BUILD_ROOT%{_libdir}/%{pname}/SUPInstall
rm $RPM_BUILD_ROOT%{_libdir}/%{pname}/SUPLoggerCtl
rm $RPM_BUILD_ROOT%{_libdir}/%{pname}/SUPUninstall
rm $RPM_BUILD_ROOT%{_libdir}/%{pname}/VBox.sh
rm $RPM_BUILD_ROOT%{_libdir}/%{pname}/vboxshell.py
rm $RPM_BUILD_ROOT%{_libdir}/%{pname}/xpidl
rm $RPM_BUILD_ROOT%{_libdir}/%{pname}/additions/runasroot.sh
rm $RPM_BUILD_ROOT%{_libdir}/%{pname}/load.sh
rm $RPM_BUILD_ROOT%{_libdir}/%{pname}/loadall.sh
rm $RPM_BUILD_ROOT%{_libdir}/%{pname}/dtrace/lib/%{vbox_arch}/CPUMInternal.d
rm $RPM_BUILD_ROOT%{_libdir}/%{pname}/dtrace/lib/%{vbox_arch}/cpumctx.d
rm $RPM_BUILD_ROOT%{_libdir}/%{pname}/dtrace/lib/%{vbox_arch}/vbox-arch-types.d
rm $RPM_BUILD_ROOT%{_libdir}/%{pname}/dtrace/lib/%{vbox_arch}/vbox-types.d
rm $RPM_BUILD_ROOT%{_libdir}/%{pname}/dtrace/lib/%{vbox_arch}/vm.d
rm $RPM_BUILD_ROOT%{_libdir}/%{pname}/dtrace/lib/%{vbox_arch}/x86.d
rm $RPM_BUILD_ROOT%{_libdir}/%{pname}/dtrace/testcase/%{vbox_arch}/vbox-vm-struct-test.d
%endif

# packaged by kernel part
rm $RPM_BUILD_ROOT%{_libdir}/%{pname}/additions/mount.vboxsf
%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,modules-load.d},%{_sbindir},%{systemdunitdir}}
install -p %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/vboxdrv
install -p %{SOURCE4} $RPM_BUILD_ROOT/etc/rc.d/init.d/vboxguest
install -p %{SOURCE5} $RPM_BUILD_ROOT/etc/rc.d/init.d/vboxnetflt
install -p %{SOURCE6} $RPM_BUILD_ROOT/etc/rc.d/init.d/vboxsf
install -p %{SOURCE7} $RPM_BUILD_ROOT/etc/rc.d/init.d/vboxnetadp
install -p %{SOURCE8} $RPM_BUILD_ROOT/etc/rc.d/init.d/vboxpci
%install_kernel_modules -m PLD-MODULE-BUILD/HostDrivers/vboxdrv/vboxdrv -d misc
%install_kernel_modules -m PLD-MODULE-BUILD/HostDrivers/vboxnetadp/vboxnetadp -d misc
%install_kernel_modules -m PLD-MODULE-BUILD/HostDrivers/vboxnetflt/vboxnetflt -d misc
%install_kernel_modules -m PLD-MODULE-BUILD/HostDrivers/vboxpci/vboxpci -d misc
%install_kernel_modules -m PLD-MODULE-BUILD/GuestDrivers/vboxguest/vboxguest -d misc
%install_kernel_modules -m PLD-MODULE-BUILD/GuestDrivers/vboxsf/vboxsf -d misc
%install_kernel_modules -m PLD-MODULE-BUILD/GuestDrivers/vboxvideo/vboxvideo -d misc

install -p mount.vboxsf $RPM_BUILD_ROOT%{_sbindir}/mount.vboxsf

# Tell systemd to load modules
cp -p %{SOURCE12} $RPM_BUILD_ROOT/etc/modules-load.d/vboxdrv.conf
cp -p %{SOURCE13} $RPM_BUILD_ROOT/etc/modules-load.d/vboxguest.conf
cp -p %{SOURCE14} $RPM_BUILD_ROOT/etc/modules-load.d/vboxnetflt.conf
cp -p %{SOURCE15} $RPM_BUILD_ROOT/etc/modules-load.d/vboxsf.conf
cp -p %{SOURCE16} $RPM_BUILD_ROOT/etc/modules-load.d/vboxnetadp.conf
cp -p %{SOURCE17} $RPM_BUILD_ROOT/etc/modules-load.d/vboxpci.conf

# And mask module-loading services
ln -sf /dev/null $RPM_BUILD_ROOT%{systemdunitdir}/vboxdrv.service
ln -sf /dev/null $RPM_BUILD_ROOT%{systemdunitdir}/vboxguest.service
ln -sf /dev/null $RPM_BUILD_ROOT%{systemdunitdir}/vboxnetflt.service
ln -sf /dev/null $RPM_BUILD_ROOT%{systemdunitdir}/vboxsf.service
ln -sf /dev/null $RPM_BUILD_ROOT%{systemdunitdir}/vboxnetadp.service
ln -sf /dev/null $RPM_BUILD_ROOT%{systemdunitdir}/vboxpci.service
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 221 -r -f vbox

%post
%update_desktop_database

cat << 'EOF'
You must install vboxdrv kernel module for this software to work:
    kernel-misc-vboxdrv-%{version}-%{rel}@%{_kernel_ver_str}

Additionally you might want to install:
    kernel-misc-vboxnetadp-%{version}-%{rel}@%{_kernel_ver_str}
    kernel-misc-vboxnetflt-%{version}-%{rel}@%{_kernel_ver_str}
    kernel-misc-vboxpci-%{version}-%{rel}@%{_kernel_ver_str}

On Guest Linux system you might want to install:
    kernel-misc-vboxguest-%{version}-%{rel}@%{_kernel_ver_str}
    kernel-misc-vboxsf-%{version}-%{rel}@%{_kernel_ver_str}
    kernel-misc-vboxvideo-%{version}-%{rel}@%{_kernel_ver_str}

EOF

%postun
if [ "$1" = "0" ]; then
	%groupremove vbox
fi

%post	-n kernel%{_alt_kernel}-misc-vboxguest
%depmod %{_kernel_ver}
/sbin/chkconfig --add vboxguest
%service vboxguest restart "VirtualBox Guest additions driver"
%systemd_reload

%postun	-n kernel%{_alt_kernel}-misc-vboxguest
%depmod %{_kernel_ver}

%preun -n kernel%{_alt_kernel}-misc-vboxguest
if [ "$1" = "0" ]; then
	%service vboxguest stop
	/sbin/chkconfig --del vboxguest
fi

%post	-n kernel%{_alt_kernel}-misc-vboxdrv
%depmod %{_kernel_ver}
/sbin/chkconfig --add vboxdrv
%service vboxdrv restart "VirtualBox Support Driver"
%systemd_reload

%postun	-n kernel%{_alt_kernel}-misc-vboxdrv
%depmod %{_kernel_ver}

%preun -n kernel%{_alt_kernel}-misc-vboxdrv
if [ "$1" = "0" ]; then
	%service vboxdrv stop
	/sbin/chkconfig --del vboxdrv
fi

%post	-n kernel%{_alt_kernel}-misc-vboxnetadp
%depmod %{_kernel_ver}
/sbin/chkconfig --add vboxnetadp
%service vboxnetadp restart "VirtualBox Network HostOnly driver"
%systemd_reload

%postun	-n kernel%{_alt_kernel}-misc-vboxnetadp
%depmod %{_kernel_ver}

%preun -n kernel%{_alt_kernel}-misc-vboxnetadp
if [ "$1" = "0" ]; then
	%service vboxnetadp stop
	/sbin/chkconfig --del vboxnetadp
fi

%post	-n kernel%{_alt_kernel}-misc-vboxnetflt
%depmod %{_kernel_ver}
/sbin/chkconfig --add vboxnetflt
%service vboxnetflt restart "VirtualBox Network Filter driver"
%systemd_reload

%postun	-n kernel%{_alt_kernel}-misc-vboxnetflt
%depmod %{_kernel_ver}

%preun -n kernel%{_alt_kernel}-misc-vboxnetflt
if [ "$1" = "0" ]; then
	%service vboxnetflt stop
	/sbin/chkconfig --del vboxnetflt
fi

%post	-n kernel%{_alt_kernel}-misc-vboxpci
%depmod %{_kernel_ver}
/sbin/chkconfig --add vboxpci
%service vboxnetflt restart "VirtualBox PCI passthrough driver"
%systemd_reload

%postun	-n kernel%{_alt_kernel}-misc-vboxpci
%depmod %{_kernel_ver}

%preun -n kernel%{_alt_kernel}-misc-vboxpci
if [ "$1" = "0" ]; then
	%service vboxpci stop
	/sbin/chkconfig --del vboxpci
fi

%post	-n kernel%{_alt_kernel}-misc-vboxsf
%depmod %{_kernel_ver}
/sbin/chkconfig --add vboxsf
%service vboxsf restart "VirtualBox Host file system access (Shared Folders)"
%systemd_reload

%postun	-n kernel%{_alt_kernel}-misc-vboxsf
%depmod %{_kernel_ver}

%preun -n kernel%{_alt_kernel}-misc-vboxsf
if [ "$1" = "0" ]; then
	%service vboxsf stop
	/sbin/chkconfig --del vboxsf
fi

%post	-n kernel%{_alt_kernel}-misc-vboxvideo
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-misc-vboxvideo
%depmod %{_kernel_ver}

%if %{with userspace}
%files
%defattr(644,root,root,755)
%dir %{_libdir}/%{pname}
%dir %{_libdir}/%{pname}/ExtensionPacks
%dir %{_libdir}/%{pname}/ExtensionPacks/VNC
%dir %{_libdir}/%{pname}/ExtensionPacks/VNC/linux*
%dir %{_libdir}/%{pname}/additions
%dir %{_libdir}/%{pname}/components
%dir %{_libdir}/%{pname}/nls
%attr(755,root,root) %{_bindir}/VBoxBFE
%attr(755,root,root) %{_bindir}/VBoxHeadless
%attr(755,root,root) %{_bindir}/VBoxManage
%attr(755,root,root) %{_bindir}/VBoxSDL
%attr(755,root,root) %{_bindir}/VBoxSVC
%attr(755,root,root) %{_bindir}/VBoxTunctl
%attr(755,root,root) %{_bindir}/VBoxXPCOMIPCD
%attr(755,root,root) %{_bindir}/VirtualBox
%attr(755,root,root) %{_sbindir}/mount.vdi
%attr(755,root,root) %{_libdir}/%{pname}/DBGCPlugInDiggers.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxAuth.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxAuthSimple.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxAutostart
%attr(755,root,root) %{_libdir}/%{pname}/VBoxBFE
%attr(755,root,root) %{_libdir}/%{pname}/VBoxBalloonCtrl
%attr(755,root,root) %{_libdir}/%{pname}/VBoxCreateUSBNode.sh
%attr(755,root,root) %{_libdir}/%{pname}/VBoxDbg.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxDD2.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxDD.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxDDU.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxDragAndDropSvc.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxExtPackHelperApp
%attr(755,root,root) %{_libdir}/%{pname}/VBoxGuestControlSvc.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxGuestPropSvc.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxHeadless
%attr(755,root,root) %{_libdir}/%{pname}/VBoxHostChannel.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxKeyboard.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxManage
%if %{with doc}
%attr(755,root,root) %{_libdir}/%{pname}/VBoxManageHelp
%endif
%attr(755,root,root) %{_libdir}/%{pname}/VBoxNetAdpCtl
%attr(755,root,root) %{_libdir}/%{pname}/VBoxNetDHCP
%attr(755,root,root) %{_libdir}/%{pname}/VBoxOGLhostcrutil.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxOGLhosterrorspu.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxOGLrenderspu.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxPython*.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxREM.so
%ifarch %{ix86}
%attr(755,root,root) %{_libdir}/%{pname}/VBoxREM32.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxREM64.so
%endif
%attr(755,root,root) %{_libdir}/%{pname}/VBoxRT.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxSDL
%attr(755,root,root) %{_libdir}/%{pname}/VBoxSharedClipboard.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxSharedCrOpenGL.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxSharedFolders.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxSVC
%attr(755,root,root) %{_libdir}/%{pname}/VBoxSysInfo.sh
%attr(755,root,root) %{_libdir}/%{pname}/VBoxTestOGL
%attr(755,root,root) %{_libdir}/%{pname}/VBoxTunctl
%attr(755,root,root) %{_libdir}/%{pname}/VBoxVMM.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxVMMPreload
%attr(755,root,root) %{_libdir}/%{pname}/VBoxXPCOMC.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxXPCOMIPCD
%attr(755,root,root) %{_libdir}/%{pname}/VBoxXPCOM.so
%attr(755,root,root) %{_libdir}/%{pname}/VirtualBox
%attr(755,root,root) %{_libdir}/%{pname}/VirtualBox-wrapper.sh
%attr(755,root,root) %{_libdir}/%{pname}/ExtensionPacks/VNC/linux*/VBoxVNC*.so
%{_libdir}/%{pname}/VBoxDD2GC.gc
%{_libdir}/%{pname}/VBoxDDGC.gc
%{_libdir}/%{pname}/VMMGC.gc
%{_libdir}/%{pname}/VBoxDD2R0.r0
%{_libdir}/%{pname}/VBoxDDR0.r0
%{_libdir}/%{pname}/VMMR0.r0
#%{_libdir}/%{pname}/EfiThunk
%{_libdir}/%{pname}/VBoxEFI32.fd
%{_libdir}/%{pname}/VBoxEFI64.fd
%{_libdir}/%{pname}/components/VBoxXPCOMBase.xpt
%{_libdir}/%{pname}/ExtensionPacks/VNC/ExtPack.xml
%{_libdir}/%{pname}/components/VirtualBox_XPCOM.xpt
%attr(755,root,root) %{_libdir}/%{pname}/components/VBoxC.so
%attr(755,root,root) %{_libdir}/%{pname}/components/VBoxSVCM.so
%attr(755,root,root) %{_libdir}/%{pname}/components/VBoxXPCOMIPCC.so
%lang(bg) %{_libdir}/%{pname}/nls/*_bg.qm
%lang(ca) %{_libdir}/%{pname}/nls/*_ca.qm
%lang(ca_VA) %{_libdir}/%{pname}/nls/*_ca_VA.qm
%lang(cs) %{_libdir}/%{pname}/nls/*_cs.qm
%lang(da) %{_libdir}/%{pname}/nls/*_da.qm
%lang(de) %{_libdir}/%{pname}/nls/*_de.qm
%lang(en) %{_libdir}/%{pname}/nls/*_en.qm
%lang(es) %{_libdir}/%{pname}/nls/*_es.qm
%lang(eu) %{_libdir}/%{pname}/nls/*_eu.qm
%lang(fi) %{_libdir}/%{pname}/nls/*_fa_IR.qm
%lang(fi) %{_libdir}/%{pname}/nls/*_fi.qm
%lang(fr) %{_libdir}/%{pname}/nls/*_fr.qm
%lang(gl_ES) %{_libdir}/%{pname}/nls/*_gl_ES.qm
%lang(hu) %{_libdir}/%{pname}/nls/*_hu.qm
%lang(id) %{_libdir}/%{pname}/nls/*_id.qm
%lang(it) %{_libdir}/%{pname}/nls/*_it.qm
%lang(ja) %{_libdir}/%{pname}/nls/*_ja.qm
%lang(km_KH) %{_libdir}/%{pname}/nls/*_km_KH.qm
%lang(ko) %{_libdir}/%{pname}/nls/*_ko.qm
%lang(lt) %{_libdir}/%{pname}/nls/*_lt.qm
%lang(nl) %{_libdir}/%{pname}/nls/*_nl.qm
%lang(pl) %{_libdir}/%{pname}/nls/*_pl.qm
%lang(pt) %{_libdir}/%{pname}/nls/*_pt.qm
%lang(pt_BR) %{_libdir}/%{pname}/nls/*_pt_BR.qm
%lang(ro) %{_libdir}/%{pname}/nls/*_ro.qm
%lang(ru) %{_libdir}/%{pname}/nls/*_ru.qm
%lang(sk) %{_libdir}/%{pname}/nls/*_sk.qm
%lang(sr) %{_libdir}/%{pname}/nls/*_sr.qm
%lang(sv) %{_libdir}/%{pname}/nls/*_sv.qm
%lang(tr) %{_libdir}/%{pname}/nls/*_tr.qm
%lang(uk) %{_libdir}/%{pname}/nls/*_uk.qm
%lang(zh_CN) %{_libdir}/%{pname}/nls/*_zh_CN.qm
%lang(zh_TW) %{_libdir}/%{pname}/nls/*_zh_TW.qm
%{_pixmapsdir}/virtualbox.png
%{_desktopdir}/*.desktop
%{_libdir}/%{pname}/icons
%{_libdir}/%{pname}/virtualbox.xml

%files additions
%defattr(644,root,root,755)
%{_libdir}/%{pname}/additions/VBoxGuestAdditions.iso

%files guest
%defattr(644,root,root,755)
# NOTE: unfinished, should contain .desktop files for starting up mouse
# integration and other desktop services
# NOTE: the filelist is incomplete too
%attr(755,root,root) %{_bindir}/VBoxClient
%attr(755,root,root) %{_bindir}/VBoxControl
%attr(755,root,root) %{_bindir}/VBoxService
/etc/X11/xinit/xinitrc.d/98vboxadd-xclient.sh
/etc/xdg/autostart/vboxclient.desktop

%attr(755,root,root) %{_libdir}/%{pname}/additions/autorun.sh
%attr(755,root,root) %{_libdir}/%{pname}/additions/vboxadd
%attr(755,root,root) %{_libdir}/%{pname}/additions/vboxadd-service
%attr(755,root,root) %{_libdir}/%{pname}/additions/vboxadd-x11
# XXX these files belong to xorg-driver-video-vboxvideo
# but probably 18-system-xorg.patch patch is broken?
%attr(755,root,root) %{_libdir}/%{pname}/additions/vboxvideo_drv_111.so
%attr(755,root,root) %{_libdir}/%{pname}/additions/vboxvideo_drv_112.so

%files -n pam-pam_vbox
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/security/pam_vbox.so

%if %{with doc}
%files doc
%defattr(644,root,root,755)
# this is a symlink...
%doc %{_libdir}/%{pname}/UserManual.pdf
%lang(fr) %doc %{_libdir}/%{pname}/UserManual_fr_FR.pdf
# ..to this file
%doc %{outdir}/UserManual.pdf
%lang(fr) %doc %{outdir}/UserManual_fr_FR.pdf
%endif

%files udev
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/virtualbox.rules

%files -n xorg-driver-input-vboxmouse
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/input/vboxmouse_drv.so

%files -n xorg-driver-video-vboxvideo
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/drivers/vboxvideo_drv.so
%attr(755,root,root) %{_libdir}/xorg/modules/dri/vboxvideo_dri.so
# vboxvideo_dri.so deps
%attr(755,root,root) %{_libdir}/VBoxOGLarrayspu.so
%attr(755,root,root) %{_libdir}/VBoxOGLcrutil.so
%attr(755,root,root) %{_libdir}/VBoxOGLerrorspu.so
%attr(755,root,root) %{_libdir}/VBoxOGLfeedbackspu.so
%attr(755,root,root) %{_libdir}/VBoxOGLpackspu.so
%attr(755,root,root) %{_libdir}/VBoxOGLpassthroughspu.so
%endif

%if %{with kernel}
%files kernel-init-host
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/vboxdrv
%attr(754,root,root) /etc/rc.d/init.d/vboxnetadp
%attr(754,root,root) /etc/rc.d/init.d/vboxnetflt
%attr(754,root,root) /etc/rc.d/init.d/vboxpci
%{systemdunitdir}/vboxdrv.service
%{systemdunitdir}/vboxnetadp.service
%{systemdunitdir}/vboxnetflt.service
%{systemdunitdir}/vboxpci.service

%files kernel-init-guest
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/vboxguest
%attr(754,root,root) /etc/rc.d/init.d/vboxsf
%{systemdunitdir}/vboxguest.service
%{systemdunitdir}/vboxsf.service

%files -n kernel%{_alt_kernel}-misc-vboxguest
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/modules-load.d/vboxguest.conf
/lib/modules/%{_kernel_ver}/misc/vboxguest.ko*

%files -n kernel%{_alt_kernel}-misc-vboxdrv
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/modules-load.d/vboxdrv.conf
/lib/modules/%{_kernel_ver}/misc/vboxdrv.ko*

%files -n kernel%{_alt_kernel}-misc-vboxnetadp
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/modules-load.d/vboxnetadp.conf
/lib/modules/%{_kernel_ver}/misc/vboxnetadp.ko*

%files -n kernel%{_alt_kernel}-misc-vboxnetflt
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/modules-load.d/vboxnetflt.conf
/lib/modules/%{_kernel_ver}/misc/vboxnetflt.ko*

%files -n kernel%{_alt_kernel}-misc-vboxpci
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/modules-load.d/vboxpci.conf
/lib/modules/%{_kernel_ver}/misc/vboxpci.ko*

%files -n kernel%{_alt_kernel}-misc-vboxsf
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/modules-load.d/vboxsf.conf
%attr(755,root,root) %{_sbindir}/mount.vboxsf
/lib/modules/%{_kernel_ver}/misc/vboxsf.ko*

%files -n kernel%{_alt_kernel}-misc-vboxvideo
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vboxvideo.ko*
%endif
