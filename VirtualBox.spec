# NOTE
# - https://www.virtualbox.org/wiki/Linux%20build%20instructions
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
%bcond_with	all_langs	# build with all manual translations
%bcond_without	doc		# don't build the documentation
%bcond_without	debuginfo		# disable debuginfo creation (to save space when compiling)
%bcond_without	kernel		# don't build kernel module
%bcond_without	userspace	# don't build userspace package
%bcond_with	webservice	# webservice (SOAP) support
%bcond_without	lightdm		# lightdm greeter
%bcond_without	dkms		# build dkms package
%bcond_without	verbose
%bcond_without	gui			# disable Qt4 GUI frontend build
%bcond_without	host			# build guest packages only

%if 0%{?_pld_builder:1} && %{with kernel} && %{with userspace}
%{error:kernel and userspace cannot be built at the same time on PLD builders}
exit 1
%endif

%if %{with kernel}
%define		_duplicate_files_terminate_build	0
%endif

%if %{without userspace}
# nothing to be placed to debuginfo package
%undefine	with_debuginfo
%endif

%if %{without debuginfo}
%define		_enable_debug_packages	0
%endif

%ifnarch %{x8664} %{?with_kernel:x32}
%undefine	with_host
%endif

%define		qtver	5.6.0

%define		rel		1
%define		pname		VirtualBox
Summary:	VirtualBox - x86 hardware virtualizer
Summary(pl.UTF-8):	VirtualBox - wirtualizator sprzętu x86
Name:		%{pname}%{?_pld_builder:%{?with_kernel:-kernel}}%{_alt_kernel}
Version:	6.1.20
Release:	%{rel}%{?_pld_builder:%{?with_kernel:@%{_kernel_ver_str}}}
License:	GPL v2
Group:		Applications/Emulators
Source0:	https://download.virtualbox.org/virtualbox/%{version}/%{pname}-%{version}.tar.bz2
# Source0-md5:	f2fe05e72c37d40afb36b9fb3aa38b78
Source1:	https://download.virtualbox.org/virtualbox/%{version}/VBoxGuestAdditions_%{version}.iso
# Source1-md5:	59aa6c4a376e0b72a2e97be69169bad0
Source2:	vboxservice.init
Source3:	vboxservice.service
Source4:	vboxservice.sysconfig
Source5:	mount.vdi
Source6:	udev.rules
Source7:	%{pname}-virtualbox-host-modules-load.conf
Source8:	%{pname}-virtualbox-guest-modules-load.conf
Source9:	vboxautostart.init
Source10:	autostart.cfg
Source11:	vboxclient-vmsvga.service
Source12:	udev-guest.rules
Patch0:		%{pname}-version-error.patch
Patch1:		%{pname}-VBoxSysInfo.patch
Patch2:		%{pname}-warning_workaround.patch
Patch4:		wrapper.patch
Patch6:		hardening-shared.patch
Patch7:		lightdm-greeter-makefile.patch
Patch8:		lightdm-greeter-g++-link.patch
Patch9:		pld-guest.patch
Patch10:	16-no-update.patch
Patch11:	%{pname}-all-translations.patch
Patch12:	x32.patch
Patch13:	%{pname}-no-scrextend.patch
Patch14:	%{pname}-multipython.patch
Patch15:	%{pname}-lightdm-1.19.2.patch
Patch16:	%{pname}-no-vboxvideo.patch
Patch17:	qt5-gl.patch
Patch19:	kernel-4.9.256.patch
URL:		http://www.virtualbox.org/
%if %{with userspace}
%ifarch %{x8664}
BuildRequires:	gcc-multilib-32
BuildRequires:	glibc-devel(i686)
BuildRequires:	libstdc++-multilib-32-devel
BuildRequires:	libstdc++-multilib-32-static
%endif
%if "%{pld_release}" == "ac"
BuildRequires:	XFree86-devel
%else
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXcomposite-devel
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-proto-glproto-devel
BuildRequires:	xorg-xserver-server-devel
%endif
BuildRequires:	EGL-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-devel
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5DBus-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Network-devel >= %{qtver}
BuildRequires:	Qt5OpenGL-devel >= %{qtver}
BuildRequires:	Qt5PrintSupport-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	Qt5X11Extras-devel >= %{qtver}
BuildRequires:	Qt5Xml-devel >= %{qtver}
BuildRequires:	SDL-devel >= 1.2.7
BuildRequires:	acpica
BuildRequires:	alsa-lib-devel >= 1.0.6
BuildRequires:	bash
BuildRequires:	bcc
BuildRequires:	bin86
BuildRequires:	curl-devel >= 7.19.1
BuildRequires:	device-mapper-devel >= 1.02
%{?with_doc:BuildRequires:	docbook-dtd44-xml}
BuildRequires:	fakeroot
%{?with_lightdm:BuildRequires:	fltk-devel}
BuildRequires:	gcc >= 5:3.2.3
%{?with_webservice:BuildRequires:	gsoap-devel}
BuildRequires:	issue
BuildRequires:	kBuild >= 0.1.9998.3093
BuildRequires:	libIDL-devel
BuildRequires:	libcap-static
BuildRequires:	libdrm-devel
BuildRequires:	libpng-devel >= 2:1.2.5
BuildRequires:	libstdc++-devel >= 5:3.2.3
BuildRequires:	libstdc++-static >= 5:3.2.3
BuildRequires:	libuuid-devel
BuildRequires:	libvncserver-devel >= 0.9.9
BuildRequires:	libvpx-devel >= 0.9.5
BuildRequires:	libxml2-devel >= 2.6.26
BuildRequires:	libxslt-devel >= 1.1.17
BuildRequires:	libxslt-progs >= 1.1.17
%{?with_lightdm:BuildRequires:	lightdm-libs-qt5-devel}
BuildRequires:	makeself
BuildRequires:	mkisofs
BuildRequires:	openssl-devel >= 1.0.1
BuildRequires:	pam-devel
BuildRequires:	pixman-devel
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel >= 0.9.0
BuildRequires:	python-devel >= 2.3
BuildRequires:	python-modules
BuildRequires:	qt5-build
BuildRequires:	qt5-linguist
BuildRequires:	rpmbuild(macros) >= 1.752
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
BuildRequires:	yasm >= 0.5.1
BuildRequires:	zlib-devel >= 1.2.1
%endif
%{?with_kernel:%{expand:%buildrequires_kernel kernel%%{_alt_kernel}-module-build >= 3:2.6.20.2}}
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires:	libvncserver >= 0.9.9
Requires:	udev-core
Provides:	group(vbox)
Obsoletes:	VirtualBox-udev < 4.2.10-5
ExclusiveArch:	%{ix86} %{x8664} %{?with_kernel:x32}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{x8664}
%define		vbox_arch	amd64
%else
%define		vbox_arch	x86
%endif
%define		vbox_platform	linux.%{vbox_arch}
%define		outdir		out/%{vbox_platform}/release/bin
%define		objdir		out/%{vbox_platform}/release/obj

