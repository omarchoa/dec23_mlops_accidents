FROM alpine:latest

ADD /src/data/check_structure.py /home/shield/src/data/
ADD /src/data/import_raw_data.py /home/shield/src/data/

WORKDIR /home/shield/

EXPOSE 8001

RUN apk update \
&& apk add python3 \
&& apk add py3-requests

CMD ["/bin/sh", "-c", " \ 
# Run script and answer 'yes':
echo 'y' | python3 src/data/import_raw_data.py ; \
# Copy raw files on volume for persistency:
cp -r data ../volume \
 "]