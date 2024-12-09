# Use a base image that has bash installed
FROM ubuntu:latest

# Install dependencies, including Git, curl, and jq
RUN apt-get update && \
    apt-get install -y git curl jq && \
    rm -rf /var/lib/apt/lists/*

# Set the entrypoint to your script
COPY entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]
