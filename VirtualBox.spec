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

%define		rel		9

%if %{without kernel}
%undefine	with_dist_kernel
%endif

%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif

%define		pname	VirtualBox

Summary:	VirtualBox OSE - x86 hardware virtualizer
Summary(pl.UTF-8):	VirtualBox OSE - wirtualizator sprzętu x86
Name:		%{pname}%{_alt_kernel}
Version:	1.5.6
Release:	%{rel}
License:	GPL v2
Group:		Applications/Emulators
Source0:	http://www.virtualbox.org/download/%{version}/%{pname}-%{version}-1_OSE.tar.bz2
# Source0-md5:	305c65f9e91b6137cb773d578de09922
Source1:	http://www.virtualbox.org/download/%{version}/UserManual.pdf
# Source1-md5:	9ba7f17584fb3e9c98e026a1501cf7c0
Source2:	http://www.virtualbox.org/download/%{version}/VBoxGuestAdditions_%{version}.iso
# Source2-md5:	9d74dea92bd225ad59faee9fd427a55e
Source3:	%{pname}.init
Source4:	%{pname}.desktop
Source5:	%{pname}.sh
Patch0:		%{pname}-configure.patch
Patch1:		%{pname}-qt-paths.patch
Patch2:		%{pname}-shared-libstdc++.patch
Patch3:		%{pname}-disable-xclient-build.patch
Patch4:		%{pname}-configure-spaces.patch
URL:		http://www.virtualbox.org/
%if %{with userspace}
BuildRequires:	SDL-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	bash
BuildRequires:	bcc
BuildRequires:	bin86
BuildRequires:	gcc >= 5:3.2.3
BuildRequires:	iasl
%endif
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20}
%if %{with userspace}
BuildRequires:	libIDL-devel
BuildRequires:	libuuid-devel
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel
BuildRequires:	qt-devel >= 6:3.3.6
BuildRequires:	qt-linguist
%endif
BuildRequires:	rpmbuild(macros) >= 1.379
%if %{with userspace}
BuildRequires:	which
BuildRequires:	xalan-c-devel >= 1.10.0
BuildRequires:	xerces-c-devel >= 2.6.0
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	zlib-devel >= 1.2.1
%ifarch %{x8664}
BuildRequires:	gcc-multilib
BuildRequires:	glibc-devel(i686)
BuildRequires:	libstdc++-multilib-devel
%endif
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
line. VirtualBox OSE also comes with a full Software Development Kit: even
though it is Open Source Software, you don't have to hack the source
to write a new interface for VirtualBox OSE.

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
poleceń. VirtualBox OSE dostarcza również pełny pakiet deweloperski, co
pozwala stworzyć dowolny inny interfejs zarządzania maszyną wirtualną.

Opisy maszyn wirtualnych w XML-u: konfiguracje poszczególnych maszyn
wirtualnych są w całości przechowywane w XML-u i są niezależne od
lokalnej maszyny. Dzięki temu można szybko i łatwo przenieść
konfigurację maszyny wirtualnej na inny komputer.

%package udev
Summary:	udev rules for VirtualBox OSE kernel modules
Summary(pl.UTF-8):	Reguły udev dla modułów jądra Linuksa dla VirtualBoksa
Release:	%{rel}
Group:		Base/Kernel
Requires:	udev

%description udev
udev rules for VirtualBox OSE kernel modules

%description udev -l pl.UTF-8
Reguły udev dla modułów jądra Linuksa dla VirtualBoksa

%package -n kernel%{_alt_kernel}-misc-vboxadd
Summary:	Linux kernel module for VirtualBox OSE
Summary(pl.UTF-8):	Moduł jądra Linuksa dla VirtualBoksa
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
#Requires(postun):	%%releq_kernel
%endif
Provides:	kernel(vboxadd) = %{version}-%{rel}

%description -n kernel%{_alt_kernel}-misc-vboxadd
Linux kernel module vboxadd for VirtualBox OSE.

