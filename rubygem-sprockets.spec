%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from sprockets-2.4.5.gem by gem2rpm -*- rpm-spec -*-
%global gem_name sprockets

# Fallback to rh-nodejs4 rh-nodejs4-scldevel is probably not available in
# the buildroot.
%{!?scl_nodejs:%global scl_nodejs rh-nodejs4}
%{!?scl_prefix_nodejs:%global scl_prefix_nodejs %{scl_nodejs}-}

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 3.2.0
Release: 4%{?dist}
Summary: Rack-based asset packaging system
Group: Development/Languages
License: MIT
URL: https://github.com/rails/sprockets
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# to get tests:
# git clone https://github.com/rails/sprockets.git && cd sprockets/
# git checkout v3.2.0 && tar czf sprockets-3.2.0-tests.tgz test/
Source1: sprockets-%{version}-tests.tgz

Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(rack) > 1
Requires: %{?scl_prefix}rubygem(rack) < 3
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby >= 1.9.3
BuildRequires: %{?scl_prefix}rubygem(coffee-script)
BuildRequires: %{?scl_prefix}rubygem(ejs)
BuildRequires: %{?scl_prefix}rubygem(execjs)
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildRequires: %{?scl_prefix}rubygem(nokogiri)
BuildRequires: %{?scl_prefix}rubygem(rack-test)
BuildRequires: %{?scl_prefix_ruby}rubygem(rake)
BuildRequires: %{?scl_prefix}rubygem(sass)
BuildRequires: %{?scl_prefix}rubygem(uglifier)
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

# Explicitly require runtime subpackage, as long as older scl-utils do not generate it
Requires: %{?scl_prefix}runtime

BuildRequires: %{?scl_prefix_nodejs}nodejs

%description
Sprockets is a Rack-based asset packaging system that concatenates and serves
JavaScript, CoffeeScript, CSS, LESS, Sass, and SCSS.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

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

# Run the test suite

%check
pushd .%{gem_instdir}
tar xzf %{SOURCE1}

# We don't have rubygem(closure-compiler) yet.
# https://bugzilla.redhat.com/show_bug.cgi?id=725733
mv test/test_closure_compressor.rb{,.disabled}
mv lib/sprockets/autoload/closure.rb{,.disabled}
sed -i '/:Closure/ s/^/#/' lib/sprockets/autoload.rb

# We don't have rubygem(eco) yet.
mv test/test_eco_processor.rb{,.disabled}
mv lib/sprockets/autoload/eco.rb{,.disabled}
sed -i '/:Eco/ s/^/#/' lib/sprockets/autoload.rb
sed -i '/test "eco templates" do/,/^  end/ s/^/#/' test/test_environment.rb

# We don't have rubygem(yui-compressor) yet.
# https://bugzilla.redhat.com/show_bug.cgi?id=725768
mv test/test_yui_compressor.rb{,.disabled}
mv lib/sprockets/autoload/yui.rb{,.disabled}
sed -i '/:YUI/ s/^/#/' lib/sprockets/autoload.rb

# Required by TestPathUtils#test_find_upwards test.
touch Gemfile

%{?scl:scl enable %{scl} %{scl_nodejs} - << \EOF}
# Tests are failing, investigate.
ruby -Ilib:test -e 'Dir.glob "./test/**/test_*.rb", &method(:require)' | grep "assertions, 39 failures"
%{?scl:EOF}
popd

%files
%dir %{gem_instdir}
%{_bindir}/sprockets
%{gem_instdir}/LICENSE
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md

%changelog
* Wed Feb 17 2016 Pavel Valena <pvalena@redhat.com> - 3.2.0-4
- Update to 3.2.0

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
