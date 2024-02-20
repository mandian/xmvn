#{?_javapackages_macros:%_javapackages_macros}
# XMvn uses OSGi environment provided by Tycho, it shouldn't require
# any additional bundles.
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^osgi\\($

# Bootstrap mode "cheats" by using the prebuilt jar files from upstream.
# There's not much of a way around it, given xmvn requires xmvn to
# build these days.
%bcond_with bootstrap

# Bootstrap2 builds xmvn from source, but uses binary downloads of
# various libraries used by maven that often need to be built with
# xmvn. Refer to the xmvn-package-dependencies script to see where
# the binaries come from.  Also it can use only a very limited set
# of RPM macros from japapackages-tools becaute them requires xmvn
# to work properly.  So at the stage are built only classes needed
# for build japapackages-tools then xmvn canshould be rebuilt.
%bcond_without bootstrap2

# Bootstrap3 builds xmvn from source, but uses binary downloads of
# various libraries used by maven that often need to be built with
# xmvn. Refer to the xmvn-package-dependencies script to see where
# the binaries come from. At this stage all needed RPM macros from
# japapackages-tools can be used.
%bcond_without bootstrap3

# required compnents for bootstrap2:
# xmvn-mojo		(maven-local)
# xmvn-install	(javapackages-local)
# xmvn-subst	(javapackages-local)
# xmvn-resolve	(javapackages-local)
# optional
# xmvn-connector-gradle	(javapackages-gradle-local)
# xmvn-connector-ivy	(javapackages-ivy-local)
%if %{with bootstrap2} ||  %{with bootstrap3}
%bcond_without aether
%bcond_with bisect
%bcond_without gradle
%bcond_without ivy
%bcond_with javadoc
%bcond_with launcher
%bcond_without maven
%bcond_without mojo
%else
%bcond_without aether
%bcond_with bisect
%bcond_without gradle
%bcond_without ivy
%bcond_without javadoc
%bcond_without launcher
%bcond_without maven
%bcond_without mojo
%endif
 
Summary:	Local Extensions for Apache Maven
Name:		xmvn
Version:	4.2.0
Release:	1
Group:		Development/Java
License:	ASL 2.0
URL:		http://mizdebsk.fedorapeople.org/xmvn
BuildArch:	noarch

#Source0:	https://fedorahosted.org/released/%{name}/%{name}-%{version}.tar.xz
Source0:	https://github.com/fedora-java/xmvn/releases/download/%{version}/xmvn-%{version}.tar.xz

%if %{with bootstrap2} || %{with bootstrap3}
# Generated from Source1000
Source3:	xmvn-dependencies-%{version}.tar.zst
Source1000:	xmvn-package-dependencies
%endif
%if %{with bootstrap2} || %{with bootstrap3}
Patch10:	xmvn-package-dependencies.patch
%endif

#Patch0:	0001-Avoid-installing-the-same-attached-artifact-twice.patch
#Patch1:	0002-Fix-installation-of-attached-Eclipse-artifacts.patch
#Patch2:         0003-Fix-conversion-of-Ivy-to-XMvn-artifacts.patch
#Patch3:         0004-Use-topmost-repository-namespace-during-installation.patch
#Patch4:         0005-Ignore-any-system-dependencies-in-Tycho-projects.patch
#Patch5:         0006-Add-fully-qualified-osgi-version-to-install-plan-whe.patch
#Patch6:		xmvn-2.1.0-modular-java.patch

# Import Gradle connector (by upstreamer, adapted)
# https://pagure.io/xmvn/c/64438a57367519c2c1d861f1ce1e01e819e19142?branch=master
#if %{with gradle}
#Patch100:	xmvn-2.1.0-import_gradle_connector.patch
#endif

BuildRequires:	jdk-current
%if ! %{with bootstrap2} &&  ! %{with bootstrap3}
BuildRequires:	maven >= 3.2.1-10
BuildRequires:	maven-local
BuildRequires:	beust-jcommander
BuildRequires:	cglib
BuildRequires:	maven-dependency-plugin
BuildRequires:	maven-plugin-build-helper
BuildRequires:	maven-assembly-plugin
BuildRequires:	maven-invoker-plugin
BuildRequires:	maven-site-plugin
BuildRequires:	xmvn-parent-pom
BuildRequires:	objectweb-asm
BuildRequires:	modello
BuildRequires:	xmlunit
BuildRequires:	apache-ivy
BuildRequires:	sisu-mojos
BuildRequires:	junit
%if %{with gradle}
BuildRequires:	gradle >= 2.2.1
%endif
%endif

Requires:	maven >= 3.2.2
Requires:	xmvn-api = %{version}-%{release}
Requires:	xmvn-connector-aether = %{version}-%{release}
Requires:	xmvn-core = %{version}-%{release}

%description
This package provides extensions for Apache Maven that can be used to
manage system artifact repository and use it to resolve Maven
artifacts in offline mode, as well as Maven plugins to help with
creating RPM packages containing Maven artifacts.

%files
%{_bindir}/%{name}
%{_bindir}/mvn-local
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/bin
%dir %{_datadir}/%{name}/lib
%{_datadir}/%{name}/lib/*.jar
%{_datadir}/%{name}/lib/ext
#{_datadir}/%{name}/lib/jansi-native
%{_datadir}/%{name}/bin/m2.conf
%{_datadir}/%{name}/bin/mvn
%{_datadir}/%{name}/bin/mvnDebug
%{_datadir}/%{name}/bin/mvnyjp
#{_datadir}/%{name}/bin/xmvn
%{_datadir}/%{name}/boot
%{_datadir}/%{name}/conf

#-----------------------------------------------------------------------

%package parent-pom
Summary:        XMvn Parent POM

%description    parent-pom
This package provides XMvn parent POM.

%files parent-pom -f .mfiles-xmvn-parent
%license LICENSE NOTICE

#-----------------------------------------------------------------------

%package        api
Summary:        XMvn API

%description    api
This package provides XMvn API module which contains public interface
for functionality implemented by XMvn Core.

%files api -f .mfiles-xmvn-api
%license LICENSE NOTICE
%doc AUTHORS README.md

#-----------------------------------------------------------------------

%if %{with launcher}
%package        launcher
Summary:        XMvn Launcher

%description    launcher
This package provides XMvn Launcher module, which provides a way of
launching XMvn running in isolated class realm and locating XMVn
services.

%files launcher -f .mfiles-xmvn-launcher
%dir %{_datadir}/%{name}/lib
%{_datadir}/%{name}/lib/core
%endif

#-----------------------------------------------------------------------

%package        core
Summary:        XMvn Core

%description    core
This package provides XMvn Core module, which implements the essential
functionality of XMvn such as resolution of artifacts from system
repository.

%files core -f .mfiles-xmvn-core  -f .mfiles-xmvn
%license LICENSE NOTICE
%doc AUTHORS README.md

#-----------------------------------------------------------------------

%if %{with aether}
%package        connector-aether
Summary:        XMvn Connector for Eclipse Aether

%description    connector-aether
This package provides XMvn Connector for Eclipse Aether, which
provides integration of Eclipse Aether with XMvn.  It provides an
adapter which allows XMvn resolver to be used as Aether workspace
reader.

%files connector-aether -f .mfiles-xmvn-connector-aether
%endif

#-----------------------------------------------------------------------

%if %{with gradle}
%package        connector-gradle
Summary:        XMvn Connector for Gradle

%description    connector-gradle
This package provides XMvn Connector for Gradle, which provides
integration of Gradle with XMvn.  It provides an adapter which allows
XMvn resolver to be used as Gradle resolver.

%files connector-gradle -f .mfiles-xmvn-connector-gradle
%endif

#-----------------------------------------------------------------------

%if %{with ivy}
%package        connector-ivy
Summary:        XMvn Connector for Apache Ivy

%description    connector-ivy
This package provides XMvn Connector for Apache Ivy, which provides
integration of Apache Ivy with XMvn.  It provides an adapter which
allows XMvn resolver to be used as Ivy resolver.

%files connector-ivy -f .mfiles-xmvn-connector-ivy
%dir %{_datadir}/%{name}/lib
%{_datadir}/%{name}/lib/ivy
%endif

#-----------------------------------------------------------------------

%if %{with mojo}
%package        mojo
Summary:        XMvn MOJO

%description    mojo
This package provides XMvn MOJO, which is a Maven plugin that consists
of several MOJOs.  Some goals of these MOJOs are intended to be
attached to default Maven lifecycle when building packages, others can
be called directly from Maven command line.

%files mojo -f .mfiles-xmvn-mojo
%endif

#-----------------------------------------------------------------------

%package        tools-pom
Summary:        XMvn Tools POM

%description    tools-pom
This package provides XMvn Tools parent POM.

%files tools-pom -f .mfiles-xmvn-tools

#-----------------------------------------------------------------------

%package        resolve
Summary:        XMvn Resolver

%description    resolve
This package provides XMvn Resolver, which is a very simple
commald-line tool to resolve Maven artifacts from system repositories.
Basically it's just an interface to artifact resolution mechanism
implemented by XMvn Core.  The primary intended use case of XMvn
Resolver is debugging local artifact repositories.

%files resolve -f .mfiles-xmvn-resolve
%{_bindir}/%{name}-resolve
%dir %{_datadir}/%{name}/bin
%dir %{_datadir}/%{name}/lib
#{_datadir}/%{name}/bin/%{name}-resolve
%{_datadir}/%{name}/lib/resolver

#-----------------------------------------------------------------------

%if %{with bisect}
%package        bisect
Summary:        XMvn Bisect

%description    bisect
This package provides XMvn Bisect, which is a debugging tool that can
diagnose build failures by using bisection method.

%files bisect -f .mfiles-xmvn-bisect
%{_bindir}/%{name}-bisect
%dir %{_datadir}/%{name}/bin
%dir %{_datadir}/%{name}/lib
#{_datadir}/%{name}/bin/%{name}-bisect
%{_datadir}/%{name}/lib/bisect
%endif

#-----------------------------------------------------------------------

%package        subst
Summary:        XMvn Subst

%description    subst
This package provides XMvn Subst, which is a tool that can substitute
Maven artifact files with symbolic links to corresponding files in
artifact repository.

%files subst -f .mfiles-xmvn-subst
%{_bindir}/%{name}-subst
%dir %{_datadir}/%{name}/bin
%dir %{_datadir}/%{name}/lib
#{_datadir}/%{name}/bin/%{name}-subst
%{_datadir}/%{name}/lib/subst

#-----------------------------------------------------------------------

%package        install
Summary:        XMvn Install

%description    install
This package provides XMvn Install, which is a command-line interface
to XMvn installer.  The installer reads reactor metadata and performs
artifact installation according to specified configuration.

%files install -f .mfiles-xmvn-install
%{_bindir}/%{name}-install
%dir %{_datadir}/%{name}/bin
%dir %{_datadir}/%{name}/lib
#{_datadir}/%{name}/bin/%{name}-install
%{_datadir}/%{name}/lib/installer

#-----------------------------------------------------------------------

%if %{with javadoc}
%package        javadoc
Summary:        API documentation for %{name}

%description    javadoc
This package provides %{summary}.

%files javadoc %{?!with_bootstrap2-f .mfiles-javadoc}
%license LICENSE
%doc NOTICE
%endif

#-----------------------------------------------------------------------

%prep
%autosetup -p1
. %{_sysconfdir}/profile.d/90java.sh
%if %{with bootstrap2} || %{with bootstrap3}
cd ..
tar xf %{S:3}
cd -
%endif

#patch0 -p1
#patch1 -p1
#patch2 -p1
#patch3 -p1
#patch4 -p1
#patch5 -p1
#patch6 -p1

#patch100 -p1 -b.orig

%mvn_package :xmvn __noinstall

%if %{without gradle}
#pom_disable_module xmvn-connector-gradle
%endif

# In XMvn 2.x xmvn-connector was renamed to xmvn-connector-aether
%mvn_alias :xmvn-connector-aether :xmvn-connector

# remove dependency plugin maven-binaries execution
# we provide apache-maven by symlink
%pom_xpath_remove "pom:executions/pom:execution[pom:id[text()='maven-binaries']]"

# get mavenVersion that is expected
mver=$(sed -n '/<mavenVersion>/{s/.*>\(.*\)<.*/\1/;p}' \
           xmvn-parent/pom.xml)