%description -n kernel%{_alt_kernel}-misc-vboxadd -l pl.UTF-8
Moduł jądra Linuksa vboxadd dla VirtualBoksa.

%package -n kernel%{_alt_kernel}-misc-vboxdrv
Summary:	Linux kernel module for VirtualBox OSE
Summary(pl.UTF-8):	Moduł jądra Linuksa dla VirtualBoksa
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
Linux kernel module vboxdrv for VirtualBox OSE.

%description -n kernel%{_alt_kernel}-misc-vboxdrv -l pl.UTF-8
Moduł jądra Linuksa vboxdrv dla VirtualBoksa.

%package -n kernel%{_alt_kernel}-misc-vboxvfs
Summary:	Linux kernel module for VirtualBox OSE
Summary(pl.UTF-8):	Moduł jądra Linuksa dla VirtualBoksa
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(vboxvfs) = %{version}-%{rel}

%description -n kernel%{_alt_kernel}-misc-vboxvfs
Linux kernel module vboxvfs for VirtualBox OSE.

%description -n kernel%{_alt_kernel}-misc-vboxvfs -l pl.UTF-8
Moduł jądra Linuksa vboxvfs dla VirtualBoksa.

%package -n xorg-driver-input-vboxmouse
Summary:	X.org mouse driver for VirtualBox OSE guest OS
Summary(pl.UTF-8):	Sterownik myszy dla systemu gościa w VirtualBoksie
Release:	%{rel}
Group:		X11/Applications
Requires:	xorg-xserver-server >= 1.0.99.901

%description -n xorg-driver-input-vboxmouse
X.org mouse driver for VirtualBox OSE guest OS.

%description -n xorg-driver-input-vboxmouse  -l pl.UTF-8
Sterownik myszy dla systemu gościa w VirtualBoksie.

%package -n xorg-driver-video-vboxvideo
Summary:	X.org video driver for VirtualBox OSE guest OS
Summary(pl.UTF-8):	Sterownik grafiki dla systemu gościa w VirtualBoksie
Release:	%{rel}
Group:		X11/Applications
Requires:	xorg-xserver-server >= 1.0.99.901

%description -n xorg-driver-video-vboxvideo
X.org video driver for VirtualBox OSE guest OS.

%description -n xorg-driver-video-vboxvideo -l pl.UTF-8
Sterownik grafiki dla systemu gościa w VirtualBoksie.

%prep
%setup -q -n %{pname}-%{version}_OSE
%patch0 -p0
%patch1 -p0
%patch2 -p1

%ifarch %{x8664}
%patch3 -p1
%endif

%patch4 -p1

cat <<'EOF' > udev.conf
KERNEL=="vboxdrv", NAME="%k", GROUP="vbox", MODE="0660"
EOF

install %{SOURCE1} .

rm -rf PLD-MODULE-BUILD && mkdir PLD-MODULE-BUILD && cd PLD-MODULE-BUILD
../src/VBox/Additions/linux/export_modules modules.tar.gz
	tar -zxf modules.tar.gz && rm -f modules.tar.gz
../src/VBox/HostDrivers/Support/linux/export_modules modules.tar.gz && \
	tar -zxf modules.tar.gz && rm -f modules.tar.gz

%ifarch %{x8664}
# HACK, is this really safe on x86_64?
sed -i -e '/#.*define.*RTMEMALLOC_EXEC_HEAP/d' vboxadd/r0drv/linux/alloc-r0drv-linux.c vboxvfs/r0drv/linux/alloc-r0drv-linux.c
%endif

%build
%if %{with userspace}
./configure \
	--with-gcc="%{__cc}" \
	--with-g++="%{__cxx}" \
	--disable-kmods

. ./env.sh && kmk -j1
%endif

%if %{with kernel}
cd PLD-MODULE-BUILD
%build_kernel_modules -m vboxadd -C vboxadd
%build_kernel_modules -m vboxdrv -C vboxdrv
cp -a vboxadd/Module.symvers vboxvfs
%build_kernel_modules -m vboxvfs -C vboxvfs -c
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d \
	$RPM_BUILD_ROOT{%{_bindir},%{_pixmapsdir},%{_desktopdir}} \
	$RPM_BUILD_ROOT%{_libdir}/VirtualBox \
	$RPM_BUILD_ROOT/etc/rc.d/init.d