%define		filterout		-Werror=format-security

%define		_noautochrpath	.*\\.debug$

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
Requires:	Qt5Core >= %{qtver}
Requires:	Qt5Gui-platform-xcb >= %{qtver}
Requires:	desktop-file-utils
Requires:	desktop-file-utils
Requires:	fontconfig
Requires:	fonts-Type1-urw
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	shared-mime-info
Suggests:	Qt5Gui-platform-xcb-glx >= %{qtver}
Suggests:	Qt5Gui-platform-xcb-egl >= %{qtver}
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
BuildArch:	noarch

%description additions
VirtualBox Guest Additions.

This package contains ISO9660 image with drivers for Guest OS.

You should install this package in your Host OS.

%package guest
Summary:	VirtualBox Guest tools
Group:		Base
Provides:	group(vboxsf)
Requires(post):	systemd-units >= 38
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
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
Summary:	VirtualBox Guest X11 Additions
Group:		X11/Applications
Requires:	%{name}-guest = %{version}-%{release}
Requires:	xorg-app-xrandr
Requires:	kernel(vboxvideo)
Obsoletes:	xorg-driver-input-vboxmouse < %{version}-%{release}
Obsoletes:	xorg-driver-video-vboxvideo < %{version}-%{release}

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
Requires:	%{name} = %{version}-%{release}
Requires:	kernel(vboxguest)
Requires:	lightdm >= 1.0.1
Requires:	pam-pam_vbox = %{version}-%{release}
Provides:	lightdm-greeter

%description -n lightdm-greeter-vbox
VirtualBox greeter for LightDM.

%package -n pam-pam_vbox
Summary:	PAM module to perform automated guest logons
Group:		Base

%description  -n pam-pam_vbox
PAM module (Pluggable Authentication Module) which can be used to
perform automated guest logons.

%package -n dkms-vboxguest
Summary:	VirtualBox kernel modules source for Linux Guest
Summary(pl.UTF-8):	Moduły VirtualBoksa do jądra Linuksa dla systemu gościa
License:	GPL v2+
Group:		Base/Kernel
Requires:	dkms
BuildArch:	noarch

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
Requires:	dkms
BuildArch:	noarch

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
%requires_releq_kernel\
Requires:	%{releq_kernel -n drm}\
Requires(postun):	%releq_kernel\
Provides:	kernel(vboxguest) = %{version}-%{rel}\
Provides:	kernel(vboxsf) = %{version}-%{rel}\
%if %{_kernel_version_code} < %{_kernel_version_magic 4 13 0}\
Provides:	kernel(vboxvideo) = %{version}-%{rel}\
%endif\
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
%requires_releq_kernel\
Requires(postun):	%releq_kernel\
Requires:	systemd-units >= 38\
Provides:	kernel(vboxdrv) = %{version}-%{rel}\
Provides:	kernel(vboxnetadp) = %{version}-%{rel}\
Provides:	kernel(vboxnetflt) = %{version}-%{rel}\
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
%if %{_kernel_version_code} >= %{_kernel_version_magic 4 16 0}\
%config(noreplace) %verify(not md5 mtime size) /etc/depmod.d/%{_kernel_ver}/vboxguest.conf\
%endif\
%config(noreplace) %verify(not md5 mtime size) /etc/modules-load.d/virtualbox-guest.conf\
/lib/modules/%{_kernel_ver}/misc/vboxguest.ko*\
/lib/modules/%{_kernel_ver}/misc/vboxsf.ko*\
%if %{_kernel_version_code} < %{_kernel_version_magic 4 13 0}\
/lib/modules/%{_kernel_ver}/misc/vboxvideo.ko*\
%endif\
\
%if %{with host}\
%files -n kernel%{_alt_kernel}-virtualbox-host\
%config(noreplace) %verify(not md5 mtime size) /etc/modules-load.d/virtualbox-host.conf\
/lib/modules/%{_kernel_ver}/misc/vboxdrv.ko*\
/lib/modules/%{_kernel_ver}/misc/vboxnetadp.ko*\
/lib/modules/%{_kernel_ver}/misc/vboxnetflt.ko*\
%endif\
%endif\
\
%post -n kernel%{_alt_kernel}-virtualbox-guest\
%depmod %{_kernel_ver}\
\
%postun	-n kernel%{_alt_kernel}-virtualbox-guest\
%depmod %{_kernel_ver}\
\
%if %{with host}\
%post	-n kernel%{_alt_kernel}-virtualbox-host\
%depmod %{_kernel_ver}\
\
%postun	-n kernel%{_alt_kernel}-virtualbox-host\
%depmod %{_kernel_ver}\
%endif\
%{nil}

