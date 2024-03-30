FROM alpine:latest

ADD /src/data/check_structure.py /home/shield/src/data/
ADD /src/data/make_dataset.py /home/shield/src/data/
# ADD /src/data/requirements_make_dataset.txt /home/shield/src/data/
# ADD /src/data/requirements_make_dataset.txt /home/shield/data/preprocessed

WORKDIR /home/shield/

EXPOSE 8002


RUN apk update \
&& apk add python3 \
&& apk add py3-click \
&& apk add py3-numpy \
&& apk add py3-pandas \
&& apk add py3-scikit-learn
# && apk add --no-cache $(cat /src/data/requirements.txt | xargs)


# CMD ["/bin/sh", "-c", "cp -r ../volume/data data ; echo 'data/preprocessed/' | echo 'data/raw/' | python3 src/data/make_dataset.py ; cp -r data ../volume/"]
# CMD ["/bin/sh", "-c", "cp -r ../volume/data data ; echo 'y' | echo 'data/preprocessed/' | echo 'data/raw/' | python3 src/data/make_dataset.py ; cp -r data ../volume"]
# python3 src/data/make_dataset.py
# tail -f /dev/null
CMD ["/bin/sh", "-c", " \
cp -r ../volume/data data ; \
mkdir data/preprocessed ; \
python3 src/data/make_dataset.py 'data/raw/' 'data/preprocessed' ;\
cp -r data/preprocessed/ ../volume/data\
"]