install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/virtualbox

install %{SOURCE5} $RPM_BUILD_ROOT%{_libdir}/VirtualBox/VirtualBox-wrapper.sh
for f in {VBox{BFE,Manage,SDL,SVC,XPCOMIPCD},VirtualBox,vditool}; do
	install out/linux.%{outdir}/release/bin/$f $RPM_BUILD_ROOT%{_libdir}/VirtualBox/$f
	ln -s %{_libdir}/VirtualBox/VirtualBox-wrapper.sh $RPM_BUILD_ROOT%{_bindir}/$f
done

%ifarch %{x8664}
install out/linux.%{outdir}/release/bin/VBox*.rel \
        $RPM_BUILD_ROOT%{_libdir}/VirtualBox
%endif

install out/linux.%{outdir}/release/bin/VBox*.so \
	$RPM_BUILD_ROOT%{_libdir}/VirtualBox
install out/linux.%{outdir}/release/bin/{VBox{DD,DD2}{GC.gc,R0.r0},VMM{GC.gc,R0.r0},*.xpt} \
	$RPM_BUILD_ROOT%{_libdir}/VirtualBox

install -d $RPM_BUILD_ROOT%{_libdir}/VirtualBox/additions
install -d $RPM_BUILD_ROOT%{_libdir}/VirtualBox/nls

