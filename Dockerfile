FROM ubuntu:xenial-20160706

RUN apt-get -y update
RUN apt-get -y upgrade

RUN apt install -y tree && \
  apt install -y gnuplot && \
  apt install -y gcc && \
  apt install -y g++ && \
  apt install -y python && \
  apt install -y python-dev && \
  apt install -y mercurial && \
  apt install -y bzr && \
  apt install -y gdb && \
  apt install -y valgrind && \
  apt install -y gsl-bin && \
  apt install -y libgsl0-dev && \
  apt install -y flex && \
  apt install -y bison && \
  apt install -y tcpdump && \
  apt install -y sqlite && \
  apt install -y sqlite3 && \
  apt install -y libsqlite3-dev && \
  apt install -y libxml2 && \
  apt install -y libxml2-dev && \
  apt install -y libgtk2.0-0 && \
  apt install -y libgtk2.0-dev && \
  apt install -y uncrustify && \
  apt install -y doxygen && \
  apt install -y graphviz && \
  apt install -y imagemagick && \
  apt install -y texlive && \
  apt install -y texlive-latex-extra && \
  apt install -y texlive-generic-extra && \
  apt install -y texlive-generic-recommended && \
  apt install -y texinfo && \
  apt install -y dia && \
  apt install -y texlive && \
  apt install -y texlive-latex-extra && \
  apt install -y texlive-extra-utils && \
  apt install -y texlive-generic-recommended && \
  apt install -y texi2html && \
  apt install -y python-pygraphviz && \
  apt install -y python-kiwi && \
  apt install -y python-pygoocanvas && \
  apt install -y libgoocanvas-dev && \
  apt install -y python-pygccxml && \
  apt install -y wget && \
  apt install -y git && \
  apt install -y python3-pip && \
  apt install -y python3-dev && \
  apt install -y vim

RUN apt install -y ca-certificates
RUN cd && mkdir -p /home/vagrant/ns3 && cd /home/vagrant/ns3/

# Install
RUN cd /home/vagrant/ns3
RUN wget -P /home/vagrant/ns3/ https://www.nsnam.org/release/ns-allinone-3.27.tar.bz2
RUN cd /home/vagrant/ns3 && tar xjf ns-allinone-3.27.tar.bz2

WORKDIR /home/vagrant/ns3/ns-allinone-3.27
RUN ./build.py --enable-examples --enable-tests

WORKDIR /home/vagrant/ns3/ns-allinone-3.27/ns-3.27
RUN ./waf -d debug --enable-examples --enable-tests configure
RUN ./waf

# RUN cd
# # RUN rm -r /home/vagrant/tmp
# RUN git clone https://github.com/neko9laboratories/tcp-book.git /home/vagrant/tmp/
# RUN cp /home/vagrant/tmp/ns3/*.py /home/vagrant/ns3/ns-allinone-3.27/ns-3.27/
# RUN cp /home/vagrant/tmp/ns3/*.sh /home/vagrant/ns3/ns-allinone-3.27/ns-3.27/
# RUN cp /home/vagrant/tmp/ns3/scratch/* /home/vagrant/ns3/ns-allinone-3.27/ns-3.27/scratch/
# RUN cp -r /home/vagrant/tmp/ns3/data /home/vagrant/ns3/ns-allinone-3.27/ns-3.27/
# RUN cp /home/vagrant/tmp/ns3/requirements.txt /home/vagrant/ns3/ns-allinone-3.27/ns-3.27/
# RUN cp /home/vagrant/tmp/ns3/src/internet/model/* /home/vagrant/ns3/ns-allinone-3.27/ns-3.27/src/internet/model/
# RUN cp /home/vagrant/tmp/ns3/src/internet/test/* /home/vagrant/ns3/ns-allinone-3.27/ns-3.27/src/internet/test/
# RUN cp /home/vagrant/tmp/ns3/src/internet/wscript /home/vagrant/ns3/ns-allinone-3.27/ns-3.27/src/internet/wscript
# RUN cd /home/vagrant/ns3/ns-allinone-3.27/ns-3.27
# RUN chmod -R 777 *

# # Update waf configuration
# RUN ./waf clean
# RUN ./waf
# RUN shopt -s dotglob
# RUN chmod -R 777 *
# RUN shopt -u dotglob

ADD requirements.txt .
RUN pip3 install -r requirements.txt

ADD simulation.py .
ADD chapter4-base.cc /home/vagrant/ns3/ns-allinone-3.27/ns-3.27/scratch
RUN mkdir data
