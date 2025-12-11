FROM node:alpine

# Set the working directory in the container
WORKDIR /usr/src/app

# Install app dependencies
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

# Copy the app source code
COPY . .

# Build the app
RUN yarn build

# Use a lightweight web server to serve the static files
FROM nginx:alpine
COPY --from=0 /usr/src/app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
