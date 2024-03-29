%define		dictname mueller7acc
Summary:	English-Russian dictionary with accents for dictd
Summary(pl.UTF-8):	Słownik angielsko-rosyjski z akcentami dla dictd
Name:		dict-%{dictname}
Version:	1.2
Release:	5
License:	GPL
Group:		Applications/Dictionaries
Source0:	http://mueller-dic.chat.ru/Mueller7accentGPL.tgz
# Source0-md5:	b882581e130ffa0ea3baea5eeea484a2
# This one is compressed with bzip2 (do not trust tgz!)
#Source0:	http://www.geocities.com/mueller_dic/Mueller7accentGPL.tgz
Source1:	http://www.math.sunysb.edu/~comech/tools/to-dict
# Source1-md5:	3c1b69c290fb4c06bf3456baf5bf8b97
URL:		http://mueller-dic.chat.ru/
BuildRequires:	dictfmt
BuildRequires:	dictzip
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	%{_sysconfdir}/dictd
Requires:	dictd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Electronic version of 7th edition of English-Russian dictionary with
accents by V. K. Mueller.

%description -l pl.UTF-8
Elektroniczna wersja 7. wydania słownika angielsko rosyjskiego z
akcentami V. K. Muellera.

%prep
%setup -q -c
cp %{SOURCE1} .
chmod +x ./to-dict

%build
./to-dict --no-trans usr/local/share/dict/Mueller7accentGPL.koi mueller7acc.notr
./to-dict --src-data mueller7acc.notr mueller7acc.data && rm -f mueller7acc.notr
./to-dict --data-dict mueller7acc.data mueller7acc && rm -f mueller7acc.data
./to-dict --expand-index mueller7acc.index mueller7acc.index.exp
mv -f mueller7acc.index.exp mueller7acc.index

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/dictd,%{_sysconfdir}/dictd}

dictprefix=%{_datadir}/dictd/%{dictname}
echo "# Mueller English-Russian dictionary, 7-th edition with accents (%{version})
database %{dictname} {
	data  \"$dictprefix.dict\"
	index \"$dictprefix.index\"
}" > $RPM_BUILD_ROOT%{_sysconfdir}/dictd/%{dictname}.dictconf
mv %{dictname}.* $RPM_BUILD_ROOT%{_datadir}/dictd

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q dictd restart

%postun
if [ "$1" = 0 ]; then
	%service -q dictd restart
fi

%files
%defattr(644,root,root,755)
%doc usr/local/share/mova/Mueller7.txt
%lang(ru) %doc usr/local/share/mova/Mueller7_koi.txt
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dictd/%{dictname}.dictconf
%{_datadir}/dictd/%{dictname}.*