%define build_kernel_pkg()\
export KERN_DIR=%{_kernelsrcdir}\
%if %{with host}\
cd kernel/HostDrivers\
%build_kernel_modules -m vboxdrv -C vboxdrv\
%build_kernel_modules -m vboxnetadp -C vboxnetadp KBUILD_EXTRA_SYMBOLS=$PWD/../vboxdrv/Module.symvers\
%build_kernel_modules -m vboxnetflt -C vboxnetflt KBUILD_EXTRA_SYMBOLS=$PWD/../vboxdrv/Module.symvers\
%install_kernel_modules -D ../../kernel/installed -m vboxdrv/vboxdrv,vboxnetadp/vboxnetadp,vboxnetflt/vboxnetflt -d misc\
cd ../..\
%endif\
cd kernel/GuestDrivers\
%build_kernel_modules -m vboxguest -C vboxguest\
%build_kernel_modules -m vboxsf -C vboxsf KBUILD_EXTRA_SYMBOLS=$PWD/../vboxguest/Module.symvers\
%install_kernel_modules -D ../../kernel/installed -m vboxsf/vboxsf,vboxguest/vboxguest -d misc\
%if %{_kernel_version_code} < %{_kernel_version_magic 4 13 0}\
%build_kernel_modules -m vboxvideo -C vboxvideo KBUILD_EXTRA_SYMBOLS=$PWD/../vboxguest/Module.symvers\
%install_kernel_modules -D ../../kernel/installed -m vboxvideo/vboxvideo -d misc\
%endif\
cd ../..\
%{nil}

%define install_kernel_pkg()\
%if %{_kernel_version_code} >= %{_kernel_version_magic 4 16 0}\
install -d kernel/installed/etc/depmod.d/%{_kernel_ver}\
echo override vboxguest %{_kernel_ver} misc > kernel/installed/etc/depmod.d/%{_kernel_ver}/vboxguest.conf\
%if %{_kernel_version_code} >= %{_kernel_version_magic 5 6 0}\
echo override vboxsf %{_kernel_ver} misc >> kernel/installed/etc/depmod.d/%{_kernel_ver}/vboxguest.conf\
%endif\
%endif\
%{nil}

%{?with_kernel:%{expand:%create_kernel_packages}}

