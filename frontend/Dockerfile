# ---- build stage: compile the React app with Vite ----
FROM node:20-alpine AS build

WORKDIR /app

# install deps first so this layer is cached unless package.json changes
COPY package*.json ./
RUN npm install

COPY . .

# the backend URL can be overridden at build time; defaults to localhost:8000
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

# ---- serve stage: hand the static build to nginx ----
FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
