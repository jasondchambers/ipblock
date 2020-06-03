FROM python:3
ENV api_key YOUR_MERAKI_API_KEY_GOES_HERE
ENV network_id YOUR_MERAKI_NETWORK_ID_KEY_GOES_HERE
ENV src_cidr YOUR_LOCAL_SRC_CIDR_GOES_HERE
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt 
ENTRYPOINT [ "python" ] 
CMD [ "app.py" ] 