%prep
%setup -q -n %{pname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch4 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%if %{with all_langs}
%patch11 -p0
%endif
%patch12 -p1
%patch13 -p1
%patch14 -p0
%patch15 -p0
%patch16 -p0
%patch17 -p1

%{__sed} -i -e 's,@VBOX_DOC_PATH@,%{_docdir}/%{name}-%{version},' \
	-e 's/Categories=.*/Categories=Utility;Emulator;/' src/VBox/Installer/common/virtualbox.desktop.in

# Respect LDFLAGS
%{__sed} -i -e "s@_LDFLAGS\.%{vbox_arch}*.*=@& %{rpmldflags}@g" \
	-i Config.kmk src/libs/xpcom18a4/Config.kmk

%{__sed} -i -e 's#@INSTALL_DIR@#%{_libdir}/%{pname}#' src/VBox/Installer/linux/VBox.sh

%if %{with kernel}
install -d kernel/{GuestDrivers,HostDrivers}
cd kernel
../src/VBox/Additions/linux/export_modules.sh guest-modules.tar.gz
tar -zxf guest-modules.tar.gz -C GuestDrivers

../src/VBox/HostDrivers/linux/export_modules.sh --file host-modules.tar.gz --without-hardening
tar -zxf host-modules.tar.gz -C HostDrivers
cd -
%patch19 -p1
%endif

# using system kBuild package
%{__rm} -r kBuild

# use linux icon for now
cp -p src/VBox/Frontends/VirtualBox/images/os_{linux26,pld}.png
cp -p src/VBox/Frontends/VirtualBox/images/os_{linux26,pld}_64.png

# don't force whole userspace to be built with -fPIC
# see https://www.virtualbox.org/pipermail/vbox-dev/2015-February/012863.html
%define		filterout_c		-fPIC
%define		filterout_cxx		-fPIC

cat <<'EOF'>> LocalConfig.kmk
%{?with_verbose:KBUILD_VERBOSE=3}
USERNAME=%(id -un)
VBOX_BUILD_PUBLISHER=_PLD
VBOX_VERSION_STRING=$(VBOX_VERSION_MAJOR).$(VBOX_VERSION_MINOR).$(VBOX_VERSION_BUILD)_PLD
XSERVER_VERSION=%(rpm -q --queryformat '%{V}\n' xorg-xserver-server-devel | awk -F. '{ print $1 $2 }' 2>/dev/null || echo ERROR)
VBOX_USE_SYSTEM_XORG_HEADERS=1
VBOX_USE_SYSTEM_GL_HEADERS=1
%if %{with lightdm}
VBOX_WITH_LIGHTDM_GREETER=1
VBOX_WITH_LIGHTDM_GREETER_PACKING=1
%endif
TOOL_GCC3_CFLAGS=%{rpmcflags}
TOOL_GCC3_CXXFLAGS=%{rpmcxxflags}
VBOX_GCC_OPT=%{rpmcxxflags}

VBOX_PATH_APP_PRIVATE_ARCH := %{_libdir}/%{pname}
VBOX_PATH_APP_PRIVATE := %{_datadir}/%{pname}
VBOX_PATH_SHARED_LIBS := $(VBOX_PATH_APP_PRIVATE_ARCH)
VBOX_WITH_ORIGIN :=
VBOX_WITH_RUNPATH := $(VBOX_PATH_APP_PRIVATE_ARCH)
#VBOX_PATH_APP_DOCS := %{_docdir}/%{pname}-doc-%{version}
VBOX_PATH_DOCBOOK_DTD := %{_datadir}/sgml/docbook/xml-dtd-4.4

# don't build testcases to save time, they are not needed for the package
VBOX_WITH_TESTCASES :=
VBOX_WITH_TESTSUITE :=

VBOX_WITH_VRDP_RDESKTOP=
VBOX_WITH_MULTIVERSION_PYTHON=0
%{!?with_host:VBOX_ONLY_ADDITIONS_WITHOUT_RTISOMAKER=1}
EOF

%undefine	filterout_c
%undefine	filterout_cxx

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
	%{!?with_gui:--disable-qt} \
	%{__enable webservice} \
	%{!?with_host:--only-additions} \
	%{nil}

. "$PWD/env.sh"
kmk %{?_smp_mflags}
%endif

%{?with_kernel:%{expand:%build_kernel_packages}}
%{?with_kernel:%{expand:%install_kernel_packages}}

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d $RPM_BUILD_ROOT{%{_bindir},/sbin,%{_sbindir},%{_libdir}/%{pname}/ExtensionPacks} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir},%{_datadir}/mime/packages} \
	$RPM_BUILD_ROOT/etc/sysconfig \
	$RPM_BUILD_ROOT%{_sysconfdir}/vbox/autostart \
	$RPM_BUILD_ROOT%{_libdir}/xorg/modules/{drivers,dri,input} \
	$RPM_BUILD_ROOT{/lib/udev,/etc/udev/rules.d} \
	$RPM_BUILD_ROOT{/etc/rc.d/init.d,%{systemdunitdir},%{_usrsrc}}

# test if we can hardlink -- %{_builddir} and $RPM_BUILD_ROOT on same partition
if cp -al COPYING $RPM_BUILD_ROOT/COPYING; then
	l=l
	%{__rm} $RPM_BUILD_ROOT/COPYING
fi

install -d $RPM_BUILD_ROOT%{_datadir}/%{pname}

