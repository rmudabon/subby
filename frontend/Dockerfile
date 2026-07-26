FROM node:22-slim

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

CMD ["npx", "run", "dev", "--", "--host", "0.0.0.0"]