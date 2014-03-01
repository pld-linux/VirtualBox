# TODO
# - java bindings
# - Package SDK.
# - Check License of VBoxGuestAdditions_*.iso, it's probably not GPL v2.
#   If so check if it is distributable.
# - guest x11 additions: currently incomplete/untested
# - enable VDE networking: --enable-vde
# - initscripts for webservice
# - fix desc for dkms packages (proper wording needed), kernel modules desc is mess as well
#
# Conditional build:
%bcond_without	doc		# don't build the documentation
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel module
%bcond_without	userspace	# don't build userspace package
%bcond_with	webservice	# webservice (SOAP) support
%bcond_without	lightdm		# lightdm greeter
%bcond_without	dkms		# build dkms package
%bcond_without	verbose

%if %{without kernel}
%undefine	with_dist_kernel
%else
%define		_duplicate_files_terminate_build	0
%endif

# The goal here is to have main, userspace, package built once with
# simple release number, and only rebuild kernel packages with kernel
# version as part of release number, without the need to bump release
# with every kernel change.
%if 0%{?_pld_builder:1} && %{with kernel} && %{with userspace}
%{error:kernel and userspace cannot be built at the same time on PLD builders}
exit 1
%endif

%if "%{_alt_kernel}" != "%{nil}"
%if 0%{?build_kernels:1}
%{error:alt_kernel and build_kernels are mutually exclusive}
exit 1
%endif
%undefine	with_userspace
%global		_build_kernels		%{alt_kernel}
%else
%global		_build_kernels		%{?build_kernels:,%{?build_kernels}}
%endif

%if %{without userspace}
# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0
%endif

%define		kbrs	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo "BuildRequires:kernel%%{_alt_kernel}-module-build >= 3:2.6.20.2" ; done)
%define		kpkg	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo %%kernel_pkg ; done)
%define		bkpkg	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo %%build_kernel_pkg ; done)
%define		ikpkg	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo %%install_kernel_pkg ; done)

%define		rel		3
%define		pname		VirtualBox
Summary:	VirtualBox - x86 hardware virtualizer
Summary(pl.UTF-8):	VirtualBox - wirtualizator sprzętu x86
Name:		%{pname}%{?_pld_builder:%{?with_kernel:-kernel}}%{_alt_kernel}
Version:	4.3.8
Release:	%{rel}%{?_pld_builder:%{?with_kernel:@%{_kernel_ver_str}}}
License:	GPL v2
Group:		Applications/Emulators
Source0:	http://download.virtualbox.org/virtualbox/%{version}/%{pname}-%{version}.tar.bz2
# Source0-md5:	422ab09b7eb9c0564b55a6a0a6e6678f
Source1:	http://download.virtualbox.org/virtualbox/%{version}/VBoxGuestAdditions_%{version}.iso
# Source1-md5:	f23d3980a509418b2dcb614483271ffa
Source2:	vboxservice.init
Source3:	vboxservice.service
Source4:	%{pname}.sh
Source5:	mount.vdi
Source6:	udev.rules
Source7:	%{pname}-virtualbox-host-modules-load.conf
Source8:	%{pname}-virtualbox-guest-modules-load.conf
Patch0:		%{pname}-configure-spaces.patch
Patch1:		%{pname}-VBoxSysInfo.patch
Patch2:		%{pname}-warning_workaround.patch
Patch3:		%{pname}-dri.patch
Patch5:		xserver-1.12.patch
Patch7:		lightdm-greeter-glib-includes.patch
Patch8:		lightdm-greeter-g++-link.patch
Patch9:		pld-guest.patch
Patch10:	16-no-update.patch
Patch11:	18-system-xorg.patch
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
%{?with_lightdm:BuildRequires:	fltk-devel}
BuildRequires:	gcc >= 5:3.2.3
%{?with_webservice:BuildRequires:	gsoap-devel}
BuildRequires:	issue
BuildRequires:	kBuild >= 0.1.9998.2700
BuildRequires:	libIDL-devel
BuildRequires:	libcap-static
BuildRequires:	libdrm-devel
BuildRequires:	libpng-devel >= 1.2.5
BuildRequires:	libstdc++-devel >= 5:3.2.3
BuildRequires:	libstdc++-static >= 5:3.2.3
BuildRequires:	libuuid-devel
BuildRequires:	libvncserver-devel >= 0.9.9
BuildRequires:	libvpx-devel
BuildRequires:	libxml2-devel >= 2.6.26
BuildRequires:	libxslt-devel >= 1.1.17
BuildRequires:	libxslt-progs >= 1.1.17
%{?with_lightdm:BuildRequires:	lightdm-libs-qt-devel}
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
BuildRequires:	rpmbuild(macros) >= 1.678
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
%{?with_dist_kernel:%{expand:%kbrs}}
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires:	libvncserver >= 0.9.9
Requires:	udev-core
Provides:	group(vbox)
Obsoletes:	VirtualBox-udev < 4.2.10-5
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{x8664}
%define		vbox_arch	amd64
%else
%define		vbox_arch	x86
%endif
%define		vbox_platform	linux.%{vbox_arch}
%define		outdir		out/%{vbox_platform}/release/bin
%define		objdir		out/%{vbox_platform}/release/obj

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

