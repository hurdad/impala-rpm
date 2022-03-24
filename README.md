# impala-rpm

Tested on CentOS 7

### Install Dependancies :
```
yum install java-1.8.0-openjdk-devel python-setuptools doxygen redhat-lsb gcc-c++ python-devel cyrus-sasl-devel openssl-devel vim-common wget curl rpm-build maven git make
```

### Set JAVA_HOME :
add /etc/profile.d/java.sh 
```
export JAVA_HOME=/usr/lib/jvm/java
```

### Clone and Build RPMS
```
git clone https://github.com/hurdad/impala-rpm.git
cd impala-rpm && make
```

### RPMS Location
```
cd rpmbuild/RPMS/x86_64/
```
