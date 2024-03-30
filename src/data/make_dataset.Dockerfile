FROM alpine:latest

ADD /src/data/check_structure.py /home/shield/src/data/
ADD /src/data/make_dataset.py /home/shield/src/data/

# Unused ADD: 
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

# Install requirements from file: (unused)
# && apk add --no-cache $(cat /src/data/requirements.txt | xargs)

# Command to keep container running for debugging if needed:
# tail -f /dev/null

CMD ["/bin/sh", "-c", " \
# Import raw data (previously created in step 1) from volume to container:
cp -r ../volume/data data ; \
# Make requested directory on container:
mkdir data/preprocessed ; \
# Run Preprocessing with path arguments:
python3 src/data/make_dataset.py 'data/raw/' 'data/preprocessed' ;\
# Copy processed files to volume for persistency:
cp -r data/preprocessed/ ../volume/data\
"]
