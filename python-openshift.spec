%global with_python3 0

%global library openshift

Name:       python-%{library}
Version:    1.0.0
Release:    0.3%{?dist}
Summary:    Python client for the OpenShift API  
License:    MIT
URL:        https://github.com/openshift/openshift-restclient-python
Source0:    https://github.com/openshift/openshift-restclient-python/%{library}-%{version}.tar.gz
BuildArch:  noarch

%package -n python2-%{library}
Summary:    Python client for the OpenShift API  
%{?python_provide:%python_provide python2-%{library}}

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: git

Requires: python2
Requires: python2-dictdiffer
Requires: python2-kubernetes
Requires: python2-string_utils
Requires: python2-ruamel-yaml
Requires: python-six
Requires: python-jinja2

%description -n python2-%{library}
Python client for the kubernetes API.

%if 0%{?with_python3}
%package -n python3-%{library}
Summary: Python client for the OpenShift API 
%if 0%{?rhel}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{library}}
%else
%{?python_provide:%python_provide python3-%{library}}
%endif

%if 0%{?rhel}
BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: python%{python3_pkgversion}-setuptools
%else
BuildRequires: python3-devel
BuildRequires: python3-setuptools
%endif
BuildRequires: git

%if 0%{?rhel}
Requires: python%{python3_pkgversion}
Requires: python%{python3_pkgversion}-dictdiffer
Requires: python%{python3_pkgversion}-jinja2
Requires: python%{python3_pkgversion}-kubernetes
Requires: python%{python3_pkgversion}-string_utils
Requires: python%{python3_pkgversion}-ruamel-yaml
Requires: python%{python3_pkgversion}-six

%else
Requires: python3
Requires: python3-dictdiffer
Requires: python3-jinja2
Requires: python3-kubernetes
Requires: python3-string_utils
Requires: python3-ruamel-yaml
Requires: python3-six
%endif

%description -n python3-%{library}
Python client for the OpenShift API 
%endif # with_python3

%description
Python client for the OpenShift API 

%prep
%autosetup -n %{library}-%{version} -S git
#there is no include in RHEL7 setuptools find_packages
#the requirements are also done in an non-backwards compatible way
%if 0%{?rhel}
sed -i -e "s/find_packages(include='openshift.*')/['openshift', 'openshift.ansiblegen', 'openshift.client', 'openshift.client.apis', 'openshift.client.models', 'openshift.config', 'openshift.docs', 'openshift.helper', 'openshift.test']/g" setup.py
sed -i -e '30s/^/REQUIRES = [\n    "certifi",\n    "ipaddress",\n    "oauth2client",\n    "setuptools",\n    "six",\n    "urllib3!=1.21",\n    "python-dateutil",\n    "pyyaml",\n    "websocket-client",\n]\n/g' setup.py
sed -i -e "s/extract_requirements('requirements.txt')/REQUIRES/g" setup.py
#sed -i -e '14,21d' setup.py
%endif

%build
%if 0%{?rhel}
%py_build
%else
%py2_build
%endif
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?rhel}
%py_install
%else
%py2_install
%endif
%if 0%{?with_python3}
%py3_install
%endif

%check

%files -n python2-%{library}
%license LICENSE
%{python2_sitelib}/%{library}/*
%{python2_sitelib}/%{library}-*.egg-info
%exclude %{python2_sitelib}/scripts
#TODO: What about for python3?
%if %{with_python3} == 0
%{_bindir}/openshift-ansible-gen
%endif

%if 0%{?with_python3}
%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{library}/*
%{python3_sitelib}/%{library}-*.egg-info
%exclude %{python3_sitelib}/scripts
%{_bindir}/openshift-ansible-gen
%endif # with_python3

%changelog
* Wed May 10 2017 Jason Montleon <jmontleo@redhat.com> 1.0.0-0.3
- Initial Build