cp -a$l %{outdir}/* $RPM_BUILD_ROOT%{_libdir}/%{pname}

%if %{without gui}
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{pname}/icons
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/virtualbox.xml
%endif

# Guest Only Tools
%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_bindir}}/VBoxClient
%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_bindir}}/VBoxControl
%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_bindir}}/VBoxDRMClient
%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_bindir}}/VBoxService
install -d $RPM_BUILD_ROOT/etc/xdg/autostart
cp -p src/VBox/Additions/x11/Installer/vboxclient.desktop \
	$RPM_BUILD_ROOT/etc/xdg/autostart/vboxclient.desktop
install -p src/VBox/Additions/x11/Installer/98vboxadd-xclient $RPM_BUILD_ROOT%{_bindir}/VBoxClient-all
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/vboxservice
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{systemdunitdir}/vboxservice.service
cp -p %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/vboxservice

cp -p %{SOURCE11} $RPM_BUILD_ROOT%{systemdunitdir}/vboxclient-vmsvga.service

install -p %{SOURCE9} $RPM_BUILD_ROOT/etc/rc.d/init.d/vboxautostart
%{__sed} -i -e 's#@INSTALL_DIR@#%{_libdir}/%{pname}#' $RPM_BUILD_ROOT/etc/rc.d/init.d/vboxautostart
cp -p %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/vbox

%if %{with lightdm}
install -d $RPM_BUILD_ROOT%{_datadir}/xgreeters
%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,%{_sbindir}}/vbox-greeter
cp -p %{objdir}/Additions/Installer/linux/other/vbox-greeter.desktop $RPM_BUILD_ROOT%{_datadir}/xgreeters
%endif

%if %{with dkms}
mv $RPM_BUILD_ROOT%{_libdir}/%{pname}/additions/src $RPM_BUILD_ROOT%{_usrsrc}/vboxguest-%{version}-%{rel}
%endif

# pam
install -d $RPM_BUILD_ROOT/%{_lib}/security
%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname}/additions,/%{_lib}/security}/pam_vbox.so

# mount.vboxsf
%{__mv} $RPM_BUILD_ROOT%{_libdir}/%{pname}/additions/mount.vboxsf $RPM_BUILD_ROOT/sbin/mount.vboxsf

# mount.vdi
install -p %{SOURCE5} $RPM_BUILD_ROOT/sbin/mount.vdi

# these belong to .iso
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/additions/autorun.sh
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/additions/runasroot.sh

cp -p %{SOURCE12} $RPM_BUILD_ROOT/etc/udev/rules.d/60-vboxguest.rules

%if %{with host}
# unknown - checkme
%if 1
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/SUPInstall
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/SUPLoggerCtl
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/SUPUninstall
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/load.sh
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/loadall.sh
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/vboxshell.py
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/xpidl
%endif

cp -p$l %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/%{pname}/VBoxGuestAdditions.iso ||
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/%{pname}/VBoxGuestAdditions.iso

# manual installation steps based on src/VBox/Installer/linux/install.sh
ln -sf %{_libdir}/%{pname}/VBox.sh $RPM_BUILD_ROOT%{_bindir}/VirtualBox
ln -sf %{_libdir}/%{pname}/VBox.sh $RPM_BUILD_ROOT%{_bindir}/VBoxManage
ln -sf %{_libdir}/%{pname}/VBox.sh $RPM_BUILD_ROOT%{_bindir}/VBoxSDL
ln -sf %{_libdir}/%{pname}/VBox.sh $RPM_BUILD_ROOT%{_bindir}/VBoxVRDP
ln -sf %{_libdir}/%{pname}/VBox.sh $RPM_BUILD_ROOT%{_bindir}/VBoxHeadless
ln -sf %{_libdir}/%{pname}/VBox.sh $RPM_BUILD_ROOT%{_bindir}/VBoxBalloonCtrl
ln -sf %{_libdir}/%{pname}/VBox.sh $RPM_BUILD_ROOT%{_bindir}/VBoxAutostart
ln -sf %{_libdir}/%{pname}/VBox.sh $RPM_BUILD_ROOT%{_bindir}/vboxwebsrv
ln -sf %{_libdir}/%{pname}/vbox-img $RPM_BUILD_ROOT%{_bindir}/vbox-img
ln -sf %{_libdir}/%{pname}/VBox.sh $RPM_BUILD_ROOT%{_bindir}/VBoxDTrace
cp -p $RPM_BUILD_ROOT%{_libdir}/%{pname}/icons/128x128/virtualbox.png $RPM_BUILD_ROOT%{_pixmapsdir}/virtualbox.png
mv $RPM_BUILD_ROOT%{_libdir}/%{pname}/virtualbox.desktop $RPM_BUILD_ROOT%{_desktopdir}/virtualbox.desktop
mv $RPM_BUILD_ROOT%{_libdir}/%{pname}/virtualbox.xml $RPM_BUILD_ROOT%{_datadir}/mime/packages/virtualbox.xml

mv $RPM_BUILD_ROOT%{_libdir}/%{pname}/nls $RPM_BUILD_ROOT%{_datadir}/%{pname}

(
cd $RPM_BUILD_ROOT%{_libdir}/%{pname}/icons
for i in *; do
cd $i
    for j in *; do
	if expr "$j" : "virtualbox\..*" > /dev/null; then
	    dst=apps
	else
	    dst=mimetypes
	fi
        if [ ! -e $RPM_BUILD_ROOT%{_iconsdir}/hicolor/$i/$dst ]; then
		install -d $RPM_BUILD_ROOT%{_iconsdir}/hicolor/$i/$dst
	fi
	mv $RPM_BUILD_ROOT%{_libdir}/%{pname}/icons/$i/$j $RPM_BUILD_ROOT%{_iconsdir}/hicolor/$i/$dst/$j
    done
cd -
done
)

rm -r $RPM_BUILD_ROOT%{_libdir}/%{pname}/icons

%{__mv} $RPM_BUILD_ROOT{%{_libdir}/%{pname},/lib/udev}/VBoxCreateUSBNode.sh
cp -p %{SOURCE6} $RPM_BUILD_ROOT/etc/udev/rules.d/60-vboxdrv.rules

%if %{with dkms}
mv $RPM_BUILD_ROOT%{_libdir}/%{pname}/src $RPM_BUILD_ROOT%{_usrsrc}/vboxhost-%{version}-%{rel}
%endif

# cleanup unpackaged
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{pname}/{sdk,testcase}
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{pname}/dtrace
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/vboxkeyboard.tar.bz2
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/scripts/generated.sh
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pname}/ExtensionPacks/VNC/ExtPack-license.*

%if %{with gui}
# weird icon size
%{__rm} -r $RPM_BUILD_ROOT%{_iconsdir}/hicolor/40x40
%endif

# duplicate, we already have virtualbox.png (128x128), this is 32x32
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{pname}/VBox.png

%if %{with doc}
ln -sf %{_docdir}/%{pname}-doc-%{version}/UserManual.pdf $RPM_BUILD_ROOT%{_libdir}/%{pname}/UserManual.pdf
%if %{with all_langs}
ln -sf %{_docdir}/%{pname}-doc-%{version}/UserManual_fr_FR.pdf $RPM_BUILD_ROOT%{_libdir}/%{pname}/UserManual_fr_FR.pdf
%endif
%endif
%endif
%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT{/etc/modules-load.d,/sbin}

cp -a kernel/installed/* $RPM_BUILD_ROOT

# Tell systemd to load modules
cp -p %{SOURCE7} $RPM_BUILD_ROOT/etc/modules-load.d/virtualbox-host.conf
cp -p %{SOURCE8} $RPM_BUILD_ROOT/etc/modules-load.d/virtualbox-guest.conf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 221 -r -f vbox

%post
/sbin/chkconfig --add vboxautostart
%service -n vboxautostart restart

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

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del vboxautostart
	%service vboxautostart -q stop
fi


%postun
if [ "$1" = "0" ]; then
	%groupremove vbox
fi

%post gui
%update_desktop_database
%update_icon_cache hicolor
%update_mime_database

%postun gui
%update_desktop_database
%update_icon_cache hicolor
%update_mime_database

%pre guest
%useradd -u 336 -d /usr/share/empty -s /bin/false -c "VirtualBox guest additions" -g nobody vboxadd
# Add a group "vboxsf" for Shared Folders access
# All users which want to access the auto-mounted Shared Folders have to be added to this group.
%groupadd -g 266 -r -f vboxsf

%post guest
/sbin/chkconfig --add vboxservice
%service vboxservice restart
%systemd_post vboxservice.service vboxclient-vmsvga.service

%preun guest
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del vboxservice
	%service vboxservice -q stop
fi
%systemd_preun vboxservice.service vboxclient-vmsvga.service

%postun guest
if [ "$1" = "0" ]; then
	%userremove vboxadd
	%groupremove vboxsf
fi
%systemd_reload

%triggerpostun guest -- VirtualBox-guest < 4.3.0-1
%systemd_trigger vboxservice.service

%pre -n lightdm-greeter-vbox
%addusertogroup xdm vbox

%post -n dkms-vboxguest
dkms add -m vboxguest -v %{version}-%{rel} --rpm_safe_upgrade && \
dkms build -m vboxguest -v %{version}-%{rel} --rpm_safe_upgrade && \
dkms install -m vboxguest -v %{version}-%{rel} --rpm_safe_upgrade || :

%preun -n dkms-vboxguest
dkms remove -m vboxguest -v %{version}-%{rel} --rpm_safe_upgrade --all || :

%post -n dkms-vboxhost
dkms add -m vboxhost -v %{version}-%{rel} --rpm_safe_upgrade && \
dkms build -m vboxhost -v %{version}-%{rel} --rpm_safe_upgrade && \
dkms install -m vboxhost -v %{version}-%{rel} --rpm_safe_upgrade || :

%preun -n dkms-vboxhost
dkms remove -m vboxhost -v %{version}-%{rel} --rpm_safe_upgrade --all || :

%if %{with userspace}
%if %{with host}
%files
%defattr(644,root,root,755)
%dir %attr(751,root,root) %{_sysconfdir}/vbox
%dir %attr(770,root,vbox) %{_sysconfdir}/vbox/autostart
%attr(640,root,vbox) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vbox/autostart.cfg
%attr(754,root,root) /etc/rc.d/init.d/vboxautostart
%attr(755,root,root) /sbin/mount.vdi
%attr(755,root,root) %{_bindir}/VBoxAutostart
%attr(755,root,root) %{_bindir}/VBoxBalloonCtrl
%attr(755,root,root) %{_bindir}/VBoxDTrace
%attr(755,root,root) %{_bindir}/VBoxHeadless
%attr(755,root,root) %{_bindir}/VBoxManage
%attr(755,root,root) %{_bindir}/VBoxSDL
%attr(755,root,root) %{_bindir}/VBoxVRDP
%attr(755,root,root) %{_bindir}/vbox-img
%dir %{_libdir}/%{pname}
# libraries
%attr(755,root,root) %{_libdir}/%{pname}/DbgPlugInDiggers.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxAuth.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxAuthSimple.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxDD.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxDD2.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxDDU.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxDragAndDropSvc.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxGuestControlSvc.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxGuestPropSvc.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxHostChannel.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxKeyboard.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxPython*.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxRT.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxSVGA3D.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxSharedClipboard.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxSharedFolders.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxVMM.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxXPCOM.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxXPCOMC.so
%ifarch %{ix86}
%attr(755,root,root) %{_libdir}/%{pname}/VBoxREM32.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxREM64.so
%endif

# binaries
%attr(755,root,root) %{_libdir}/%{pname}/VBox.sh
%attr(755,root,root) %{_libdir}/%{pname}/VBoxAutostart
%attr(755,root,root) %{_libdir}/%{pname}/VBoxBalloonCtrl
%attr(755,root,root) %{_libdir}/%{pname}/VBoxDTrace
%attr(755,root,root) %{_libdir}/%{pname}/VBoxExtPackHelperApp
%attr(755,root,root) %{_libdir}/%{pname}/VBoxHeadless
%attr(755,root,root) %{_libdir}/%{pname}/VBoxManage
%attr(755,root,root) %{_libdir}/%{pname}/VBoxNetAdpCtl
%attr(755,root,root) %{_libdir}/%{pname}/VBoxNetDHCP
%attr(755,root,root) %{_libdir}/%{pname}/VBoxNetNAT
%attr(755,root,root) %{_libdir}/%{pname}/VBoxSDL
%attr(755,root,root) %{_libdir}/%{pname}/VBoxSVC
%attr(755,root,root) %{_libdir}/%{pname}/VBoxTunctl
%attr(755,root,root) %{_libdir}/%{pname}/VBoxVMMPreload
%attr(755,root,root) %{_libdir}/%{pname}/VBoxVolInfo
%attr(755,root,root) %{_libdir}/%{pname}/VBoxXPCOMIPCD
%attr(755,root,root) %{_libdir}/%{pname}/VirtualBoxVM
%attr(755,root,root) %{_libdir}/%{pname}/bldRTLdrCheckImports
%attr(755,root,root) %{_libdir}/%{pname}/iPxeBaseBin
%attr(755,root,root) %{_libdir}/%{pname}/vboximg-mount
%if %{with doc}
%attr(755,root,root) %{_libdir}/%{pname}/VBoxManageHelp
%endif
%dir %{_libdir}/%{pname}/tools
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTCat
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTChMod
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTCp
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTDbgSymCache
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTEfiFatExtract
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTFTPServer
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTFuzzClient
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTFuzzMaster
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTGzip
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTHttp
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTIsoMaker
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTKrnlModInfo
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTLdrCheckImports
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTLdrFlt
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTLs
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTManifest
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTMkDir
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTRm
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTRmDir
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTShutdown
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTSignTool
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTTar
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTTraceLogTool
%attr(755,root,root) %{_libdir}/%{pname}/tools/RTUnzip
%attr(755,root,root) %{_libdir}/%{pname}/tools/scm

%dir %{_libdir}/%{pname}/ExtensionPacks
%{_libdir}/%{pname}/ExtensionPacks/VNC/ExtPack.xml
%dir %{_libdir}/%{pname}/ExtensionPacks/VNC
%dir %{_libdir}/%{pname}/ExtensionPacks/VNC/linux*
%attr(755,root,root) %{_libdir}/%{pname}/ExtensionPacks/VNC/linux*/VBoxVNC*.so
%dir %{_libdir}/%{pname}/ExtensionPacks/Oracle_VBoxDTrace_Extension_Pack
%{_libdir}/%{pname}/ExtensionPacks/Oracle_VBoxDTrace_Extension_Pack/ExtPack.xml
%dir %{_libdir}/%{pname}/ExtensionPacks/Oracle_VBoxDTrace_Extension_Pack/linux*
%attr(755,root,root) %{_libdir}/%{pname}/ExtensionPacks/Oracle_VBoxDTrace_Extension_Pack/linux*/VBoxDTrace*.so
%{_libdir}/%{pname}/ExtensionPacks/Oracle_VBoxDTrace_Extension_Pack/linux*/VBoxDTraceR0.debug
%{_libdir}/%{pname}/ExtensionPacks/Oracle_VBoxDTrace_Extension_Pack/linux*/VBoxDTraceR0.r0

