FROM node:23-alpine AS builder

WORKDIR /app

COPY ./package.json /app/package.json

RUN npm install --only=prod

COPY . /app

RUN npm run build

FROM nginx:1.27.2-alpine

COPY --from=builder /app/build /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]
