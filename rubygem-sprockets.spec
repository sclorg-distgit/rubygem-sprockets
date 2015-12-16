%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from sprockets-2.4.5.gem by gem2rpm -*- rpm-spec -*-
%global gem_name sprockets

Summary: Rack-based asset packaging system
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 2.8.2
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: http://getsprockets.org/
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# to get tests:
# git clone https://github.com/sstephenson/sprockets.git && cd sprockets/
# git checkout v2.8.2 && tar czf sprockets-2.8.2-tests.tgz test/
Source1: sprockets-%{version}-tests.tgz
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(hike) => 1.2
Requires: %{?scl_prefix}rubygem(hike) < 2
Requires: %{?scl_prefix}rubygem(multi_json) => 1.0
Requires: %{?scl_prefix}rubygem(multi_json) < 2
Requires: %{?scl_prefix}rubygem(rack) => 1.0
Requires: %{?scl_prefix}rubygem(rack) < 2
Requires: %{?scl_prefix}rubygem(tilt) => 1.1
Requires: %{?scl_prefix}rubygem(tilt) < 2
Conflicts: %{?scl_prefix}rubygem(tilt) = 1.3.0
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix}rubygem(coffee-script)
# these two gems aren't in Fedora yet and are only soft dependencies
# BuildRequires: %{?scl_prefix}rubygem(eco)
# BuildRequires: %{?scl_prefix}rubygem(ejs)
BuildRequires: %{?scl_prefix}rubygem(execjs)
BuildRequires: %{?scl_prefix}rubygem(hike) => 1.2
BuildRequires: %{?scl_prefix}rubygem(hike) < 2
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildRequires: %{?scl_prefix}rubygem(uglifier)
BuildRequires: %{?scl_prefix}rubygem(multi_json)
BuildRequires: %{?scl_prefix}rubygem(rack) => 1.0
BuildRequires: %{?scl_prefix}rubygem(rack) < 2
BuildRequires: %{?scl_prefix}rubygem(rack-test)
BuildRequires: %{?scl_prefix_ruby}rubygem(rake)
BuildRequires: %{?scl_prefix}rubygem(sass)
BuildRequires: %{?scl_prefix}rubygem(therubyracer)
%{?scl:BuildRequires: scldevel(v8)}
BuildRequires: %{?scl_prefix}rubygem(tilt) => 1.1
BuildRequires: %{?scl_prefix}rubygem(tilt) < 2
BuildConflicts: %{?scl_prefix}rubygem(tilt) = 1.3.0
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Sprockets is a Rack-based asset packaging system that concatenates and serves
JavaScript, CoffeeScript, CSS, LESS, Sass, and SCSS.


%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
%{?scl:scl enable %{scl} - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
tar xzf %{SOURCE1}
# 4 errors due to missing Gems "eco" and "ejs"
# 1 failure in test "read ASCII asset"(EncodingTest).
# https://github.com/sstephenson/sprockets/issues/418
# https://github.com/sstephenson/sprockets/commit/2a0ecc841b6c06f1bf322373a0988d5019bef07b
%{?scl:scl enable %{scl} %{scl_v8} - << \EOF}
testrb -Ilib test | grep '447 tests, 1158 assertions, 1 failures, 4 errors, 0 skips'
%{?scl:EOF}
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE
%{_bindir}/sprockets
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/README.md
%doc %{gem_docdir}

%changelog
* Mon Feb 17 2014 Josef Stribny <jstribny@redhat.com> - 2.8.2-3
- Depend on scldevel(v8) virtual provide

* Tue Nov 26 2013 Josef Stribny <jstribny@redhat.com> - 2.8.2-2
- Use v8 scl macro

* Wed Oct 16 2013 Josef Stribny <jstribny@redhat.com> - 2.8.2-1
- Upgrade to version 2.8.2
- Added rubygem-uglifier build dependency

* Wed Jun 12 2013 Josef Stribny <jstribny@redhat.com> - 2.4.5-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Jul 26 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.4.5-2
- Imported from Fedora again.

* Wed Jul 18 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.4.5-1
- Initial package
