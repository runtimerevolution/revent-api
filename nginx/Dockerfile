FROM nginx:1.25.3-alpine

RUN sed -i 's/^http {/&\n   proxy_connect_timeout 300; proxy_send_timeout 300; proxy_read_timeout 300; client_max_body_size 100M; server_names_hash_bucket_size 128;/g' /etc/nginx/nginx.conf

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/templates/nginx.conf.template
EXPOSE 80