%package gui
Summary:	Qt GUI part for VirtualBox
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	QtCore >= 4.7.0
Requires:	desktop-file-utils
Requires:	desktop-file-utils
Requires:	fontconfig
Requires:	fonts-Type1-urw
Requires:	shared-mime-info
Suggests:	gxmessage
Conflicts:	%{name} < 4.3.8-3

%description gui
Qt GUI part for VirtualBox.

%package doc
Summary:	VirtualBox documentation
Group:		Documentation

%description doc
This package contains VirtualBox User Manual.

%package additions
Summary:	VirtualBox Guest Additions
Group:		Base
Requires:	%{name} = %{version}

%description additions
VirtualBox Guest Additions.

This package contains ISO9660 image with drivers for Guest OS.

You should install this package in your Host OS.

%package guest
Summary:	VirtualBox Guest tools
Group:		Base
Requires(post,preun):	/sbin/chkconfig
Requires(post):	systemd-units >= 38
Requires:	rc-scripts
Requires:	systemd-units >= 38
Suggests:	kernel(vboxguest)
Suggests:	kernel(vboxsf)
Suggests:	pam-pam_vbox

%description guest
Tools that utilize kernel modules for supporting integration with the
Host, including file sharing.

You should install this package in your Guest OS for base VirtualBox
communication

%package guest-x11
Summary:	VirtualBox Guest Additions
Group:		Base
Requires:	%{name}-guest = %{version}-%{release}
Requires:	xorg-driver-video-vboxvideo = %{version}-%{release}
Suggests:	kernel(vboxvideo)
Obsoletes:	xorg-driver-input-vboxmouse < %{version}-%{release}

%description guest-x11
Tools for X11 session that utilize kernel modules for supporting
integration with the Host, like tracking of mouse pointer movement and
X.org X11 video and mouse drivers

You should install this package in your Guest OS for X11 session.

%package webservice
Summary:	VirtualBox Web Service
Group:		Applications/Emulators
Requires:	%{name} = %{version}-%{release}

%description webservice
This package contains VirtualBox web service API daemon. It allows to
control virtual machines via web interface.

%package -n lightdm-greeter-vbox
Summary:	VirtualBox greeter for lightdm
Group:		Themes
# NOTE: '#' in url is lost because rpm treats it as comment, even hacking with
# macros doesn't help as rpmbuild takes final result to parse
URL:		http://www.virtualbox.org/manual/ch09.html#autologon_unix_lightdm
Requires:	kernel(vboxguest)
Requires:	lightdm >= 1.0.1
Provides:	lightdm-greeter

%description -n lightdm-greeter-vbox
VirtualBox greeter for LightDM.

%package -n pam-pam_vbox
Summary:	PAM module to perform automated guest logons
Group:		Base

%description  -n pam-pam_vbox
PAM module (Pluggable Authentication Module) which can be used to
perform automated guest logons.

%package -n xorg-driver-video-vboxvideo
Summary:	X.org video driver for VirtualBox guest OS
Summary(pl.UTF-8):	Sterownik grafiki dla systemu gościa w VirtualBoksie
Group:		X11/Applications
Requires:	Mesa-dri-driver-swrast
Requires:	xorg-xserver-libdri >= 1.7.4
Requires:	xorg-xserver-server >= 1.0.99.901
Requires:	xorg-xserver-server(videodrv-abi) <= 15.0
Requires:	xorg-xserver-server(videodrv-abi) >= 2.0
Provides:	xorg-driver-video

%description -n xorg-driver-video-vboxvideo
X.org video driver for VirtualBox guest OS.

