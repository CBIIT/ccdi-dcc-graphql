# Use Node.js base image
FROM node:20
WORKDIR /ccdi-data-x

# Copy package.json and install dependencies
COPY package.json .
RUN npm install

# Copy the rest of the app
COPY . .

# Expose port
EXPOSE 4000

# Run Apollo server
CMD ["node", "index.js"]
