%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from sprockets-2.4.5.gem by gem2rpm -*- rpm-spec -*-
%global gem_name sprockets

Summary: Rack-based asset packaging system
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 2.12.3
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: http://getsprockets.org/
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# to get tests:
# git clone https://github.com/sstephenson/sprockets.git && cd sprockets/
# git checkout v2.12.3 && tar czf sprockets-2.12.3-tests.tgz test/
Source1: sprockets-%{version}-tests.tgz
# Moves test suite to use minitest.
# https://github.com/sstephenson/sprockets/commit/f29903ace62fd43280996b0cb32634f1e5108e52
Patch0: rubygem-sprockets-2.12.1-load-minitest.patch
# https://github.com/sstephenson/sprockets/commit/e840d7fedd180929d089f17d6d6e322e672780f0
Patch1: rubygem-sprockets-2.12.1-Tests-need-to-be-test_.patch
# https://github.com/sstephenson/sprockets/commit/a454ecb17cd1058ad46665824ca4d0f309f0eccf
Patch2: rubygem-sprockets-2.12.1-assert_raise-assert_raises.patch
# https://github.com/sstephenson/sprockets/commit/9be057ce5804492c7c5bd1b20ba7da49c5538740
Patch3: rubygem-sprockets-2.12.1-assert_no_equal-is-gone.patch
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
BuildRequires: v8314-v8
BuildRequires: v8314-scldevel
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
# Patch tests to use Minitest 5
cat %{PATCH0} | patch -p1
cat %{PATCH1} | patch -p1
cat %{PATCH2} | patch -p1
cat %{PATCH3} | patch -p1
# One failure due to changes in ExecJS exceptions
# Fixed in https://github.com/sstephenson/sprockets/commit/47dc70c61b122284299d68c6010dbdb57b6a1211
# And 4 because newer SASS returns #666 for grey instead of #666666
# https://github.com/sstephenson/sprockets/issues/660
%{?scl:scl enable %{scl} %{scl_v8} - << \EOF}
ruby -Ilib:test -e 'Dir.glob "./test/**/test_*.rb", &method(:require)' #| grep '284 runs, 761 assertions, 5 failures, 0 errors, 0 skips'
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
* Tue Jan 27 2015 Josef Stribny <jstribny@redhat.com> - 2.12.3-3
- Revert back to multi_json as it is now part of SCL

* Mon Jan 26 2015 Josef Stribny <jstribny@redhat.com> - 2.12.3-2
- Fix: properly delete any multi_json mention in gemspec

* Mon Jan 26 2015 Josef Stribny <jstribny@redhat.com> - 2.12.3-1
- Update to 2.12.3

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