%description -n xorg-driver-video-vboxvideo -l pl.UTF-8
Sterownik grafiki dla systemu gościa w VirtualBoksie.

%package -n dkms-vboxguest
Summary:	VirtualBox kernel modules source for Linux Guest
Summary(pl.UTF-8):	Moduły VirtualBoksa do jądra Linuksa dla systemu gościa
License:	GPL v2+
Group:		Base/Kernel
Requires(pre):	dkms
Requires(post):	dkms
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n dkms-vboxguest
This package contains DKMS-ready VirtualBox Guest Additions for Linux
Module, host file system access (Shared Folders) and DRM support for
Linux guest system.

%description -n dkms-vboxguest -l pl.UTF-8
Ten pakiet zawiera moduł jądra Linuksa vboxguest dla VirtualBoksa -
dodatki dla systemu gościa, dostęp do plików systemu głównego z
poziomu systemu gościa i sterownik obsługi DRM.

%package -n dkms-vboxhost
Summary:	VirtualBox Support Drivers source
Summary(pl.UTF-8):	Moduły jądra Linuksa dla VirtualBoksa
License:	GPL v2+
Group:		Base/Kernel
Requires(pre):	dkms
Requires(post):	dkms
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n dkms-vboxhost
This package contains DKMS enabled sourcecode of VirtualBox Support
Driver, Network Adapter Driver, Network Filter Driver and PCI card
passthrough driver that works as host proxy between guest and PCI
hardware.

%description -n dkms-vboxhost -l pl.UTF-8
Ten pakiet zawiera sterownik wsparcia dla systemu głównego, sterownik
witrualnej karty sieciowej, sterownik filtrowania sieci dla systemu
głównego oraz sterownik, ktory działa jako proxy między gościem i
gospodarzem sprzętu PCI.

# KERNEL PACKAGES

# KEEP ALL REGULAR SUBPACKAGES BEFORE KERNEL PACKAGES.

%define	kernel_pkg()\
%package -n kernel%{_alt_kernel}-virtualbox-guest\
Summary:	VirtualBox kernel modules for Linux Guest\
Summary(pl.UTF-8):	Moduły VirtualBoksa do jądra Linuksa dla systemu gościa\
Release:	%{rel}@%{_kernel_ver_str}\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
Requires(post):	systemd-units >= 38\
Requires:	dev >= 2.9.0-7\
Requires:	systemd-units >= 38\
%if %{with dist_kernel}\
%requires_releq_kernel\
Requires:	%{releq_kernel -n drm}\
Requires(postun):	%releq_kernel\
%endif\
Provides:	kernel(vboxguest) = %{version}-%{rel}\
Provides:	kernel(vboxsf) = %{version}-%{rel}\
Provides:	kernel(vboxvideo) = %{version}-%{rel}\
Obsoletes:	kernel-init-guest\
Conflicts:	kernel%{_alt_kernel}-virtualbox-host\
\
%description -n kernel%{_alt_kernel}-virtualbox-guest\
This package contains VirtualBox Guest Additions for Linux Module,\
host file system access (Shared Folders) and DRM support for\
Linux guest system.\
\
%description -n kernel%{_alt_kernel}-virtualbox-guest -l pl.UTF-8\
Ten pakiet zawiera moduł jądra Linuksa vboxguest dla VirtualBoksa -\
dodatki dla systemu gościa, dostęp do plików systemu głównego z\
poziomu systemu gościa i sterownik obsługi DRM.\
\
%package -n kernel%{_alt_kernel}-virtualbox-host\
Summary:	VirtualBox Support Drivers\
Summary(pl.UTF-8):	Moduły jądra Linuksa dla VirtualBoksa\
Release:	%{rel}@%{_kernel_ver_str}\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
Requires(post):	systemd-units >= 38\
Requires:	dev >= 2.9.0-7\
%if %{with dist_kernel}\
%requires_releq_kernel\
Requires(postun):	%releq_kernel\
%endif\
Requires:	systemd-units >= 38\
Provides:	kernel(vboxdrv) = %{version}-%{rel}\
Provides:	kernel(vboxnetadp) = %{version}-%{rel}\
Provides:	kernel(vboxnetflt) = %{version}-%{rel}\
Provides:	kernel(vboxpci) = %{version}-%{rel}\
Obsoletes:	kernel-init-host\
\
%description -n kernel%{_alt_kernel}-virtualbox-host\
This package contains VirtualBox Support Driver, Network Adapter\
Driver, Network Filter Driver and PCI card passthrough driver that\
works as host proxy between guest and PCI hardware.\
\
%description -n kernel%{_alt_kernel}-virtualbox-host -l pl.UTF-8\
Ten pakiet zawiera sterownik wsparcia dla systemu głównego, sterownik\
witrualnej karty sieciowej, sterownik filtrowania sieci dla systemu\
głównego oraz sterownik, ktory działa jako proxy między gościem i\
gospodarzem sprzętu PCI.\
\
%if %{with kernel}\
%files -n kernel%{_alt_kernel}-virtualbox-guest\
%defattr(644,root,root,755)\
%config(noreplace) %verify(not md5 mtime size) /etc/modules-load.d/virtualbox-guest.conf\
/lib/modules/%{_kernel_ver}/misc/vboxguest.ko*\
/lib/modules/%{_kernel_ver}/misc/vboxsf.ko*\
/lib/modules/%{_kernel_ver}/misc/vboxvideo.ko*\
\
%files -n kernel%{_alt_kernel}-virtualbox-host\
%config(noreplace) %verify(not md5 mtime size) /etc/modules-load.d/virtualbox-host.conf\
/lib/modules/%{_kernel_ver}/misc/vboxdrv.ko*\
/lib/modules/%{_kernel_ver}/misc/vboxnetadp.ko*\
/lib/modules/%{_kernel_ver}/misc/vboxnetflt.ko*\
/lib/modules/%{_kernel_ver}/misc/vboxpci.ko*\
%endif\
\
%post -n kernel%{_alt_kernel}-virtualbox-guest\
%depmod %{_kernel_ver}\
\
%postun	-n kernel%{_alt_kernel}-virtualbox-guest\
%depmod %{_kernel_ver}\
\
%post	-n kernel%{_alt_kernel}-virtualbox-host\
%depmod %{_kernel_ver}\
\
%postun	-n kernel%{_alt_kernel}-virtualbox-host\
%depmod %{_kernel_ver}\
%{nil}

