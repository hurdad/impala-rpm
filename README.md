# impala-rpm

Tested on CentOS 7

### Install Dependancies :
```
yum install java-1.7.0-openjdk-devel redhat-lsb gcc-c++ python-devel cyrus-sasl-devel openssl-devel vim-common wget curl rpm-build maven git
```
### Set JAVA_HOME :
add /etc/profile.d/java.sh 
```
export JAVA_HOME=/usr/lib/jvm/java; export PATH=$JAVA_HOME/bin:$PATH
```
 
### Clone and Build RPMS
```
git clone https://github.com/hurdad/impala-rpm.git
cd impala-rpm && make
```