%{_libdir}/%{pname}/VBoxBugReport
%{_libdir}/%{pname}/VBoxCpuReport
%{_libdir}/%{pname}/VBoxDDR0.debug
%{_libdir}/%{pname}/VBoxDDR0.r0
%{_libdir}/%{pname}/VBoxEFI32.fd
%{_libdir}/%{pname}/VBoxEFI64.fd
%{_libdir}/%{pname}/VMMR0.debug
%{_libdir}/%{pname}/VMMR0.r0

%dir %{_libdir}/%{pname}/components
%{_libdir}/%{pname}/components/VBoxXPCOMBase.xpt
%{_libdir}/%{pname}/components/VirtualBox_XPCOM.xpt
%attr(755,root,root) %{_libdir}/%{pname}/components/VBoxC.so
%attr(755,root,root) %{_libdir}/%{pname}/components/VBoxSVCM.so
%attr(755,root,root) %{_libdir}/%{pname}/components/VBoxXPCOMIPCC.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxSysInfo.sh

%{_libdir}/%{pname}/UnattendedTemplates

%dir %{_datadir}/%{pname}

%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/60-vboxdrv.rules
%attr(755,root,root) /lib/udev/VBoxCreateUSBNode.sh

%if %{with gui}
%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/VirtualBox
%attr(755,root,root) %{_libdir}/%{pname}/UICommon.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxDbg.so
%attr(755,root,root) %{_libdir}/%{pname}/VBoxTestOGL
%attr(755,root,root) %{_libdir}/%{pname}/VirtualBox
%dir %{_datadir}/%{pname}/nls
%lang(bg) %{_datadir}/%{pname}/nls/*_bg.qm
%lang(ca) %{_datadir}/%{pname}/nls/*_ca.qm
%lang(ca_VA) %{_datadir}/%{pname}/nls/*_ca_VA.qm
%lang(cs) %{_datadir}/%{pname}/nls/*_cs.qm
%lang(da) %{_datadir}/%{pname}/nls/*_da.qm
%lang(de) %{_datadir}/%{pname}/nls/*_de.qm
%lang(en) %{_datadir}/%{pname}/nls/*_el.qm
%lang(en) %{_datadir}/%{pname}/nls/*_en.qm
%lang(es) %{_datadir}/%{pname}/nls/*_es.qm
%lang(eu) %{_datadir}/%{pname}/nls/*_eu.qm
%lang(fa) %{_datadir}/%{pname}/nls/*_fa.qm
%lang(fi) %{_datadir}/%{pname}/nls/*_fi.qm
%lang(fr) %{_datadir}/%{pname}/nls/*_fr.qm
%lang(gl) %{_datadir}/%{pname}/nls/*_gl.qm
%lang(he) %{_datadir}/%{pname}/nls/*_he.qm
%lang(hr) %{_datadir}/%{pname}/nls/*_hr_HR.qm
%lang(hu) %{_datadir}/%{pname}/nls/*_hu.qm
%lang(id) %{_datadir}/%{pname}/nls/*_id.qm
%lang(it) %{_datadir}/%{pname}/nls/*_it.qm
%lang(ja) %{_datadir}/%{pname}/nls/*_ja.qm
%lang(km_KH) %{_datadir}/%{pname}/nls/*_km_KH.qm
%lang(ko) %{_datadir}/%{pname}/nls/*_ko.qm
%lang(lt) %{_datadir}/%{pname}/nls/*_lt.qm
%lang(nl) %{_datadir}/%{pname}/nls/*_nl.qm
%lang(pl) %{_datadir}/%{pname}/nls/*_pl.qm
%lang(pt) %{_datadir}/%{pname}/nls/*_pt.qm
%lang(pt_BR) %{_datadir}/%{pname}/nls/*_pt_BR.qm
%lang(ro) %{_datadir}/%{pname}/nls/*_ro.qm
%lang(ru) %{_datadir}/%{pname}/nls/*_ru.qm
%lang(sk) %{_datadir}/%{pname}/nls/*_sk.qm
%lang(sk) %{_datadir}/%{pname}/nls/*_sl.qm
%lang(sr) %{_datadir}/%{pname}/nls/*_sr.qm
%lang(sv) %{_datadir}/%{pname}/nls/*_sv.qm
%lang(th) %{_datadir}/%{pname}/nls/*_th.qm
%lang(tr) %{_datadir}/%{pname}/nls/*_tr.qm
%lang(uk) %{_datadir}/%{pname}/nls/*_uk.qm
%lang(zh_CN) %{_datadir}/%{pname}/nls/*_zh_CN.qm
%lang(zh_TW) %{_datadir}/%{pname}/nls/*_zh_TW.qm
%{_desktopdir}/virtualbox.desktop
%{_pixmapsdir}/virtualbox.png
%{_iconsdir}/hicolor/*/apps/virtualbox.png
%{_iconsdir}/hicolor/*/apps/virtualbox.svg
%{_iconsdir}/hicolor/*/mimetypes/virtualbox-*.png
%{_datadir}/mime/packages/virtualbox.xml
%endif