%define build_kernel_pkg()\
export KERN_DIR=%{_kernelsrcdir}\
cd PLD-MODULE-BUILD/HostDrivers\
%build_kernel_modules -m vboxdrv -C vboxdrv\
%build_kernel_modules -m vboxnetadp -C vboxnetadp\
%build_kernel_modules -m vboxnetflt -C vboxnetflt\
%build_kernel_modules -m vboxpci -C vboxpci\
cd ../GuestDrivers\
%build_kernel_modules -m vboxguest -C vboxguest\
cp -a vboxguest/Module.symvers vboxsf\
%build_kernel_modules -m vboxsf -C vboxsf -c\
%build_kernel_modules -m vboxvideo -C vboxvideo\
cd ../..\
%install_kernel_modules -D PLD-MODULE-BUILD/installed -m PLD-MODULE-BUILD/HostDrivers/vboxdrv/vboxdrv -d misc\
%install_kernel_modules -D PLD-MODULE-BUILD/installed -m PLD-MODULE-BUILD/HostDrivers/vboxnetadp/vboxnetadp -d misc\
%install_kernel_modules -D PLD-MODULE-BUILD/installed -m PLD-MODULE-BUILD/HostDrivers/vboxnetflt/vboxnetflt -d misc\
%install_kernel_modules -D PLD-MODULE-BUILD/installed -m PLD-MODULE-BUILD/HostDrivers/vboxpci/vboxpci -d misc\
%install_kernel_modules -D PLD-MODULE-BUILD/installed -m PLD-MODULE-BUILD/GuestDrivers/vboxguest/vboxguest -d misc\
%install_kernel_modules -D PLD-MODULE-BUILD/installed -m PLD-MODULE-BUILD/GuestDrivers/vboxsf/vboxsf -d misc\
%install_kernel_modules -D PLD-MODULE-BUILD/installed -m PLD-MODULE-BUILD/GuestDrivers/vboxvideo/vboxvideo -d misc\
%{nil}

%{?with_kernel:%{expand:%kpkg}}

