FROM docker:24.0.7-dind-alpine3.19

ENV FUNCTION_HOME /usr/local/function

LABEL fn.version="latest"

USER root

WORKDIR /tmp

RUN apk update && apk add curl docker git && \
        addgroup -S function && \
        adduser -S function -G function && \
        curl -sSL https://cli.openfaas.com | sh

WORKDIR $FUNCTION_HOME

RUN faas-cli template pull https://github.com/singnet/das-openfaas-templates && \
        curl https://raw.githubusercontent.com/singnet/das-infra-stack-vultr/develop/das-function.yml -o $FUNCTION_HOME/stack.yml

COPY ./scripts/initd.sh ./

COPY ./das-query-engine/ ./das-query-engine/

RUN chmod +x ./initd.sh && touch .gitignore

SHELL ["sh"]

ENTRYPOINT ["./initd.sh"]

EXPOSE 8080