install %{SOURCE2} $RPM_BUILD_ROOT%{_libdir}/VirtualBox/additions/VBoxGuestAdditions.iso
cp -a out/linux.%{outdir}/release/bin/components $RPM_BUILD_ROOT%{_libdir}/VirtualBox
cp -a out/linux.%{outdir}/release/bin/nls/* $RPM_BUILD_ROOT%{_libdir}/VirtualBox/nls

install out/linux.%{outdir}/release/bin/additions/mountvboxsf		\
	$RPM_BUILD_ROOT%{_bindir}

%ifnarch %{x8664}
install -d $RPM_BUILD_ROOT%{_libdir}/xorg/modules/{drivers,input}
install out/linux.%{outdir}/release/bin/additions/vboxmouse_drv_14.so	\
	$RPM_BUILD_ROOT%{_libdir}/xorg/modules/input/vboxmouse_drv.so
install out/linux.%{outdir}/release/bin/additions/vboxvideo_drv_14.so	\
	$RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/vboxvideo_drv.so
%endif

install out/linux.%{outdir}/release/bin/VBox.png $RPM_BUILD_ROOT%{_pixmapsdir}/VBox.png
install %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}/%{pname}.desktop

install -d $RPM_BUILD_ROOT/etc/udev/rules.d
install udev.conf $RPM_BUILD_ROOT/etc/udev/rules.d/virtualbox.rules
%endif

%if %{with kernel}
%install_kernel_modules -m PLD-MODULE-BUILD/vboxadd/vboxadd -d misc
%install_kernel_modules -m PLD-MODULE-BUILD/vboxdrv/vboxdrv -d misc
%install_kernel_modules -m PLD-MODULE-BUILD/vboxvfs/vboxvfs -d misc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 221 -r -f vbox

%post
/sbin/chkconfig --add virtualbox
%service virtualbox restart "VirtualBox"

%preun
if [ "$1" = "0" ]; then
	%service virtualbox stop
	/sbin/chkconfig --del virtualbox
fi

%postun
if [ "$1" = "0" ]; then
	%groupremove vbox
fi

%post	-n kernel%{_alt_kernel}-misc-vboxadd
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-misc-vboxadd
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-misc-vboxdrv
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-misc-vboxdrv
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-misc-vboxvfs
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-misc-vboxvfs
%depmod %{_kernel_ver}

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc UserManual.pdf
%dir %{_libdir}/VirtualBox
%dir %{_libdir}/VirtualBox/additions
%dir %{_libdir}/VirtualBox/components
%dir %{_libdir}/VirtualBox/nls
%attr(754,root,root) /etc/rc.d/init.d/virtualbox
%attr(755,root,root) %{_bindir}/mountvboxsf
%attr(755,root,root) %{_bindir}/vditool
%attr(755,root,root) %{_bindir}/VBox*
%attr(755,root,root) %{_bindir}/VirtualBox
%attr(755,root,root) %{_libdir}/VirtualBox/vditool
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxSVC
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxBFE
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxManage
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxSDL
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxXPCOMIPCD
%attr(755,root,root) %{_libdir}/VirtualBox/VBox*.so
%ifarch %{x8664}
%attr(755,root,root) %{_libdir}/VirtualBox/VBox*.rel
%endif
%attr(755,root,root) %{_libdir}/VirtualBox/VirtualBox
%attr(755,root,root) %{_libdir}/VirtualBox/VirtualBox-wrapper.sh
%{_libdir}/VirtualBox/*.gc
%{_libdir}/VirtualBox/*.r0
%{_libdir}/VirtualBox/*.xpt
%{_libdir}/VirtualBox/additions/*
%{_libdir}/VirtualBox/components/*
%lang(ar) %{_libdir}/VirtualBox/nls/*_ar.qm
%lang(ca) %{_libdir}/VirtualBox/nls/*_ca.qm
%lang(cs) %{_libdir}/VirtualBox/nls/*_cs.qm
%lang(de) %{_libdir}/VirtualBox/nls/*_de.qm
%lang(es) %{_libdir}/VirtualBox/nls/*_es.qm
%lang(eu) %{_libdir}/VirtualBox/nls/*_eu.qm
%lang(fi) %{_libdir}/VirtualBox/nls/*_fi.qm
%lang(fr) %{_libdir}/VirtualBox/nls/*_fr.qm
%lang(hu) %{_libdir}/VirtualBox/nls/*_hu.qm
%lang(id) %{_libdir}/VirtualBox/nls/*_id.qm
%lang(it) %{_libdir}/VirtualBox/nls/*_it.qm
%lang(ja) %{_libdir}/VirtualBox/nls/*_ja.qm
%lang(ko) %{_libdir}/VirtualBox/nls/*_ko.qm
%lang(nl) %{_libdir}/VirtualBox/nls/*_nl.qm
%lang(pl) %{_libdir}/VirtualBox/nls/*_pl.qm
%lang(pt_BR) %{_libdir}/VirtualBox/nls/*_pt_BR.qm
%lang(pt_PT) %{_libdir}/VirtualBox/nls/*_pt_PT.qm
%lang(ro) %{_libdir}/VirtualBox/nls/*_ro.qm
%lang(ru) %{_libdir}/VirtualBox/nls/*_ru.qm
%lang(sk) %{_libdir}/VirtualBox/nls/*_sk.qm
%lang(sr) %{_libdir}/VirtualBox/nls/*_sr.qm
%lang(sv) %{_libdir}/VirtualBox/nls/*_sv.qm
%lang(tr) %{_libdir}/VirtualBox/nls/*_tr.qm
%lang(zh_CN) %{_libdir}/VirtualBox/nls/*_zh_CN.qm
%lang(zh_TW) %{_libdir}/VirtualBox/nls/*_zh_TW.qm
%{_pixmapsdir}/VBox.png
%{_desktopdir}/%{pname}.desktop

%files udev
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/virtualbox.rules

# Drivers are for Guest OS, which is 32-bit.
%ifnarch %{x8664}
%files -n xorg-driver-input-vboxmouse
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/input/vboxmouse_drv.so

%files -n xorg-driver-video-vboxvideo
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/drivers/vboxvideo_drv.so
%endif
%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-misc-vboxadd
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vboxadd.ko*

%files -n kernel%{_alt_kernel}-misc-vboxdrv
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vboxdrv.ko*

%files -n kernel%{_alt_kernel}-misc-vboxvfs
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vboxvfs.ko*
%endif