%prep
%setup -q -n %{pname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%{__sed} -i -e 's,@VBOX_DOC_PATH@,%{_docdir}/%{name}-%{version},' \
	-e 's/Categories=.*/Categories=Utility;Emulator;/' src/VBox/Installer/common/virtualbox.desktop.in

# Respect LDFLAGS
%{__sed} -i -e "s@_LDFLAGS\.%{vbox_arch}*.*=@& %{rpmldflags}@g" \
	-i Config.kmk src/libs/xpcom18a4/Config.kmk

%{__sed} 's#@LIBDIR@#%{_libdir}#' < %{SOURCE4} > VirtualBox-wrapper.sh

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

# use linux icon for now
cp -p src/VBox/Frontends/VirtualBox/images/os_{linux26,pld}.png
cp -p src/VBox/Frontends/VirtualBox/images/os_{linux26,pld}_64.png

cat <<'EOF'>> LocalConfig.kmk
%{?with_verbose:KBUILD_VERBOSE=3}
USERNAME=%(id -un)
__VBOX_BUILD_PUBLISHER=_PLD
VBOX_VERSION_STRING=$(VBOX_VERSION_MAJOR).$(VBOX_VERSION_MINOR).$(VBOX_VERSION_BUILD)_PLD
XSERVER_VERSION=%(rpm -q --queryformat '%{V}\n' xorg-xserver-server-devel | awk -F. '{ print $1 $2 }' 2>/dev/null || echo ERROR)
VBOX_USE_SYSTEM_XORG_HEADERS=1
%if %{with lightdm}
VBOX_WITH_LIGHTDM_GREETER=1
VBOX_WITH_LIGHTDM_GREETER_PACKING=1
%endif
TOOL_GCC3_CFLAGS=%{rpmcflags}
TOOL_GCC3_CXXFLAGS=%{rpmcxxflags}
VBOX_GCC_OPT=%{rpmcxxflags}
VBOX_WITH_TESTCASES=
EOF

%build
%if %{with userspace}
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

kmk %{?_smp_mflags}

%{__cc} %{rpmcflags} %{rpmldflags} -Wall -Werror src/VBox/Additions/linux/sharedfolders/{mount.vboxsf.c,vbsfmount.c} -o mount.vboxsf
%endif

%{?with_kernel:%{expand:%bkpkg}}

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d $RPM_BUILD_ROOT{%{_bindir},/sbin,%{_sbindir},%{_libdir}/%{pname}/ExtensionPacks} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir},%{_datadir}/mime/packages} \
	$RPM_BUILD_ROOT%{_libdir}/xorg/modules/{drivers,dri,input} \
	$RPM_BUILD_ROOT{/lib/udev,/etc/udev/rules.d} \
	$RPM_BUILD_ROOT{/etc/rc.d/init.d,%{systemdunitdir}}

# test if we can hardlink -- %{_builddir} and $RPM_BUILD_ROOT on same partition
if cp -al COPYING $RPM_BUILD_ROOT/COPYING; then
	l=l
	%{__rm} -f $RPM_BUILD_ROOT/COPYING
fi

