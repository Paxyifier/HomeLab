
# Oracle Cloud Infrastructure

Setup port forwarding for OCI cloud instances.

First backup your current IPtables config using the following.

```bash
sudo iptables-save > IPtablesbackup.txt
```

Replace 8080 with your desired Port.

```bash
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8080 -j ACCEPT
sudo netfilter-persistent save
sudo netfilter-persistent reload
sudo iptables -L
```

PS: You still need to allow access from Security List.