mkdir -p target/dependency/
cp -aL %{_datadir}/maven target/dependency/apache-maven-$mver

# skip ITs for now (mix of old & new XMvn config causes issues)
rm -rf src/it

# probably bug in configuration/modello?
sed -i 's|generated-site/resources/xsd/config|generated-site/xsd/config|' xmvn-core/pom.xml

# Workaround easymock incompatibility with Java 17that should be fixed
# in easymock 4.4: https://github.com/easymock/easymock/issues/274
%if ! %{with bootstrap2}
%pom_add_plugin :maven-surefire-plugin xmvn-connector "<configuration>
    <argLine>--add-opens=java.base/java.lang=ALL-UNNAMED</argLine></configuration>"
%pom_add_plugin :maven-surefire-plugin xmvn-tools/xmvn-install "<configuration>
    <argLine>--add-opens=java.base/java.lang=ALL-UNNAMED</argLine></configuration>"
%endif

%build
. %{_sysconfdir}/profile.d/90java.sh
%if %{with bootstrap2} || %{with bootstrap3}
mvn -o -Dmaven.repo.local=$(pwd)/../repository -Dproject.build.sourceEncoding=UTF-8 compile
mvn -o -Dmaven.repo.local=$(pwd)/../repository -Dproject.build.sourceEncoding=UTF-8 verify
mvn -o -Dmaven.repo.local=$(pwd)/../repository -Dproject.build.sourceEncoding=UTF-8 validate
%else
# XXX some tests fail on ARM for unknown reason, see why
%mvn_build -s -f
%endif