cp -a$l %{outdir}/* $RPM_BUILD_ROOT%{_libdir}/%{pname}

%if %{with doc}
ln -sf %{_docdir}/%{pname}-doc-%{version}/UserManual.pdf $RPM_BUILD_ROOT%{_libdir}/%{pname}/UserManual.pdf
ln -sf %{_docdir}/%{pname}-doc-%{version}/UserManual_fr_FR.pdf $RPM_BUILD_ROOT%{_libdir}/%{pname}/UserManual_fr_FR.pdf
%endif

install -d $RPM_BUILD_ROOT%{_libdir}/%{pname}/additions
cp -a$l %{SOURCE1} $RPM_BUILD_ROOT%{_libdir}/%{pname}/additions/VBoxGuestAdditions.iso
install -p %{SOURCE5} $RPM_BUILD_ROOT/sbin/mount.vdi
install -p VirtualBox-wrapper.sh $RPM_BUILD_ROOT%{_libdir}/%{pname}
for f in {VBox{BFE,Headless,Manage,SDL,SVC,Tunctl,XPCOMIPCD},VirtualBox}; do
	ln -s %{_libdir}/%{pname}/VirtualBox-wrapper.sh $RPM_BUILD_ROOT%{_bindir}/$f
done

install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/vboxservice
install -p %{SOURCE3} $RPM_BUILD_ROOT%{systemdunitdir}/vboxservice.service

%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname}/VBox.png,%{_pixmapsdir}/virtualbox.png}
%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname},%{_desktopdir}}/virtualbox.desktop
%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname},%{_datadir}/mime/packages}/virtualbox.xml

%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions/vboxvideo_drv_system.so,%{_libdir}/xorg/modules/drivers/vboxvideo_drv.so}
%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions/VBoxOGL.so,%{_libdir}/xorg/modules/dri/vboxvideo_dri.so}

# XXX: where else to install them that vboxvideo_dri.so finds them? patch with rpath?
%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_libdir}}/VBoxOGLarrayspu.so
%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_libdir}}/VBoxOGLcrutil.so
%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_libdir}}/VBoxOGLerrorspu.so
%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_libdir}}/VBoxOGLfeedbackspu.so
%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_libdir}}/VBoxOGLpackspu.so
%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_libdir}}/VBoxOGLpassthroughspu.so

cp -a %{SOURCE6} $RPM_BUILD_ROOT/etc/udev/rules.d/virtualbox.rules
%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname},/lib/udev}/VBoxCreateUSBNode.sh

install -d $RPM_BUILD_ROOT/%{_lib}/security
%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,/%{_lib}/security}/pam_vbox.so

# cleanup unpackaged
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{pname}/{src,sdk,testcase}
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{pname}/additions/src
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/vboxkeyboard.tar.bz2
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/tst*
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/ExtensionPacks/VNC/ExtPack-license.*

# Guest Only Tools
install -d $RPM_BUILD_ROOT/etc/{X11/xinit/xinitrc.d,xdg/autostart}
%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_bindir}}/VBoxService
%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_bindir}}/VBoxClient
%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_bindir}}/VBoxControl
install -p -D src/VBox/Additions/x11/Installer/98vboxadd-xclient \
	$RPM_BUILD_ROOT/etc/X11/xinit/xinitrc.d/98vboxadd-xclient.sh
cp -p src/VBox/Additions/x11/Installer/vboxclient.desktop \
	$RPM_BUILD_ROOT/etc/xdg/autostart/vboxclient.desktop

%if %{with lightdm}
install -d $RPM_BUILD_ROOT%{_datadir}/xgreeters
%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_sbindir}}/vbox-greeter
cp -p %{objdir}/Additions/Installer/linux/share/VBoxGuestAdditions/vbox-greeter.desktop $RPM_BUILD_ROOT%{_datadir}/xgreeters
%endif

# unknown - checkme
%if 1
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/SUPInstall
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/SUPLoggerCtl
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/SUPUninstall
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/VBox.sh
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/vboxshell.py
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/xpidl
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/additions/runasroot.sh
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/load.sh
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/loadall.sh
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/dtrace/lib/%{vbox_arch}/CPUMInternal.d
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/dtrace/lib/%{vbox_arch}/cpumctx.d
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/dtrace/lib/%{vbox_arch}/vbox-arch-types.d
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/dtrace/lib/%{vbox_arch}/vbox-types.d
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/dtrace/lib/%{vbox_arch}/vm.d
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/dtrace/lib/%{vbox_arch}/x86.d
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/dtrace/testcase/%{vbox_arch}/vbox-vm-struct-test.d
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/helpers/generate_service_file
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/scripts/VBoxHeadlessXOrg.sh
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/scripts/generated.sh
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/scripts/init_template.sh
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/scripts/install_service
%endif

%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/additions/mount.vboxsf

install -p mount.vboxsf $RPM_BUILD_ROOT/sbin/mount.vboxsf

%if %{with dkms}
install -d $RPM_BUILD_ROOT%{_usrsrc}/vbox{host,guest}-%{version}-%{rel}
cp -a PLD-MODULE-BUILD/HostDrivers/* $RPM_BUILD_ROOT%{_usrsrc}/vboxhost-%{version}-%{rel}
cp -p src/VBox/HostDrivers/linux/dkms.conf $RPM_BUILD_ROOT%{_usrsrc}/vboxhost-%{version}-%{rel}
%{__make} -C $RPM_BUILD_ROOT%{_usrsrc}/vboxhost-%{version}-%{rel} clean
rm -rf $RPM_BUILD_ROOT%{_usrsrc}/vboxhost-%{version}-%{rel}/*/o

cp -a PLD-MODULE-BUILD/GuestDrivers/* $RPM_BUILD_ROOT%{_usrsrc}/vboxguest-%{version}-%{rel}
cp -p src/VBox/Additions/common/VBoxGuest/linux/dkms.conf $RPM_BUILD_ROOT%{_usrsrc}/vboxguest-%{version}-%{rel}
%{__make} -C $RPM_BUILD_ROOT%{_usrsrc}/vboxguest-%{version}-%{rel} clean
rm -rf $RPM_BUILD_ROOT%{_usrsrc}/vboxguest-%{version}-%{rel}/*/o
%endif
%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT{/etc/modules-load.d,/sbin}