%files additions
%defattr(644,root,root,755)
%{_datadir}/%{pname}/VBoxGuestAdditions.iso

%if %{with webservice}
%files webservice
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/vboxwebsrv
%attr(755,root,root) %{_libdir}/%{pname}/vboxwebsrv
%attr(755,root,root) %{_libdir}/%{pname}/webtest
%endif

%if %{with doc}
%files doc
%defattr(644,root,root,755)
# this is a symlink...
%doc %{_libdir}/%{pname}/UserManual.pdf
%if %{with all_langs}
%lang(fr) %doc %{_libdir}/%{pname}/UserManual_fr_FR.pdf
%endif
# ..to this file
%doc %{outdir}/UserManual.pdf
%if %{with all_langs}
%lang(fr) %doc %{outdir}/UserManual_fr_FR.pdf
%endif
%endif
%endif

%files guest
%defattr(644,root,root,755)
%attr(755,root,root) /sbin/mount.vboxsf
%attr(754,root,root) /etc/rc.d/init.d/vboxservice
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/vboxservice
%{systemdunitdir}/vboxservice.service
%{systemdunitdir}/vboxclient-vmsvga.service
%attr(755,root,root) %{_bindir}/VBoxControl
%attr(755,root,root) %{_bindir}/VBoxService
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/60-vboxguest.rules

%files guest-x11
%defattr(644,root,root,755)
/etc/xdg/autostart/vboxclient.desktop
%attr(755,root,root) %{_bindir}/VBoxClient
%attr(755,root,root) %{_bindir}/VBoxClient-all
%attr(755,root,root) %{_bindir}/VBoxDRMClient

%if %{with lightdm}
%files -n lightdm-greeter-vbox
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/vbox-greeter
%{_datadir}/xgreeters/vbox-greeter.desktop
%endif

%files -n pam-pam_vbox
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/security/pam_vbox.so

%if %{with dkms}
%files -n dkms-vboxguest
%defattr(644,root,root,755)
%{_usrsrc}/vboxguest-%{version}-%{rel}

%if %{with host}
%files -n dkms-vboxhost
%defattr(644,root,root,755)
%{_usrsrc}/vboxhost-%{version}-%{rel}
%endif
%endif
%endif