tar -xvf target/*tar.gz
chmod -R +rwX %{name}-%{version}*
# These are installed as doc
rm -f %{name}-%{version}/{AUTHORS-XMVN,README-XMVN.md,LICENSE,NOTICE,NOTICE-XMVN}
# Not needed - we use JPackage launcher scripts
%if ! %{with bootstrap2} && ! %{with bootstrap3}
rm -Rf %{name}-%{version}/lib/{installer,resolver,subst}/
%endif
# Irrelevant Maven launcher scripts
rm -f %{name}-%{version}/bin/*

%install
%if ! %{with bootstrap2} && ! %{with bootstrap3}
%mvn_install
%else
mvn -o -Dmaven.repo.local=$(pwd)/../repository -Dproject.build.sourceEncoding=UTF-8 install

# jars
install -dm 0755 %{buildroot}%{_datadir}/java
for j in %{name}-api %{name}-connector %{name}-core %{name}-install %{name}-mojo %{name}-resolve %{name}-subst
do
	install -pm 0644 $(pwd)/../repository/org/fedoraproject/%{name}/${j}/%{version}/${j}-%version.jar \
					%{buildroot}%{_datadir}/java/${j}.jar
	echo "%{_datadir}/java/${j}.jar" >> .mfiles-${j}
done

# poms
install -dm 0755 %{buildroot}%{_datadir}/maven-poms/%{name}/
for j in %{name} %{name}-api %{name}-connector %{name}-core %{name}-install %{name}-mojo %{name}-parent %{name}-resolve %{name}-subst %{name}-tools
do
	install -pm 0644 $(pwd)/../repository/org/fedoraproject/%{name}/${j}/%{version}/${j}-%version.pom \
					%{buildroot}%{_datadir}/maven-poms/%{name}/${j}.pom
	echo "%{_datadir}/maven-poms/%{name}/${j}.pom" >> .mfiles-${j}
done

# metadata
install -dm 0755 %{buildroot}%{_datadir}/maven-metadata/
for j in %{name}-api %{name}-connector %{name}-core %{name}-install %{name}-mojo %{name}-resolve %{name}-subst
do
	python /usr/share/java-utils/maven_depmap.py \
		%{buildroot}%{_datadir}/maven-metadata/${j}.xml \
		%{buildroot}%{_datadir}/maven-poms/%{name}/${j}.pom \
		%{buildroot}%{_javadir}/%{name}/${j}.jar
	echo "%{_datadir}/maven-metadata/${j}.xml" >> .mfiles-${j}
done

# fix .mfiles name
mv .mfiles-%{name}-connector .mfiles-%{name}-connector-aether
%endif

# binaries
install -dm 0755 %{buildroot}%{_datadir}/%{name}
cp -r %{name}-%{version}*/* %{buildroot}%{_datadir}/%{name}/
ln -sf %{_datadir}/maven/bin/mvn %{buildroot}%{_datadir}/%{name}/bin/mvn
ln -sf %{_datadir}/maven/bin/mvnDebug %{buildroot}%{_datadir}/%{name}/bin/mvnDebug
ln -sf %{_datadir}/maven/bin/mvnyjp %{buildroot}%{_datadir}/%{name}/bin/mvnyjp

