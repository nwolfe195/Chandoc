FROM httpd:2.4

RUN apt-get update && \
apt-get install -y git && \
apt-get install -y vim && \
apt-get install -y less && \
apt-get install -y python2.7 && \
apt-get install -y perl && \
apt-get install libfile-slurp-perl && \
apt-get install liblist-moreutils-perl && \
apt-get install -y wget

RUN rm -rf /etc/apache2/sites-enabled/000-default.conf && \
rm -rf /usr/local/apache2/htdocs/

RUN echo 'search bwh.harvard.edu partners.org\nnameserver 170.223.101.17\nnameserver 170.223.101.33' > /etc/resolv.conf && \
git clone https://0700163929fa2c005b0c8163cd01b058b12afc87@changit.bwh.harvard.edu/rejpz/chandoc.bwh.harvard.edu.git /usr/local/apache2/htdocs/

COPY ./resources/httpd.conf /usr/local/apache2/conf/httpd.conf
COPY ./resources/custom/index.html /usr/local/apache2/htdocs/
COPY ./resources/custom/Search.html /usr/local/apache2/htdocs/
COPY ./resources/custom/SearchResults.html /usr/local/apache2/cgi-bin/
COPY ./resources/custom/index.pl /usr/local/bin/
COPY ./resources/custom/stopwords.txt /usr/local/bin/

RUN chmod a+x /usr/local/bin/index.pl

RUN perl /usr/local/bin/index.pl

COPY ./resources/custom/htsearch.cgi /usr/local/apache2/htdocs/
COPY ./resources/custom/SearchResults.html /usr/local/apache2/htdocs/
RUN chmod a+x /usr/local/apache2/htdocs/htsearch.cgi