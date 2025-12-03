# hadolint ignore=DL3006
FROM registry.access.redhat.com/ubi9/ubi-minimal

WORKDIR /sonarqube_exporter/
COPY . .

# hadolint ignore=DL3041
RUN microdnf install -y python3 python3-pip shadow-utils && \
    microdnf clean all

RUN pip3 install --no-cache-dir -r requirements.txt

RUN groupadd -g 1001 sonarqube_exporter && \
    useradd -u 1001 -g sonarqube_exporter -s /bin/sh sonarqube_exporter && \
    mkdir -p logs && \
    chown -R 1001:1001 /sonarqube_exporter

USER 1001

EXPOSE 8198
ENTRYPOINT [ "/bin/sh",  "entrypoint.sh" ]