# helper scripts
install -dm 0755 %{buildroot}%{_bindir}
# bisect
for tool in subst resolve  install;do
    cat <<EOF >%{buildroot}%{_bindir}/%{name}-$tool
#!/bin/sh -e
exec %{_datadir}/%{name}/bin/%{name}-$tool "\${@}"
EOF
    chmod +x %{buildroot}%{_bindir}/%{name}-$tool
done
%jpackage_script org.fedoraproject.xmvn.tools.install.cli.InstallerCli "" "" xmvn/xmvn-install:xmvn/xmvn-api:xmvn/xmvn-core:beust-jcommander:slf4j/api:slf4j/simple:objectweb-asm/asm:commons-compress xmvn-install
%jpackage_script org.fedoraproject.xmvn.tools.resolve.ResolverCli "" "" xmvn/xmvn-resolve:xmvn/xmvn-api:xmvn/xmvn-core:beust-jcommander xmvn-resolve
%jpackage_script org.fedoraproject.xmvn.tools.subst.SubstCli "" "" xmvn/xmvn-subst:xmvn/xmvn-api:xmvn/xmvn-core:beust-jcommander xmvn-subst

# copy over maven lib directory
cp -r %{_datadir}/maven/boot/* %{buildroot}%{_datadir}/%{name}/boot/
cp -r %{_datadir}/maven/lib/* %{buildroot}%{_datadir}/%{name}/lib/

# possibly recreate symlinks that can be automated with xmvn-subst
%if ! %{with bootstrap2}
%{name}-subst %{buildroot}%{_datadir}/%{name}/
#else
#c=`find %{buildroot}%{_datadir}/%{name}/lib/ -name \*jar `
#CLASSPATH=${c//$'\n'/:} %{buildroot}%{_bindir}/%{name}-subst %{buildroot}%{_datadir}/%{name}/
#else
%endif

# /usr/bin/xmvn script
cat <<EOF >%{buildroot}%{_bindir}/%{name}
#!/bin/sh -e
export M2_HOME="\${M2_HOME:-%{_datadir}/%{name}}"
exec mvn "\${@}"
EOF
chmod +x %{buildroot}%{_bindir}/%{name}

# mvn-local script
cat <<EOF >%{buildroot}%{_bindir}/mvn-local
#!/bin/sh -e
export M2_HOME="\${M2_HOME:-%{_datadir}/%{name}}"
exec mvn-local "\${@}"
EOF
chmod +x %{buildroot}%{_bindir}/mvn-local

# make sure our conf is identical to maven so yum won't freak out
install -d -m 755 %{buildroot}%{_datadir}/%{name}/conf/
cp -P %{_datadir}/maven/conf/settings.xml %{buildroot}%{_datadir}/%{name}/conf/
cp -P %{_datadir}/maven/bin/m2.conf %{buildroot}%{_datadir}/%{name}/bin/

# Make sure javapackages config is not bundled
#rm -rf %{buildroot}%{_datadir}/%{name}/{configuration.xml,config.d/,conf/toolchains.xml,maven-metadata/}

