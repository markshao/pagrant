__author__ = 'root'

from pagrant.vendors.docker import Client

docker = Client()

# print docker.create_container("mark/ubuntu:test", command="/usr/sbin/sshd -D", detach=True,
#                               volumes=['/root/share'])

#{u'Id': u'4ebadf848eeeb8d75067516df2aaecab7e4ca3e9d1a77710146d279d9f34d902'}

# docker.start("4ebadf848eeeb8d75067516df2aaecab7e4ca3e9d1a77710146d279d9f34d902", port_bindings={22: None},
#                     binds={
#                         '/home/mark/workspace/docker': '/root/share'
#                     })
print docker.inspect_container("4ebadf848eeeb8d75067516df2aaecab7e4ca3e9d1a77710146d279d9f34d902")['NetworkSettings'][
    'IPAddress']