cp -a PLD-MODULE-BUILD/installed/* $RPM_BUILD_ROOT

# Tell systemd to load modules
cp -p %{SOURCE7} $RPM_BUILD_ROOT/etc/modules-load.d/virtualbox-host.conf
cp -p %{SOURCE8} $RPM_BUILD_ROOT/etc/modules-load.d/virtualbox-guest.conf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 221 -r -f vbox

%post
for i in /sys/bus/usb/devices/*; do
	if [ -r "$i/dev" ]; then
		dev="`cat "$i/dev" 2>/dev/null || true`"
		major="`expr "$dev" : '\(.*\):' 2> /dev/null || true`"
		minor="`expr "$dev" : '.*:\(.*\)' 2> /dev/null || true`"
		class="`cat $i/bDeviceClass 2> /dev/null || true`"
		/lib/udev/VBoxCreateUSBNode.sh "$major" "$minor" "$class" vbox 2>/dev/null
	fi
done

cat << 'EOF'
You must install vboxdrv kernel modules for this software to work:
    kernel*-virtualbox-host-%{version}-%{rel}@*

On Guest Linux system you might want to install:
    kernel*-virtualbox-guest-%{version}-%{rel}@*

EOF

%postun
if [ "$1" = "0" ]; then
	%groupremove vbox
fi

%post gui
%update_desktop_database
%update_mime_database

%postun gui
%update_desktop_database
%update_mime_database

%post guest
/sbin/chkconfig --add vboxservice
%service vboxservice restart
%systemd_post vboxservice.service

%preun guest
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del vboxservice
	%service vboxservice -q stop
fi
%systemd_preun vboxservice.service

%postun guest
%systemd_reload

%triggerpostun guest -- VirtualBox-guest < 4.3.0-1
%systemd_trigger vboxservice.service

%pre -n lightdm-greeter-vbox
%addusertogroup xdm vbox

%post -n dkms-vboxguest
set -x
dkms add -m vboxguest -v %{version}-%{rel} --rpm_safe_upgrade && \
dkms build -m vboxguest -v %{version}-%{rel} --rpm_safe_upgrade && \
dkms install -m vboxguest -v %{version}-%{rel} --rpm_safe_upgrade || :

%preun -n dkms-vboxguest
set -x
dkms remove -m vboxguest -v %{version}-%{rel} --rpm_safe_upgrade --all || :

%post -n dkms-vboxhost
set -x
dkms add -m vboxhost -v %{version}-%{rel} --rpm_safe_upgrade && \
dkms build -m vboxhost -v %{version}-%{rel} --rpm_safe_upgrade && \
dkms install -m vboxhost -v %{version}-%{rel} --rpm_safe_upgrade || :

%preun -n dkms-vboxhost
set -x
dkms remove -m vboxhost -v %{version}-%{rel} --rpm_safe_upgrade --all || :

%if %{with userspace}
%files
%defattr(644,root,root,755)
%dir %{_libdir}/%{pname}
%dir %{_libdir}/%{pname}/ExtensionPacks
%dir %{_libdir}/%{pname}/ExtensionPacks/VNC
%dir %{_libdir}/%{pname}/ExtensionPacks/VNC/linux*
%dir %{_libdir}/%{pname}/additions
%dir %{_libdir}/%{pname}/components
%attr(755,root,root) %{_bindir}/VBoxBFE
%attr(755,root,root) %{_bindir}/VBoxHeadless
%attr(755,root,root) %{_bindir}/VBoxManage
%attr(755,root,root) %{_bindir}/VBoxSDL
%attr(755,root,root) %{_bindir}/VBoxSVC
%attr(755,root,root) %{_bindir}/VBoxTunctl
%attr(755,root,root) %{_bindir}/VBoxXPCOMIPCD
%attr(755,root,root) /sbin/mount.vdi
%attr(755,root,root) %{_libdir}/%{pname}/DBGCPlugInDiggers.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxAuth.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxAuthSimple.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxAutostart
%attr(755,root,root) %{_libdir}/%{pname}/VBoxBalloonCtrl
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
%attr(755,root,root) %{_libdir}/%{pname}/VBoxNetNAT
%attr(755,root,root) %{_libdir}/%{pname}/VBoxVolInfo
%attr(755,root,root) %{_libdir}/%{pname}/iPxeBaseBin
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
%attr(755,root,root) %{_libdir}/%{pname}/VBoxTunctl
%attr(755,root,root) %{_libdir}/%{pname}/VBoxVMM.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxVMMPreload
%attr(755,root,root) %{_libdir}/%{pname}/VBoxXPCOMC.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxXPCOMIPCD
%attr(755,root,root) %{_libdir}/%{pname}/VBoxXPCOM.so
%attr(755,root,root) %{_libdir}/%{pname}/VirtualBox-wrapper.sh
%attr(755,root,root) %{_libdir}/%{pname}/ExtensionPacks/VNC/linux*/VBoxVNC*.so
%{_libdir}/%{pname}/VBoxDD2GC.debug
%{_libdir}/%{pname}/VBoxDD2GC.gc
%{_libdir}/%{pname}/VBoxDD2R0.debug
%{_libdir}/%{pname}/VBoxDD2R0.r0
%{_libdir}/%{pname}/VBoxDDGC.debug
%{_libdir}/%{pname}/VBoxDDGC.gc
%{_libdir}/%{pname}/VBoxDDR0.debug
%{_libdir}/%{pname}/VBoxDDR0.r0
%{_libdir}/%{pname}/VBoxEFI32.fd
%{_libdir}/%{pname}/VBoxEFI64.fd
%{_libdir}/%{pname}/VMMGC.debug
%{_libdir}/%{pname}/VMMGC.gc
%{_libdir}/%{pname}/VMMR0.debug
%{_libdir}/%{pname}/VMMR0.r0
%{_libdir}/%{pname}/ExtensionPacks/VNC/ExtPack.xml
%{_libdir}/%{pname}/components/VBoxXPCOMBase.xpt
%{_libdir}/%{pname}/components/VirtualBox_XPCOM.xpt
%attr(755,root,root) %{_libdir}/%{pname}/components/VBoxC.so
%attr(755,root,root) %{_libdir}/%{pname}/components/VBoxSVCM.so
%attr(755,root,root) %{_libdir}/%{pname}/components/VBoxXPCOMIPCC.so

