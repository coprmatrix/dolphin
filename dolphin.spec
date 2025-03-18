%global tests 1

Name:           dolphin
Summary:        KDE File Manager
Version:        24.12.2
Release:        2%{?dist}

Patch0:         dolphin-go_up.diff
Patch1:         0001-Revert-Disallow-executing-Dolphin-as-root-on-Linux.patch

License:        BSD-2-Clause AND BSD-3-Clause AND GPL-2.0-only AND GPL-2.0-or-later AND GPL-3.0-only AND LGPL-2.0-only AND LGPL-2.0-or-later AND LGPL-2.1-only AND LGPL-3.0-only AND (GPL-2.0-only OR GPL-3.0-only) AND (LGPL-2.1-only OR LGPL-3.0-only)
URL:            https://invent.kde.org/system/dolphin
Source0:        https://github.com/KDE/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  systemd-rpm-macros

BuildRequires:  extra-cmake-modules
BuildRequires:  kf6-rpm-macros

BuildRequires:  cmake(KF6Baloo)
BuildRequires:  cmake(KF6BalooWidgets)
BuildRequires:  cmake(KF6Bookmarks)
BuildRequires:  cmake(KF6Codecs)
BuildRequires:  cmake(KF6Completion)
BuildRequires:  cmake(KF6Config)
BuildRequires:  cmake(KF6CoreAddons)
BuildRequires:  cmake(KF6Crash)
BuildRequires:  cmake(KF6DBusAddons)
BuildRequires:  cmake(KF6DocTools)
BuildRequires:  cmake(KF6FileMetaData)
BuildRequires:  cmake(KF6I18n)
BuildRequires:  cmake(KF6IconThemes)
BuildRequires:  cmake(KF6KCMUtils)
BuildRequires:  cmake(KF6KIO)
BuildRequires:  cmake(KF6NewStuff)
BuildRequires:  cmake(KF6Notifications)
BuildRequires:  cmake(KF6Parts)
BuildRequires:  cmake(KF6Solid)
BuildRequires:  cmake(KF6TextWidgets)
BuildRequires:  cmake(KF6UserFeedback)
BuildRequires:  cmake(KF6WidgetsAddons)
BuildRequires:  cmake(KF6WindowSystem)
BuildRequires:  cmake(KF6GuiAddons)

BuildRequires:  cmake(PlasmaActivities)

BuildRequires:  cmake(Qt6Concurrent)
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  qt6-qtbase-private-devel

BuildRequires:  cmake(packagekitqt6)
BuildRequires:  cmake(Phonon4Qt6)

%if 0%{?tests}
BuildRequires: xorg-x11-server-Xvfb
BuildRequires: rubygem(test-unit)
%endif

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

Recommends:     konsole-part%{?_isa}
Recommends:     kio-fuse%{?_isa}
Recommends:     kio-extras%{?_isa}
Recommends:     %{name}-plugins
# Image Previews
Recommends:     kf6-kimageformats%{?_isa}
Recommends:     qt6-qtimageformats%{?_isa}
Recommends:     ffmpegthumbs%{?_isa}

%description
%{summary}.

%package        libs
Summary:        Dolphin runtime libraries
%description    libs
%{summary}.

%package        devel
Summary:        Developer files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       qt6-qtbase-devel%{?_isa}
Requires:       kf6-kio-devel%{?_isa}
%description    devel
%{summary}.


%prep
%autosetup -n %{name}-%{version} -p1


%build
%cmake_kf6 \
  %{?flatpak:-DFLATPAK:BOOL=ON} \
  -DKDE_INSTALL_SYSTEMDUSERUNITDIR=%{_userunitdir} \
  -DBUILD_TESTING:BOOL=%{?tests:ON}%{!?tests:OFF}

%cmake_build


%install
%cmake_install

%find_lang dolphin --all-name --with-html


%check
appstream-util validate-relax --nonet %{buildroot}%{_kf6_metainfodir}/org.kde.%{name}.appdata.xml
desktop-file-validate %{buildroot}%{_kf6_datadir}/applications/org.kde.%{name}.desktop
%if 0%{?tests}
xvfb-run -a bash -c "%ctest" || :
%endif


%files -f dolphin.lang
%license LICENSES/*
%doc README*
%{_kf6_datadir}/qlogging-categories6/dolphin.*
%{_kf6_bindir}/dolphin
%{_kf6_bindir}/servicemenuinstaller
%{_kf6_datadir}/config.kcfg/dolphin_*
%{_kf6_datadir}/knsrcfiles/*
%if 0%{?flatpak}
%{_datadir}/dbus-1/services/org.freedesktop.FileManager1.service
%else
%{_datadir}/dbus-1/services/org.kde.dolphin.FileManager1.service
%endif
%{_userunitdir}/plasma-dolphin.service
%{_kf6_metainfodir}/org.kde.%{name}.appdata.xml
%{_kf6_datadir}/applications/org.kde.%{name}.desktop
%dir %{_kf6_datadir}/kglobalaccel/
%{_kf6_datadir}/kglobalaccel/org.kde.dolphin.desktop
%{_kf6_datadir}/kconf_update/*.*
%{_kf6_libdir}/kconf_update_bin/*                            

%dir %{_kf6_datadir}/dolphin
%{_kf6_datadir}/dolphin/dolphinpartactions.desktop
%{_kf6_datadir}/zsh/site-functions/_dolphin
%{_kf6_datadir}/icons/hicolor/scalable/apps/org.kde.dolphin.svg

%files libs
%{_kf6_libdir}/libdolphinprivate.so.*
%{_kf6_libdir}/libdolphinvcs.so.*
%{_kf6_plugindir}/parts/dolphinpart.so
%{_kf6_qtplugindir}/dolphin/
%{_kf6_qtplugindir}/kf6/kfileitemaction/movetonewfolderitemaction.so

%files devel
%{_includedir}/Dolphin/
%{_includedir}/dolphin*_export.h
%{_kf6_libdir}/cmake/DolphinVcs/
%{_kf6_libdir}/libdolphinvcs.so
%{_datadir}/dbus-1/interfaces/org.freedesktop.FileManager1.xml