%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/virtualbox.rules
%attr(755,root,root) /lib/udev/VBoxCreateUSBNode.sh

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/VirtualBox
%attr(755,root,root) %{_libdir}/%{pname}/VirtualBox
%attr(755,root,root) %{_libdir}/%{pname}/VBoxDbg.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxTestOGL
%{_libdir}/%{pname}/icons
%dir %{_libdir}/%{pname}/nls
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
%{_desktopdir}/virtualbox.desktop
%{_datadir}/mime/packages/virtualbox.xml

%files additions
%defattr(644,root,root,755)
%{_libdir}/%{pname}/additions/VBoxGuestAdditions.iso

%files guest
%defattr(644,root,root,755)
%attr(755,root,root) /sbin/mount.vboxsf
%attr(754,root,root) /etc/rc.d/init.d/vboxservice
%{systemdunitdir}/vboxservice.service
%attr(755,root,root) %{_bindir}/VBoxControl
%attr(755,root,root) %{_bindir}/VBoxService

%files guest-x11
%defattr(644,root,root,755)
# NOTE: unfinished, should contain .desktop files for starting up mouse
# integration and other desktop services
# NOTE: the filelist is incomplete too
%attr(755,root,root) %{_bindir}/VBoxClient
/etc/X11/xinit/xinitrc.d/98vboxadd-xclient.sh
/etc/xdg/autostart/vboxclient.desktop

%attr(755,root,root) %{_libdir}/%{pname}/additions/autorun.sh
%attr(755,root,root) %{_libdir}/%{pname}/additions/vboxadd
%attr(755,root,root) %{_libdir}/%{pname}/additions/vboxadd-service
%attr(755,root,root) %{_libdir}/%{pname}/additions/vboxadd-x11

%if %{with webservice}
%files webservice
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{pname}/vboxwebsrv
%attr(755,root,root) %{_libdir}/%{pname}/webtest
%endif

%if %{with lightdm}
%files -n lightdm-greeter-vbox
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/vbox-greeter
%{_datadir}/xgreeters/vbox-greeter.desktop
%endif

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

%if %{with dkms}
%files -n dkms-vboxguest
%defattr(644,root,root,755)
%{_usrsrc}/vboxguest-%{version}-%{rel}

%files -n dkms-vboxhost
%defattr(644,root,root,755)
%{_usrsrc}/vboxhost-%{version}-%{rel}
%endif
%endif
